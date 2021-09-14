# Standard library:
import gzip  # for decompressing .gz files downloaded from DoGSiteScorer
from enum import Enum  # for creating enumeration classes
import io  # for creating file-like objects from strings of data (needed as input for some functions)
import logging  # for setting the logging level of some packages (i.e. to disable excessive logging default to some packages e.g. PLIP)
from pathlib import Path  # for creating folders and handling local paths
import subprocess  # for creating shell processes (needed to communicate with Smina program)
import time  # for creating pauses during the runtime (to wait for the response of API requests)
from urllib.parse import quote  # for url quoting

# 3rd-party packages:
from biopandas.pdb import PandasPdb  # for working with PDB files
from IPython.display import (
    Markdown,
    Image,
)  # ror more display options in the Jupyter Notebook
from ipywidgets import (
    AppLayout,
    Layout,
    Select,
    Button,
)  # for interactive outputs in the Jupyter Notebook
import matplotlib as mpl  # for changing the display settings of plots (see bottom of the cell: Settings)
from matplotlib import (
    colors,
)  # for plotting color-maps (for visualization of protein-ligand interactions)
import matplotlib.pyplot as plt  # for plotting of data
import nglview as nv  # for visualization of the protein and protein-related data (e.g. binding sites, docking poses)
import numpy as np  # for some more functionalities when using Pandas (e.g. for handling NaN values)
from openbabel import (
    pybel,
)  # for preparing protein and ligand for docking, and other manipulations of PDB files
import pandas as pd  # for creating dataframes and handling data
import plip  # for changing the logging setting of the package (see bottom of the cell: Settings)
from plip.structure.preparation import (
    PDBComplex,
)  # for calculating protein-ligand interactions
from plip.exchange.report import (
    BindingSiteReport,
)  # for calculating protein-ligand interactions
import pypdb  # for communicating with the RCSB Protein Data Bank (PDB) to fetch PDB files
from rdkit import (
    Chem,
)  # for handling ligand data and calculating ligand-related properties
from rdkit.Chem import Draw, AllChem, Descriptors, PandasTools, rdFMCS
import requests  # for communicating with web-service APIs

# In-house packages:
from opencadd.structure.core import Structure  # for manipulating PDB files

# Settings:
logging.getLogger(plip.__name__).setLevel(
    logging.WARNING
)  # disabling excessive INFO logs of the PLIP package
mpl.rcParams["figure.dpi"] = 300  # for plots with higher resolution
mpl.rcParams["agg.path.chunksize"] = 10000  # for handling plots with large number of data points
pd.set_option("display.max_columns", 100)  # showing 100 columns at most
pd.set_option("display.max_colwidth", 200)  # increasing the maximum column width
pd.set_option("display.width", None)  # showing each row in a single line

"""
Miscellaneous utilities for Talktorial T018
"""

class LeadOptimizationPipeline:
    def __init__(self, project_name):
        self.name = project_name

class Consts:
    """
    Data-class containing the required constants for defining the expected input data.
    The rest of the code will refer to these constants.
    """

    # Constants for the input dataframe
    class DataFrame:

        # Name of the columns
        class ColumnNames(Enum):
            SUBJECT = "Subject"
            PROPERTY = "Property"
            VALUE = "Value"
            DESCRIPTION = "Description"

        # Name of the subjects
        class SubjectNames(Enum):
            PROTEIN = "Protein"
            LIGAND = "Ligand"
            BINDING_SITE = "Binding Site"
            LIGAND_SIMILARITY_SEARCH = "Ligand Similarity Search"
            DOCKING = "Docking"
            INTERACTION_ANALYSIS = "Interaction Analysis"
            OPTIMIZED_LIGAND = "Optimized Ligand"

    # Constants for the input protein data
    # i.e. name of protein properties, and their respective allowed values
    class Protein:
        class Properties(Enum):
            INPUT_TYPE = "Input Type*"
            INPUT = "Input Value*"

        class InputTypes(Enum):
            PDB_CODE = "pdb_code"
            PDB_FILEPATH = "pdb_filepath"

    # Constants for the input ligand data
    class Ligand:
        class Properties(Enum):
            INPUT_TYPE = "Input Type*"
            INPUT = "Input Value*"

        class InputTypes(Enum):
            NAME = "name"
            IUPAC_NAME = "iupac_name"
            SMILES = "smiles"
            CID = "cid"
            INCHI = "inchi"
            INCHIKEY = "inchikey"

    # Constants for the input specification data regarding binding-site
    class BindingSite:
        class Properties(Enum):
            DEFINITION_METHOD = "Definition Method"
            COORDINATES = "Coordinates"
            LIGAND = "LIGAND"
            DETECTION_METHOD = "Detection Method"
            SELECTION_METHOD = "Selection Method"
            SELECTION_CRITERIA = "Selection Criteria"
            PROTEIN_CHAIN_ID = "Protein Chain-ID"
            PROTEIN_LIGAND_ID = "Protein Ligand-ID"

        class DefinitionMethods(Enum):
            DETECTION = "detection"
            LIGAND = "ligand"
            COORDINATES = "coordinates"

        class DetectionMethods(Enum):
            DOGSITESCORER = "dogsitescorer"

        class SelectionMethods(Enum):
            SORTING = "sorting"
            FUNCTION = "function"

        class SelectionCriteria(Enum):
            LIGAND_COVERAGE = "lig_cov"
            POCKET_COVERAGE = "poc_cov"
            VOLUME = "volume"
            ENCLOSURE = "enclosure"
            SURFACE = "surface"
            DEPTH = "depth"
            SURFACE_VOLUME_RATIO = "surf/vol"
            ELLIPSOID_MAIN_AXIS_C_A_RATIO = "ell c/a"
            ELLIPSOID_MAIN_AXIS_B_A_RATIO = "ell b/a"
            NUM_POCKET_ATOMS = "siteAtms"
            NUM_CARBONS = "Cs"
            NUM_NITROGENS = "Ns"
            NUM_OXYGENS = "Os"
            NUM_SULFURS = "Ss"
            NUM_OTHER_ELEM = "Xs"
            NUM_H_ACCEPTORS = "accept"
            NUM_H_DONORS = "donor"
            NUM_HYDROPHOBIC_INTERACTIONS = "hydrophobic_interactions"
            NUM_HYDROPHOBICITY = "hydrophobicity"
            NUM_METALS = "metal"
            NUM_NEGATIVE_AA = "negAA"
            NUM_POSITIVE_AA = "posAA"
            NUM_POLAR_AA = "polarAA"
            NUM_APOLAR_AA = "apolarAA"
            SIMPLE_SCORE = "simpleScore"
            DRUG_SCORE = "drugScore"

    # Constants for the input specification data regarding ligand similarity search
    class LigandSimilaritySearch:
        class Properties(Enum):
            SEARCH_ENGINE = "Search Engine"
            MIN_SIMILARITY_PERCENT = "Minumum Similarity [%]"
            MAX_NUM_RESULTS = "Maximum Number of Results"
            MAX_NUM_DRUGLIKE = "Maximum Number of Most Drug-Like Analogs to Continue With"

        class SearchEngines(Enum):
            PUBCHEM = "pubchem"

    # Constants for the input specification data regarding docking
    class Docking:
        class Properties(Enum):
            PROGRAM = "Program"
            NUM_POSES_PER_LIGAND = "Number of Docking Poses per Ligand"
            EXHAUSTIVENESS = "Exhaustiveness"
            RANDOM_SEED = "Random Seed"

        class Programs(Enum):
            SMINA = "smina"

    # Constants for the input specification data regarding interaction analysis
    class InteractionAnalysis:
        class Properties(Enum):
            PROGRAM = "Program"

        class Programs(Enum):
            PLIP = "plip"

    class OptimizedLigands:
        class Properties(Enum):
            NUM_RESULTS = "Number of Results"
            SELECTION_METHOD = "Selection Method"
            SELECTION_CRITERIA = "Selection Criteria"

        class SelectionMethods(Enum):
            SORTING = "sorting"
            FUNCTION = "function"

        class SelectionCriteria(Enum):
            BINDING_AFFINITY = "affinity"
            NUM_H_BONDS = "h_bond"
            NUM_HYDROPHOBIC_INTERACTIONS = "hydrophobic"
            NUM_SALT_BRIDGES = "salt_bridge"
            NUM_WATER_BRIDGES = "water_bridge"
            NUM_PI_STACKINGS = "pi_stacking"
            NUM_CATION_PI = "pi_cation"
            NUM_HALGON_BONDS = "halogen"
            NUM_METAL_BONDS = "metal"
            NUM_ALL_INTERACTIONS = "total_num_interactions"
            DRUG_SCORE_LIPINSKI = "drug_score_lipinski"
            DRUG_SCORE_QED = "drug_score_qed"
            DRUG_SCORE_CUSTOM = "drug_score_custom"
            DRUG_SCORE_TOTAL = "drug_score_total"

    # Constants for the input data regarding output paths
    class Output:
        class FolderNames(Enum):
            PROTEIN = "1_Protein"
            LIGAND = "2_Ligand"
            BINDING_SITE_DETECTION = "3_Binding Site Detection"
            SIMILARITY_SEARCH = "4_Ligand Similarity Search"
            DOCKING = "5_Docking"
            INTERACTION_ANALYSIS = "6_Interaction Analysis"
            VISUALIZATION = "7_Visualizations"
            OPTIMIZED_LIGANDS = "8_Optimized Ligands"

class IO:
    """
    Set of functions for handling the input/output data.
    """

    @staticmethod
    def create_dataframe_from_csv_input_file(
        input_data_filepath, list_of_index_column_names, list_of_columns_to_keep
    ):
        """
        Read a CSV file and create a pandas DataFrame with given specifications.

        Parameters
        ----------
        input_data_filepath : str or pathlib.Path object
            Path of the CSV data file.
        list_of_index_column_names : list of strings
            List of column names in the CSV file to be used as indices for the dataframe.
        list_of_columns_to_keep : list of strings
            List of column names from the CSV file to keep in the dataframe.

        Returns
        -------
            Pandas DataFrame
        """
        input_df = pd.read_csv(input_data_filepath)
        input_df.set_index(list_of_index_column_names, inplace=True)
        input_df.drop(input_df.columns.difference(list_of_columns_to_keep), 1, inplace=True)
        return input_df

    @staticmethod
    def copy_series_from_dataframe(input_df, index_name, column_name):
        """
        Take a multi-index dataframe, and make a copy of the data
        corresponding to a given index and column.

        Parameters
        ----------
        input_df : Pandas DataFrame
            The dataframe to extract the data from.
        index_name : str
            The index-value of the needed rows.
        column_name : str
            The column-name of the needed values.
        Returns
        -------
            Pandas Series
            Copy of the data corresponding to given index- and column-name.
        """
        subject_data = input_df.xs(index_name, level=0, axis=0)[column_name].copy()
        return subject_data

    @staticmethod
    def create_folder(folder_name, folder_path=""):
        """
        Create a folder with a given name in a given path.
        Also creates all non-existing parent folders.

        Parameters
        ----------
        folder_name : str
            Name of the folder to be created.

        folder_path : str (optional; default: current path)
            Either relative or absolute path of the folder to be created.

        Returns
        -------
            pathlib.Path object
            Full path of the created folder.
        """
        path = Path(folder_path) / folder_name
        # Creating the folder and all non-existing parent folders.
        path.mkdir(parents=True, exist_ok=True)
        return path

