"""Containers for the two resolutions a feature attribution can live at.

Every method in this talktorial ends up saying the same kind of thing --
*this input pushed the predicted value up or down by this much* -- but not
every method says it about the same kind of input. Gradient methods on the
D-MPNN speak about atoms and bonds. TreeSHAP on a random forest speaks
about *fingerprint bits*, and a bit is not a piece of the molecule: it is a
hash of a circular environment, which may or may not be present.

Hence two classes:

:class:`FingerprintAttribution`
    What a fingerprint model actually produced, one value per bit. Complete:
    ``bit_attributions.sum() + baseline == prediction``. It is the only
    place the model's verdict on *absent* substructures survives -- "no
    basic amine here, and that costs you" is a real SHAP value on a bit
    that is off.

:class:`MolAttribution`
    Per-atom (and optionally per-bond) numbers, the form the drawing code
    in :mod:`talktorial_xai.visualization` understands.
    :meth:`FingerprintAttribution.to_mol_attribution` projects the bit-level
    explanation down onto the graph; graph-native methods build one
    directly.

The projection loses something, and it is not a rounding error: an off-bit
has no atoms, so its attribution has nowhere to land. A MolAttribution made
from a fingerprint model therefore carries the *present*-substructure mass
only. That is why it has no ``baseline`` field to hide the remainder in --
the remainder is not a constant to be swept up, it is a set of substructures
the model looked for and did not find, and
:meth:`FingerprintAttribution.plot` draws them.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

__all__ = ["FingerprintAttribution", "MolAttribution", "spread_bits_over_atoms"]


def spread_bits_over_atoms(
    bit_attributions: np.ndarray,
    inv_map: np.ndarray,
) -> np.ndarray:
    """Push per-bit attributions onto atoms, splitting each bit evenly.

    Splitting equally is an assumption, and worth stating out loud: the
    model attributed the value to the *substructure*, not to any atom
    inside it.

    Parameters
    ----------
    bit_attributions
        Shape ``(fp_size,)``. One value per fingerprint bit.
    inv_map
        Shape ``(fp_size, n_atoms)``. ``inv_map[b, a]`` is truthy iff atom
        ``a`` lies in an environment that set bit ``b``, as returned by
        :meth:`~talktorial_xai.util.fingerprints.InvertibleFingerprintGen.get`.

    Returns
    -------
    np.ndarray
        Shape ``(n_atoms,)``. Bits with no atoms contribute nothing, so the
        result generally sums to less than ``bit_attributions.sum()``.
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


@dataclass
class MolAttribution:
    """Attribution of a single-task regression prediction, on the graph.

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

    Notes
    -----
    There is deliberately no ``baseline``: how much of the prediction the
    atoms fail to explain depends on the method, and for fingerprint models
    the leftover is not a number worth naming but a set of absent
    substructures -- kept, and drawable, on the
    :class:`FingerprintAttribution` this was projected from.
    """

    smiles: str | None
    prediction: float
    atom_attributions: np.ndarray | None = None
    bond_attributions: np.ndarray | None = None

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
                    f"{what} needs the molecule, but this MolAttribution has smiles=None "
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
        panel column and a standalone figure of the same attribution can
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
        # imported here so `MolAttribution` stays usable (and cheap) in code
        # that never draws anything
        from talktorial_xai.visualization import draw_atom_attributions

        mol = self.molecule(mol)
        atom_weights, bond_weights = self.weights_for(bonds, mol)

        kwargs.setdefault("prediction", self.prediction)
        return draw_atom_attributions(
            mol, atom_weights, bond_weights=bond_weights, mode=mode, **kwargs
        )


