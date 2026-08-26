"""Input x Gradient attribution for Chemprop v2 D-MPNN regression models.

Input x Gradient (Shrikumar et al., 2016) attributes a model's scalar output
to its inputs via ``attribution = input * d(output)/d(input)``.

For a D-MPNN the "input" is not a flat vector but a molecular graph, so the
gradient is taken with respect to the two featurized tensors that enter
message passing:

    * ``bmg.V`` -- atom (node) features, shape (n_atoms_total, d_v)
    * ``bmg.E`` -- bond (edge) features, shape (2 * n_bonds_total, d_e)

Per-feature products are summed over the feature axis, giving one scalar per
atom and per bond -- what you need to colour a molecule.

Usage
-----
    from chemprop.models import MPNN
    from talktorial_xai.input_x_gradient import input_x_gradient

    model = MPNN.load_from_file("model.pt")
    for attr in input_x_gradient(["CCO", "c1ccccc1C(=O)O"], model):
        print(attr.smiles, attr.prediction, attr.atom_attributions)

A ``MoleculeDataset`` can be passed instead of SMILES -- e.g. the test split
the model was evaluated on -- which reuses its featurizer and any scaling
already applied to it::

    attrs = input_x_gradient(test_dset, model)
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import torch
from chemprop import data, featurizers
from chemprop.models import MPNN
from rdkit import Chem
from tqdm import tqdm

from talktorial_xai.attribution import MolAttribution

__all__ = ["input_x_gradient"]


def _align_to_smiles(mol: Chem.Mol) -> tuple[str, Chem.Mol, np.ndarray]:
    """A SMILES for ``mol`` plus the permutation onto its atom order.

    :attr:`MolAttribution.smiles` is a promise that re-parsing the string lines
    the numbers up with atoms, and canonical SMILES output order is *not*
    the input mol's atom order. RDKit records the order it wrote the atoms
    in, so the attributions can be permuted to match instead of quietly
    landing on the wrong atoms.
    """
    smi = Chem.MolToSmiles(mol)
    # "_smilesAtomOutputOrder" is written by MolToSmiles: position k in the
    # string holds atom `order[k]` of `mol`
    order = np.fromstring(
        mol.GetProp("_smilesAtomOutputOrder").strip("[]").rstrip(","), sep=",", dtype=int
    )
    perm = np.empty_like(order)
    perm[order] = np.arange(order.size)  # mol atom index -> re-parsed atom index
    return smi, Chem.MolFromSmiles(smi), perm


def input_x_gradient(
    molecules: Sequence[str] | data.MoleculeDataset,
    model: MPNN,
    *,
    featurizer: featurizers.GraphFeaturizer | None = None,
    batch_size: int = 64,
    device: str | torch.device | None = None,
) -> list[MolAttribution]:
    """Compute Input x Gradient attributions for a list of SMILES.

    Parameters
    ----------
    molecules
        SMILES strings (parseable by RDKit), or a pre-built
        :class:`~chemprop.data.MoleculeDataset`. Passing the dataset is the
        safer route when one already exists: it carries its own featurizer
        and any input scaling applied to it, so the graphs the gradients are
        taken through are the same ones the model was trained or evaluated
        on.
    model
        A trained single-task regression :class:`~chemprop.models.MPNN`.
    featurizer
        Featurizer used to build the graphs. Must match the one used at
        training time. Defaults to
        :class:`SimpleMoleculeMolGraphFeaturizer`. Rejected alongside a
        pre-built dataset, which brings its own.
    batch_size
        Molecules per forward/backward pass.
    device
        Torch device. Defaults to the device the model is already on.

    Returns
    -------
    list[MolAttribution]
        One entry per input molecule, in the input order.

    Notes
    -----
    * The model is put in ``eval()`` mode. This matters: Chemprop's optional
      ``BatchNorm1d`` would otherwise couple molecules within a batch and
      make per-molecule attributions batch-size dependent.
    * Atom features are mostly one-hot, so ``input * grad`` picks out the
      gradient of the active bits only, which is the intended behaviour.
    * Input x Gradient does not satisfy completeness for nonlinear models:
      the attributions do not sum to the prediction. Use Integrated
      Gradients if you need that property.
    """
    if isinstance(molecules, data.MoleculeDataset):
        if featurizer is not None:
            raise ValueError("featurizer= is unused when passing a pre-built MoleculeDataset")
        dset = molecules
        mols = list(dset.mols)
        # the dataset kept molecules, not strings; derive both the SMILES and
        # the permutation onto its atom order
        aligned = [_align_to_smiles(mol) for mol in mols]
    else:
        featurizer = featurizer or featurizers.SimpleMoleculeMolGraphFeaturizer()
        datapoints = [data.MoleculeDatapoint.from_smi(smi) for smi in molecules]
        dset = data.MoleculeDataset(datapoints, featurizer)
        mols = [dp.mol for dp in datapoints]
        # the input string already parses to exactly these atoms
        aligned = [
            (smi, mol, np.arange(mol.GetNumAtoms()))
            for smi, mol in zip(molecules, mols, strict=True)
        ]

    if not mols:
        return []

    device = torch.device(device) if device is not None else next(model.parameters()).device
    model = model.to(device)
    model.eval()  # freeze BatchNorm / dropout; do NOT use torch.no_grad()

    loader = data.build_dataloader(dset, batch_size=batch_size, shuffle=False, num_workers=0)

    results: list[MolAttribution] = []
    mol_offset = 0

    for batch in tqdm(loader):
        bmg = batch.bmg
        bmg.to(device)  # move first: .to() rebinds tensors, so grad must be set after
        bmg.V.requires_grad_(True)
        bmg.E.requires_grad_(True)

        with torch.enable_grad():
            preds = model(bmg)  # (B, 1) for single-task regression
            scores = preds[:, 0]

            # Each molecule's score depends only on its own nodes/edges, so a
            # single backward pass over the summed scores yields all
            # per-molecule gradients at once.
            g_V, g_E = torch.autograd.grad(scores.sum(), [bmg.V, bmg.E])

        atom_attr = (g_V * bmg.V).detach().sum(dim=1).cpu().numpy()
        edge_attr = (g_E * bmg.E).detach().sum(dim=1).cpu().numpy()

        edge_index = bmg.edge_index.detach().cpu().numpy()
        # molecule index of every directed edge, via the atom it starts at
        edge_mol = bmg.batch.detach().cpu().numpy()[edge_index[0]]

        n_mols = len(bmg)
        counts = torch.bincount(bmg.batch, minlength=n_mols)
        offsets = torch.cat([counts.new_zeros(1), counts.cumsum(0)[:-1]]).cpu().numpy()
        scores_np = scores.detach().cpu().numpy()

        for j in range(n_mols):
            smi, ref_mol, perm = aligned[mol_offset + j]
            n_atoms, n_bonds = ref_mol.GetNumAtoms(), ref_mol.GetNumBonds()
            start = int(offsets[j])

            # Map directed edges back to RDKit bond indices via their atom
            # pair; both directions land on the same bond and are summed.
            # `perm` puts the pair in the re-parsed molecule's indexing, so
            # the bond index is the one a reader of `smi` would compute.
            bond_attr = np.zeros(n_bonds, dtype=atom_attr.dtype)
            (edge_ids,) = np.nonzero(edge_mol == j)
            for e in edge_ids:
                u = int(perm[int(edge_index[0, e]) - start])
                v = int(perm[int(edge_index[1, e]) - start])
                bond = ref_mol.GetBondBetweenAtoms(u, v)
                if bond is not None:
                    bond_attr[bond.GetIdx()] += edge_attr[e]

            atoms_out = np.empty(n_atoms, dtype=atom_attr.dtype)
            atoms_out[perm] = atom_attr[start : start + n_atoms]

            results.append(
                MolAttribution(
                    smiles=smi,
                    prediction=float(scores_np[j]),
                    atom_attributions=atoms_out,
                    bond_attributions=bond_attr,
                )
            )

        mol_offset += n_mols

    return results
