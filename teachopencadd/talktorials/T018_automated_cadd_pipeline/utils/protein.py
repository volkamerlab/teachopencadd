"""
Contains protein class.
"""

from enum import Enum  # for creating enumeration classes
from pathlib import Path

from IPython.display import display, Markdown  # for more display options in the Jupyter Notebook
import numpy as np

from .consts import Consts
from .helpers import pdb, nglview


class Protein:
    """
    Protein object with properties as attributes and methods to visualize and work with the protein.
    Take a protein identifier type and corresponding value,
    and create a Protein object, while assigning some properties as attributes.

    Attributes
    ----------
    pdb_filepath : pathlib.Path
        Filepath of the protein PDB file.
    
    TODO see `Consts` class.
    """

    class Consts:
        """
        Available properties that are assigned as instance attributes upon instantiation.
        """

        class Properties(Enum):
            STRUCTURE_TITLE = "Structure Title"
            NAME = "Name"
            CHAINS = "Chains"
            LIGANDS = "Ligands"
            RESIDUE_NUMBER_FIRST = "First Residue Number"
            RESIDUE_NUMBER_LAST = "Last Residue Number"
            RESIDUES_LENGTH = "Number of Residues"

    def __init__(self, identifier_type, identifier_value, protein_output_path):
        """
        Parameters
        ----------
        identifier_type : enum 'InputTypes' from the 'Consts.Protein' class
            Type of the protein identifier, e.g. InputTypes.PDB_CODE.
        identifier_value : str
            Value of the protein identifier, e.g. its PDB code.
        protein_output_path : str or pathlib.Path
            Output path of the project for protein data.
        """

        setattr(self, identifier_type.name.lower(), identifier_value)
        # if the protein is inputted by its PDB code, also download its PDB file
        if identifier_type is Consts.Protein.InputTypes.PDB_CODE:
            self.pdb_filepath = pdb.fetch_and_save_pdb_file(
                identifier_value, Path(protein_output_path) / identifier_value
            )
        
        self.file_content = pdb.read_pdb_file_content(identifier_type.value, identifier_value)

        dict_of_dataframes = pdb.load_pdb_file_as_dataframe(self.file_content)
        for key, value in dict_of_dataframes.items():
            setattr(self, f"dataframe_PDBcontent_{key.lower()}", value)

        chain_ids = list(np.unique(self.dataframe_PDBcontent_atom["chain_id"].values))
        chain_lengths = []
        for chain_id in chain_ids:
            chain_lengths.append(
                self.dataframe_PDBcontent_atom[
                    self.dataframe_PDBcontent_atom["chain_id"] == chain_id
                ].shape[0]
            )
        index_of_longest_chain = chain_ids[chain_lengths.index(max(chain_lengths))]
        longest_chain = self.dataframe_PDBcontent_atom[
            self.dataframe_PDBcontent_atom["chain_id"] == index_of_longest_chain
        ]
        self.residue_number_first = longest_chain.iloc[0]["residue_number"]
        self.residue_number_last = longest_chain.iloc[-1]["residue_number"]
        self.residues_length = self.residue_number_last - self.residue_number_first + 1

        protein_info = pdb.extract_info_from_pdb_file_content(self.file_content)

        for protein_property in protein_info: 
            setattr(
                self,
                self.Consts.Properties(protein_property).name.lower(),
                protein_info[protein_property],
            )

    def __call__(self):
        for protein_property in self.Consts.Properties:
            # Display property if available
            if hasattr(self, protein_property.name.lower()):
                display(
                    Markdown(
                        f"<span style='color:black'>"
                        f"&nbsp;&nbsp;&nbsp;&nbsp;{protein_property.value}: "
                        f"</span><span style='color:black'>"
                        f"**{getattr(self, protein_property.name.lower())}**</span>"
                    )
                )
        if hasattr(self, "pdb_code"):
            viewer = nglview.protein("pdb_code", self.pdb_code)
        else:
            viewer = nglview.protein("pdb", self.pdb_filepath)
        return viewer

    def __repr__(self):
        return f"<Protein: {self.name}>"