@dataclass
class FingerprintAttribution:
    """Attribution of a single-task regression prediction, one value per bit.

    This is the explanation as the model gave it. Every bit gets a value,
    including the ones that are *off*: for a Morgan fingerprint the vast
    majority of features are zero, and "this molecule does not contain that
    substructure" is evidence a tree ensemble uses constantly.

    Attributes
    ----------
    smiles
        The molecule, or None when the method was handed a pre-featurized
        dataset. Carried through to the :class:`MolAttribution` this
        projects to.
    prediction
        The scalar model output that was attributed.
    bit_attributions
        Shape ``(fp_size,)``, one value per fingerprint bit.
    fingerprint
        Shape ``(fp_size,)``, the molecule's own fingerprint. Kept
        alongside the attributions so present and absent bits can never be
        told apart by a vector that belongs to some other molecule.
    inv_map
        Shape ``(fp_size, n_atoms)`` bit -> atom incidence, from
        :meth:`~talktorial_xai.util.fingerprints.InvertibleFingerprintGen.get`.
        The projection to atoms needs it; without one,
        :meth:`to_mol_attribution` has to be given it explicitly.
    baseline
        The explainer's expected value, i.e. the model's output before any
        feature is seen. Unlike the atom-level view, this level is
        complete: ``bit_attributions.sum() + baseline == prediction``.
    """

    smiles: str | None
    prediction: float
    bit_attributions: np.ndarray
    fingerprint: np.ndarray
    inv_map: np.ndarray | None = None
    baseline: float | None = None

    def __post_init__(self) -> None:
        self.bit_attributions = np.asarray(self.bit_attributions, dtype=float)
        self.fingerprint = np.asarray(self.fingerprint)
        if self.bit_attributions.ndim != 1:
            raise ValueError(
                f"expected one attribution per bit, got shape {self.bit_attributions.shape}"
            )
        if self.fingerprint.shape != self.bit_attributions.shape:
            raise ValueError(
                f"fingerprint has {self.fingerprint.size} bits but "
                f"{self.bit_attributions.size} attributions were given"
            )
        if self.inv_map is not None:
            inv_map = np.asarray(self.inv_map)
            if inv_map.ndim != 2 or inv_map.shape[0] != self.bit_attributions.size:
                raise ValueError(
                    f"inv_map shape {inv_map.shape} does not match "
                    f"{self.bit_attributions.size} fingerprint bits"
                )
            self.inv_map = inv_map

    # ------------------------------------------------------------------ #
    # present / absent
    # ------------------------------------------------------------------ #

    @property
    def present(self) -> np.ndarray:
        """Boolean mask of the bits this molecule actually sets."""
        return np.asarray(self.fingerprint, dtype=float) > 0

    def present_mass(self) -> float:
        """Total attribution on substructures the molecule *has*.

        The part a molecular graph can show -- i.e. what
        :meth:`to_mol_attribution` hands to the atoms.
        """
        return float(self.bit_attributions[self.present].sum())

    def absent_mass(self) -> float:
        """Total attribution on substructures the molecule *lacks*.

        The size of what an atom map leaves out. Compare it against
        :meth:`present_mass` before reading much into either picture: when
        this dominates, the prediction was driven by what the molecule does
        not contain.
        """
        return float(self.bit_attributions[~self.present].sum())

    def rank_bits(
        self,
        bit_dictionary,
        *,
        which: str = "absent",
        top_k: int = 6,
        min_frequency: float = 0.0,
    ) -> list[tuple[int, float]]:
        """The ``(bit, attribution)`` pairs worth looking at, strongest first.

        Parameters
        ----------
        bit_dictionary
            A :class:`~talktorial_xai.bit_dictionary.BitDictionary` over
            the model's training set, used to drop bits it has never seen
            (undrawable, and ~0 anyway) and to apply ``min_frequency``.
        which
            ``"absent"``, ``"present"`` or ``"all"``.
        min_frequency
            Ignore bits set in fewer than this fraction of training
            molecules.
        """
        return bit_dictionary.rank_bits(
            self.bit_attributions,
            self.fingerprint,
            which=which,
            top_k=top_k,
            min_frequency=min_frequency,
        )

    def absent_bits(
        self,
        bit_dictionary,
        *,
        top_k: int = 6,
        min_frequency: float = 0.0,
    ) -> list[tuple[int, float]]:
        """The off-bits this prediction hinged on, strongest first.

        Precisely the attributions missing from
        :meth:`MolAttribution.plot`, which has no atom to put them on.
        """
        return self.rank_bits(
            bit_dictionary, which="absent", top_k=top_k, min_frequency=min_frequency
        )

    # ------------------------------------------------------------------ #
    # views
    # ------------------------------------------------------------------ #

    def to_mol_attribution(self, inv_map=None, *, smiles: str | None = None) -> MolAttribution:
        """Project the bit-level explanation onto the molecular graph.

        Each set bit's value is split evenly over the atoms of the
        environments that set it. Off-bits have no atoms and are simply not
        represented: the result carries :meth:`present_mass` only, and the
        rest of the explanation stays here, where :meth:`plot` can draw it.

        Parameters
        ----------
        inv_map
            The bit -> atom incidence matrix. Defaults to :attr:`inv_map`;
            pass one only when this attribution was built without it, and
            make sure it belongs to *this* molecule.
        smiles
            Override the SMILES attached to the result, e.g. when the
            attribution was computed on a pre-featurized input and the
            structure is only known here.

        Returns
        -------
        MolAttribution
        """
        inv_map = self.inv_map if inv_map is None else inv_map
        if inv_map is None:
            raise ValueError(
                "projecting bits onto atoms needs the bit -> atom incidence matrix, but "
                "this FingerprintAttribution has inv_map=None; pass the inv_map that "
                "InvertibleFingerprintGen returned for this molecule"
            )
        return MolAttribution(
            smiles=self.smiles if smiles is None else smiles,
            prediction=self.prediction,
            atom_attributions=spread_bits_over_atoms(self.bit_attributions, inv_map),
        )

    def plot(
        self,
        bit_dictionary,
        *,
        which: str = "absent",
        top_k: int = 6,
        min_frequency: float = 0.0,
        **kwargs,
    ):
        """Draw the strongest bits as substructures from the training set.

        The companion to :meth:`MolAttribution.plot`: that one colours what
        the molecule has, this one shows what the model was looking for --
        by default the substructures it did *not* find. ``**kwargs`` go to
        :func:`~talktorial_xai.visualization.draw_bit_attributions` (pass
        ``vmax`` from the atom map to put both figures on one scale).
        """
        from talktorial_xai.visualization import draw_bit_attributions

        ranked = self.rank_bits(
            bit_dictionary, which=which, top_k=top_k, min_frequency=min_frequency
        )
        return draw_bit_attributions(ranked, bit_dictionary, **kwargs)