class Specs:

    """
    Data-class containing all the input data and output paths of the project.
    Take the filepath to the CSV input-data as well as output path, and
    internalize all the data as instance attributes.

    Parameters
    ----------
    input_data_filepath : str or pathlib.Path object
        Relative or absolute local path of the input CSV-data-file for the project.
    output_data_root_folder_path : str or pathlib.Path object
        Relative or absolute local path of root folder to store output data in.
    """

    # Defining the default values for all optional entries
    # -----------------------------------------------------
    class BindingSiteDefaults(Enum):
        DEFINITION_METHOD = Consts.BindingSite.DefinitionMethods.DETECTION
        DETECTION_METHOD = Consts.BindingSite.DetectionMethods.DOGSITESCORER
        SELECTION_METHOD = Consts.BindingSite.SelectionMethods.SORTING
        SELECTION_CRITERIA_SORTING = [
            Consts.BindingSite.SelectionCriteria.LIGAND_COVERAGE.value,
            Consts.BindingSite.SelectionCriteria.POCKET_COVERAGE.value,
        ]
        SELECTION_CRITERIA_FUNCTION = f"(df[{Consts.BindingSite.SelectionCriteria.DRUG_SCORE.value}] + df[{Consts.BindingSite.SelectionCriteria.SIMPLE_SCORE.value}]) / df[{Consts.BindingSite.SelectionCriteria.VOLUME}]"
        PROTEIN_CHAIN_ID = ""
        PROTEIN_LIGAND_ID = ""

    class LigandSimilaritySearchDefaults(Enum):
        SEARCH_ENGINE = Consts.LigandSimilaritySearch.SearchEngines.PUBCHEM
        MIN_SIMILARITY_PERCENT = 80
        MAX_NUM_RESULTS = 100
        MAX_NUM_DRUGLIKE = 30

    class DockingDefaults(Enum):
        PROGRAM = Consts.Docking.Programs.SMINA
        NUM_POSES_PER_LIGAND = 5
        EXHAUSTIVENESS = 10
        RANDOM_SEED = 1111

    class InteractionAnalysisDefaults(Enum):
        PROGRAM = Consts.InteractionAnalysis.Programs.PLIP

    class OptimizedLigandsDefaults(Enum):
        NUM_RESULTS = 1
        SELECTION_METHOD = Consts.OptimizedLigands.SelectionMethods.SORTING
        SELECTION_CRITERIA_SORTING = [
            Consts.OptimizedLigands.SelectionCriteria.BINDING_AFFINITY.value,
            Consts.OptimizedLigands.SelectionCriteria.NUM_ALL_INTERACTIONS.value,
        ]
        SELECTION_CRITERIA_FUNCTION = f"-2*df[{Consts.OptimizedLigands.SelectionCriteria.BINDING_AFFINITY.value}] + df[{Consts.OptimizedLigands.SelectionCriteria.NUM_ALL_INTERACTIONS}] * df[{Consts.OptimizedLigands.SelectionCriteria.DRUG_SCORE_TOTAL}]"

    # -----------------------------------------------------

    def __init__(self, input_data_filepath, output_data_root_folder_path):
        self.RawData = self.RawData(input_data_filepath)
        self.Protein = self.Protein(self.RawData.protein)
        self.Ligand = self.Ligand(self.RawData.ligand)
        self.BindingSite = self.BindingSite(self.RawData.binding_site)
        self.LigandSimilaritySearch = self.LigandSimilaritySearch(
            self.RawData.ligand_similarity_search
        )
        self.Docking = self.Docking(self.RawData.docking)
        self.InteractionAnalysis = self.InteractionAnalysis(self.RawData.interaction_analysis)
        self.OptimizedLigands = self.OptimizedLigands(self.RawData.optimized_ligand)
        self.OutputPaths = self.OutputPaths(output_data_root_folder_path)

    # Defining a sub-class for each part of the pipeline
    # -----------------------------------------------------
    class RawData:
        def __init__(self, input_data_filepath):
            self.filepath = input_data_filepath
            self.all_data = IO.create_dataframe_from_csv_input_file(
                input_data_filepath=input_data_filepath,
                list_of_index_column_names=[
                    Consts.DataFrame.ColumnNames.SUBJECT.value,
                    Consts.DataFrame.ColumnNames.PROPERTY.value,
                ],
                list_of_columns_to_keep=[Consts.DataFrame.ColumnNames.VALUE.value],
            )

            for subject_name in Consts.DataFrame.SubjectNames:
                subject_data = IO.copy_series_from_dataframe(
                    input_df=self.all_data,
                    index_name=subject_name.value,
                    column_name=Consts.DataFrame.ColumnNames.VALUE.value,
                )
                setattr(self, subject_name.name.lower(), subject_data)

    class Protein:
        def __init__(self, input_protein_data):
            self.input_type = Consts.Protein.InputTypes(
                input_protein_data[Consts.Protein.Properties.INPUT_TYPE.value]
            )
            self.input_value = input_protein_data[Consts.Protein.Properties.INPUT.value]

    class Ligand:
        def __init__(self, input_ligand_data):
            self.input_type = Consts.Ligand.InputTypes(
                input_ligand_data[Consts.Ligand.Properties.INPUT_TYPE.value]
            )
            self.input_value = input_ligand_data[Consts.Ligand.Properties.INPUT.value]

    class BindingSite:
        def __init__(self, input_binding_site_data):
            definition_method = input_binding_site_data[
                Consts.BindingSite.Properties.DEFINITION_METHOD.value
            ]
            # check if definition method is given, if not set to default (i.e. detection)
            self.definition_method = (
                Specs.BindingSiteDefaults.DEFINITION_METHOD
                if definition_method is np.nan
                else Consts.BindingSite.DefinitionMethods(definition_method)
            )

            if self.definition_method is Consts.BindingSite.DefinitionMethods.COORDINATES:
                coordinates_as_string = input_binding_site_data[
                    Consts.BindingSite.Properties.COORDINATES.value
                ]
                coordinates = coordinates_as_string.split(" ")
                self.coordinates = {"center": coordinates[:3], "size": coordinates[3:]}

            elif self.definition_method is Consts.BindingSite.DefinitionMethods.LIGAND:
                self.ligand = input_binding_site_data[Consts.BindingSite.Properties.LIGAND.value]

            elif self.definition_method is Consts.BindingSite.DefinitionMethods.DETECTION:
                detection_method = input_binding_site_data[
                    Consts.BindingSite.Properties.DETECTION_METHOD.value
                ]
                self.detection_method = (
                    Specs.BindingSiteDefaults.DETECTION_METHOD
                    if detection_method is np.nan
                    else Consts.BindingSite.DetectionMethods(detection_method)
                )

                protein_chain_id = input_binding_site_data[
                    Consts.BindingSite.Properties.PROTEIN_CHAIN_ID.value
                ]
                self.protein_chain_id = (
                    Specs.BindingSiteDefaultValues.PROTEIN_CHAIN_ID
                    if protein_chain_id is np.nan
                    else protein_chain_id
                )

                protein_ligand_id = input_binding_site_data[
                    Consts.BindingSite.Properties.PROTEIN_LIGAND_ID.value
                ]
                self.protein_ligand_id = (
                    Specs.BindingSiteDefaultValues.PROTEIN_LIGAND_ID
                    if protein_ligand_id is np.nan
                    else protein_ligand_id
                )

                selection_method = input_binding_site_data[
                    Consts.BindingSite.Properties.SELECTION_METHOD.value
                ]
                self.selection_method = (
                    Specs.BindingSiteDefaultValues.SELECTION_METHOD
                    if selection_method is np.nan
                    else Consts.BindingSite.SelectionMethods(selection_method)
                )

                if self.selection_method is Consts.BindingSite.SelectionMethods.SORTING:
                    selection_criteria = input_binding_site_data[
                        Consts.BindingSite.Properties.SELECTION_CRITERIA.value
                    ]
                    if selection_criteria is np.nan:
                        self.selection_criteria = (
                            Specs.BindingSiteDefaults.SELECTION_CRITERIA_SORTING.value
                        )
                    else:
                        # pass the column names through the SelectionCriteria enumeration class to make sure they are valid
                        self.selection_criteria = [
                            Consts.BindingSite.SelectionCriteria(pocket_property.strip()).value
                            for pocket_property in selection_criteria.split(",")
                        ]

                elif self.selection_method is Consts.BindingSite.SelectionMethods.FUNCTION:
                    selection_criteria = input_binding_site_data[
                        Consts.BindingSite.Properties.SELECTION_CRITERIA.value
                    ]
                    self.selection_criteria = (
                        Specs.BindingSiteDefaults.SELECTION_CRITERIA_FUNCTION.value
                        if selection_criteria is np.nan
                        else selection_criteria
                    )

    class LigandSimilaritySearch:
        def __init__(self, similarity_search_data):

            search_engine = similarity_search_data[
                Consts.LigandSimilaritySearch.Properties.SEARCH_ENGINE.value
            ]
            self.search_engine = (
                Specs.LigandSimilaritySearchDefaults.SEARCH_ENGINE
                if search_engine is np.nan
                else Consts.LigandSimilaritySearch.SearchEngines(search_engine)
            )

            min_similarity_percent = similarity_search_data[
                Consts.LigandSimilaritySearch.Properties.MIN_SIMILARITY_PERCENT.value
            ]
            self.min_similarity_percent = (
                Specs.LigandSimilaritySearchDefaults.MIN_SIMILARITY_PERCENT
                if min_similarity_percent is np.nan
                else min_similarity_percent
            )

            max_num_results = similarity_search_data[
                Consts.LigandSimilaritySearch.Properties.MAX_NUM_RESULTS.value
            ]
            self.max_num_results = (
                Specs.LigandSimilaritySearchDefaults.MAX_NUM_RESULTS
                if max_num_results is np.nan
                else max_num_results
            )

            max_num_druglike = int(
                similarity_search_data[
                    Consts.LigandSimilaritySearch.Properties.MAX_NUM_DRUGLIKE.value
                ]
            )
            self.max_num_druglike = (
                Specs.LigandSimilaritySearchDefaults.MAX_NUM_DRUGLIKE
                if max_num_druglike is np.nan
                else max_num_druglike
            )

    class Docking:
        def __init__(self, docking_data):

            program = docking_data[Consts.Docking.Properties.PROGRAM.value]
            self.program = (
                Specs.DockingDefaults.PROGRAM
                if program is np.nan
                else Consts.Docking.Programs(program)
            )

            num_poses_per_ligand = docking_data[
                Consts.Docking.Properties.NUM_POSES_PER_LIGAND.value
            ]
            self.num_poses_per_ligand = (
                Specs.DockingDefaults.NUM_POSES_PER_LIGAND.value
                if num_poses_per_ligand is np.nan
                else num_poses_per_ligand
            )

            exhaustiveness = docking_data[Consts.Docking.Properties.EXHAUSTIVENESS.value]
            self.exhaustiveness = (
                Specs.DockingDefaults.EXHAUSTIVENESS.value
                if exhaustiveness is np.nan
                else exhaustiveness
            )

            random_seed = docking_data[Consts.Docking.Properties.RANDOM_SEED.value]
            self.random_seed = (
                Specs.DockingDefaults.RANDOM_SEED.value if random_seed is np.nan else random_seed
            )

    class InteractionAnalysis:
        def __init__(self, interaction_analysis_data):

            program = interaction_analysis_data[
                Consts.InteractionAnalysis.Properties.PROGRAM.value
            ]
            self.program = (
                Specs.InteractionAnalysisDefaults.PROGRAM
                if program is np.nan
                else Consts.InteractionAnalysis.Programs(program)
            )

    class OptimizedLigands:
        def __init__(self, optimized_ligand_data):
            num_results = optimized_ligand_data[
                Consts.OptimizedLigands.Properties.NUM_RESULTS.value
            ]
            self.num_results = (
                Specs.OptimizedLigandsDefaults.NUM_RESULTS.value
                if num_results is np.nan
                else int(num_results)
            )

            selection_method = optimized_ligand_data[
                Consts.OptimizedLigands.Properties.SELECTION_METHOD.value
            ]
            self.selection_method = (
                Specs.OptimizedLigandsDefaults.SELECTION_METHOD
                if selection_method is np.nan
                else Consts.OptimizedLigands.SelectionMethods(selection_method)
            )

            if self.selection_method is Consts.OptimizedLigands.SelectionMethods.SORTING:
                selection_criteria = optimized_ligand_data[
                    Consts.OptimizedLigands.Properties.SELECTION_CRITERIA.value
                ]
                if selection_criteria is np.nan:
                    self.selection_criteria = (
                        Specs.OptimizedLigandsDefaults.SELECTION_CRITERIA_SORTING.value
                    )
                else:
                    # pass the column names through the SelectionCriteria enumeration class to make sure they are valid
                    self.selection_criteria = [
                        Consts.OptimizedLigands.SelectionCriteria(criterion.strip()).value
                        for criterion in selection_criteria.split(",")
                    ]

            elif self.selection_method is Consts.OptimizedLigands.SelectionMethods.FUNCTION:
                selection_criteria = optimized_ligand_data[
                    Consts.OptimizedLigands.Properties.SELECTION_CRITERIA.value
                ]
                self.selection_criteria = (
                    Specs.OptimizedLigandsDefaults.SELECTION_CRITERIA_FUNCTION.value
                    if selection_criteria is np.nan
                    else selection_criteria
                )

    class OutputPaths:
        """
        Data-class containing all the output paths for different parts of the pipeline.
        Take a main output path, and create all required parent folders,
        as well as sub-folders for each part of the pipeline.
        """

        def __init__(self, output_path):
            self.root = Path(output_path)
            for folder_name in Consts.Output.FolderNames:
                folder_path = IO.create_folder(folder_name.value, output_path)
                setattr(self, folder_name.name.lower(), folder_path)

class PDB:
    """
    Set of functions for working with PDB files.
    """

    @staticmethod
    def read_pdb_file_content(input_type, input_value):
        """
        Read the content of a PDB file either from a local path or via fetching the file from PDB webserver.

        Parameters
        ----------
        input_type : str
            Either 'pdb_code' or 'pdb_filepath'.

        input_value : str
            Either a valid PDB-code, or a local filepath of a PDB file.

        Returns
        -------
        str
            Content of the PDB file as a single string.
        """
        if input_type == "pdb_code":
            pdb_file_content = pypdb.get_pdb_file(input_value)
        elif input_type == "pdb_filepath":
            with open(input_value) as f:
                pdb_file_content = f.read()
        return pdb_file_content

    @staticmethod
    def fetch_and_save_pdb_file(pdb_code, output_filepath):
        """
        Fetch a PDB file from the PDB webserver and save locally.

        Parameters
        ----------
        pdb_code : str
            PDB-code of the protein structure.

        output_filepath : str or pathlib.Path object
            Local file path (including file name, but not the extension) to save the PDB file in.

        Returns
        -------
        pathlib.Path object
            The full path of the saved PDB file.
        """
        pdb_file_content = pypdb.get_pdb_file(pdb_code)
        full_filepath = str(output_filepath) + ".pdb"
        with open(full_filepath, "w") as f:
            f.write(pdb_file_content)
        return Path(full_filepath)

    @staticmethod
    def extract_molecule_from_pdb_file(molecule_name, input_filepath, output_filepath):
        """
        Extract a specific molecule (i.e. the protein or a ligand)
        from a local PDB file and save as a new PDB file in a given path.

        Parameters
        ----------
        molecule_name : str
            Name of the molecule to be extracted.
            For the protein, enter 'protein'. For a ligand, enter the ligand-ID.

        input_filepath : str or pathlib.Path object
            Local path of the original PDB file.

        output_filepath : str or pathlib.Path object
            Local file path (including file name) to save the PDB file of the extracted molecule in.

        Returns
        -------
            <Universe> Structure object
            Structure object of the extracted molecule.
        """

        pdb_structure = Structure.from_string(input_filepath)
        molecule_name = f"resname {molecule_name}" if molecule_name != "protein" else molecule_name
        extracted_structure = pdb_structure.select_atoms(molecule_name)
        extracted_structure.write(output_filepath)
        return extracted_structure

    @staticmethod
    def load_pdb_file_as_dataframe(pdb_file_text_content):
        """
        Transform the textual content of a PDB file into a dictionary of Pandas DataFrames.

        Parameters
        ----------
        pdb_file_text_content : str
            Textual content of a PDB file as a single string.

        Returns
        -------
        Dictionary of Pandas DataFrames.
        The dictionary has four entries with following keys: 'ATOM', 'HETATM', 'ANISOU' and 'OTHERS'.
        Each value is a Pandas DataFrame corresponding to the specific information described by the key.
        """
        ppdb = PandasPdb()
        pdb_df = ppdb._construct_df(pdb_file_text_content.splitlines(True))
        # TODO: Change _construct_df to read_pdb_from_lines once biopandas
        # cuts a new release (currently: 0.2.7), see https://github.com/rasbt/biopandas/pull/72
        return pdb_df

    @staticmethod
    def extract_info_from_pdb_file_content(pdb_file_text_content):
        """
        Extract some useful information from the contents of a PDB file.

        Parameters
        ----------
        pdb_file_text_content : str
            Textual content of a PDB file as a single string.

        Returns
        -------
            dict
            Dictionary of the successfully extracted information.
            Possible keys are:
                'structure_title' : str
                    Title of the PDB structure.
                'name' : str
                    Name of the protein.
                'chains' : list of strings
                    List of chain-IDs of the available chains in the protein.
                'ligands' : list of lists of strings
                    List of ligand information: [ligand-ID, chain-ID+residue number, number of heavy atoms]
        """

        pdb_content = pdb_file_text_content.strip().split("\n")
        for index in range(len(pdb_content)):
            pdb_content[index] = pdb_content[index].split(" ", 1)
            try:
                pdb_content[index][1] = pdb_content[index][1].strip()
                if pdb_content[index][1][-1] == ";":
                    pdb_content[index][1] = pdb_content[index][1][:-1]
                if (
                    pdb_content[index][0] in ["REMARK", "COMPND"]
                    and pdb_content[index][1][0].isdigit()
                ):
                    try:
                        pdb_content[index][1] = pdb_content[index][1].split(" ", 1)[1]
                    except:
                        pass
            except:
                pdb_content[index].append(" ")

        info = {}
        ligands = []
        for content in pdb_content:
            if content[0] == "TITLE":
                info["Structure Title"] = content[1]
            if content[0] == "COMPND" and content[1].startswith("MOLECULE: "):
                info["Name"] = content[1].split("MOLECULE: ")[1]
            if content[0] == "COMPND" and content[1].startswith("CHAIN: "):
                info["Chains"] = content[1].split("CHAIN: ")[1].split(", ")
            if content[0] == "HET":
                lig = list(filter(lambda x: x != "", content[1].split(" ")))
                lig[-1] = int(lig[-1])
                ligands.append(lig)
        info["Ligands"] = ligands
        return info

