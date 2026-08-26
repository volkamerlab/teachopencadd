"""TreeSHAP attributions for tree models over Morgan fingerprints.

TreeSHAP (Lundberg et al., 2020) attributes a tree ensemble's output to its
*input features*. For a random forest over a Morgan fingerprint those
features are hashed bits, not atoms, so what comes out is a
:class:`~talktorial_xai.attribution.FingerprintAttribution`: one value per
bit, and complete::

    fp_attr.bit_attributions.sum() + fp_attr.baseline == model.predict(x)

Getting from there to a picture of the molecule means projecting the bits
onto the graph, which
:meth:`~talktorial_xai.attribution.FingerprintAttribution.to_mol_attribution`
does by splitting each set bit's value evenly over the atoms of its
environments. That conserves the bit's contribution but is an assumption:
the model attributed the value to the substructure, not to any atom in it.

What the projection cannot carry
--------------------------------
A bit that is *off* still gets a SHAP value -- the absence of a
substructure is evidence too -- but it has no environment, hence no atoms
to receive it. The resulting
:class:`~talktorial_xai.attribution.MolAttribution` therefore holds the
on-bit mass only, and says so by having no baseline to sweep the remainder
into. The remainder is not lost: it stays on the FingerprintAttribution,
where ``absent_mass()`` measures it and ``plot()`` draws the substructures
behind it, borrowing them from a
:class:`~talktorial_xai.bit_dictionary.BitDictionary` built over the
training set.

Usage
-----
    from talktorial_xai.tree_shap import tree_shap

    for fp_attr in tree_shap(["CCO", "c1ccccc1C(=O)O"], rf, fp_gen=fpGen):
        fp_attr.to_mol_attribution().plot()      # what is there
        fp_attr.plot(bits)                       # what is missing

Fingerprinting a large set is the slow part, so a pre-built dataset can be
passed instead of SMILES -- the ``(X, inv_maps)`` pair that
:meth:`InvertibleFingerprintGen.batch` returns, i.e. exactly what was fed to
``model.fit``::

    X, inv_maps = fpGen.batch(smiles)
    attrs = tree_shap((X, inv_maps), rf, smiles=smiles)
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol

import numpy as np

from talktorial_xai.attribution import FingerprintAttribution
from talktorial_xai.util.fingerprints import InvertibleFingerprintGen

__all__ = ["tree_shap"]


class _TreeModel(Protocol):
    """The bit of the scikit-learn API this module needs."""

    def predict(self, X: np.ndarray) -> np.ndarray: ...


def _resolve_fingerprints(
    molecules: Sequence[str] | tuple[np.ndarray, Sequence[np.ndarray]],
    fp_gen: InvertibleFingerprintGen | None,
    smiles: Sequence[str] | None,
) -> tuple[np.ndarray, list[np.ndarray], list[str | None]]:
    """Normalise the two accepted input forms to ``(X, inv_maps, labels)``."""
    prebuilt = (
        isinstance(molecules, tuple) and len(molecules) == 2 and not isinstance(molecules[0], str)
    )

    if not prebuilt:
        if smiles is not None:
            raise ValueError("smiles= only applies when passing a pre-built (X, inv_maps) pair")
        labels = list(molecules)
        fp_gen = fp_gen or InvertibleFingerprintGen()
        X, inv_maps = fp_gen.batch(labels)
        return X, list(inv_maps), labels

    if fp_gen is not None:
        # the bits are already computed; a second generator could only
        # disagree with them, silently
        raise ValueError("fp_gen= is unused when passing a pre-built (X, inv_maps) pair")

    X, inv_maps = molecules
    X = np.asarray(X)
    inv_maps = list(inv_maps)
    if X.ndim != 2:
        raise ValueError(f"expected X of shape (n_mols, fp_size), got {X.shape}")
    if X.shape[0] != len(inv_maps):
        raise ValueError(f"X has {X.shape[0]} rows but {len(inv_maps)} inv_maps were given")
    for i, inv_map in enumerate(inv_maps):
        if np.asarray(inv_map).shape[0] != X.shape[1]:
            raise ValueError(
                f"inv_maps[{i}] has {np.asarray(inv_map).shape[0]} bit rows, "
                f"but X has {X.shape[1]} bits"
            )

    if smiles is None:
        # nothing to attach; the attributions are still indexed by the atom
        # order of whatever molecule produced each inv_map
        labels: list[str | None] = [None] * X.shape[0]
    else:
        labels = list(smiles)
        if len(labels) != X.shape[0]:
            raise ValueError(f"got {len(labels)} smiles for {X.shape[0]} fingerprints")
    return X, inv_maps, labels


def tree_shap(
    molecules: Sequence[str] | tuple[np.ndarray, Sequence[np.ndarray]],
    model: _TreeModel,
    *,
    smiles: Sequence[str] | None = None,
    fp_gen: InvertibleFingerprintGen | None = None,
    explainer=None,
    check_additivity: bool = True,
) -> list[FingerprintAttribution]:
    """Compute per-bit TreeSHAP attributions.

    Parameters
    ----------
    molecules
        Either SMILES strings to fingerprint here, or a pre-built dataset:
        the ``(X, inv_maps)`` pair from
        :meth:`InvertibleFingerprintGen.batch`, with ``X`` of shape
        ``(n_mols, fp_size)`` and one ``(fp_size, n_atoms)`` incidence
        matrix per molecule. Pass the pair to reuse the fingerprints the
        model was trained on instead of recomputing them -- and to be sure
        the bits mean the same thing they did at fit time.
    model
        A fitted single-output tree model, e.g.
        :class:`~sklearn.ensemble.RandomForestRegressor`, trained on
        fingerprints from ``fp_gen``.
    smiles
        Only with a pre-built dataset: the SMILES the rows came from, used
        to fill :attr:`FingerprintAttribution.smiles`. Omit it and that
        field is None,
        which is enough for the numbers but leaves nothing to draw them on
        (pass the molecule to the plotting call yourself).
    fp_gen
        The generator used at training time -- radius and size must match,
        or the bits mean something else entirely. Defaults to
        :class:`InvertibleFingerprintGen` with its own defaults. Rejected
        alongside a pre-built dataset, whose bits it cannot influence.
    explainer
        A pre-built :class:`shap.TreeExplainer`. Building one is cheap but
        not free, so pass it in when explaining several batches.
    check_additivity
        Forwarded to ``TreeExplainer.shap_values``; leave on to catch a
        mismatch between the explainer and the model.

    Returns
    -------
    list[FingerprintAttribution]
        One entry per input molecule, in the input order, with
        ``bit_attributions.sum() + baseline == prediction``. Each carries
        the molecule's ``inv_map``, so
        :meth:`~talktorial_xai.attribution.FingerprintAttribution.to_mol_attribution`
        projects it onto atoms without being handed anything else.
    """
    X, inv_maps, labels = _resolve_fingerprints(molecules, fp_gen, smiles)
    if X.shape[0] == 0:
        return []

    if explainer is None:
        from shap import TreeExplainer

        explainer = TreeExplainer(model)

    shap_values = np.asarray(explainer.shap_values(X, check_additivity=check_additivity))
    if shap_values.ndim == 3:  # (n_mols, fp_size, n_outputs) for multi-output trees
        if shap_values.shape[2] != 1:
            raise ValueError("tree_shap only handles single-output models")
        shap_values = shap_values[:, :, 0]

    expected_value = float(np.ravel(explainer.expected_value)[0])
    predictions = np.ravel(model.predict(X))

    return [
        FingerprintAttribution(
            smiles=label,
            prediction=float(predictions[i]),
            bit_attributions=shap_values[i],
            fingerprint=X[i],
            inv_map=inv_maps[i],
            baseline=expected_value,
        )
        for i, label in enumerate(labels)
    ]
