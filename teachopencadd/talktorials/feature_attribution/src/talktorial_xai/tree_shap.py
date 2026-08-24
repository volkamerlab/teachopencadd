"""TreeSHAP attributions for tree models over Morgan fingerprints.

TreeSHAP (Lundberg et al., 2020) attributes a tree ensemble's output to its
*input features*. For a random forest over a Morgan fingerprint those
features are hashed bits, not atoms, so the SHAP values have to be pushed
back onto the molecular graph before they can be drawn.

Each set bit stands for one or more circular atom environments, recorded by
:class:`~talktorial_xai.util.fingerprints.InvertibleFingerprintGen` as a
bit -> atom incidence matrix. This module splits every bit's SHAP value
equally over the atoms of its environments, which conserves that bit's
contribution but is an assumption: the model attributed the value to the
substructure, not to any atom in it.

Completeness
------------
TreeSHAP is complete at the level of *bits*::

    shap_values.sum() + explainer.expected_value == model.predict(x)

That property does **not** survive the trip to atoms. A bit that is *off*
still gets a SHAP value -- the absence of a substructure is evidence too --
but it has no environment, hence no atoms to receive it. The atom
attributions therefore sum to the on-bit mass only, and the missing part is
a per-molecule constant, reported as :attr:`Attribution.baseline` (together
with ``expected_value``) rather than silently dropped. Pass
``absence="spread"`` to smear it uniformly over the atoms instead; that
restores completeness at the cost of inventing a localisation the model
never expressed.

Usage
-----
    from talktorial_xai.tree_shap import tree_shap

    for attr in tree_shap(["CCO", "c1ccccc1C(=O)O"], rf, fp_gen=fpGen):
        print(attr.smiles, attr.prediction, attr.atom_attributions)
        attr.plot()

Fingerprinting a large set is the slow part, so a pre-built dataset can be
passed instead of SMILES -- the ``(X, inv_maps)`` pair that
:meth:`InvertibleFingerprintGen.batch` returns, i.e. exactly what was fed to
``model.fit``::

    X, inv_maps = fpGen.batch(smiles)
    attrs = tree_shap((X, inv_maps), rf, smiles=smiles)
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal, Protocol

import numpy as np

from talktorial_xai.attribution import Attribution
from talktorial_xai.util.fingerprints import InvertibleFingerprintGen

__all__ = ["tree_shap", "spread_bits_over_atoms", "atom_attributions_from_bits"]

Absence = Literal["baseline", "spread"]


class _TreeModel(Protocol):
    """The bit of the scikit-learn API this module needs."""

    def predict(self, X: np.ndarray) -> np.ndarray: ...


def spread_bits_over_atoms(
    bit_attributions: np.ndarray,
    inv_map: np.ndarray,
) -> np.ndarray:
    """Push per-bit attributions onto atoms, splitting each bit evenly.

    Parameters
    ----------
    bit_attributions
        Shape ``(fp_size,)``. One value per fingerprint bit.
    inv_map
        Shape ``(fp_size, n_atoms)``. ``inv_map[b, a]`` is truthy iff atom
        ``a`` lies in an environment that set bit ``b``, as returned by
        :meth:`InvertibleFingerprintGen.get`.

    Returns
    -------
    np.ndarray
        Shape ``(n_atoms,)``. Bits with no atoms contribute nothing, so the
        result generally sums to less than ``bit_attributions.sum()``; see
        the module docstring.
    """
    bit_attributions = np.asarray(bit_attributions, dtype=float)
    if bit_attributions.ndim != 1:
        raise ValueError(f"expected one attribution per bit, got shape {bit_attributions.shape}")
    inv_map = np.asarray(inv_map, dtype=float)
    if inv_map.ndim != 2 or inv_map.shape[0] != bit_attributions.shape[0]:
        raise ValueError(
            f"inv_map shape {inv_map.shape} does not match "
            f"{bit_attributions.shape[0]} fingerprint bits"
        )

    atoms_per_bit = inv_map.sum(axis=1, keepdims=True)
    # rows of empty bits stay all-zero instead of turning into NaN
    share = np.divide(inv_map, atoms_per_bit, out=np.zeros_like(inv_map), where=atoms_per_bit > 0)
    return bit_attributions @ share


def atom_attributions_from_bits(
    bit_attributions: np.ndarray,
    inv_map: np.ndarray,
    *,
    absence: Absence = "baseline",
) -> tuple[np.ndarray, float]:
    """Per-atom attributions plus the attribution mass no atom could take.

    Parameters
    ----------
    bit_attributions, inv_map
        As in :func:`spread_bits_over_atoms`.
    absence
        What to do with the mass sitting on bits that have no atoms
        (off-bits, mostly):

        * ``"baseline"`` -- leave it out of the atoms and return it, to be
          folded into the explanation's baseline.
        * ``"spread"`` -- distribute it uniformly over all atoms, which
          makes the atom values sum to ``bit_attributions.sum()``.

    Returns
    -------
    (atom_attributions, unattributed)
        ``unattributed`` is 0.0 when ``absence="spread"``.
    """
    if absence not in ("baseline", "spread"):
        raise ValueError("absence must be 'baseline' or 'spread'")

    atom_attributions = spread_bits_over_atoms(bit_attributions, inv_map)
    unattributed = float(np.sum(bit_attributions) - atom_attributions.sum())

    if absence == "spread" and atom_attributions.size:
        atom_attributions = atom_attributions + unattributed / atom_attributions.size
        unattributed = 0.0

    return atom_attributions, unattributed


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
    absence: Absence = "baseline",
    check_additivity: bool = True,
) -> list[Attribution]:
    """Compute per-atom TreeSHAP attributions.

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
        to fill :attr:`Attribution.smiles`. Omit it and that field is None,
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
    absence
        See :func:`atom_attributions_from_bits`.
    check_additivity
        Forwarded to ``TreeExplainer.shap_values``; leave on to catch a
        mismatch between the explainer and the model.

    Returns
    -------
    list[Attribution]
        One entry per input molecule, in the input order.
        ``atom_attributions.sum() + baseline == prediction`` holds exactly;
        with ``absence="baseline"`` the baseline carries both the
        explainer's expected value and the off-bit mass.
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

    results: list[Attribution] = []
    for i, label in enumerate(labels):
        atom_attributions, unattributed = atom_attributions_from_bits(
            shap_values[i], inv_maps[i], absence=absence
        )
        results.append(
            Attribution(
                smiles=label,
                prediction=float(predictions[i]),
                atom_attributions=atom_attributions,
                baseline=expected_value + unattributed,
            )
        )
    return results