class NGLView:
    @staticmethod
    def protein(input_type, input_value, output_image_filename=None):
        """
        Visualize the protein.

        Parameters
        ----------
        input_type : str
            Either "pdb_code" or a file extension e.g. "pdb".
        input_value: str or pathlib.Path object
            Either the PDB-code of the protein, or a local filepath.
        output_image_filename : str (optional; default: None)
            Filename to save a static image of the protein.

        Returns
        -------
            NGLViewer object
            Interactive NGL viewer of the given Protein
            and (if available) its co-crystallized ligand.
        """

        if input_type == "pdb_code":
            viewer = nv.show_pdbid(input_value, height="600px")
        else:
            with open(input_value) as f:
                viewer = nv.show_file(
                    f, ext=input_type, height="600px", default_representation=False
                )
                viewer.add_representation("cartoon", selection="protein")

        viewer.add_representation(repr_type="ball+stick", selection="hetero and not water")
        viewer.center("protein")

        if output_image_filename != None:
            viewer.render_image(trim=True, factor=2)
            viewer._display_image()
            viewer.download_image(output_image_filename)
        return viewer

    @staticmethod
    def binding_site(protein_input_type, protein_input_value, ccp4_filepath):
        """
        3D visualization of a binding pocket using a CCP4 file.

        Parameters
        ----------
        protein_input_type : str
            Either "pdb_code" or a file extension e.g. "pdb".
        protein_input_value: str or pathlib.Path object
            Either the PDB-code of the protein, or a local filepath.
        ccp4_filepath : str
            Local file path of the output of the Binding Site Detection.

        Returns
        -------
        NGL viewer that visualizes the selected pocket at its respective position.
        """
        viewer = NGLView.protein(protein_input_type, protein_input_value)
        with open(ccp4_filepath, "rb") as f:
            viewer.add_component(f, ext="ccp4")
        viewer.center()

        return viewer

    @staticmethod
    def docking(
        protein_filepath,
        protein_file_extension,
        list_docking_poses_filepaths,
        docking_poses_file_extension,
        list_docking_poses_labels,
        list_docking_poses_affinities,
    ):
        """
        Visualize a list of docking poses
        in the protein structure, using NGLView.

        Parameters
        ----------
        protein_filepath : str or pathlib.Path object
            Filepath of the extracted protein structure used in docking experiment.
        protein_file_extension : str
            File extension of the protein file, e.g. "pdb", "pdbqt" etc.
        list_docking_poses_filepaths : list of strings/pathlib.Path objects
            List of filepaths for the separated docking poses.
        docking_poses_file_extension : str
            File extension of the docking-pose files, e.g. "pdb", "pdbqt" etc.
        list_docking_poses_labels : list of strings
            List of labels for docking poses to be used for the selection menu.
        list_docking_poses_affinities : list of strings/numbers
            List of binding affinities in kcal/mol, to be viewed for each docking pose.

        Returns
        -------
            NGLView viewer
            Interactive viewer containing the protein structure and all docking poses,
            with menu to select between docking poses.
        """

        # JavaScript code needed to update residues around the ligand
        # because this part is not exposed in the Python widget
        # Based on: http://nglviewer.org/ngl/api/manual/snippets.html
        _RESIDUES_AROUND = """
        var protein = this.stage.compList[0];
        var ligand_center = this.stage.compList[{index}].structure.atomCenter();
        var around = protein.structure.getAtomSetWithinPoint(ligand_center, {radius});
        var around_complete = protein.structure.getAtomSetWithinGroup(around);
        var last_repr = protein.reprList[protein.reprList.length-1];
        protein.removeRepresentation(last_repr);
        protein.addRepresentation("licorice", {{sele: around_complete.toSeleString()}});
        """
        print("Docking modes")
        print("(CID - mode)")
        # Create viewer widget
        viewer = nv.NGLWidget(height="860px")
        viewer.add_component(protein_filepath, ext=protein_file_extension)
        # viewer.add_representation("cartoon", selection="protein")
        # Select first atom in molecule (@0) so it holds the affinity label
        label_kwargs = dict(
            labelType="text",
            sele="@0",
            showBackground=True,
            backgroundColor="black",
        )
        list_docking_poses_affinities = list(
            map(lambda x: str(x) + " kcal/mol", list_docking_poses_affinities)
        )
        for docking_pose_filepath, ligand_label in zip(
            list_docking_poses_filepaths, list_docking_poses_affinities
        ):
            ngl_ligand = viewer.add_component(
                docking_pose_filepath, ext=docking_poses_file_extension
            )
            ngl_ligand.add_label(labelText=[str(ligand_label)], **label_kwargs)

        # Create selection widget
        #   Options is a list of (text, value) tuples. When we click on select, the value will be passed
        #   to the callable registered in `.observe(...)`
        selector = Select(
            options=[(label, i) for (i, label) in enumerate(list_docking_poses_labels, 1)],
            description="",
            rows=len(list_docking_poses_filepaths)
            if len(list_docking_poses_filepaths) <= 52
            else 52,
            layout=Layout(flex="flex-grow", width="auto"),
        )

        # Arrange GUI elements
        # The selection box will be on the left, the viewer will occupy the rest of the window
        display(AppLayout(left_sidebar=selector, center=viewer, pane_widths=[1, 6, 1]))

        # This is the event handler - action taken when the user clicks on the selection box
        # We need to define it here so it can "see" the viewer variable
        def _on_selection_change(change):
            # Update only if the user clicked on a different entry
            if change["name"] == "value" and (change["new"] != change["old"]):
                viewer.hide(
                    list(range(1, len(list_docking_poses_filepaths) + 1))
                )  # Hide all ligands (components 1-n)
                component = getattr(viewer, f"component_{change['new']}")
                component.show()  # Display the selected one
                component.center(500)  # Zoom view
                # Call the JS code to show sidechains around ligand
                viewer._execute_js_code(_RESIDUES_AROUND.format(index=change["new"], radius=6))

        # Register event handler
        selector.observe(_on_selection_change)
        # Trigger event manually to focus on the first solution
        _on_selection_change({"name": "value", "new": 1, "old": None})
        return viewer

    @staticmethod
    def interactions(
        protein_filepath,
        protein_file_extension,
        list_docking_poses_filepaths,
        docking_poses_file_extension,
        list_docking_poses_labels,
        list_docking_poses_affinities,
        list_docking_poses_plip_dicts,
    ):

        color_map = {
            "hydrophobic": [0.90, 0.10, 0.29],
            "hbond": [0.26, 0.83, 0.96],
            "waterbridge": [1.00, 0.88, 0.10],
            "saltbridge": [0.67, 1.00, 0.76],
            "pistacking": [0.75, 0.94, 0.27],
            "pication": [0.27, 0.60, 0.56],
            "halogen": [0.94, 0.20, 0.90],
            "metal": [0.90, 0.75, 1.00],
        }

        # Create selection widget
        # Options is a list of (text, value) tuples.
        # When we click on select, the value will be passed
        # to the callable registered in `.observe(...)`
        selector = Select(
            options=[(label, i) for (i, label) in enumerate(list_docking_poses_labels, 1)],
            description="",
            rows=len(list_docking_poses_filepaths)
            if len(list_docking_poses_filepaths) <= 52
            else 52,
            layout=Layout(flex="flex-grow", width="auto"),
        )

        # Arrange GUI elements
        # The selection box will be on the left,
        # the viewer will occupy the rest of the window (but it will be added later)
        app = AppLayout(
            left_sidebar=selector,
            center=None,
            pane_widths=[1, 6, 1],
            height="860px",
        )

        # Show color-map
        fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(12, 1))
        plt.subplots_adjust(hspace=1)
        fig.suptitle("Color-map of interactions", size=10, y=1.3)
        for ax, (interaction, color) in zip(fig.axes, color_map.items()):
            ax.imshow(np.zeros((1, 5)), cmap=colors.ListedColormap(color_map[interaction]))
            ax.set_title(interaction, loc="center", fontsize=10)
            ax.set_axis_off()
        plt.show()

        list_docking_poses_affinities = list(
            map(lambda x: str(x) + " kcal/mol", list_docking_poses_affinities)
        )

        # This is the event handler - action taken when the user clicks on the selection box
        # We need to define it here so it can "see" the viewer variable
        def _on_selection_change(change):
            # Update only if the user clicked on a different entry
            if change["name"] == "value" and (change["new"] != change["old"]):
                if app.center is not None:
                    app.center.close()

                # NGL Viewer
                app.center = viewer = nv.NGLWidget(height="860px", default=True, gui=True)
                prot_component = viewer.add_component(
                    protein_filepath, ext=protein_file_extension, default_representation=False
                )  # add protein
                prot_component.add_representation("cartoon")
                time.sleep(1)

                label_kwargs = dict(
                    labelType="text",
                    sele="@0",
                    showBackground=True,
                    backgroundColor="black",
                )
                lig_component = viewer.add_component(
                    list_docking_poses_filepaths[change["new"]], ext=docking_poses_file_extension
                )  # add selected ligand
                lig_component.add_label(
                    labelText=[str(list_docking_poses_affinities[change["new"]])], **label_kwargs
                )
                time.sleep(1)
                lig_component.center(duration=500)

                # Add interactions
                interactions = list_docking_poses_plip_dicts[change["new"]]

                interacting_residues = []

                for interaction_type, interaction_list in interactions.items():
                    color = color_map[interaction_type]
                    if len(interaction_list) == 1:
                        continue
                    df_interactions = pd.DataFrame.from_records(
                        interaction_list[1:], columns=interaction_list[0]
                    )
                    for _, interaction in df_interactions.iterrows():
                        name = interaction_type
                        viewer.shape.add_cylinder(
                            interaction["LIGCOO"],
                            interaction["PROTCOO"],
                            color,
                            [0.1],
                            name,
                        )
                        interacting_residues.append(interaction["RESNR"])
                # Display interacting residues
                res_sele = " or ".join([f"({r} and not _H)" for r in interacting_residues])
                res_sele_nc = " or ".join(
                    [f"({r} and ((_O) or (_N) or (_S)))" for r in interacting_residues]
                )

                prot_component.add_ball_and_stick(
                    sele=res_sele, colorScheme="chainindex", aspectRatio=1.5
                )
                prot_component.add_ball_and_stick(
                    sele=res_sele_nc, colorScheme="element", aspectRatio=1.5
                )

        # Register event handler
        selector.observe(_on_selection_change)
        # Trigger event manually to focus on the first solution
        _on_selection_change({"name": "value", "new": 1, "old": None})
        return app

