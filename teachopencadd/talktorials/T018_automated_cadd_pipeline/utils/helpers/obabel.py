"""
A set of functions based on the OpenBabel's pybel package,
for preparing proteins and ligands for the docking experiment.
"""

# for creating folders and handling local paths
from pathlib import Path  
# for preparing protein and ligand for docking, and other manipulations of PDB files
from openbabel import pybel  


def optimize_structure_for_docking(
    pybel_structure_object,
    add_hydrogens=True,
    protonate_for_pH=7.4,
    calculate_partial_charges=True,
    generate_3d_structure=False,
):
    """
    Take a pybel structure object and prepare it for docking.

    Parameters
    ----------
    pybel_structure_object : openbabel.pybel.Molecule
        The structure to optimize.
    add_hydrogens : bool
        Optional; default: True.
        Whether to add hydrogen atoms to the structure.
    protonate_for_pH : float
        Optional; default: 7.4
        pH value to protonate the structure at.
        If set to 0 or False, will not protonate.
    calculate_partial_charges : bool
        Optional; default: True.
        Whether to calculate partial charges for each atom
    generate_3d_structure : bool
        Optional; default: False.
        Whether to generate a 3D conformation.
        Must be set to True if the pybel structure is 2D,
        for example is structure is made from SMILES string.

    Returns
    -------
    None
        The structure object is optimized in place.
    """

    if protonate_for_pH:
        pybel_structure_object.OBMol.CorrectForPH(protonate_for_pH)
    if add_hydrogens:
        pybel_structure_object.addh()
    if generate_3d_structure:
        pybel_structure_object.make3D(forcefield="mmff94s", steps=10000)
    if calculate_partial_charges:
        for atom in pybel_structure_object.atoms:
            atom.OBAtom.GetPartialCharge()
    return


def create_pdbqt_from_pdb_file(pdb_filepath, pdbqt_filepath, pH=7.4):
    """
    Convert a PDB file to a PDBQT file,
    while adding hydrogen atoms, correcting the protonation state,
    and assigning partial charges.

    Parameters
    ----------
    pdb_filepath: str or pathlib.Path
        Path to input PDB file.
    pdbqt_filepath: str or pathlib.path
        Path to output PDBQT file.
    pH: float
        pH value for defining the protonation state of the atoms.

    Returns
    -------
    openbabel.pybel.Molecule
        Molecule object of PDB file optimized for docking.
    """
    # readfile() provides an iterator over the Molecules in a file.
    # To access the first (and possibly only) molecule in a file,
    # we use next()
    molecule = next(pybel.readfile("pdb", str(Path(pdb_filepath).with_suffix(".pdb"))))
    optimize_structure_for_docking(molecule, protonate_for_pH=pH)
    molecule.write("pdbqt", str(Path(pdbqt_filepath).with_suffix(".pdbqt")), overwrite=True)
    return


def create_pdbqt_from_smiles(smiles, pdbqt_path, pH=7.4):
    """
    Convert a SMILES string to a PDBQT file,
    while adding hydrogen atoms, correcting the protonation state, assigning partial charges,
    and generating a 3D conformer.

    Parameters
    ----------
    smiles: str
        SMILES string.
    pdbqt_path: str or pathlib.path
        Path to output PDBQT file.
    pH: float
        Protonation at given pH.
        Optional; default: 7.4
    """

    molecule = pybel.readstring("smi", smiles)
    optimize_structure_for_docking(molecule, protonate_for_pH=pH, generate_3d_structure=True)
    molecule.write("pdbqt", str(Path(pdbqt_path).with_suffix(".pdbqt")), overwrite=True)
    return


def split_multistructure_file(filetype, filepath, output_folder_path=None):
    """
    Split a multi-structure file into seperate files (with the same format)
    for each structure. Each file is named with consecutive numbers (starting at 1)
    at the end of the original filename.

    Parameters
    ----------
    filetype : str
        Type of the multimodel file to be split.
        Examples: 'sdf', 'pdb', 'pdbqt' etc.
        For a full list of acceptable file types, call pybel.informats
    filepath : str or pathlib.Path
        Path of the file to be split.
    output_folder_path : str or pathlib.Path
        Optional; default: same folder as input filepath.
        Path of the output folder to save the split files.

    Returns
    -------
    list of pathlib.Path
        List of the full paths for each split file.
    """
    filepath = Path(filepath)
    filename = filepath.stem
    if output_folder_path is None:
        output_folder_path = filepath.parent
    else:
        output_folder_path = Path(output_folder_path)
        output_folder_path.mkdir(parents=True, exist_ok=True)

    structures = pybel.readfile(filetype, str(filepath))
    output_filepaths = []
    for i, structure in enumerate(structures, 1):
        output_filepath = output_folder_path / f"{filename}_{i}.{filetype}"
        output_filepaths.append(output_filepath)
        structure.write(filetype, str(output_filepath), overwrite=True)
    return output_filepaths


def merge_molecules_to_single_file(
    list_of_pybel_molecule_objects, output_filetype, output_filepath
):
    """
    Create a single file containing several molecules.

    Parameters
    ----------
    list_of_pybel_molecule_objects : list of openbabel.pybel.Molecule
        List of molecule ojects to be merged into a single file.
    output_filetype : str
        Type of the output file.
        Examples: 'sdf', 'pdb', 'pdbqt' etc.
        For a full list of acceptable file types, call pybel.outformats
    output_filepath : str or pathlib.Path
        Path of the output file including file name, but excluding extension.

    Returns
    -------
    pathlib.Path
        Full path (including extension) of the output file.
    """
    fullpath = Path(f"{output_filepath}.{output_filetype}")

    merged_molecule_file = pybel.Outputfile(output_filetype, str(fullpath))

    for pybel_molecule_object in list_of_pybel_molecule_objects:
        merged_molecule_file.write(pybel_molecule_object)

    merged_molecule_file.close()
    return fullpath
