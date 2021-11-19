"""
Contains the Ligand class of the pipeline.
"""

from enum import Enum  # for creating enumeration classes
from pathlib import Path

import pandas as pd  # for creating dataframes and handling data
from rdkit.Chem import PandasTools # for displaying structures inside Pandas DataFrame

from .helpers import pubchem, rdkit


class Ligand:
    """
    Ligand object with properties as attributes and methods to visualize and work with ligands.
    Take a ligand identifier type and corresponding value,
    and create a Ligand object, while assigning some properties as attributes.

    Attributes
    ----------
    dataframe : Pandas DataFrame
        Dataframe containing the most important data available for the ligand.
        Each time a process is performed on the ligand (e.g. docking), 
        the important results are added to the dataframe.
    rdkit_obj : rdkit.Chem.rdchem.Mol
        RDKit molecule object for the ligand with its own set of attributes.
    
    TODO see `Consts` class. More attributes?
    """

    class Consts:
        """
        Available properties that are assigned as instance attributes upon instantiation.
        """

        class IdentifierTypes(Enum):
            NAME = "name"
            IUPAC_NAME = "iupac_name"
            SMILES = "smiles"
            CID = "cid"
            INCHI = "inchi"
            INCHIKEY = "inchikey"

    def __init__(self, identifier_type, identifier_value, ligand_output_path):
        """
        Parameters
        ----------
        identifier_type : enum 'InputTypes' from the 'Consts.Ligand' class
            Type of the ligand identifier, e.g. InputTypes.SMILES.
        indentifier_value : str
            Value of the ligand identifier, e.g. its SMILES.
        ligand_output_path : str or pathlib.Path
            Output path of the project for ligand data.
        """

        self.dataframe = pd.DataFrame(columns=["Value"])
        self.dataframe.index.name = "Property"

        setattr(self, identifier_type.name.lower(), identifier_value)
        for identifier in self.Consts.IdentifierTypes:
            new_id = pubchem.convert_compound_identifier(
                identifier_type.value, identifier_value, identifier.value
            )
            setattr(self, identifier.value, new_id)
            self.dataframe.loc[identifier.value] = new_id

        self.rdkit_obj = rdkit.create_molecule_object("smiles", self.smiles)

        dict_of_properties = rdkit.calculate_druglikeness(self.rdkit_obj)
        for property_ in dict_of_properties:
            setattr(self, property_, dict_of_properties[property_])
            self.dataframe.loc[property_] = dict_of_properties[property_]

        ligand_output_path = Path(ligand_output_path)
        self.save_as_image(ligand_output_path / f"CID_{self.cid}")
        self.dataframe.to_csv(ligand_output_path / f"CID_{self.cid}.csv")

    def __repr__(self):
        return f"<Ligand CID: {self.cid}>"

    def __call__(self):
        df = pd.DataFrame(columns=["smiles"])
        df.loc[1] = self.smiles
        PandasTools.AddMoleculeColumnToFrame(df, smilesCol="smiles")
        romol = df.loc[1, "ROMol"]

        return pd.concat({romol: self.dataframe}, names=["Structure"])

    def remove_counterion(self):
        """
        Remove the counter-ion from the SMILES of a salt.

        Returns
        -------
        str
            SMILES of the molecule without its counter-ion.
        """
        
        # SMILES of salts contain a dot, separating the anion and the cation
        if "." in self.smiles:  
            ions = self.smiles.split(".")
            length_ions = list(map(len, ions))
            # The parent molecule is almost always larger than its corresponding counter-ion
            molecule_index = length_ions.index(max(length_ions))  
            molecule_smiles = ions[molecule_index]
        else:
            molecule_smiles = self.smiles
        return molecule_smiles

    def dice_similarity(self, mol_obj):
        """
        Calculate Dice similarity between the ligand and another input ligand,
        based on 4096-bit Morgan fingerprints with a radius of 2.

        Parameters
        ----------
        mol_obj : RDKit molecule object
            The molecule to calculate the Dice similarity with.

        Returns
        -------
        float
            Dice similarity between the two ligands.
        """
        return rdkit.calculate_similarity_dice(self.rdkit_obj, mol_obj)

    def save_as_image(self, filepath):
        """
        Save the ligand as image.

        Parameters
        ----------
        filepath : str or pathlib.Path object
            Full filepath of the image to be saved.

        Returns
        -------
        None
        """
        rdkit.save_molecule_image_to_file(self.rdkit_obj, filepath)

    def save_3D_structure_as_SDF_file(self, filepath):
        """
        Generate a 3D conformer and save as SDF file.

        Parameters
        ----------
        filepath : str or pathlib.Path object
            Full filpath to save the image in.

        Returns
        -------
        None
        """
        rdkit.save_3D_molecule_to_SDfile(self.rdkit_obj, filepath)
