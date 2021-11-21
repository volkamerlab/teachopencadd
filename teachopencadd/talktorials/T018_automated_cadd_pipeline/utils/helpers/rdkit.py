"""
Contains RDKit-related functions.
"""

# for handling ligand data and calculating ligand-related properties
from rdkit import Chem  
from rdkit.Chem import Draw, AllChem, Descriptors
import numpy as np  # for some more functionalities when using Pandas (e.g. for handling NaN values)


def create_molecule_object(input_type, input_value):
    """
    This class is used to create an RDKit molecule object from various sources.
    It can be used to calculate or retrieve properties and descriptors (MW, h-bonds, etc.),
    generate images or SDF files or to perform similarity searches.

    Parameters
    ----------
    input_type : str
        Type of the input.
        Allowed input-types are: 'smiles', 'inchi', 'smarts', 'pdb_file'
    input_value : str
        Value of the corresponding input type.

    Returns
    -------
    rdkit.Chem.rdchem.Mol
        Structure as RDKit molecule object.
    """

    functions = {
        "smiles": Chem.MolFromSmiles,
        "inchi": Chem.MolFromInchi,
        "smarts": Chem.MolFromSmarts,
        "pdb_file": Chem.MolFromPDBFile,
    }
    Molobj = functions[input_type](input_value)
    Molobj.smiles = Chem.MolToSmiles(Molobj)
    return Molobj


def draw_molecules(
    list_mol_objs,
    list_legends=None,
    mols_per_row=3,
    sub_img_size=(350, 350),
    filepath=None,
):
    """
    Take a list of RDKit molecule objects and draws them as a grid image.

    Parameters
    ----------
    list_mol_objs: list
        List of RDKit molecule objects to be drawn.
    list_legends: list
        Optional; default: None
        List of legends for the molecules.
        If not provided, the list indices (+1) will be used as legends.
    mols_per_row : int
        Optional; default: 3
        Number of structures to show per row.
    sub_img_size : tuple (int, int)
        Optional; default: (350, 350)
        Size of each structure.
    filepath : str or pathlib.Path
        Full filepath to save the image in.

    Returns
    -------
    rdkit.Chem.Draw.MolsToGridImage
        Molecules shown as grid.
    """
    if list_legends is None:
        list_legends = list(map(str, range(1, len(list_mol_objs) + 1)))
    figure = Draw.MolsToGridImage(
        list_mol_objs,
        molsPerRow=mols_per_row,
        subImgSize=sub_img_size,
        legends=list(map(str, list_legends)),
    )
    if filepath is not None:
        with open(f"{filepath}.png", "wb") as f:
            f.write(figure.data)
    return figure


def save_molecule_image_to_file(mol_obj, filepath):
    """
    Save the image of a single molecule as a PNG file.

    Parameters
    ----------
    mol_obj : rdkit.Chem.rdchem.Mol
        The molecule to be saved as image.
    filepath : str or pathlib.Path
        Full filpath to save the image in.
    """
    Draw.MolToFile(mol_obj, f"{filepath}.png")


def save_3D_molecule_to_SDfile(mol_obj, filepath):
    """
    Generate a 3D conformer and save as SDF file.

    Parameters
    ----------
    mol_obj : rdkit.Chem.rdchem.Mol
        The molecule to be saved as SDF file.
    filepath : str or pathlib.Path
        Full filpath to save the image in.
    """
    mol = Chem.AddHs(mol_obj)
    embedding = AllChem.EmbedMolecule(mol, maxAttempts=1000, clearConfs=True)
    uffoptim = AllChem.UFFOptimizeMolecule(mol, maxIters=1000)
    # check if calculations converged (both should return 0 when converged)
    if embedding + uffoptim != 0:
        raise ValueError("Embedding/Optimization failed to converge.")
    session = Chem.SDWriter(f"{filepath}.sdf")
    session.write(mol)
    session.close()


def calculate_similarity_dice(mol_obj1, mol_obj2, morgan_radius=2, morgan_nbits=4096):
    """
    Calculate the Dice similarity between two molecules,
    based on 4096-bit Morgan fingerprints with a radius of 2.

    Parameters
    ----------
    mol_obj1 : rdkit.Chem.rdchem.Mol
        The first molecule.
    mol_obj2 : rdkit.Chem.rdchem.Mol
        The second molecule.
    morgan_radius : int
        Optional; default: 2
        The radius used to generate Morgan fingerprints.
    morgan_nbits : int
        Optional; default: 4096
        The number of bits in the Morgan fingerprints.
    Returns
    -------
    float
        Dice similarity between the two molecules rounded to two decimal places.
    """
    morgan_fp_mol1 = AllChem.GetMorganFingerprintAsBitVect(
        mol_obj1, radius=morgan_radius, nBits=morgan_nbits
    )
    morgan_fp_mol2 = AllChem.GetMorganFingerprintAsBitVect(
        mol_obj2, radius=morgan_radius, nBits=morgan_nbits
    )
    dice_similarity = round(
        AllChem.DataStructs.DiceSimilarity(morgan_fp_mol1, morgan_fp_mol2), 2
    )
    return dice_similarity


