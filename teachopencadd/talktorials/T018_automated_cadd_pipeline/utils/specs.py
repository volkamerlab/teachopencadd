"""
Contains pipeline's specification class.
"""

from enum import Enum  # for creating enumeration classes
from pathlib import Path  # for creating folders and handling local paths

import numpy as np  # for some more functionalities when using Pandas (e.g. for handling NaN values)

from .consts import Consts
from .helpers import io


class Specs:
    """
    Class containing all the input data and output paths of the project.
    Take the filepath to the CSV input data, as well as a main output path, 
    and internalize all the data as instance attributes, categorized into
    sub-classes corresponding to each process of the pipeline.
    The validity and integrity of the data will be examined,
    and any missing optional parameter will be set to its default value.
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
        SELECTION_CRITERIA_FUNCTION = (
            f"(df[{Consts.BindingSite.SelectionCriteria.DRUG_SCORE.value}] "
            f"+ df[{Consts.BindingSite.SelectionCriteria.SIMPLE_SCORE.value}]) "
            f"/ df[{Consts.BindingSite.SelectionCriteria.VOLUME}]"
        )
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
        SELECTION_CRITERIA_FUNCTION = (
            f"-2*df[{Consts.OptimizedLigands.SelectionCriteria.BINDING_AFFINITY.value}] "
            f"+ df[{Consts.OptimizedLigands.SelectionCriteria.NUM_ALL_INTERACTIONS}] "
            f"* df[{Consts.OptimizedLigands.SelectionCriteria.DRUG_SCORE_TOTAL}]"
        )
    # -----------------------------------------------------

    def __init__(self, input_data_filepath, output_data_root_folder_path):
        """
        Parameters
        ----------
        input_data_filepath : str or pathlib.Path
            Relative or absolute local path of the input CSV file for the project.
        output_data_root_folder_path : str or pathlib.Path
            Relative or absolute local path of the root folder to store output data in.
        """

        input_data_filepath = Path(input_data_filepath)
        output_data_root_folder_path = Path(output_data_root_folder_path)

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

    class RawData:
        """
        Subclass containing the raw data from the input CSV file,
        initialized automatically by the parent class.
        """

        def __init__(self, input_data_filepath):
            self.filepath = input_data_filepath
            self.all_data = io.create_dataframe_from_csv_input_file(
                input_data_filepath=input_data_filepath,
                list_of_index_column_names=[
                    Consts.DataFrame.ColumnNames.SUBJECT.value,
                    Consts.DataFrame.ColumnNames.PROPERTY.value,
                ],
                list_of_columns_to_keep=[Consts.DataFrame.ColumnNames.VALUE.value],
            )

            for subject_name in Consts.DataFrame.SubjectNames:
                subject_data = io.copy_series_from_dataframe(
                    input_df=self.all_data,
                    index_name=subject_name.value,
                    column_name=Consts.DataFrame.ColumnNames.VALUE.value,
                )
                setattr(self, subject_name.name.lower(), subject_data)

    class Protein:
        """
        Subclass containing the input protein data,
        initialized automatically by the parent class.
        """

        def __init__(self, input_protein_data):
            self.input_type = Consts.Protein.InputTypes(
                input_protein_data[Consts.Protein.Properties.INPUT_TYPE.value]
            )
            self.input_value = input_protein_data[Consts.Protein.Properties.INPUT.value]

    class Ligand:
        """
        Subclass containing the input ligand data,
        initialized automatically by the parent class.
        """

        def __init__(self, input_ligand_data):
            self.input_type = Consts.Ligand.InputTypes(
                input_ligand_data[Consts.Ligand.Properties.INPUT_TYPE.value]
            )
            self.input_value = input_ligand_data[Consts.Ligand.Properties.INPUT.value]

    class BindingSite:
        """
        Subclass containing input specifications for 
        the binding site detection process of the pipeline,
        initialized automatically by the parent class.
        """

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
                    Specs.BindingSiteDefaults.PROTEIN_CHAIN_ID.value
                    if protein_chain_id is np.nan
                    else protein_chain_id
                )

                protein_ligand_id = input_binding_site_data[
                    Consts.BindingSite.Properties.PROTEIN_LIGAND_ID.value
                ]
                self.protein_ligand_id = (
                    Specs.BindingSiteDefaults.PROTEIN_LIGAND_ID.value
                    if protein_ligand_id is np.nan
                    else protein_ligand_id
                )

                selection_method = input_binding_site_data[
                    Consts.BindingSite.Properties.SELECTION_METHOD.value
                ]
                self.selection_method = (
                    Specs.BindingSiteDefaults.SELECTION_METHOD
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
                        # pass the column names through the SelectionCriteria enumeration class
                        # to make sure they are valid
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

                else:
                    raise ValueError(f"Binding site selection method: {self.selection_method}")

            else:
                raise ValueError(
                    f"Binding site detection method unknown: {self.definition_method}"
                )

    class LigandSimilaritySearch:
        """
        Subclass containing input specifications for 
        the ligand similarity search process of the pipeline,
        initialized automatically by the parent class.
        """

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
        """
        Subclass containing input specifications for 
        the docking process of the pipeline,
        initialized automatically by the parent class.
        """

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
        """
        Subclass containing input specifications for 
        the interaction analysis process of the pipeline,
        initialized automatically by the parent class.
        """

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
        """
        Subclass containing input specifications for 
        the selection of the output ligand,
        initialized automatically by the parent class.
        """

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

            else:
                raise ValueError(
                    f"Optimized ligand selection method unknown: {self.selection_method}"
                )

    class OutputPaths:
        """
        Subclass containing all the output paths for different parts of the pipeline,
        initialized automatically by the parent class.
        Take a main output path, and create all required parent folders,
        as well as sub-folders for each part of the pipeline,
        and store their paths.
        """

        def __init__(self, output_path):
            self.root = Path(output_path)
            for folder_name in Consts.Output.FolderNames:
                folder_path = io.create_folder(folder_name.value, output_path)
                setattr(self, folder_name.name.lower(), folder_path)
