"""
Set of functions required to analyze protein-ligand interactions using the PLIP package.
"""

from enum import Enum  # for creating enumeration classes
from pathlib import Path  # for creating folders and handling local paths
import logging  # for setting logging levels (to disable logging defaults of packages e.g. PLIP)

import plip  # for changing the logging setting of the package (see bottom of the cell: Settings)
# for calculating protein-ligand interactions
from plip.structure.preparation import PDBComplex  
# for calculating protein-ligand interactions
from plip.exchange.report import BindingSiteReport
import pandas as pd  # for creating dataframes and handling data

# Settings:
# disabling excessive INFO logs of the PLIP package
logging.getLogger(plip.__name__).setLevel(logging.WARNING)


class Consts:
    """
    Constants for PLIP.
    """

    class InteractionTypes(Enum):
        H_BOND = "hbond"
        HYDROPHOBIC = "hydrophobic"
        SALT_BRIDGE = "saltbridge"
        WATER_BRIDGE = "waterbridge"
        PI_STACKING = "pistacking"
        PI_CATION = "pication"
        HALOGEN = "halogen"
        METAL = "metal"


def calculate_interactions(pdb_filepath):
    """
    Calculate protein-ligand interactions in a PDB file.

    Parameters
    ----------
    pdb_filepath : str or pathlib.Path
        Filepath of the PDB file containing the protein-ligand complex.

    Returns
    -------
    dict of dict
        Dictionary of all different interaction data for all detected ligands.
        - The keys of first dictionary correspond to the ligand-IDs of detected ligands in the
          PDB file.
        - The keys of each sub-dictionary correspond to interaction types, as defined in
          `PLIP.Consts.InteractionTypes`.
    """
    protein_ligand_complex = PDBComplex()
    protein_ligand_complex.load_pdb(str(Path(pdb_filepath).with_suffix(".pdb")))

    for ligand in protein_ligand_complex.ligands:
        protein_ligand_complex.characterize_complex(ligand)

    all_ligands_interactions = {}

    for ligand, ligand_binding_site in sorted(protein_ligand_complex.interaction_sets.items()):

        interaction_object = BindingSiteReport(
            ligand_binding_site
        )  # collect data about interactions

        interaction_data = {
            interaction_type.value: (
                [getattr(interaction_object, f"{interaction_type.value}_features")]
                + getattr(interaction_object, f"{interaction_type.value}_info")
            )
            for interaction_type in Consts.InteractionTypes
        }

        all_ligands_interactions[ligand] = interaction_data

    return all_ligands_interactions


def create_dataframe_of_ligand_interactions(ligand_interaction_data, interaction_type):
    """
    Create a pandas.DataFrame from interaction data of a specific ligand,
    for a specific interaction type.

    Parameters
    ----------
    ligand_interaction_data : dict
        Interaction data calculated by the `calculate_interactions` function,
        where only one ligand's interaction data is chosen from the output of
        that function.
    interaction_type : Enum
        One of the enumerations from `PLIP.Consts.InteractionTypes`,
        specifying the type of interaction, for which the DataFrame should be created.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all the information for the specified interactions
        in the input ligand interaction data.
    """

    interaction_df = pd.DataFrame.from_records(
        # interaction data are stored after the first element
        ligand_interaction_data[interaction_type.value][1:],
        # the first element corresponds to interaction parameters,
        # which are used here as column names.
        columns=ligand_interaction_data[interaction_type.value][0],
    )

    return interaction_df


def create_protein_ligand_complex(
    protein_pdbqt_filepath, docking_pose_pdbqt_filepath, ligand_id, output_filepath
):
    """
    Create a protein-ligand complex PDB file out of separate protein and ligand files.

    Parameters
    ----------
    protein_pdbqt_filepath : str or pathlib.Path
        Filepath of the PDB file containing the protein.
    docking_pose_pdbqt_filepath : str or pathlib.Path
        Filepath of the PDB file containing the ligand.
    ligand_id : str
        An identifier for the ligand to write into the PDB file.
    output_filepath : str or pathlib.Path
        Output filepath of the PDB file containing the protein-ligand complex.

    Returns
    -------
    pathlib.Path
        Complete filepath of the created protein-ligand complex PDB file.
    """

    def pdbqt_to_pdbblock(pdbqt_filepath):
        lines = []
        with open(Path(pdbqt_filepath).with_suffix(".pdbqt")) as file:
            for line in file:
                # we are only interested in lines starting with "ATOM"
                # and ignore the rest.
                if line[:4] == "ATOM":
                    lines.append(line[:67].strip())
        return "\n".join(lines)

    protein_pdbblock = pdbqt_to_pdbblock(protein_pdbqt_filepath)

    ligand_pdbblock = pdbqt_to_pdbblock(docking_pose_pdbqt_filepath)

    full_output_filepath = Path(output_filepath).with_suffix(".pdb")
    with open(full_output_filepath, "w") as file:
        file.write(protein_pdbblock)
        file.write(f"\nCOMPND    {ligand_id}\n")
        file.write(ligand_pdbblock)

    return full_output_filepath


def correct_protein_residue_numbers(ligand_interaction_data, protein_first_residue_number):
    """
    Correct the protein residue numbers in interaction data.
    
    Parameters
    ----------
    ligand_interaction_data : dict
        One of sub-dicts (corresponding to a single ligand)
        created by the function `calculate_interactions`.
    
    protein_first_residue_number : int
        The first residue number in the protein.
    
    Returns
    -------
    dict
        Corrects the residue numbers in-place 
        in the input dict and returns it.
    """
    
    # loop through interaction data for each interaction type (i.e. dict values)
    for certain_interactions_data in ligand_interaction_data.values():
        # for each type, the interaction data is a list,
        # and the actual data starts from the second element
        for single_interaction_data in range(1, len(certain_interactions_data)):
            # the data are stored in tuples, we have to convert them to a list first, 
            # in order to be able to change them.
            list_from_tuple = list(
                certain_interactions_data[single_interaction_data]
            )
            # add the protein's first residue number to them, and subtract 1,
            # so that we get back the original residue numbers.
            list_from_tuple[0] += protein_first_residue_number - 1
            # convert back to tuple and overwrite in-place
            certain_interactions_data[single_interaction_data] = tuple(
                list_from_tuple
            )
    return ligand_interaction_data
    