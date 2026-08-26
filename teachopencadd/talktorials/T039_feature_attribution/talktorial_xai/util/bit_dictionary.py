"""What a Morgan bit *means*, learned from the training set.

A fingerprint bit is a hash, not a substructure. Inside one molecule the
bit->atom incidence matrix from
:class:`~talktorial_xai.util.fingerprints.InvertibleFingerprintGen` is
enough to say which atoms switched a bit on, and that is what the atom
maps in :mod:`talktorial_xai.tree_shap` draw.

It says nothing about a bit that is *off*. Yet an off-bit still gets a
SHAP value: "this molecule does not contain that substructure" is
evidence, and a random forest trained on kinase inhibitors uses plenty of
it. Those values are exactly the ones the molecular graph cannot show --
there is no atom to colour -- so they do not survive
:meth:`~talktorial_xai.attribution.FingerprintAttribution.to_mol_attribution`
and disappear from the picture.

To draw them, the substructure has to come from somewhere else: the
training set. This module walks the training molecules once, records for
every bit which circular environments hashed to it and how often, and
keeps a concrete exemplar (molecule + centre atom + radius) that can be
re-drawn later. An absent bit then becomes "the model wanted a
*p*-aminophenyl group here, seen in 18% of the training set, and did not
find one".

Two caveats the pictures should not hide:

* **Collisions.** Several unrelated environments can hash to one bit, so a
  bit is not a substructure but a *bag* of them. Every record keeps the
  distinct fragments it saw with their counts, and
  :attr:`BitRecord.purity` says how dominant the top one is.
* **The exemplar is a witness, not a definition.** It is one training
  molecule that happened to contain the fragment, chosen for drawing.

Usage
-----
    from talktorial_xai.bit_dictionary import BitDictionary

    bits = BitDictionary.from_smiles(train_smiles, fpGen)
    bits.save(DATA_PROCESSED / "morgan_bits.json")

    bits[389].top_fragment.smiles   # 'OC(c)=O'
    bits.frequency(389)             # 0.31
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path

from rdkit import Chem

from talktorial_xai.util.fingerprints import InvertibleFingerprintGen

__all__ = ["BitDictionary", "BitRecord", "Fragment"]


@dataclass(frozen=True)
class Fragment:
    """One distinct circular environment that hashed to a given bit.

    Attributes
    ----------
    smiles
        Canonical SMILES of the environment on its own, rooted at the
        centre atom. Written with ``MolFragmentToSmiles``, so aromatic
        atoms whose ring is cut by the radius show up lower-case with an
        open valence (``'c'``) -- the fragment is a piece of a molecule,
        not a molecule.
    radius
        The Morgan radius of the environment.
    count
        How many environments in the training set produced this fragment.
    exemplar_smiles, exemplar_center
        A training molecule containing the environment, and the atom it is
        centred on. Together with ``radius`` this is enough to re-draw the
        fragment in context; see :meth:`atoms`.
    """

    smiles: str
    radius: int
    count: int
    exemplar_smiles: str
    exemplar_center: int

    def molecule(self) -> Chem.Mol:
        """The exemplar molecule, parsed."""
        mol = Chem.MolFromSmiles(self.exemplar_smiles)
        if mol is None:  # pragma: no cover -- it parsed once already
            raise ValueError(f"could not re-parse exemplar SMILES: {self.exemplar_smiles!r}")
        return mol

    def atoms(self, mol: Chem.Mol | None = None) -> tuple[list[int], list[int]]:
        """``(atom indices, bond indices)`` of the environment in the exemplar.

        Pass ``mol`` only to reuse an already-parsed exemplar; it must be
        the molecule ``exemplar_smiles`` names, since the indices are that
        molecule's.
        """
        mol = self.molecule() if mol is None else mol
        return InvertibleFingerprintGen.environment(mol, self.exemplar_center, self.radius)


@dataclass
class BitRecord:
    """Everything the training set had to say about one fingerprint bit.

    Attributes
    ----------
    bit
        The bit index.
    n_molecules
        Training molecules in which the bit was on. This -- not the
        environment count -- is what :meth:`BitDictionary.frequency`
        normalises, because the question an absent bit raises is "how many
        molecules *did* have it".
    fragments
        The distinct environments that hashed here, most common first.
        Truncated to ``max_fragments`` at build time.
    n_environments
        Total environments that hashed to this bit, counting the ones
        truncated out of ``fragments``, so :attr:`purity` stays exact.
    """

    bit: int
    n_molecules: int
    n_environments: int
    fragments: list[Fragment] = field(default_factory=list)

    @property
    def top_fragment(self) -> Fragment:
        """The most common environment behind this bit."""
        if not self.fragments:
            raise ValueError(f"bit {self.bit} has no recorded fragments")
        return self.fragments[0]

    @property
    def purity(self) -> float:
        """Share of those environments that are the top fragment.

        1.0 means the bit stood for exactly one substructure in this
        training set; a low value means the bit is a collision and any
        single picture of it is a half-truth.
        """
        if not self.fragments or not self.n_environments:
            return 0.0
        return self.fragments[0].count / self.n_environments

    def label(self) -> str:
        """Short human-readable name, e.g. ``'bit 389: OC(c)=O'``."""
        if not self.fragments:
            return f"bit {self.bit}: unseen"
        return f"bit {self.bit}: {self.top_fragment.smiles}"


class BitDictionary:
    """Bit -> substructures, counted over a training set.

    Build it once with :meth:`from_smiles` (fingerprinting is the slow
    part), then :meth:`save` it next to the model: the mapping is a
    property of the training data and the generator, so it only has to be
    recomputed when either changes.
    """

    def __init__(
        self,
        records: dict[int, BitRecord],
        *,
        n_molecules: int,
        fp_size: int,
        radius: int,
    ):
        self.records = records
        self.n_molecules = n_molecules
        self.fp_size = fp_size
        self.radius = radius

    # ------------------------------------------------------------------ #
    # construction
    # ------------------------------------------------------------------ #

    @classmethod
    def from_smiles(
        cls,
        smiles: Iterable[str],
        fp_gen: InvertibleFingerprintGen | None = None,
        *,
        max_fragments: int = 4,
        skip_unparsable: bool = False,
    ) -> BitDictionary:
        """Walk a training set and record what each bit stood for.

        Parameters
        ----------
        smiles
            The training molecules. Use the same ones the model was fitted
            on: a bit's meaning here is only an explanation of *that*
            model's behaviour if it was counted over the data that shaped
            it.
        fp_gen
            The generator used at training time. Radius and size must
            match the model's features, or the bit indices refer to
            different substructures than the ones the model split on.
        max_fragments
            How many distinct environments to keep per bit, most common
            first. The tail is usually a long list of one-off collisions;
            keeping all of them bloats the stored dictionary without
            changing any picture. Counts of dropped fragments are still
            reflected in :attr:`BitRecord.n_environments` only if they are
            kept, so ``purity`` is computed over what was kept -- set this
            higher if you want the exact figure.
        skip_unparsable
            Skip SMILES RDKit cannot read instead of raising.

        Returns
        -------
        BitDictionary
        """
        fp_gen = fp_gen or InvertibleFingerprintGen()

        # bit -> fragment smiles -> [count, radius, exemplar smiles, centre]
        seen: dict[int, dict[str, list]] = {}
        molecules_with_bit: dict[int, int] = {}
        n_molecules = 0

        for smi in smiles:
            try:
                mol = fp_gen.parse(smi)
            except ValueError:
                if skip_unparsable:
                    continue
                raise
            n_molecules += 1

            for bit, envs in fp_gen.bit_envs(mol).items():
                molecules_with_bit[bit] = molecules_with_bit.get(bit, 0) + 1
                per_bit = seen.setdefault(bit, {})
                for center, rad in envs:
                    frag = _fragment_smiles(mol, center, rad)
                    entry = per_bit.get(frag)
                    if entry is None:
                        per_bit[frag] = [1, rad, smi, center]
                    else:
                        entry[0] += 1

        records = {}
        for bit, per_bit in seen.items():
            fragments = [
                Fragment(
                    smiles=frag,
                    radius=rad,
                    count=count,
                    exemplar_smiles=exemplar,
                    exemplar_center=center,
                )
                for frag, (count, rad, exemplar, center) in sorted(
                    per_bit.items(), key=lambda kv: (-kv[1][0], kv[0])
                )[:max_fragments]
            ]
            records[bit] = BitRecord(
                bit=bit,
                n_molecules=molecules_with_bit[bit],
                n_environments=sum(count for count, *_ in per_bit.values()),
                fragments=fragments,
            )

        return cls(
            records,
            n_molecules=n_molecules,
            fp_size=fp_gen.fp_size,
            radius=fp_gen.radius,
        )

    # ------------------------------------------------------------------ #
    # lookup
    # ------------------------------------------------------------------ #

    def __getitem__(self, bit: int) -> BitRecord:
        return self.records[int(bit)]

    def get(self, bit: int) -> BitRecord | None:
        """The record for ``bit``, or None if no training molecule set it."""
        return self.records.get(int(bit))

    def __contains__(self, bit: object) -> bool:
        return int(bit) in self.records if isinstance(bit, (int, float)) else False

    def __len__(self) -> int:
        return len(self.records)

    def frequency(self, bit: int) -> float:
        """Fraction of training molecules in which ``bit`` was on.

        0.0 for a bit no training molecule ever set -- which is also why
        the model can have learned nothing from it.
        """
        record = self.get(bit)
        return record.n_molecules / self.n_molecules if record and self.n_molecules else 0.0

    def describe(self, bit: int) -> str:
        """One line: the bit's top fragment, its frequency and its purity."""
        record = self.get(bit)
        if record is None:
            return f"bit {bit}: never set in the training set"
        return (
            f"{record.label()} -- in {self.frequency(bit):.1%} of training molecules, "
            f"radius {record.top_fragment.radius}, purity {record.purity:.0%} "
            f"of {record.n_environments} environments"
        )

    def most_common(self, n: int = 20) -> list[BitRecord]:
        """The ``n`` bits set in the most training molecules."""
        return sorted(self.records.values(), key=lambda r: -r.n_molecules)[:n]

    # ------------------------------------------------------------------ #
    # persistence
    # ------------------------------------------------------------------ #

    def to_dict(self) -> dict:
        return {
            "format": "talktorial-xai/bit-dictionary/1",
            "n_molecules": self.n_molecules,
            "fp_size": self.fp_size,
            "radius": self.radius,
            "records": [
                {
                    "bit": r.bit,
                    "n_molecules": r.n_molecules,
                    "n_environments": r.n_environments,
                    "fragments": [
                        {
                            "smiles": f.smiles,
                            "radius": f.radius,
                            "count": f.count,
                            "exemplar_smiles": f.exemplar_smiles,
                            "exemplar_center": f.exemplar_center,
                        }
                        for f in r.fragments
                    ],
                }
                for r in sorted(self.records.values(), key=lambda r: r.bit)
            ],
        }

    @classmethod
    def from_dict(cls, payload: dict) -> BitDictionary:
        records = {
            int(r["bit"]): BitRecord(
                bit=int(r["bit"]),
                n_molecules=int(r["n_molecules"]),
                n_environments=int(r["n_environments"]),
                fragments=[Fragment(**f) for f in r["fragments"]],
            )
            for r in payload["records"]
        }
        return cls(
            records,
            n_molecules=int(payload["n_molecules"]),
            fp_size=int(payload["fp_size"]),
            radius=int(payload["radius"]),
        )

    def save(self, path: str | Path, *, indent: int | None = None) -> Path:
        """Write the dictionary as JSON (gzipped when the path ends in .gz)."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(self.to_dict(), indent=indent)
        if path.suffix == ".gz":
            with gzip.open(path, "wt", encoding="utf-8") as fh:
                fh.write(text)
        else:
            path.write_text(text, encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: str | Path) -> BitDictionary:
        path = Path(path)
        if path.suffix == ".gz":
            with gzip.open(path, "rt", encoding="utf-8") as fh:
                payload = json.load(fh)
        else:
            payload = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(payload)

    # ------------------------------------------------------------------ #
    # the point of the whole thing
    # ------------------------------------------------------------------ #

    def rank_bits(
        self,
        bit_attributions: Sequence[float],
        fingerprint: Sequence[float] | None = None,
        *,
        which: str = "absent",
        top_k: int = 6,
        min_frequency: float = 0.0,
        require_known: bool = True,
    ) -> list[tuple[int, float]]:
        """The ``(bit, attribution)`` pairs worth drawing, strongest first.

        Parameters
        ----------
        bit_attributions
            One value per bit, e.g. the raw TreeSHAP values behind an
            :class:`~talktorial_xai.attribution.Attribution`.
        fingerprint
            The molecule's fingerprint, needed to tell present bits from
            absent ones. Required unless ``which="all"``.
        which
            ``"absent"`` (bits that are off -- the ones no atom map can
            show), ``"present"`` or ``"all"``.
        top_k
            How many to return.
        min_frequency
            Drop bits set in fewer than this fraction of training
            molecules. A bit seen twice in the whole training set has an
            exemplar, but it is anecdote, not a learned rule.
        require_known
            Drop bits with no training exemplar. They cannot be drawn, and
            a forest that never saw them set gives them ~0 anyway.

        Returns
        -------
        list of (bit, attribution), by descending \\|attribution\\|.
        """
        if which not in ("absent", "present", "all"):
            raise ValueError("which must be 'absent', 'present' or 'all'")

        import numpy as np

        values = np.asarray(bit_attributions, dtype=float)
        if values.ndim != 1:
            raise ValueError(f"expected one attribution per bit, got shape {values.shape}")

        if which == "all":
            candidates = np.arange(values.size)
        else:
            if fingerprint is None:
                raise ValueError(f"which={which!r} needs the molecule's fingerprint")
            present = np.asarray(fingerprint, dtype=float) > 0
            if present.shape != values.shape:
                raise ValueError(
                    f"fingerprint has {present.size} bits but {values.size} attributions were given"
                )
            candidates = np.flatnonzero(present if which == "present" else ~present)

        scored = []
        for bit in candidates.tolist():
            record = self.get(bit)
            if require_known and (record is None or not record.fragments):
                continue
            if self.frequency(bit) < min_frequency:
                continue
            scored.append((bit, float(values[bit])))

        scored.sort(key=lambda bv: -abs(bv[1]))
        return scored[:top_k]


def _fragment_smiles(mol: Chem.Mol, center: int, radius: int) -> str:
    """Canonical SMILES of one circular environment, rooted at its centre."""
    atoms, bonds = InvertibleFingerprintGen.environment(mol, center, radius)
    return Chem.MolFragmentToSmiles(
        mol,
        atomsToUse=atoms,
        bondsToUse=bonds,
        rootedAtAtom=center,
        canonical=True,
    )


if __name__ == "__main__":
    train = [
        "CC(=O)Oc1ccccc1C(=O)O",
        "CC(=O)Nc1ccc(O)cc1",
        "CN1C=NC2=C1C(=O)N(C)C(=O)N2C",
        "c1ccc2c(c1)[nH]c1ccccc12",
    ]
    bits = BitDictionary.from_smiles(train)
    print(f"{len(bits)} bits seen over {bits.n_molecules} molecules")
    for record in bits.most_common(5):
        print(" ", bits.describe(record.bit))