def calculate_druglikeness(mol_obj):
    """
    Calculate several molecular properties and drug-likeness scores,
    from an RDKit molecule object.

    Parameters
    ----------
    mol_obj: rdkit.Chem.rdchem.Mol
        Molecule object of interest.

    Returns
    -------
    dict
        The calculated values are returned in a dictionary with following keys:
        MolWt, NumHAcceptors, NumHDonors, MolLogP, TPSA, NumRotBonds, Saturation,
        lipinski_score, custom_drug_score, qed_score, total_drug_score
    """
    properties = {
        "mol_weight": round(Descriptors.MolWt(mol_obj), 3),
        "num_H_acceptors": Descriptors.NumHAcceptors(mol_obj),
        "num_H_donors": Descriptors.NumHDonors(mol_obj),
        "logp": round(Descriptors.MolLogP(mol_obj), 2),
        "tpsa": round(Descriptors.TPSA(mol_obj), 2),
        "num_rot_bonds": Descriptors.NumRotatableBonds(mol_obj),
        "saturation": round(Descriptors.FractionCSP3(mol_obj), 2),
        "drug_score_qed": round(Descriptors.qed(mol_obj), 2),
    }

    # Calculating Lipinski score
    l1 = int(properties["mol_weight"] < 500)
    l2 = int(properties["num_H_acceptors"] <= 10)
    l3 = int(properties["num_H_donors"] <= 5)
    l4 = int(properties["logp"] < 5)
    properties["drug_score_lipinski"] = round((l1 + l2 + l3 + l4) / 4, 2)

    # Calculating druglikeness score with custom scoring functions
    # derived from Hopkins paper: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3524573/
    def molWt_score(molWt):
        if molWt <= 440:
            return np.exp(-((molWt - 300) ** 2) / 15000)
        else:
            return np.exp(-(molWt - 180) / 190) + 0.01

    def molLogP_score(molLogP):
        return np.exp(-((molLogP - 2.5) ** 2) / 9)

    def numHDonors_score(numHDonors):
        if numHDonors == 0:
            return 0.6
        elif numHDonors < 5:
            return np.exp(-((numHDonors - 1) ** 2) / 5)
        else:
            return np.exp(-((numHDonors - 1) ** 2) / 5) + (0.4 / numHDonors)

    def numHAcceptors_score(numHAcceptors):
        if numHAcceptors < 4:
            return np.exp(-((numHAcceptors - 3) ** 2) / 3)
        else:
            return np.exp(-0.3 * numHAcceptors / 0.8 + 1.4)

    def TPSA_score(TPSA):
        if TPSA < 50:
            return 0.015 * TPSA + 0.25
        else:
            return np.exp(-((TPSA - 50) ** 2) / 8000)

    def numRotBonds_score(numRotBonds):
        if numRotBonds < 10:
            return np.exp(-((numRotBonds - 4) ** 2) / 19)
        else:
            return np.exp(-((numRotBonds - 4) ** 2) / 19) + (1.5 / numRotBonds ** 1.5)

    def saturation_score(saturation):
        return np.exp(-((saturation - 0.625) ** 2) / 0.05)

    d1 = molWt_score(properties["mol_weight"])
    d2 = numHAcceptors_score(properties["num_H_acceptors"])
    d3 = numHDonors_score(properties["num_H_donors"])
    d4 = molLogP_score(properties["logp"])
    d5 = TPSA_score(properties["tpsa"])
    d6 = numRotBonds_score(properties["num_rot_bonds"])
    d7 = saturation_score(properties["saturation"])
    properties["drug_score_custom"] = round((d1 + d2 + d3 + d4 + d5 + d6 + d7) / 7, 2)

    properties["drug_score_total"] = round(
        (
            3 * properties["drug_score_qed"]
            + 2 * properties["drug_score_custom"]
            + properties["drug_score_lipinski"]
        )
        / 6,
        2,
    )
    return properties
