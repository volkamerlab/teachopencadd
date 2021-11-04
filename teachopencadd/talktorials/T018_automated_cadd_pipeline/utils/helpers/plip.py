"""
Set of functions required to analyze protein-ligand interactions using the PLIP package.
"""

# Standard library:
from enum import Enum  # for creating enumeration classes
from pathlib import Path  # for creating folders and handling local paths
import logging  # for setting the logging level of some packages (i.e. to disable excessive logging default to some packages e.g. PLIP)

# 3rd-party packages:
import plip  # for changing the logging setting of the package (see bottom of the cell: Settings)
from plip.structure.preparation import (
    PDBComplex,
)  # for calculating protein-ligand interactions
from plip.exchange.report import (
    BindingSiteReport,
)  # for calculating protein-ligand interactions
import pandas as pd  # for creating dataframes and handling data

# Settings:
logging.getLogger(plip.__name__).setLevel(
    logging.WARNING
)  # disabling excessive INFO logs of the PLIP package


class Consts:
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
    pdb_filepath : str or pathlib.Path object
        Filepath of the PDB file containing the protein-ligand complex.

    Returns
    -------
        dict of dicts
        Dictionary of all different interaction data for all detected ligands.
        The keys of first dictionary correspond to the ligand-IDs of detected ligands in the PDB file.
        The keys of each sub-dictionary correspond to interaction types, as defined in PLIP.Consts.InteractionTypes.
    """
    protein_ligand_complex = PDBComplex()
    protein_ligand_complex.load_pdb(str(pdb_filepath))

    for ligand in protein_ligand_complex.ligands:
        protein_ligand_complex.characterize_complex(ligand)

    all_ligands_interactions = {}

    for ligand, ligand_binding_site in sorted(protein_ligand_complex.interaction_sets.items()):

        interaction_object = BindingSiteReport(
            ligand_binding_site
        )  # collect data about interactions

        interaction_data = {
            interaction_type.value: (
                [getattr(interaction_object, interaction_type.value + "_features")]
                + getattr(interaction_object, interaction_type.value + "_info")
            )
            for interaction_type in Consts.InteractionTypes
        }

        all_ligands_interactions[ligand] = interaction_data

    return all_ligands_interactions


def create_dataframe_of_ligand_interactions(ligand_interaction_data, interaction_type):
    """
    Create a Pandas DataFrame from interaction data of a specific ligand,
    for a specific interaction type.

    Parameters
    ----------
    ligand_interaction_data : dict
        Interaction data calculated by the 'calculate_interactions' function,
        where only one ligand's interaction data is chosen from the output of
        that function.
    interaction_type : Enum
        One of the enumerations from PLIP.Consts.InteractionTypes,
        specifying the type of interaction, for which the DataFrame should be created.

    Returns
    -------
        pandas DataFrame
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
    Create a protein-ligand-complex PDB file out of separate protein and ligand files.

    Parameters
    ----------
    protein_pdbqt_filepath : str or pathlib.Path object
        Filepath of the PDB file containing the protein.
    docking_pose_pdbqt_filepath : str or pathlib.Path object
        Filepath of the PDB file containing the ligand.
    ligand_id : str
        An identifier for the ligand to write into the PDB file.
    output_filepath : str or pathlib.Path object
        Output filepath of the PDB file containing the protein-ligand complex.

    Returns
    -------
        pathlib.Path object
        Complete filepath of the created protein-ligand-complex PDB file.
    """

    def pdbqt_to_pdbblock(pdbqt_filepath):
        lines = []
        with open(pdbqt_filepath) as file:
            for line in file:
                if line[:4] == "ATOM":
                    lines.append(line[:67].strip())
        return "\n".join(lines)

    protein_pdbblock = pdbqt_to_pdbblock(protein_pdbqt_filepath)

    ligand_pdbblock = pdbqt_to_pdbblock(docking_pose_pdbqt_filepath)
    # ligand_pdbblock = ligand_pdbblock.replace('ATOM', 'HETATM')
    # ligand_pdbblock = ligand_pdbblock.replace('UNL     ', (ligand_id[:8]+
    #                                    " "*(8-len(ligand_id))))

    full_output_filepath = str(output_filepath) + ".pdb"
    with open(full_output_filepath, "w") as file:
        file.write(protein_pdbblock)
        file.write(f"\nCOMPND    {ligand_id}\n")
        file.write(ligand_pdbblock)

    return Path(full_output_filepath)
