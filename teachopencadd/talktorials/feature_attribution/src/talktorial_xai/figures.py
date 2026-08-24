"""Static figures for the theory part of the talktorial.

The theory section is markdown, so any picture it shows has to exist as a
file on disk before the notebook is read. Keeping the generating code here
(rather than in a throwaway cell) means the figures can be regenerated and
checked instead of being trusted::

    python -m talktorial_xai.figures
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from rdkit import Chem

from talktorial_xai.paths import IMAGES
from talktorial_xai.visualization import _png_to_array, draw_molecule, save

__all__ = ["hinge_motif_figure"]

ATP = "C1=NC(=C2C(=N1)N(C=N2)[C@H]3[C@@H]([C@@H]([C@H](O3)COP(=O)(O)OP(=O)(O)OP(=O)(O)O)O)O)N"
ERLOTINIB = "C#Cc1cccc(Nc2ncnc3cc(OCCOC)c(OCCOC)cc23)c1"

# The heteroaromatic core that occupies the adenine pocket. Both cores are
# matched by SMARTS rather than hard-coded indices, so editing the SMILES
# above cannot silently shift the highlight onto the wrong atoms.
ADENINE = "Nc1ncnc2c1ncn2"
QUINAZOLINE = "c1ncnc2ccccc12"

# muted fill for the whole core, saturated for the two hinge H-bond atoms
CORE_COLOR = (0.78, 0.86, 0.94)
HBOND_COLOR = (0.84, 0.19, 0.15)


def _core_atoms(mol: Chem.Mol, smarts: str) -> list[int]:
    matches = mol.GetSubstructMatches(Chem.MolFromSmarts(smarts))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {smarts} match, got {len(matches)}")
    return list(matches[0])


def _hinge_atoms_atp(mol: Chem.Mol) -> tuple[list[int], dict[int, str]]:
    """Adenine N1 (acceptor) and the exocyclic N6-H2 (donor)."""
    core = _core_atoms(mol, ADENINE)
    # the amino nitrogen is the one carrying hydrogens
    n6 = next(
        i
        for i in core
        if mol.GetAtomWithIdx(i).GetSymbol() == "N" and mol.GetAtomWithIdx(i).GetTotalNumHs() > 0
    )
    c6 = next(nbr.GetIdx() for nbr in mol.GetAtomWithIdx(n6).GetNeighbors())
    # N1 is the ring nitrogen next to C6
    n1 = next(
        nbr.GetIdx()
        for nbr in mol.GetAtomWithIdx(c6).GetNeighbors()
        if nbr.GetSymbol() == "N" and nbr.IsInRing()
    )
    return core, {n1: "N1", n6: "N6-H"}


def _hinge_atoms_erlotinib(mol: Chem.Mol) -> tuple[list[int], dict[int, str]]:
    """Quinazoline N1 (direct acceptor) and N3 (water-bridged acceptor)."""
    core = _core_atoms(mol, QUINAZOLINE)
    # in the SMARTS c1ncnc2ccccc12 the ring nitrogens sit at positions 1 and 3
    n_a, n_b = core[1], core[3]

    # N3 is the one adjacent to C4, i.e. to the carbon bearing the anilino N
    def next_to_anilino(idx: int) -> bool:
        for nbr in mol.GetAtomWithIdx(idx).GetNeighbors():
            if any(far.GetSymbol() == "N" and not far.IsInRing() for far in nbr.GetNeighbors()):
                return True
        return False

    n3, n1 = (n_a, n_b) if next_to_anilino(n_a) else (n_b, n_a)
    return core, {n1: "N1", n3: "N3"}


def hinge_motif_figure(path=None, dpi: int = 200):
    """ATP and erlotinib side by side, hinge-binding motif marked.

    The point of the figure is the shared pharmacophore: both ligands put a
    nitrogen heterocycle in the adenine pocket, and in both cases the same
    ring nitrogen accepts a hydrogen bond from the hinge backbone amide.
    That is the substructure a *plausible* explanation of a Type I
    inhibitor's predicted affinity should point at.
    """
    path = IMAGES / "hinge_binding_motif.png" if path is None else path

    panels = []
    for smiles, name, hinge_fn in (
        (ATP, "ATP (the natural ligand)", _hinge_atoms_atp),
        (ERLOTINIB, "Erlotinib (Type I inhibitor)", _hinge_atoms_erlotinib),
    ):
        mol = Chem.MolFromSmiles(smiles)
        core, notes = hinge_fn(mol)
        colors = {i: CORE_COLOR for i in core}
        colors.update({i: HBOND_COLOR for i in notes})
        png = draw_molecule(
            mol,
            size=(560, 460),
            highlight_atoms=colors,
            atom_notes=notes,
            as_figure=False,
        )
        # crop=False keeps both panels on the same canvas, so the two column
        # titles line up instead of drifting with the structure's bounding box
        panels.append((name, _png_to_array(png, crop=False)))

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.8))
    fig.patch.set_facecolor("white")
    for ax, (name, img) in zip(axes, panels, strict=True):
        ax.imshow(img)
        ax.set_axis_off()
        ax.set_title(name, fontsize=11, weight="bold", pad=4)
    fig.supxlabel(
        "The hinge-binding motif.  Blue: the nitrogen heterocycle that occupies the adenine "
        "pocket.  Red: the nitrogens that\nhydrogen bond to the hinge backbone -- ATP N1 "
        "(acceptor) and N6-H (donor); erlotinib N1 (acceptor) and N3 (water-bridged).",
        fontsize=9.5,
        linespacing=1.5,
    )
    fig.tight_layout()
    save(fig, path, dpi=dpi)
    print(f"wrote {path}")
    return fig


if __name__ == "__main__":
    hinge_motif_figure()
