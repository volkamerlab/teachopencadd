from rdkit import Chem


def crippen_contrib_per_atom(smiles):
    """Will throw exception when ground truth is calculated incorrectly."""
    mol = Chem.MolFromSmiles(smiles)
    from rdkit.Chem import rdMolDescriptors
    from rdkit.Chem import Crippen

    contribs = rdMolDescriptors._CalcCrippenContribs(mol)
    crippen_heavy_atoms = [x[0] for x in contribs]
    crippen = []
    mod_acid_smarts = ["OC=[#6]", "OC=[#7]", "OC=O", "OC=S", "OO", "OS"]
    mod_acid_smarts_mols = [Chem.MolFromSmarts(x) for x in mod_acid_smarts]
    hit_acid_atoms = []
    for masm in mod_acid_smarts_mols:
        hits = list(mol.GetSubstructMatch(masm))
        for h in hits:
            if h not in hit_acid_atoms:
                hit_acid_atoms.append(h)
    countedHs = 0
    for i, atom in enumerate(mol.GetAtoms()):
        contrib = crippen_heavy_atoms[i]
        # add contribution of hydrogen atoms
        if atom.GetSymbol() == "C":
            contrib += atom.GetTotalNumHs() * 0.1230
            countedHs += atom.GetTotalNumHs()
        elif atom.GetSymbol() == "N":
            contrib += atom.GetTotalNumHs() * 0.2142
            countedHs += atom.GetTotalNumHs()
        elif atom.GetSymbol() == "O":
            if atom.GetIdx() in hit_acid_atoms:  # acid contribution
                contrib += atom.GetTotalNumHs() * 0.2980
                countedHs += atom.GetTotalNumHs()
            else:  # should be alcohol
                contrib += atom.GetTotalNumHs() * -0.2677
                countedHs += atom.GetTotalNumHs()
        elif atom.GetSymbol() == "S":  # thiolates apparently count as alcohols
            contrib += atom.GetTotalNumHs() * -0.2677
            countedHs += atom.GetTotalNumHs()
        else:
            contrib += atom.GetTotalNumHs() * 0.1125
            countedHs += atom.GetTotalNumHs()
        crippen.append(contrib)
    correctnumHs = sum([atom.GetTotalNumHs() for atom in mol.GetAtoms()])
    assert correctnumHs == countedHs, f"correctnumHs={correctnumHs}, countedHs={countedHs}"
    assert len(crippen) == mol.GetNumAtoms(), (
        f"len(crippen)={len(crippen)}, num atoms={mol.GetNumAtoms()}"
    )
    assert round(sum(crippen), 4) == round(Crippen.MolLogP(mol), 4), (
        f"sum(crippen)={round(sum(crippen), 4)}, completeCrippen={round(Crippen.MolLogP(mol), 4)}"
    )
    # quality = [abs(y-x) for x,y in zip(crippen, weights)]
    return crippen


def literal_weight_per_atom(smiles):
    pse = Chem.GetPeriodicTable()
    mol = Chem.MolFromSmiles(smiles)

    literal_weights = []
    for a in mol.GetAtoms():
        atom_weight = pse.GetAtomicWeight(a.GetSymbol())
        hydrogens = a.GetNumExplicitHs() + a.GetNumImplicitHs()
        literal_weights.append(atom_weight + pse.GetAtomicWeight("H") * hydrogens)
    return literal_weights
