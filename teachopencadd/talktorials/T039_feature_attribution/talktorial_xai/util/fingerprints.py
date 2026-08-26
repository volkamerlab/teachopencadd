"""Morgan fingerprints with a bit -> atom incidence matrix.

Requires RDKit >= 2022.09 (rdFingerprintGenerator.AdditionalOutput).
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator


class InvertibleFingerprintGen:
    """Turn a SMILES into (fingerprint, bit->atom matrix).

    The mapping matrix has shape (fp_size, n_atoms) and is boolean:
    ``M[b, a]`` is True iff atom ``a`` lies inside at least one circular
    environment that switched bit ``b`` on. Atom indices follow RDKit's
    ordering for the parsed molecule, i.e. the order the atoms occur in
    the input SMILES string.

    Note that rows are generally *not* disjoint: a single atom belongs to
    one environment per radius per neighbour, so it typically contributes
    to many bits. Rows for unset bits are all-False.
    """

    def __init__(
        self,
        radius: int = 2,
        size: int = 2048,
        use_chirality: bool = True,
        use_bond_types: bool = True,
        use_ring_membership: bool = True,
        add_hs: bool = False,
        dtype: np.dtype = np.float32,
    ):
        self.radius = radius
        self.fp_size = size
        self.add_hs = add_hs
        self.dtype = dtype

        self._gen = rdFingerprintGenerator.GetMorganGenerator(
            radius=radius,
            fpSize=size,
            includeChirality=use_chirality,
            useBondTypes=use_bond_types,
            includeRingMembership=use_ring_membership,
        )

    # ------------------------------------------------------------------ #
    # public API
    # ------------------------------------------------------------------ #

    def get(self, smiles: str) -> tuple[np.ndarray, np.ndarray]:
        """Return (fp, mapping) for a SMILES string.

        fp:      shape (fp_size,), dtype ``self.dtype``
        mapping: shape (fp_size, n_atoms), dtype bool
        """
        return self.from_mol(self.parse(smiles))

    __call__ = get

    def batch(self, smiles: Iterable[str]) -> tuple[np.ndarray, list[np.ndarray]]:
        """Return (fps, mappings) for many SMILES.

        fps:      shape (n_mols, fp_size), dtype ``self.dtype``
        mappings: list of n_mols arrays, each (fp_size, n_atoms) and bool.
                  Ragged in the atom axis, so this one stays a list.
        """
        results = [self.get(s) for s in smiles]
        if not results:
            return np.empty((0, self.fp_size), dtype=self.dtype), []
        fps, mappings = zip(*results)
        return np.stack(fps), list(mappings)

    def parse(self, smiles: str) -> Chem.Mol:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"RDKit could not parse SMILES: {smiles!r}")
        if self.add_hs:
            mol = Chem.AddHs(mol)
        return mol

    def from_mol(self, mol: Chem.Mol) -> tuple[np.ndarray, np.ndarray]:
        fp, envs_per_bit = self._fp_and_envs(mol)

        mapping = np.zeros((self.fp_size, mol.GetNumAtoms()), dtype=bool)
        for bit, envs in envs_per_bit.items():
            for center, rad in envs:
                mapping[bit, self._env_atoms(mol, center, rad)] = True

        return fp, mapping

    def bit_envs(self, mol_or_smiles) -> dict[int, tuple[tuple[int, int], ...]]:
        """Bit -> the ``(center atom, radius)`` environments that set it.

        The incidence matrix from :meth:`get` collapses this down to "which
        atoms did this bit touch", which is all the plotting code on a
        *single* molecule needs. Keeping the centre and the radius is what
        lets a substructure be re-drawn on some *other* molecule -- see
        :mod:`talktorial_xai.bit_dictionary`.

        Bits that are off do not appear in the mapping at all.
        """
        mol = self.parse(mol_or_smiles) if isinstance(mol_or_smiles, str) else mol_or_smiles
        return self._fp_and_envs(mol)[1]

    @staticmethod
    def environment(mol: Chem.Mol, center: int, radius: int) -> tuple[list[int], list[int]]:
        """The ``(atom indices, bond indices)`` of one circular environment.

        Both lists are what ``Chem.MolFragmentToSmiles`` wants in order to
        write the substructure out on its own.
        """
        if radius == 0:
            return [center], []
        bond_ids = list(Chem.FindAtomEnvironmentOfRadiusN(mol, radius, center))
        if not bond_ids:
            return [center], []
        atoms = {center}
        for bid in bond_ids:
            bond = mol.GetBondWithIdx(bid)
            atoms.add(bond.GetBeginAtomIdx())
            atoms.add(bond.GetEndAtomIdx())
        return sorted(atoms), bond_ids

    # ------------------------------------------------------------------ #
    # internals
    # ------------------------------------------------------------------ #

    def _fp_and_envs(
        self, mol: Chem.Mol
    ) -> tuple[np.ndarray, dict[int, tuple[tuple[int, int], ...]]]:
        ao = rdFingerprintGenerator.AdditionalOutput()
        ao.AllocateBitInfoMap()

        fp = self._gen.GetFingerprintAsNumPy(mol, additionalOutput=ao)
        fp = fp.astype(self.dtype, copy=False)

        envs_per_bit = {
            int(bit): tuple((int(center), int(rad)) for center, rad in envs)
            for bit, envs in ao.GetBitInfoMap().items()
        }
        return fp, envs_per_bit

    @staticmethod
    def _env_atoms(mol: Chem.Mol, center: int, radius: int) -> Sequence[int]:
        """Atom indices of the circular environment of `radius` around `center`."""
        return InvertibleFingerprintGen.environment(mol, center, radius)[0]


if __name__ == "__main__":
    mapper = InvertibleFingerprintGen(radius=2, size=2048)
    fp, m = mapper("CC(=O)Oc1ccccc1C(=O)O")  # aspirin

    print(f"fp {fp.shape} {fp.dtype}, {int(fp.sum())} bits on")
    print(f"map {m.shape}, {m.any(axis=1).sum()} non-empty rows")

    # sanity: every on-bit has at least one atom, every off-bit has none
    on = fp > 0
    assert m[on].any(axis=1).all()
    assert not m[~on].any()

    # atoms touched by an arbitrary on-bit
    bit = int(np.flatnonzero(on)[0])
    print(f"bit {bit} -> atoms {np.flatnonzero(m[bit]).tolist()}")
