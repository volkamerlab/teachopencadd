# Standard Library
from enum import Enum  # for creating enumeration classes


class Consts:
    """
    Data-class containing the required constants for defining the expected input data.
    Contains all the possible keywords in the input dataframe, such as the column names,
    index names, subject names, properties, etc.
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