class Protein:
    """
    Protein object with properties as attributes and methods to visualize and work with the protein.
    Take a protein identifier type and corresponding value,
    and create a Protein object, while assigning some properties as attributes.

    Parameters
    ----------
    identifier_type : enum 'InputTypes' from the 'Consts.Protein' class
        Type of the protein identifier, e.g. InputTypes.PDB_CODE.
    indentifier_value : str
        Value of the protein identifier, e.g. its PDB-code.
    protein_output_path : str or pathlib.Path object
        Output path of the project for protein data.
    """

    class Consts:
        # Available properties that are assigned as instance attributes upon instantiation.
        class Properties(Enum):
            STRUCTURE_TITLE = "Structure Title"
            NAME = "Name"
            CHAINS = "Chains"
            LIGANDS = "Ligands"
            RESIDUE_NUMBER_FIRST = "First Residue Number"
            RESIDUE_NUMBER_LAST = "Last Residue Number"
            RESIDUES_LENGTH = "Number of Residues"

    def __init__(self, identifier_type, identifier_value, protein_output_path):

        setattr(self, identifier_type.name.lower(), identifier_value)

        self.file_content = PDB.read_pdb_file_content(identifier_type.value, identifier_value)

        dict_of_dataframes = PDB.load_pdb_file_as_dataframe(self.file_content)
        for key, value in dict_of_dataframes.items():
            setattr(self, f"dataframe_PDBcontent_{key.lower()}", value)

        self.residue_number_first = self.dataframe_PDBcontent_atom.iloc[0]["residue_number"]
        self.residue_number_last = self.dataframe_PDBcontent_atom.iloc[-1]["residue_number"]
        self.residues_length = self.residue_number_last - self.residue_number_first + 1

        protein_info = PDB.extract_info_from_pdb_file_content(self.file_content)

        for protein_property in self.Consts.Properties:
            if protein_property.value in protein_info:
                setattr(
                    self,
                    protein_property.name.lower(),
                    protein_info[protein_property.value],
                )

        if identifier_type is Consts.Protein.InputTypes.PDB_CODE:
            self.pdb_filepath = PDB.fetch_and_save_pdb_file(
                identifier_value, str(protein_output_path) + "/" + identifier_value
            )

    def __call__(self):
        for protein_property in self.Consts.Properties:
            if hasattr(self, protein_property.name.lower()):
                display(
                    Markdown(
                        f"<span style='color:black'>&nbsp;&nbsp;&nbsp;&nbsp;{protein_property.value}: </span><span style='color:black'>**{getattr(self, protein_property.name.lower())}**</span>"
                    )
                )
        if hasattr(self, "pdb_code"):
            viewer = NGLView.protein("pdb_code", self.pdb_code)
        else:
            viewer = NGLView.protein("pdb", self.pdb_filepath)

        return viewer

    def __repr__(self):
        return f"<Protein: {self.name}>"                

class PubChem:
    """
    Implementation of the functionalities of PubChem PUG REST API.
    """

    # -----------------------------------------------------------------------------
    # Constants for API requests
    class APIConsts:
        """
        Constants for API requests.
        Request URLs should have the format:
            APIConsts.URLs.PROLOG + APIConsts.URLs.Inputs.<type>.value + ...
            ... <input_value> + APIConsts.URLs.Operations.GET_<property>.value + ...
            ... APIConsts.URLs.Outputs.<type>.value + <?optional parameters>
        """

        class URLs:
            PROLOG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"

            class Inputs(Enum):
                CID = "compound/cid/"
                NAME = "compound/name/"
                SMILES = "compound/smiles/"
                INCHI = "compound/inchi/"
                INCHIKEY = "compound/inchikey/"
                SIMILARITY_FROM_SMILES = "compound/similarity/smiles/"
                SIMILARITY_RESULTS = "compound/listkey/"

            class Operations(Enum):
                GET_CID = "/cids/"
                GET_NAME = "/property/title/"
                GET_SMILES = "/property/CanonicalSMILES/"
                GET_INCHI = "/property/InChI/"
                GET_INCHIKEY = "/property/InChIKey/"
                GET_IUPAC_NAME = "/property/IUPACName/"
                GET_DESCRIPTION = "/description/"
                GET_RECORD = "/record/"

            class Outputs(Enum):
                TXT = "TXT"
                JSON = "JSON"
                PNG = "PNG"
                CSV = "CSV"
                SDF = "SDF"
                XML = "XML"

        class ResponseMsgs:
            class SimilaritySearch(Enum):
                JOBKEY_KEY1 = "Waiting"
                JOBKEY_KEY2 = "ListKey"
                RESULT_KEY1 = "PropertyTable"
                RESULT_KEY2 = "Properties"

            class GetRecords(Enum):
                RESPONSE_KEY = "PC_Compounds"

            class GetDescription(Enum):
                RESPONSE_KEY1 = "InformationList"
                RESPONSE_KEY2 = "Information"

    # -----------------------------------------------------------------------------

    @staticmethod
    def send_request(partial_url, response_type="txt", optional_params=""):
        """
        Send an API request to PubChem and get the response data.

        Parameters
        ----------
        partial_url : str
            The URL part of the request consisting of input-type, input-value and operation.
            E.g. 'compound/cid/2244/property/CanonicalSMILES/' requests the SMILES of
            the compound with an CID of 2244.
        response_type : str (optional; default: txt)
            Expected response-type of the API request.
            Valid values are 'txt', 'json', 'png', 'csv' and 'sdf'.
            Valid values are stored in: PubChem.APIConsts.URLs.Outputs
        optional_params : str
            The URL part of the request consisting of optional parameters.

        Returns
        -------
            Datatype depends on the value of input parameter 'response_type'.
            The response data of the API request.
        """
        full_url = (
            PubChem.APIConsts.URLs.PROLOG
            + partial_url
            + getattr(PubChem.APIConsts.URLs.Outputs, response_type.upper()).value
            + f"?{optional_params}"
        )
        response = requests.get(full_url)
        response.raise_for_status()
        if response_type == "txt":
            response_data = response.text
        elif response_type == "json":
            response_data = response.json()
        else:
            response_data = response.content
        return response_data

    @staticmethod
    def convert_compound_identifier(
        input_id_type, input_id_value, output_id_type, output_data_type="txt"
    ):
        """
        Convert an identifier to another identifier, e.g. CID to SMILES, SMILES to IUPAC-name etc.

        Parameters
        ----------
        input_id_type : str
            Type of the input identifier.
            Valid values are: 'name', 'cid', 'smiles', 'inchi' and 'inchikey'.
            Valid values are stored in: PubChem.APIConsts.URLs.Inputs
        input_id_value : str, integer, list of strings or list of integers
            Value of the input identifier.
        output_id_type : str
            Type of the ouput identifier.
            Valid values are: 'name', 'cid', 'smiles', 'inchi', 'inchikey', 'iupac_name'.
            Valid values are stored in: PubChem.APIConsts.URLs.Operations
        output_data_type : str (optional; default: 'txt')
            Datatype of the output data.
            Valid values are 'txt', 'json', 'csv'.
            A list of all valid values are stored in: PubChem.APIConsts.URLs.Outputs

        Returns
        -------
            Datatype depends on the value of input parameter 'response_type'
            The response data of the API request.
        """
        if isinstance(input_id_value, list):
            input_id_value = ",".join(map(str, input_id_value))
        url = (
            getattr(PubChem.APIConsts.URLs.Inputs, input_id_type.upper()).value
            + str(input_id_value)
            + getattr(PubChem.APIConsts.URLs.Operations, f"GET_{output_id_type}".upper()).value
        )
        response_data = PubChem.send_request(url, output_data_type)
        if isinstance(input_id_value, list):
            return response_data.strip().split("\n")
        else:
            return response_data.strip()

    @staticmethod
    def get_compound_record(input_id_type, input_id_value, output_data_type="json"):
        """
        Get a full record of all physiochemical properties of the compound.

        Parameters
        ----------
        input_id_type : str
            Type of the input identifier.
            Valid values are: 'name', 'cid', 'smiles', 'inchi' and 'inchikey'.
            Valid values are stored in: PubChem.APIConsts.URLs.Inputs
        input_id_value : str or integer
            Value of the input identifier.
        output_data_type : str (optional; default: 'txt')
            Datatype of the output data.
            Valid values are 'txt', 'json', 'csv'.
            A list of all valid values are stored in: PubChem.APIConsts.URLs.Outputs

        Returns
        -------
            dict
            Dictionary keys are: 'id', 'atoms', 'bonds', 'coords', 'charge', 'props', 'count'
        """
        url = (
            getattr(PubChem.APIConsts.URLs.Inputs, input_id_type.upper()).value
            + str(input_id_value)
            + getattr(PubChem.APIConsts.URLs.Operations, "GET_RECORD").value
        )
        response_data = PubChem.send_request(url, output_data_type)[
            PubChem.APIConsts.ResponseMsgs.GetRecords.RESPONSE_KEY.value
        ][0]
        return response_data

    @staticmethod
    def get_description_from_smiles(smiles, output_data_type="json", printout=False):
        """
        Get a textual description of a molecule, including its usage, properties, source etc.

        Parameters
        ----------
        smiles : str
            SMILES of the molecule.
        output_data_type : str (optional; default: 'txt')
            Datatype of the output data.
            Valid values are 'txt', 'json', 'csv'.
            A list of all valid values are stored in: PubChem.APIConsts.URLs.Outputs
        printout : bool
            Whether to print the descriptions, or return the data.

        Returns
        -------
            list of dicts
            When the parameter printout is set to False, the raw data is
            returned as a list of dicts, where each element of the list
            corresponds to a description from a specific source (e.g. a journal article).
        """
        url = (
            PubChem.APIConsts.URLs.Inputs.SMILES.value
            + smiles
            + PubChem.APIConsts.URLs.Operations.GET_DESCRIPTION.value
        )
        response_data = PubChem.send_request(url, output_data_type)[
            PubChem.APIConsts.ResponseMsgs.GetDescription.RESPONSE_KEY1.value
        ][PubChem.APIConsts.ResponseMsgs.GetDescription.RESPONSE_KEY2.value]

        if printout:
            for entry in response_data:
                try:
                    print(entry["Description"] + "\n")
                except:
                    pass
        else:
            return response_data

    @staticmethod
    def similarity_search(
        smiles,
        min_similarity=80,
        max_num_results=100,
        output_data_type="json",
        max_num_attempts=30,
    ):
        """
        Run a similarity search on a molecule and get all the similar ligands.

        Parameters
        ----------
        smiles : str
            The canonical SMILES string for the given compound.
        min_similarity : int (optional; default: 80)
            The threshold of similarity in percent.
        max_num_results : int (optional; default: 100)
            The maximum number of feedback records.
        output_data_type : str (optional; default: 'json')
            Datatype of the output data.
            Valid values are 'txt', 'json', 'csv'.
            A list of all valid values are stored in: PubChem.APIConsts.URLs.Outputs
        max_num_attempts : int (optional; default: 30)
            Maximum number of attempts to fetch the API response, after the job has been submitted.
            Each failed attempt is followed by a 10-second pause.
        Returns
        -------
            Datatype depends on the 'output_data_type' parameter
            E.g. when set to "json", returns a list of dicts
            Each dictionary in the list corresponds to a similar compound,
            which has a 'CID' and a 'CanonicalSMILES' key.
        """
        escaped_smiles = quote(smiles).replace("/", ".")
        url = PubChem.APIConsts.URLs.Inputs.SIMILARITY_FROM_SMILES.value + escaped_smiles + "/"
        response_data = PubChem.send_request(
            url,
            output_data_type,
            f"Threshold={min_similarity}&MaxRecords={max_num_results}",
        )
        job_key = response_data[PubChem.APIConsts.ResponseMsgs.SimilaritySearch.JOBKEY_KEY1.value][
            PubChem.APIConsts.ResponseMsgs.SimilaritySearch.JOBKEY_KEY2.value
        ]

        url = (
            PubChem.APIConsts.URLs.Inputs.SIMILARITY_RESULTS.value
            + job_key
            + PubChem.APIConsts.URLs.Operations.GET_SMILES.value
        )

        num_attempts = 0
        while num_attempts < max_num_attempts:
            response_data = PubChem.send_request(url, output_data_type)
            if PubChem.APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY1.value in response_data:
                similar_compounds = response_data[
                    PubChem.APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY1.value
                ][PubChem.APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY2.value]
                break
            time.sleep(10)
            num_attempts += 1
        else:
            raise ValueError(f"Could not find matches in the response URL: {url}")
        return similar_compounds

