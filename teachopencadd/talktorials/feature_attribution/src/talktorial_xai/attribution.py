"""Shared container for per-atom / per-bond feature attributions.

Every attribution method in this talktorial -- gradient-based ones on the
D-MPNN, TreeSHAP on a random forest over Morgan fingerprints -- ends up
saying the same kind of thing: *this atom (or bond) pushed the predicted
value up or down by this much*. Keeping that in one class means the
plotting code in :mod:`talktorial_xai.visualization` does not care which
method produced the numbers.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["Attribution"]


@dataclass
class Attribution:
    """Attribution of a single-task regression prediction for one molecule.

    Attributes
    ----------
    smiles
        The molecule the attributions belong to. Attribution arrays are
        indexed exactly as ``Chem.MolFromSmiles(smiles)``, so anything
        that re-parses this string can line the numbers up with atoms.
        None when the method was handed a pre-featurized dataset and never
        saw a structure; the numbers are still valid, but drawing them
        needs the molecule supplied from outside.
    prediction
        The scalar model output that was attributed.
    atom_attributions
        One value per heavy atom, or None if the method gives no per-atom
        signal. Positive means "pushed the prediction up".
    bond_attributions
        One value per bond, or None if the method has no notion of bonds
        (e.g. fingerprint-based methods that only reach atoms).
    baseline
        The part of ``prediction`` that the attributions do *not* explain,
        or None if the method has no such notion. For a complete method,
        ``atom_attributions.sum() + bond_attributions.sum() + baseline``
        equals ``prediction``; the baseline then holds whatever is left
        over when every input is "absent" -- plus, for fingerprint methods,
        the attribution mass that lives on absent substructures and so has
        no atom to sit on (see :mod:`talktorial_xai.tree_shap`).
    """

    smiles: str | None
    prediction: float
    atom_attributions: np.ndarray | None = None
    bond_attributions: np.ndarray | None = None
    baseline: float | None = None

    def molecule(self, mol=None, *, what: str = "drawing"):
        """The molecule these attributions are indexed by, as an RDKit Mol.

        Falls back to ``self.smiles``, which is why plotting code never has
        to be handed the structure a second time; an explicit ``mol`` is
        for the case where the method never saw one.
        """
        from rdkit import Chem

        if mol is None:
            if self.smiles is None:
                raise ValueError(
                    f"{what} needs the molecule, but this Attribution has smiles=None "
                    "(the method was handed a pre-featurized input); pass the molecule "
                    "the attributions were computed on explicitly"
                )
            mol = self.smiles
        return Chem.MolFromSmiles(mol) if isinstance(mol, str) else mol

    def folded_atom_attributions(self, mol=None) -> np.ndarray:
        """Atom attributions with each bond's share split over its two atoms.

        Convenient when a single per-atom colour is all you have room for,
        but note that the halves are an assumption: the model attributed
        the value to the *bond*, not to either atom in particular.

        Parameters
        ----------
        mol
            The molecule whose bonds the ``bond_attributions`` are indexed
            by, as an RDKit Mol or SMILES string. Only needed when
            ``self.smiles`` is None; it must be the structure the
            attributions were computed on, since only its bond order says
            which two atoms each value belongs to.
        """
        if self.atom_attributions is None:
            raise ValueError("no atom attributions to fold into")
        atoms = self.atom_attributions.astype(float, copy=True)
        if self.bond_attributions is None:
            return atoms

        mol = self.molecule(mol, what="folding bond attributions")

        for idx, w in enumerate(self.bond_attributions):
            bond = mol.GetBondWithIdx(idx)
            atoms[bond.GetBeginAtomIdx()] += w / 2.0
            atoms[bond.GetEndAtomIdx()] += w / 2.0
        return atoms

    def weights_for(self, bonds: str = "own", mol=None) -> tuple[np.ndarray, np.ndarray | None]:
        """The ``(atom_weights, bond_weights)`` a ``bonds`` policy asks for.

        Shared by :meth:`plot` and
        :func:`~talktorial_xai.visualization.draw_attribution_panel` so a
        panel column and a standalone figure of the same Attribution can
        never disagree about what ``bonds`` means.

        Parameters
        ----------
        bonds
            ``"own"``, ``"fold"`` or ``"ignore"``; see :meth:`plot`.
        mol
            Only consulted by ``"fold"``, and only when ``self.smiles`` is
            None.
        """
        if bonds not in ("own", "fold", "ignore"):
            raise ValueError("bonds must be 'own', 'fold' or 'ignore'")
        if self.atom_attributions is None:
            raise ValueError("nothing to plot: atom_attributions is None")
        if bonds == "fold":
            return self.folded_atom_attributions(mol), None
        return (
            np.asarray(self.atom_attributions, dtype=float),
            None if bonds == "ignore" else self.bond_attributions,
        )

    def plot(self, mol=None, *, bonds: str = "own", mode: str = "atoms", **kwargs):
        """Draw this attribution on the molecular structure.

        Parameters
        ----------
        mol
            The structure to draw on, as an RDKit Mol or SMILES string.
            Defaults to ``self.smiles``, so it is only worth passing when
            that is None -- or when you deliberately want to draw a
            different depiction of the same molecule.
        bonds
            How to handle ``bond_attributions``:

            * ``"own"`` -- colour each bond by its own attribution, on the
              scale shared with the atoms. The default: it shows what the
              model actually produced and keeps the two channels distinct.
            * ``"fold"`` -- split each bond's value over its two atoms and
              colour atoms only. Required for ``mode="field"``, which has
              no bond channel.
            * ``"ignore"`` -- drop bond attributions; bonds are shaded by
              the mean of their endpoints, i.e. interpolation only.

            Ignored when ``bond_attributions`` is None.
        mode
            ``"atoms"`` (discrete colouring) or ``"field"`` (Gaussian
            contours), passed through to
            :func:`~talktorial_xai.visualization.draw_atom_attributions`.
        **kwargs
            Forwarded to
            :func:`~talktorial_xai.visualization.draw_atom_attributions`
            (``cmap``, ``vmax``, ``title``, ``ax``, ...).

        Returns
        -------
        matplotlib Figure
        """
        # imported here so `Attribution` stays usable (and cheap) in code
        # that never draws anything
        from talktorial_xai.visualization import draw_atom_attributions

        mol = self.molecule(mol)
        atom_weights, bond_weights = self.weights_for(bonds, mol)

        kwargs.setdefault("prediction", self.prediction)
        return draw_atom_attributions(
            mol, atom_weights, bond_weights=bond_weights, mode=mode, **kwargs
        )