class RDKit:
    @staticmethod
    def create_molecule_object(input_type, input_value):
        """
        Create an RDKit molecule object from various sources.

        Parameters
        ----------
        input_type : str
            Type of the input.
            Allowed input-types are: 'smiles', 'inchi', 'smarts', 'pdb_files'
        input_value : str
            Value of the corresponding input type.

        Returns
        -------
            RDKit molecule object.
        """

        functions = {
            "smiles": Chem.MolFromSmiles,
            "inchi": Chem.MolFromInchi,
            "smarts": Chem.MolFromSmarts,
            "pdb_file": Chem.MolFromPDBFile,
        }
        Molobj = functions[input_type](input_value)
        return Molobj

    @staticmethod
    def draw_molecules(
        list_mol_objs,
        list_legends=None,
        mols_per_row=3,
        sub_img_size=(550, 550),
        filepath=None,
    ):
        """
        Take a list of RDKit molecule objects and draws them as a grid image.

        Parameters
        ----------
        list_mol_objs: list
            List of RDKit molecule objects to be drawn.
        list_legends: list (optional)
            List of legends for the molecules.
            If not provided, the list indices (+1) will be used as legend.
        mols_per_row : int (optional; default: 3)
            Number of structures to show per row.
        sub_img_size : tuple (int, int)
            Size of each structure.
        filepath : str or pathlib.Path object
            Full filepath to save the image in.

        Returns
        -------
            RDKit MolsToGridImage object.
        """
        if list_legends == None:
            list_legends = list(range(1, len(list_mol_objs) + 1))
        figure = Draw.MolsToGridImage(
            list_mol_objs,
            molsPerRow=mols_per_row,
            subImgSize=sub_img_size,
            legends=list_legends,
        )
        if filepath != None:
            with open(str(filepath) + ".png", "wb") as f:
                f.write(figure.data)
        return figure

    @staticmethod
    def save_molecule_image_to_file(mol_obj, filepath):
        """
        Save the image of a single molecule as a PNG file.

        Parameters
        ----------
        mol_obj : RDKit Molecule objects
            The molecule to be saved as image.
        filepath : str or pathlib.Path object
            Full filpath to save the image in.

        Returns
        -------
            None
        """
        Draw.MolToFile(mol_obj, str(filepath) + ".png")

    @staticmethod
    def save_3D_molecule_to_SDfile(mol_obj, filepath):
        """
        Generate a 3D conformer and save as SDF file.

        Parameters
        ----------
        mol_obj : RDKit Molecule objects
            The molecule to be saved as SDF file.
        filepath : str or pathlib.Path object
            Full filpath to save the image in.

        Returns
        -------
            None
        """
        mol = Chem.AddHs(mol_obj)
        embedding = AllChem.EmbedMolecule(mol, maxAttempts=1000, clearConfs=True)
        uffoptim = AllChem.UFFOptimizeMolecule(mol, maxIters=1000)
        # check if calculations converged (both should return 0 when converged)
        if embedding + uffoptim != 0:
            raise ValueError("Embedding/Optimization failed to converge.")
        session = Chem.SDWriter(str(filepath) + ".sdf")
        session.write(mol)
        session.close()

    @staticmethod
    def calculate_similarity_dice(mol_obj1, mol_obj2):
        """
        Calculate the Dice similarity between two molecules,
        based on 4096-bit Morgan fingerprints with a radius of 2.

        Parameters
        ----------
        mol_obj1 : RDKit Molecule objects
            The first molecule.
        mol_obj2 : RDKit Molecule objects
            The second molecule.

        Returns
        -------
            float
            Dice similarity between the two molecules
        """
        morgan_fp_mol1 = AllChem.GetMorganFingerprintAsBitVect(mol_obj1, radius=2, nBits=4096)
        morgan_fp_mol2 = AllChem.GetMorganFingerprintAsBitVect(mol_obj2, radius=2, nBits=4096)
        dice_similarity = round(
            AllChem.DataStructs.DiceSimilarity(morgan_fp_mol1, morgan_fp_mol2), 2
        )
        return dice_similarity

    @staticmethod
    def calculate_druglikeness(mol_obj):
        """
        Calculate several molecular properties and drug-likeness scores,
        from an RDKit molecule object.

        Parameters
        ----------
        MolObj: RDKit molecule object
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
        # derived from Hopkins paper
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

class Ligand:
    """
    Ligand object with properties as attributes and methods to visualize and work with ligands.
    Take a ligand identifier type and corresponding value,
    and create a Ligand object, while assigning some properties as attributes.

    Parameters
    ----------
    identifier_type : enum 'InputTypes' from the 'Consts.Ligand' class
        Type of the ligand identifier, e.g. InputTypes.SMILES.

    indentifier_value : str
        Value of the ligand identifier, e.g. its SMILES.
    """

    class Consts:
        # Available properties that are assigned as instance attributes upon instantiation.
        class IdentifierTypes(Enum):
            NAME = "name"
            IUPAC_NAME = "iupac_name"
            SMILES = "smiles"
            CID = "cid"
            INCHI = "inchi"
            INCHIKEY = "inchikey"

    def __init__(self, identifier_type, identifier_value, ligand_output_path):

        self.dataframe = pd.DataFrame(columns=["Value"])
        self.dataframe.index.name = "Property"

        setattr(self, identifier_type.name.lower(), identifier_value)
        for identifier in self.Consts.IdentifierTypes:
            try:
                new_id = PubChem.convert_compound_identifier(
                    identifier_type.value, identifier_value, identifier.value
                )
                setattr(self, identifier.value, new_id)
                self.dataframe.loc[identifier.value] = new_id
            except:
                pass

        self.rdkit_obj = RDKit.create_molecule_object("smiles", self.smiles)

        dict_of_properties = RDKit.calculate_druglikeness(self.rdkit_obj)
        for property_ in dict_of_properties:
            setattr(self, property_, dict_of_properties[property_])
            self.dataframe.loc[property_] = dict_of_properties[property_]

        self.save_as_image(ligand_output_path / ("CID_" + self.cid))
        self.dataframe.to_csv(ligand_output_path / ("CID_" + self.cid + ".csv"))

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
        if (
            "." in self.smiles
        ):  # SMILES of salts contain a dot, separating the anion and the cation
            ions = self.smiles.split(".")
            length_ions = list(map(len, ions))
            molecule_index = length_ions.index(
                max(length_ions)
            )  # The parent molecule is almost always larger than its corresponding counter-ion
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
        return RDKit.calculate_similarity_dice(self.rdkit_obj, mol_obj)

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
        RDKit.save_molecule_image_to_file(self.rdkit_obj, filepath)

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
        RDKit.save_3D_molecule_to_SDfile(self.rdkit_obj, filepath)        

class DoGSiteScorer:
    """
    Class Containing all the required functions and constants
    to communicate with the DoGSiteScorer's Rest-API.
    """

    class APIConsts:
        # See https://proteins.plus/help/
        # and https://proteins.plus/help/dogsite_rest
        # for API specifications.

        class FileUpload:
            URL = "https://proteins.plus/api/pdb_files_rest"
            REQUEST_MSG = "pdb_file[pathvar]"
            RESPONSE_MSG = {
                "status": "status_code",
                "status_codes": {"accepted": "accepted", "denied": "bad_request"},
                "message": "message",
                "url_of_id": "location",
            }
            RESPONSE_MSG_FETCH_ID = {"message": "message", "id": "id"}

        class SubmitJob:
            URL = "https://proteins.plus/api/dogsite_rest"
            QUERY_HEADERS = {
                "Content-type": "application/json",
                "Accept": "application/json",
            }

            RESPONSE_MSG = {"url_of_job": "location"}

            RESPONSE_MSG_FETCH_BINDING_SITES = {
                "result_table": "result_table",
                "pockets_pdb_files": "residues",
                "pockets_ccp4_files": "pockets",
            }

    @staticmethod
    def upload_pdb_file(filepath):
        """
        Upload a PDB file to DoGSiteScorer webserver using their API
        and get back a dummy PDB-code, which can be used to submit a detection job.

        Parameters
        ----------
        filepath : str
            Relative or absolute path of the PDB file.

        Returns
        -------
            str
            Dummy PDB-code of the uploaded structure,
            which can then be used instead of a real PDB-code.
        """
        url = DoGSiteScorer.APIConsts.FileUpload.URL  # Read API URL from Constants
        request_msg = (
            DoGSiteScorer.APIConsts.FileUpload.REQUEST_MSG
        )  # Read API request message from Constants
        with open(filepath, "rb") as f:  # Open the local PDB file for reading in binary mode
            response = requests.post(
                url, files={request_msg: f}
            )  # Post API query and get the response
        response.raise_for_status()  # Raise HTTPError if one occured during query
        if response.ok:
            response_values = response.json()  # Turn the response values into a dict
            # If the request is accepted, the response will contain a URL,
            # from which the needed ID of the uploaded protein can be obtained.
            # Here, we store this URL from the response values in the url_of_id variable.
            url_of_id = response_values[
                DoGSiteScorer.APIConsts.FileUpload.RESPONSE_MSG["url_of_id"]
            ]
        else:
            raise ValueError(
                "Uploading PDB file failed.\n"
                + f"The response values are as follows: {response_values}"
            )
        # After getting the URL, it may take some time for the server to process the uploaded file
        # and return an ID. Thus, we try 30 times in intervals of 5 seconds to query the URL,
        # until we get the ID
        for try_nr in range(30):
            id_response = requests.get(url_of_id)  # Query the URL containing the ID
            id_response_values = id_response.json()  # Turn the response values into a dict
            # The response should contain the ID keyword:
            if id_response.ok & (
                DoGSiteScorer.APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"]
                in id_response_values
            ):
                id_response_values = id_response.json()
                protein_id = id_response_values[
                    DoGSiteScorer.APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"]
                ]
                break
            else:
                time.sleep(5)
        if not (
            id_response.ok
            & (
                DoGSiteScorer.APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"]
                in id_response_values
            )
        ):
            raise ValueError(
                "Fetching the ID of uploaded protein failed.\n"
                + f"The response values are as follows: {id_response_values}"
            )
        return protein_id

    @staticmethod
    def submit_job(pdb_id, ligand_id="", chain_id="", num_attempts=30):
        """
        Submit a protein structure to DoGSiteScorer webserver using their API
        and get back all the information on the detected binding-sites.

        Parameters
        ----------
        pdb_id : str
            Either a valid 4-letter PDB-code (e.g. '3w32'),
            or a dummy PDB-code of an uploaded PDB file.
        ligand_id : str
            DogSiteScorer-name of the co-crystallized ligand of interest, e.g. 'W32_A_1101'.
            DogSiteScorer naming convention is: <PDB ligand-ID>_<chain-ID>_<PDB residue number of the ligand>
        chain_id : str (optional; default: none)
            Chain-ID to limit the binding-site detection to.
        num_attempts : int (optional; default: 30)
            Number of times to attempt to fetch the results after the job has been submitted.
            After each failed attempt there is a 10-second pause.

        Returns
        -------
            Pandas DataFrame
            Dataframe containing all the information on all detected binding-sites.
        """
        response = requests.post(
            DoGSiteScorer.APIConsts.SubmitJob.URL,
            json={
                "dogsite": {
                    "pdbCode": pdb_id,  # PDB code of protein
                    "analysisDetail": "1",  # 1 = include subpockets in results
                    "bindingSitePredictionGranularity": "1",  # 1 = include drugablity scores
                    "ligand": ligand_id,  # if name is specified, ligand coverage is calculated
                    "chain": chain_id,  # if chain is specified, calculation is only performed on this chain
                }
            },
            headers=DoGSiteScorer.APIConsts.SubmitJob.QUERY_HEADERS,
        )

        response.raise_for_status()
        response_values = response.json()
        url_of_job = response_values[DoGSiteScorer.APIConsts.SubmitJob.RESPONSE_MSG["url_of_job"]]

        attempt_count = 0
        while attempt_count <= num_attempts:
            job_response = requests.get(url_of_job)
            job_response.raise_for_status()
            job_response_values = job_response.json()

            if (
                DoGSiteScorer.APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["result_table"]
                in job_response_values
            ):
                binding_site_data_url = job_response_values[
                    DoGSiteScorer.APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES[
                        "result_table"
                    ]
                ]
                binding_sites_pdb_files_urls = job_response_values[
                    DoGSiteScorer.APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES[
                        "pockets_pdb_files"
                    ]
                ]
                binding_sites_ccp4_files_urls = job_response_values[
                    DoGSiteScorer.APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES[
                        "pockets_ccp4_files"
                    ]
                ]
                break
            attempt_count += 1
            time.sleep(10)
        else:
            raise ValueError(
                "Fetching the binding-site data failed.\n"
                + f"The response values are as follows: {job_response_values}"
            )

        binding_site_data_table = requests.get(binding_site_data_url).text
        binding_site_data_file = io.StringIO(binding_site_data_table)
        binding_site_df = pd.read_csv(binding_site_data_file, sep="\t").set_index("name")
        binding_site_df["pdb_file_url"] = binding_sites_pdb_files_urls
        binding_site_df["ccp4_file_url"] = binding_sites_ccp4_files_urls
        return binding_site_df

    @staticmethod
    def save_binding_sites_to_file(binding_site_df, output_path):
        """
        download and save the PDB and CCP4 files corresponding to the calculated binding-sites.

        Parameters
        ----------
        binding_site_df : Pandas DataFrame
            Binding-site data retrieved from the DoGSiteScorer webserver.
        output_path : str or pathlib.Path object
            Local file path to save the files in.

        Returns
        -------
            None
        """
        for binding_site in binding_site_df.index:
            for column in ["pdb_file_url", "ccp4_file_url"]:
                response = requests.get(binding_site_df.loc[binding_site, column])
                response.raise_for_status()
                if column == "pdb_file_url":
                    response_file_content = response.content
                    file_extension = ".pdb"
                else:
                    response_file_content = gzip.decompress(response.content)
                    file_extension = ".ccp4"

                file_name = binding_site + file_extension
                with open(output_path / file_name, "wb") as f:
                    f.write(response_file_content)
        return

    @staticmethod
    def select_best_pocket(binding_site_df, selection_method, selection_criteria, ascending=False):
        """
        Select the best binding-site from the table of all detected binding-sites,
        either by sorting the binding-sites based on a set of properties in the table,
        or by applying a function on the property values.

        Parameters
        ----------
        binding_site_df : Pandas DataFrame
            Binding-site data retrieved from the DoGSiteScorer webserver.
        selection_method : str
            Selection method for selecting the best binding-site.
            Either 'sorting' or 'function'.
        selection_criteria : str or list
            When 'selection_method' is 'sorting':
                List of one or several property names.
            When 'selection_method' is 'function':
                Any valid python syntax that generates a list-like object
                with the same length as the number of detected binding-sites.
        ascending : bool (optional; default: False)
            If set to True, the binding-site with the lowest value will be selected,
            otherwise, the binding-site with the highest value is selected.

        Returns
        -------
            str
            Name of the selected binding-site.
        """
        df = binding_site_df
        if selection_method == "sorting":
            sorted_df = df.sort_values(by=selection_criteria, ascending=ascending)
        elif selection_method == "function":
            df["function_score"] = eval(selection_criteria)
            sorted_df = df.sort_values(by="function_score", ascending=ascending)

        selected_pocket_name = sorted_df.iloc[0].name
        return selected_pocket_name

    @staticmethod
    def calculate_pocket_coordinates_from_pocket_pdb_file(filepath):
        """
        Calculate the coordinates of a binding-site using the binding-site's PDB file
        downloaded from DoGSiteScorer.

        Parameters
        ----------
        filepath : str or pathlib.Path object
            Local filepath (including filename, without extension) of the binding-site's PDB file.

        Returns
        -------
            dict of lists of integers
            Binding-site coordinates in format:
            {'center': [x, y, z], 'size': [x, y, z]}
        """
        with open(str(filepath) + ".pdb") as f:
            pdb_file_text_content = f.read()
        pdb_file_df = PDB.load_pdb_file_as_dataframe(pdb_file_text_content)
        pocket_coordinates_data = pdb_file_df["OTHERS"].loc[5, "entry"]
        coordinates_data_as_list = pocket_coordinates_data.split(" ")
        coordinates = []
        for elem in coordinates_data_as_list:
            try:
                coordinates.append(float(elem))
            except:
                pass
        pocket_coordinates = {
            "center": coordinates[:3],
            "size": [coordinates[-1] * 2 for dim in range(3)],
        }
        return pocket_coordinates

    @staticmethod
    def get_pocket_residues(pocket_residues_url):
        """
        Gets residue IDs and names of a specified pocket (via URL).

        Parameters
        ----------
        pocket_residues_url : str
            URL of selected pocket file on the DoGSiteScorer web server.

        Returns
        -------
            pandas.DataFrame
            Table of residues names and IDs for the selected binding site.
        """
        # Retrieve PDB file content from URL
        result = requests.get(pocket_residues_url)
        # Get content of PDB file
        pdb_residues = result.text
        # Load PDB format as DataFrame
        ppdb = PandasPdb()
        # TODO: Change _construct_df to read_pdb_from_lines once biopandas
        # cuts a new release (currently: 0.2.7), see https://github.com/rasbt/biopandas/pull/72
        pdb_df = ppdb._construct_df(pdb_residues.splitlines(True))["ATOM"]
        # Drop duplicates
        # PDB file contains per atom entries, we only need per residue info
        pdb_df.sort_values("residue_number", inplace=True)
        pdb_df.drop_duplicates(subset="residue_number", keep="first", inplace=True)
        return pdb_df[["residue_number", "residue_name"]]

class BindingSiteDetection:
    """
    Automated binding-site detection process of the pipeline.
    Take in the Protein object, Specs.BindingSite object and
    the corresponding output path, and automatically run all the necessary calculations
    to output the suitable binding-site coordinates based on the input specifications of the project.

    Parameters
    ----------
    Protein : Protein object
        The Protein object of the project.
    BindingSiteSpecs : Specs.BindingSite object
        The binding-site specification data-class of the project.
    binding_site_output_path : str or pathlib.Path object
        Output path of the project's binding-site information.
    """

    class Consts:
        class DefinitionMethods(Enum):
            DETECTION = "detection"
            LIGAND = "ligand"
            COORDINATES = "coordinates"

    def __init__(self, Protein, BindingSiteSpecs, binding_site_output_path):

        self.output_path = binding_site_output_path
        self.Protein = Protein
        # derive the relevant function name from definition method
        definition_method_name = "compute_by_" + BindingSiteSpecs.definition_method.name.lower()
        # get the function from its name
        definition_method = getattr(self, definition_method_name)
        # call the function
        definition_method(Protein, BindingSiteSpecs, binding_site_output_path)

    def compute_by_coordinates(self, Protein, BindingSiteSpecs, binding_site_output_path):
        Protein.binding_site_coordinates = BindingSiteSpecs.coordinates

    def compute_by_ligand(self, Protein, BindingSiteSpecs, binding_site_output_path):
        ligand_object = PDB.extract_molecule_from_pdb_file(
            BindingSiteSpecs.protein_ligand_id,
            Protein.pdb_filepath,
            binding_site_output_path / BindingSiteSpecs.protein_ligand_id,
        )
        # calculate the geometric center of the molecule,
        # which represents the center of the rectangular box,
        # as well as the length of the molecule in each dimension,
        # which corresponds to the edge lengths of the rectangular box.
        # Also, we will add a 5 Å buffer in each dimension to allow the
        # correct placements of ligands that are bigger than the co-crystallized ligands
        # or bind in a different fashion.
        pocket_center = (
            ligand_object.positions.max(axis=0) + ligand_object.positions.min(axis=0)
        ) / 2
        pocket_size = ligand_object.positions.max(axis=0) - ligand_object.positions.min(axis=0) + 5
        pocket_coordinates = {
            "center": pocket_center.tolist(),
            "size": [pocket_size.tolist()],
        }
        Protein.binding_site_coordinates = pocket_coordinates
        return

    def compute_by_detection(self, Protein, BindingSiteSpecs, binding_site_output_path):
        # derive the relevant function name from detection method
        detection_method_name = "detect_by_" + BindingSiteSpecs.detection_method.name.lower()
        # get the function from its name
        detection_method = getattr(self, detection_method_name)
        # call the function
        detection_method(Protein, BindingSiteSpecs, binding_site_output_path)

    def detect_by_dogsitescorer(self, Protein, BindingSiteSpecs, binding_site_output_path):

        if hasattr(Protein, "pdb_code"):
            self.dogsitescorer_pdb_id = Protein.pdb_code
        elif hasattr(Protein, "pdb_filepath"):
            self.dogsitescorer_pdb_id = DoGSiteScorer.upload_pdb_file(Protein.pdb_filepath)

        # try to get the chain_id for binding-site detection if it's available in input data
        if hasattr(BindingSiteSpecs, "protein_chain_id"):
            self.dogsitescorer_chain_id = BindingSiteSpecs.protein_chain_id
        else:
            # if chain_id is not in input data, try to set it to the first chain found in pdb file
            try:
                self.dogsitescorer_chain_id = Protein.chains[0]
            # if no chain is found in pdb file either, leave the chain_id empty
            except:
                self.dogsitescorer_chain_id = ""

        # try to get the ligand_id for detection calculation if it's available in input data
        if hasattr(BindingSiteSpecs, "protein_ligand_id"):
            ligand_id = BindingSiteSpecs.protein_ligand_id
            # check if the given ligand_id is already given in the DoGSiteScorer format
            if "_" in ligand_id:
                self.dogsitescorer_ligand_id = ligand_id
                self.dogsitescorer_chain_id = ligand_id.split("_")[1][0]
            else:
                try:
                    for ligand in Protein.ligands:
                        if (ligand[0] == ligand_id) and (
                            ligand[1][0] == self.dogsitescorer_chain_id
                        ):
                            self.dogsitescorer_ligand_id = (
                                ligand_id + "_" + self.dogsitescorer_chain_id + "_" + ligand[1][1:]
                            )
                            break
                except:
                    self.dogsitescorer_ligand_id = ""

        self.dogsitescorer_binding_sites_df = DoGSiteScorer.submit_job(
            self.dogsitescorer_pdb_id,
            self.dogsitescorer_ligand_id,
            self.dogsitescorer_chain_id,
        )

        DoGSiteScorer.save_binding_sites_to_file(
            self.dogsitescorer_binding_sites_df, binding_site_output_path
        )

        self.best_binding_site_name = DoGSiteScorer.select_best_pocket(
            self.dogsitescorer_binding_sites_df,
            BindingSiteSpecs.selection_method.value,
            BindingSiteSpecs.selection_criteria,
        )

        self.best_binding_site_data = self.dogsitescorer_binding_sites_df.loc[
            self.best_binding_site_name
        ]

        self.best_binding_site_coordinates = (
            DoGSiteScorer.calculate_pocket_coordinates_from_pocket_pdb_file(
                binding_site_output_path / (self.best_binding_site_name)
            )
        )

        Protein.binding_site_coordinates = self.best_binding_site_coordinates
        return

    def visualize(self, pocket_name):
        """
        Visualize a detected pocket.

        Parameters
        ----------
        pocket_name : str
            Name of the detected pocket, which has a corresponding CCP4 file
            with the same name stored in the output folder for binding site data.

        Returns
        -------
            NGLView viewer
            Viewer showing the given pocket.
        """
        if hasattr(self.Protein, "pdb_code"):
            viewer = NGLView.binding_site(
                "pdb_code",
                self.Protein.pdb_code,
                str(self.output_path / pocket_name) + ".ccp4",
            )
        else:
            viewer = NGLView.protein(
                "pdb",
                self.Protein.pdb_filepath,
                str(self.output_path / pocket_name) + ".ccp4",
            )
        return viewer

    def visualize_best(self):
        """
        Visualize the selected binding pocket.
        The binding pocket should have a corresponding CCP4 file
        with the same name stored in the output folder for binding site data.

        Returns
        -------
            NGLView viewer
            Viewer showing the given pocket.
        """
        return self.visualize(self.best_binding_site_name)     

class LigandSimilaritySearch:
    """
    Automated ligand similarity-search process of the pipeline.
    Take in input Ligand object, Specs.LigandSimilaritySearch object,
    and the corresponding output path, and automatically run all the necessary
    processes to output a set of analogs with the highest drug-likeness scores.

    Parameters
    ----------
    Ligand_obj : Ligand object
        The Protein object of the project.
    BindingSiteSpecs : Specs.BindingSite object
        The binding-site specification data-class of the project.
    binding_site_output_path : str or pathlib.Path object
        Output path of the project's binding-site information.
    """

    def __init__(self, Ligand_obj, SimilaritySearchSpecs, similarity_search_output_path):

        if (
            SimilaritySearchSpecs.search_engine
            is Consts.LigandSimilaritySearch.SearchEngines.PUBCHEM
        ):
            analogs_info = PubChem.similarity_search(
                Ligand_obj.smiles,
                SimilaritySearchSpecs.min_similarity_percent,
                SimilaritySearchSpecs.max_num_results,
            )

        # create dataframe from initial results
        all_analog_identifiers_df = pd.DataFrame(analogs_info)
        all_analog_identifiers_df["Mol"] = all_analog_identifiers_df["CanonicalSMILES"].apply(
            lambda smiles: RDKit.create_molecule_object("smiles", smiles)
        )
        all_analog_identifiers_df["dice_similarity"] = all_analog_identifiers_df["Mol"].apply(
            lambda mol: RDKit.calculate_similarity_dice(Ligand_obj.rdkit_obj, mol)
        )
        all_analog_properties_df = pd.DataFrame(
            (
                all_analog_identifiers_df["Mol"].apply(
                    lambda mol: RDKit.calculate_druglikeness(mol)
                )
            ).tolist()
        )
        all_analogs_df = pd.concat([all_analog_identifiers_df, all_analog_properties_df], axis=1)
        all_analogs_df.index = all_analogs_df["CID"]
        all_analogs_df.drop("CID", axis=1, inplace=True)
        all_analogs_df.sort_values(by="dice_similarity", ascending=False, inplace=True)
        self.all_analogs = all_analogs_df
        all_analogs_df.drop("Mol", axis=1).to_csv(
            similarity_search_output_path / "analogs_all.csv"
        )

        analogs_dict = {}
        for analog_cid in (
            self.all_analogs.sort_values(by="drug_score_total", ascending=False)
            .head(SimilaritySearchSpecs.max_num_druglike)
            .index
        ):
            new_analog_object = Ligand(
                Consts.Ligand.InputTypes.CID,
                analog_cid,
                similarity_search_output_path,
            )

            new_analog_object.dice_similarity = RDKit.calculate_similarity_dice(
                Ligand_obj.rdkit_obj, new_analog_object.rdkit_obj
            )

            new_analog_object.dataframe.loc["similarity"] = new_analog_object.dice_similarity

            analogs_dict[new_analog_object.cid] = new_analog_object

        Ligand_obj.analogs = analogs_dict

class OBabel:
    """
    A set of functions based on the OpenBabel's pybel package,
    for preparing proteins and ligands for the docking experiment.
    """

    @staticmethod
    def optimize_structure_for_docking(
        pybel_structure_object,
        add_hydrogens=True,
        protonate_for_pH=7.4,
        calculate_partial_charges=True,
        generate_3d_structure=False,
    ):
        """
        Take a pybel structure object and prepare for docking.

        Parameters
        ----------
        pybel_structure_object : object
            The structure to optimize.
        add_hydrogens : bool (optional; default: True)
            Whether to add hydrogen atoms to the structure.
        protonate_for_pH : float (optional; default: 7.4)
            pH value to protonate the structure at.
            If set to 0 or False, will not protonate.
        calculate_partial_charges : bool (optional; default: True)
            Whether to calculate partial charges for each atom
        generate_3d_structure : bool (optional; default: False)
            Whether to generate a 3D conformation.
            Must be set to True if the pybel structure is 2D,
            for example is structure is made from SMILES string.

        Returns
        -------
            None
            The structure object is optimized in place.
        """
        if add_hydrogens:
            pybel_structure_object.addh()
        if protonate_for_pH:
            pybel_structure_object.OBMol.CorrectForPH(protonate_for_pH)
        if generate_3d_structure:
            pybel_structure_object.make3D(forcefield="mmff94s", steps=10000)
        if calculate_partial_charges:
            for atom in pybel_structure_object.atoms:
                atom.OBAtom.GetPartialCharge()
        return

    @staticmethod
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
            Pybel Molecule object
            Molecule object of PDB file optimized for docking.
        """
        # readfile() provides an iterator over the Molecules in a file.
        # To access the first (and possibly only) molecule in a file,
        # we use .next()
        molecule = next(pybel.readfile("pdb", str(pdb_filepath)))
        OBabel.optimize_structure_for_docking(molecule, protonate_for_pH=pH)
        molecule.write("pdbqt", str(pdbqt_filepath), overwrite=True)
        return molecule

    @staticmethod
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

        Returns
        -------
            None
        """
        molecule = pybel.readstring("smi", smiles)
        OBabel.optimize_structure_for_docking(
            molecule, protonate_for_pH=pH, generate_3d_structure=True
        )
        molecule.write("pdbqt", str(pdbqt_path), overwrite=True)
        return

    @staticmethod
    def split_multistructure_file(filetype, filepath, output_folder_path=None):
        """
        Split a multi-structure file into seperate files (with the same format)
        for each structure.Each file is named with consecutive numbers (starting at 1)
        at the end of the original filename.

        Parameters
        ----------
        filetype : str
            Type of the multimodel file to be split.
            Examples: 'sdf', 'pdb', 'pdbqt' etc.
            For a full list of acceptable file-types, call pybel.informats
        filepath : str or pathlib.Path
            Path of the file to be split.
        output_folder_path : str or pathlib.Path
            (optional; default: same folder as input filepath)
            Path of the output folder to save the split files.

        Returns
        -------
            list of pathlib.Path objects
            List of the full-paths for each split file.
        """
        filepath = Path(filepath)
        filename = filepath.stem
        if output_folder_path == None:
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

    @staticmethod
    def merge_molecules_to_single_file(
        list_of_pybel_molecule_objects, output_filetype, output_filepath
    ):
        """
        Create a single file containing several molecules.

        Parameters
        ----------
        list_of_pybel_molecule_objects : list of pybel Molecule objects
            List of molecule ojects to be merged into a single file.
        output_filetype : str
            Type of the output file.
            Examples: 'sdf', 'pdb', 'pdbqt' etc.
            For a full list of acceptable file-types, call pybel.outformats
        output_filepath : str or pathlib.Path
            Path of the output file including file-name, but excluding extension.

        Returns
        -------
            pathlib.Path object
            Full-path (including extension) of the output file.
        """
        fullpath = Path(str(output_filepath) + "." + output_filetype)

        merged_molecule_file = pybel.Outputfile(output_filetype, str(fullpath))

        for pybel_molecule_object in list_of_pybel_molecule_objects:
            merged_molecule_file.write(pybel_molecule_object)

        merged_molecule_file.close()
        return fullpath

class Smina:
    """
    Set of functions for communicating with the Smina docking program,
    and extracting data from its log file.
    """

    @staticmethod
    def dock(
        ligand_path,
        protein_path,
        pocket_center,
        pocket_size,
        output_path,
        output_format="pdbqt",
        num_poses=10,
        exhaustiveness=10,
        random_seed="",
        log=True,
    ):
        """
        Perform docking with Smina.

        Parameters
        ----------
        ligand_path : str or pathlib.Path
            Path to ligand PDBQT file that should be docked.
        protein_path : str or pathlib.Path
            Path to protein PDBQT file that should be docked to.
        pocket_center : iterable of float or int
            Coordinates defining the center of the binding site.
        pocket_size : iterable of float or int
            Lengths of edges defining the binding site.
        output_path : str or pathlib.Path
            Path to which docking poses should be saved, SDF or PDB format.
        num_poses : int or str
            Maximum number of poses to generate.
        exhaustiveness : int or str
            Accuracy of docking calculations.
        random_seed : int or str
            Seed number to make the docking deterministic for reproducibility.
        log : bool (optional; default: True)
            Whether to also write a log-file in the same output path for each docking.

        Returns
        -------
        output_text: str
            The output log of the docking calculation.
        """
        smina_command = (
            [
                "smina",
                "--ligand",
                str(ligand_path),
                "--receptor",
                str(protein_path),
                "--out",
                str(output_path) + "." + output_format,
                "--center_x",
                str(pocket_center[0]),
                "--center_y",
                str(pocket_center[1]),
                "--center_z",
                str(pocket_center[2]),
                "--size_x",
                str(pocket_size[0]),
                "--size_y",
                str(pocket_size[1]),
                "--size_z",
                str(pocket_size[2]),
                "--num_modes",
                str(num_poses),
                "--exhaustiveness",
                str(exhaustiveness),
            ]
            + (["--log", str(output_path) + "_log.txt"] if log else [])
            + (["--seed", str(random_seed)] if random_seed != "" else [])
        )

        output_text = subprocess.check_output(
            smina_command,
            universal_newlines=True,
        )
        return output_text

    @staticmethod
    def convert_log_to_dataframe(raw_log):
        """
        Convert docking's raw output log into a Pandas DataFrame.

        Parameters
        ----------
        raw_log : str
            Raw output log generated after docking.

        Returns
        -------
            Pandas DataFrame
            DataFrame containing columns 'mode', 'affinity[kcal/mol]',
            'dist from best mode_rmsd_l.b', and 'dist from best mode_rmsd_u.b'
            for each generated docking pose.
        """

        # Remove the unnecessary parts and extract the results table as list of lines
        # The table starts after the line containing: -----+------------+----------+----------
        # and ends before the word "Refine"
        log = (
            raw_log.split("-----+------------+----------+----------")[1]
            .split("Refine")[0]
            .strip()
            .split("\n")
        )

        # parse each line and remove everything except the numbers
        for index in range(len(log)):
            # turn each line into a list
            log[index] = log[index].strip().split(" ")
            # First element is the mode, which is an int.
            # The rest of the elements are either empty strings, or floats
            # Elements that are not empty strings should be extracted
            # (first element as int and the rest as floats)
            log[index] = [int(log[index][0])] + [
                float(value) for value in log[index][1:] if value != ""
            ]

        df = pd.DataFrame(
            log,
            columns=[
                "mode",
                "affinity[kcal/mol]",
                "dist from best mode_rmsd_l.b",
                "dist from best mode_rmsd_u.b",
            ],
        )
        df.index = df["mode"]
        df.drop("mode", axis=1, inplace=True)
        return df

class Docking:
    """
    Automated docking process of the pipeline.
    Take in a Protein and a list of ligands, and
    dock each ligand on the protein, using the given specifications.

    Parameters
    ----------
    Protein_object : object; instance of Protein class
        The protein to perform docking on.
    list_Ligand_objects : list of Ligand objects (instances of Ligand class)
        List of ligands to dock on the protein.
    DockingSpecs_object : object; instance of Specs.Docking class
        Specifications for the docking experiment.
    docking_output_path : str or pathlib.Path object
        Output folder path to store the docking data in.
    """

    def __init__(
        self,
        Protein_object,
        list_Ligand_objects,
        DockingSpecs_object,
        docking_output_path,
    ):
        self.pdb_filepath_extracted_protein = docking_output_path / (
            Protein_object.pdb_code + "_extracted_protein.pdb"
        )
        Protein_object.Universe = PDB.extract_molecule_from_pdb_file(
            "protein", Protein_object.pdb_filepath, self.pdb_filepath_extracted_protein
        )

        self.pdbqt_filepath_extracted_protein = docking_output_path / (
            Protein_object.pdb_code + "_extracted_protein_ready_for_docking.pdbqt"
        )

        OBabel.create_pdbqt_from_pdb_file(
            self.pdb_filepath_extracted_protein, self.pdbqt_filepath_extracted_protein
        )

        temp_list_results_df = []
        temp_list_master_df = []

        for ligand in list_Ligand_objects:
            ligand.pdbqt_filepath = docking_output_path / ("CID_" + ligand.cid + ".pdbqt")
            OBabel.create_pdbqt_from_smiles(ligand.remove_counterion(), ligand.pdbqt_filepath)

            ligand.docking_poses_filepath = docking_output_path / (
                "CID_" + ligand.cid + "_docking_poses.pdbqt"
            )

            raw_log = Smina.dock(
                ligand.pdbqt_filepath,
                self.pdbqt_filepath_extracted_protein,
                Protein_object.binding_site_coordinates["center"],
                Protein_object.binding_site_coordinates["size"],
                str(ligand.docking_poses_filepath).split(".")[0],
                output_format="pdbqt",
                num_poses=DockingSpecs_object.num_poses_per_ligand,
                exhaustiveness=DockingSpecs_object.exhaustiveness,
                random_seed=DockingSpecs_object.random_seed,
                log=True,
            )

            ligand.docking_poses_split_filepaths = OBabel.split_multistructure_file(
                "pdbqt", ligand.docking_poses_filepath
            )

            # Assigning the the dataframe of the Smina output
            # to the ligand's attribute 'dataframe_docking'
            df = Smina.convert_log_to_dataframe(raw_log)
            ligand.dataframe_docking = df.copy()

            # Extracting some useful information from the Smina-output dataframe
            # and assigning them as separate ligand attributes
            # Adding the same summarized information the ligand's general dataframe as well
            ligand.dataframe.loc["binding_affinity_best"] = ligand.binding_affinity_best = df[
                "affinity[kcal/mol]"
            ].min()
            ligand.dataframe.loc["binding_affinity_mean"] = ligand.binding_affinity_mean = df[
                "affinity[kcal/mol]"
            ].mean()
            ligand.dataframe.loc["binding_affinity_std"] = ligand.binding_affinity_std = df[
                "affinity[kcal/mol]"
            ].std()
            ligand.dataframe.loc[
                "docking_poses_dist_rmsd_lb_mean"
            ] = ligand.docking_poses_dist_rmsd_lb_mean = df["dist from best mode_rmsd_l.b"].mean()
            ligand.dataframe.loc[
                "docking_poses_dist_rmsd_lb_std"
            ] = ligand.docking_poses_dist_rmsd_lb_std = df["dist from best mode_rmsd_l.b"].std()
            ligand.dataframe.loc[
                "docking_poses_dist_rmsd_ub_mean"
            ] = ligand.docking_poses_dist_rmsd_ub_mean = df["dist from best mode_rmsd_u.b"].mean()
            ligand.dataframe.loc[
                "docking_poses_dist_rmsd_ub_std"
            ] = ligand.docking_poses_dist_rmsd_ub_std = df["dist from best mode_rmsd_u.b"].std()

            df["CID"] = ligand.cid
            df["drug_score_total"] = ligand.drug_score_total
            df.set_index(["CID", df.index], inplace=True)

            master_df = df.copy()
            master_df["filepath"] = ligand.docking_poses_split_filepaths

            temp_list_results_df.append(df)
            temp_list_master_df.append(master_df)

        self.results_dataframe = pd.concat(temp_list_results_df)
        self.master_df = pd.concat(temp_list_master_df)
        self.results_dataframe.to_csv(docking_output_path / "Results_Summary.csv")

    def visualize_all_poses(self):
        """
        Visualize docking poses of a all analogs, using NGLView.

        Returns
        -------
            NGLViewer object
            Interactive viewer of all analogs' docking poses,
            sorted by their binding affinities.
        """
        df = self.master_df.sort_values(by=["affinity[kcal/mol]", "CID", "mode"])
        self.visualize(df)
        return

    def visualize_analog_poses(self, cid):
        """
        Visualize docking poses of a certain analog, using NGLView.

        Parameters
        ----------
        cid : str or int
            CID of the analog.

        Returns
        -------
            NGLViewer object
            Interactive viewer of given analog's docking poses,
            sorted by their binding affinities.
        """
        df = self.master_df.xs(str(cid), level=0, axis=0, drop_level=False)
        self.visualize(df)
        return

    def visualize(self, fitted_master_df):
        """
        Visualize any collection of docking poses, using NGLView.

        Parameters
        ----------
        fitted_master_df : Pandas DataFrame
            Any section of the master docking dataframe,
            stored under self.master_df.

        Returns
        -------
            NGLViewer object
            Interactive viewer of given analog's docking poses,
            sorted by their binding affinities.
        """
        list_docking_poses_labels = list(
            map(lambda x: x[0] + " - " + str(x[1]), fitted_master_df.index.tolist())
        )
        NGLView.docking(
            self.pdb_filepath_extracted_protein,
            "pdb",
            fitted_master_df["filepath"].tolist(),
            "pdbqt",
            list_docking_poses_labels,
            fitted_master_df["affinity[kcal/mol]"].tolist(),
        )
        return

class PLIP:
    """
    Set of functions required to analyze protein-ligand interactions using the PLIP package.
    """

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

    @staticmethod
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
                for interaction_type in PLIP.Consts.InteractionTypes
            }

            all_ligands_interactions[ligand] = interaction_data

        return all_ligands_interactions

    @staticmethod
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

    @staticmethod
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

class InteractionAnalysis:
    """
    Automated protein-ligand interaction analysis process of the pipeline.

    Parameters
    ----------
    separated_protein_pdbqt_filepath : str or pathlib.Path object
        Filepath of the separated protein PDBQT file used in docking.
    list_Ligand_objects : list of Ligand objects (instances of Ligand class)
        List of ligands to analyze their interactions with the protein.
    docking_results_df : pandas DataFrame
        Summary dataframe created by the docking class.
    InteractionAnalysisSpecs_object : object; instance of Specs.InteractionAnalysis class
        Specifications for the interaction analysis processes.
    interaction_analysis_output_path : str or pathlib.Path object
        Output folder path to store the analyzed data in.
    """

    def __init__(
        self,
        separated_protein_pdbqt_filepath,
        separated_protein_pdb_filepath,
        protein_first_residue_number,
        list_Ligand_objects,
        docking_master_df,
        InteractionAnalysisSpecs_object,
        interaction_analysis_output_path,
    ):

        self._analogs = list_Ligand_objects
        self._pdb_filepath_extracted_protein = separated_protein_pdb_filepath

        if InteractionAnalysisSpecs_object.program is Consts.InteractionAnalysis.Programs.PLIP:
            results_df = docking_master_df.copy()
            results_df.drop("filepath", axis=1, inplace=True)
            results_df["total_num_interactions"] = 0

            interaction_master_df = docking_master_df.copy()

            for analog in list_Ligand_objects:
                analog.dataframe.loc["average_num_total_interactions", "Value"] = 0
                for interaction_type in PLIP.Consts.InteractionTypes:
                    analog.dataframe.loc[
                        f"average_num_{interaction_type.name.lower()}", "Value"
                    ] = 0

                for index, docking_pose_filepath in zip(
                    range(len(analog.docking_poses_split_filepaths)),
                    analog.docking_poses_split_filepaths,
                ):
                    analog.protein_complex_filepath = PLIP.create_protein_ligand_complex(
                        separated_protein_pdbqt_filepath,
                        docking_pose_filepath,
                        analog.cid,
                        interaction_analysis_output_path / (f"CID_{analog.cid}_{index+1}"),
                    )

                    # interaction_data will be dict of dicts, where each of the
                    # outer dict's items correspond to a ligand found in the pdb file
                    interaction_data = PLIP.calculate_interactions(analog.protein_complex_filepath)

                    # Since we are only passing PDB files with a single ligand, the outer dict
                    # will only have one item, which we extract:
                    ligand_interaction_data = interaction_data[list(interaction_data.keys())[0]]
                    # This extracted item is again a dict, where items correspond to
                    # different interaction-types.

                    # NOTICE: when using pybel to create the protein PDBQT file
                    # for the docking experiment, the residue numbers are reset (i.e. start at 1).
                    # Since this PDBQT file is also used to create a protein-ligand complext file
                    # for interaction-analysis with PLIP, the residue numbers in PLIP are also affected.
                    # Now we have to fix this here, before further processing the PLIP data.
                    # To do so, we simply loop through all the interaction data to find all the
                    # residue numbers, add the protein's first residue number to them, and subtract 1,
                    # so that we get back the original residue numbers. Also, since the data are stored
                    # in tuples, we have to convert them to a list first, in order to be able to change them.
                    for certain_interactions_data in ligand_interaction_data.values():
                        for single_interaction_data in range(1, len(certain_interactions_data)):
                            list_from_tuple = list(
                                certain_interactions_data[single_interaction_data]
                            )
                            list_from_tuple[0] += protein_first_residue_number - 1
                            certain_interactions_data[single_interaction_data] = tuple(
                                list_from_tuple
                            )

                    interaction_master_df.loc[(analog.cid, index + 1), "plip_dict"] = [
                        interaction_data[list(interaction_data.keys())[0]]
                    ]

                    for interaction_type in PLIP.Consts.InteractionTypes:
                        df = PLIP.create_dataframe_of_ligand_interactions(
                            interaction_data[list(interaction_data.keys())[0]],
                            interaction_type,
                        )
                        setattr(
                            analog,
                            f"docking_pose_{index+1}_interactions_{interaction_type.name.lower()}",
                            df,
                        )

                        results_df.loc[
                            (analog.cid, index + 1), interaction_type.name.lower()
                        ] = len(df)
                        analog.dataframe.loc[
                            f"average_num_{interaction_type.name.lower()}", "Value"
                        ] += len(df)
                        analog.dataframe.loc["average_num_total_interactions", "Value"] += len(df)

                        results_df[interaction_type.name.lower()] = pd.to_numeric(
                            results_df[interaction_type.name.lower()],
                            downcast="integer",
                        )
                        results_df.loc[(analog.cid, index + 1), "total_num_interactions"] += len(
                            df
                        )

                analog.num_total_interactions_highest = results_df.loc[
                    analog.cid, "total_num_interactions"
                ].max()
                analog.dataframe.loc["average_num_total_interactions", "Value"] /= len(
                    analog.docking_poses_split_filepaths
                )
                analog.num_total_interactions_mean = analog.dataframe.loc[
                    "average_num_total_interactions", "Value"
                ]
                for interaction_type in PLIP.Consts.InteractionTypes:
                    analog.dataframe.loc[
                        f"average_num_{interaction_type.name.lower()}", "Value"
                    ] /= len(analog.docking_poses_split_filepaths)

            results_df["total_num_interactions"] = pd.to_numeric(
                results_df["total_num_interactions"], downcast="integer"
            )
            self.results = results_df
            self.master_df = interaction_master_df

    def find_poses_with_specific_interactions(self, list_interaction_data, all_or_any):
        """
        Find docking poses containing a specific set of interactions.

        Parameters
        ----------
        list_interaction_data : list of lists
            List of desired interactions. Each sub-list should have the following format:
            [interaction_type, residue_number]
            interaction_type : str
                Type of desired interaction. Allowed values are:
                'h_bond', 'hydrophobic', 'salt_bridge', 'water_bridge',
                'pi_stacking', 'pi_cation', 'halogen', 'metal'
            residue_nr : int
                Residue number involved in the given interaction_type
            Example: [["h_bond", 793], ["hydrophobic", 860]]
        all_or_any : str
            Allowed values: "all", "any"
            "all": all given interactions should be present in a docking pose.
            "any": it is enough when one of the given interactions is present in a docking pose.

        Returns
        -------
            list of tuples
            List of identifiers for the docking poses in the format:
            (CID, pose_nr)
            CID : str
                CID of the analog with the eligible docking pose
            pose_nr : int
                Docking pose number of the eligible docking pose
        """
        list_eligible_analog_cid_docking_pose_nr_tuple = []
        for analog in self._analogs:
            for analog_docking_pose_nr in range(1, len(analog.dataframe_docking) + 1):
                num_hits_in_analog_docking_pose = 0
                for interaction_type, residue_nr in list_interaction_data:
                    interaction_df = getattr(
                        analog,
                        f"docking_pose_{analog_docking_pose_nr}_interactions_{interaction_type}",
                    )
                    if residue_nr in interaction_df["RESNR"].values:
                        num_hits_in_analog_docking_pose += 1
                if (
                    (all_or_any == "all")
                    and (num_hits_in_analog_docking_pose == len(list_interaction_data))
                ) or ((all_or_any == "any") and (num_hits_in_analog_docking_pose != 0)):
                    list_eligible_analog_cid_docking_pose_nr_tuple.append(
                        (analog.cid, analog_docking_pose_nr)
                    )
        return list_eligible_analog_cid_docking_pose_nr_tuple

    def visualize_all_interactions(self):
        """
        Visualize docking poses of a all analogs, using NGLView.
        The docking poses are sorted by their binding affinities in a menu.

        Returns
        -------
            None
        """
        df = self.master_df.sort_values(by=["affinity[kcal/mol]", "CID", "mode"])
        view = self.visualize(df)
        return view

    def visualize_analog_interactions(self, cid):
        """
        Visualize interactions in the docking poses of a certain analog, using NGLView.
        The docking poses are sorted by their binding affinities in a menu.

        Parameters
        ----------
        cid : str or int
            CID of the analog.

        Returns
        -------
            None
        """
        df = self.master_df.xs(str(cid), level=0, axis=0, drop_level=False)
        view = self.visualize(df)
        return view

    def visualize_docking_poses_interactions(self, list_of_cid_pose_nr_tuples):
        """
        Visualize interactions in a given set of docking poses, using NGLView.
        The docking poses are sorted in a menu, in the same order as the given list.

        Parameters
        ----------
        list_of_cid_pose_nr_tuples : list of tuples
            List of identifiers for the docking poses in the format:
            (CID, pose_nr)
            CID : str
                CID of the analog
            pose_nr : int
                Docking pose number
            Example: [("184614", 1), ("3628", 4)]

        Returns
        -------
            None
        """
        df = self.master_df.loc[list_of_cid_pose_nr_tuples]
        view = self.visualize(df)
        return view

    def visualize(self, fitted_master_df):
        """
        Visualize interactions in any collection of docking poses, using NGLView.
        The docking poses are sorted by their given order in a menu.

        Parameters
        ----------
        fitted_master_df : Pandas DataFrame
            Any section of the master InteractionAnalysis dataframe,
            stored under self.master_df.

        Returns
        -------
            None
        """
        list_docking_poses_labels = list(
            map(lambda x: x[0] + " - " + str(x[1]), fitted_master_df.index.tolist())
        )
        view = NGLView.interactions(
            self._pdb_filepath_extracted_protein,
            "pdb",
            fitted_master_df["filepath"].tolist(),
            "pdbqt",
            list_docking_poses_labels,
            fitted_master_df["affinity[kcal/mol]"].tolist(),
            fitted_master_df["plip_dict"].tolist(),
        )
        return view

    def plot_interaction_affinity_correlation(self):
        """
        View a correlation plot between binding affinity and number of interactions
        in each docking pose.

        Returns
        -------
            None
        """
        df = self.results.sort_values(by="affinity[kcal/mol]", ascending=True)

        fig, ax1 = plt.subplots()
        color = "tab:red"
        ax1.set_ylabel("Binding Affinity [kcal/mol]", color=color)
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.plot(
            list(map(abs, df["affinity[kcal/mol]"].tolist())),
            linewidth=0.5,
            linestyle="--",
            color="r",
            marker=".",
            markersize=2,
            markerfacecolor="blue",
            markeredgecolor="red",
        )

        ax2 = ax1.twinx()
        color = "tab:blue"
        ax2.set_ylabel("Number of Interactions", color=color)
        ax2.tick_params(axis="y", labelcolor=color)

        ax2.plot(
            df["total_num_interactions"].tolist(),
            linewidth=0.5,
            label="Total Interactions",
            color="black",
        )
        ax2.plot(
            df["h_bond"].tolist(),
            linewidth=0.5,
            label="H-bond Interactions",
            color="g",
            linestyle="--",
        )
        ax2.plot(
            df["hydrophobic"].tolist(),
            linewidth=0.5,
            label="Hydrophobic Interactions",
            linestyle="dashed",
        )

        plt.legend(fontsize=7)
        plt.show()
        return

class OptimizedLigands:
    """
    The automated selection process of optimized analog(s) at the end of the pipeline.
    Take in the whole project, create a short summary of results, and select the best
    optimized analogs based on user's specifications defined in the input data.
    """
    def __init__(self, project):

        self._project = project

        df = project.InteractionAnalysis.results.rename(columns={"affinity[kcal/mol]": "affinity"})

        self.higher_affinity_poses = (
            df[df["affinity"] < project.Ligand.binding_affinity_best]
            .copy()
            .sort_values(by="affinity")
        )
        self.higher_affinity_analogs = [
            project.Ligand.analogs[cid]
            for cid in self.higher_affinity_poses.index.get_level_values(0).unique()
        ]
        self.higher_interacting_poses = (
            df[
                df["total_num_interactions"]
                > project.Ligand.InteractionAnalysis.results["total_num_interactions"].max()
            ]
            .copy()
            .sort_values(by="total_num_interactions", ascending=False)
        )
        self.higher_interacting_analogs = [
            project.Ligand.analogs[cid]
            for cid in self.higher_interacting_poses.index.get_level_values(0).unique()
        ]
        self.higher_affinity_and_interacting_poses = df.loc[
            self.higher_affinity_poses.index.intersection(self.higher_interacting_poses.index)
        ]
        self.higher_affinity_and_interacting_analogs = [
            project.Ligand.analogs[cid]
            for cid in self.higher_affinity_and_interacting_poses.index.get_level_values(
                0
            ).unique()
        ]
        self.higher_affinity_and_interacting_and_druglike_analogs = [
            analog
            for analog in self.higher_affinity_and_interacting_analogs
            if analog.drug_score_total > project.Ligand.drug_score_total
        ]

        if (
            project.Specs.OptimizedLigands.selection_method
            is Consts.OptimizedLigands.SelectionMethods.SORTING
        ):
            df["affinity"] = df["affinity"].apply(abs)
            final_results_cids = (
                df.sort_values(
                    by=project.Specs.OptimizedLigands.selection_criteria,
                    ascending=False,
                )
                .index.get_level_values(0)
                .unique()
            )

        elif (
            project.Specs.OptimizedLigands.selection_method
            is Consts.OptimizedLigands.SelectionMethods.FUNCTION
        ):
            df["function_score"] = eval(selection_criteria)
            final_results_cids = (
                df.sort_values(by="function_score", ascending=False)
                .index.get_level_values(0)
                .unique()
            )

        self.output = [project.Ligand.analogs[cid] for cid in final_results_cids][
            : int(project.Specs.OptimizedLigands.num_results)
        ]

    def show_higher_affinity_analogs(self):
        for analog in self.higher_affinity_analogs:
            display(analog())

    def show_higher_interacting_analogs(self):
        for analog in self.higher_interacting_analogs:
            display(analog())

    def show_higher_affinity_and_interacting_analogs(self):
        for analog in self.higheraffinity_and_interacting_analogs:
            display(analog())

    def show_higher_affinity_and_interacting_and_druglike_analogs(self):
        for analog in self.higher_affinity_and_interacting_and_druglike_analogs:
            display(analog)

    def show_final_output(self):
        for analog in self.output:
            display(analog())

    def __call__(self):
        def pprint(text1, text2):
            display(
                Markdown(
                    f"<span style='color:blue'>{text1}</span><span style='color:black'>{text2}</span>"
                )
            )

        pprint(
            "Number of docking poses with higher binding affinity than highest binding affinity of ligand: ",
            len(self.higher_affinity_poses),
        )
        pprint(
            "&nbsp;&nbsp;&nbsp;&nbsp;CIDs of analogs corresponding to these docking poses: ",
            [analog.cid for analog in self.higher_affinity_analogs],
        )
        pprint(
            "Number of docking poses with higher number of total interactions than highest interacting pose of ligand: ",
            len(self.higher_interacting_poses),
        )
        pprint(
            "&nbsp;&nbsp;&nbsp;&nbsp;CIDs of analogs corresponding to these docking poses: ",
            [analog.cid for analog in self.higher_interacting_analogs],
        )
        pprint(
            "Number of docking poses with higher affinity and number of total interactions than best corresponding poses of ligand: ",
            len(self.higher_affinity_and_interacting_poses),
        )
        pprint(
            "&nbsp;&nbsp;&nbsp;&nbsp;CIDs of analogs corresponding to these docking poses: ",
            [analog.cid for analog in self.higher_affinity_and_interacting_analogs],
        )
        pprint(
            "CIDs of analogs with higher binding affinity, number of total interactions and drug-likeness score than ligand: ",
            [analog.cid for analog in self.higher_affinity_and_interacting_and_druglike_analogs],
        )
        pprint(
            "**CIDs of selected analogs as final output:** ",
            [analog.cid for analog in self.output],
        )

        pprint("Comparison between the input ligand and optimized analog: ", "")

        self.comparison_dataframe = df = pd.DataFrame(columns=["Input Ligand", "Optimized Analog"])
        df.loc["Drug-Score"] = [
            self._project.Ligand.drug_score_total,
            self._project.OptimizedLigands.output[0].drug_score_total,
        ]
        df.loc["Highest Binding Affinity"] = [
            self._project.Ligand.binding_affinity_best,
            self._project.OptimizedLigands.output[0].binding_affinity_best,
        ]
        df.loc["Highest Number of Total Interactions"] = [
            self._project.Ligand.num_total_interactions_highest,
            self._project.OptimizedLigands.output[0].num_total_interactions_highest,
        ]
        display(self.comparison_dataframe)
        return                                                