"""
Contains the full lead optimization pipeline.
"""

from pathlib import Path

from IPython.display import display, Markdown  # for more display options in the Jupyter Notebook

from .consts import Consts
from .specs import Specs
from .protein import Protein
from .ligand import Ligand
from .binding_site_detection import BindingSiteDetection
from .ligand_similarity_search import LigandSimilaritySearch
from .docking import Docking
from .interaction_analysis import InteractionAnalysis
from .optimized_ligands import OptimizedLigands


class LeadOptimizationPipeline:
    """
    Contains the full automated lead optimization pipeline.

    Attributes
    ----------
    TODO add static attributes to this class?
    name : str
        Project name
    """

    def __init__(self, project_name):
        self.name = project_name

    @classmethod
    def run(
        cls,
        project_name,
        input_data_filepath,
        output_data_root_folder_path,
        frozen_data_filepath={"pubchem_similarity_search": None, "docking_pdbqt_files": None},
    ):
        """
        Automatically run the whole lead optimization pipeline to completion,
        and print out a summary in real-time.

        Parameters
        ----------
        project_name : str
            Name of the lead optimization project.
        input_data_filepath : str or pathlib.Path
            Filepath of the input CSV file containing all the specifications of the project.
        output_data_root_folder_path : str or pathlib.Path
            Root folder path to save the pipeline's data in.
        frozen_data_filepath : dict of str or pathlib.Path
            "pubchem_similarity_search":
                If existing data is to be used, provide the path to a csv file
                containing the columns "CID" and "CanonicalSMILES" for the analogs.
            "docking_pdbqt_files":
                If existing data is to be used, provide the path to a folder
                containing the pdbqt files for
                (a) the protein `<PDBcode>_extracted_protein_ready_for_docking.pdbqt` and
                (b) all previously defined ligands/analogs `CID_<CID>.pdbqt`.

        Returns
        -------
        utils.LeadOptimizationPipeline
            Object containing all the information about the pipeline.
        """

        input_data_filepath = Path(input_data_filepath)
        output_data_root_folder_path = Path(output_data_root_folder_path)
        frozen_data_filepath = {
            key: Path(path) if path is not None else path
            for key, path in frozen_data_filepath.items()
        }

        # Initialize project
        project = cls(project_name=project_name)
        project._report_initialized_project("1. Initializing Project")

        # Initialize IO
        project.Specs = Specs(
            input_data_filepath=input_data_filepath,
            output_data_root_folder_path=f"{output_data_root_folder_path}/{project.name}",
        )
        project._report_initialized_io("2. Initializing Input/Output")

        # Process protein
        project.Protein = Protein(
            identifier_type=project.Specs.Protein.input_type,
            identifier_value=project.Specs.Protein.input_value,
            protein_output_path=project.Specs.OutputPaths.protein,
        )
        project._report_processed_protein("3. Processing Protein")

        # Process ligand
        project.Ligand = Ligand(
            identifier_type=project.Specs.Ligand.input_type,
            identifier_value=project.Specs.Ligand.input_value,
            ligand_output_path=project.Specs.OutputPaths.ligand,
        )
        project._report_processed_ligand("4. Processing Ligand")

        # Detect binding site
        project.BindingSiteDetection = BindingSiteDetection(
            project.Protein,
            project.Specs.BindingSite,
            project.Specs.OutputPaths.binding_site_detection,
        )
        project._report_detected_binding_site("5. Binding Site Detection")

        # Search similar ligands
        project.LigandSimilaritySearch = LigandSimilaritySearch(
            project.Ligand,
            project.Specs.LigandSimilaritySearch,
            project.Specs.OutputPaths.similarity_search,
            frozen_data_filepath["pubchem_similarity_search"],
        )
        project._report_similar_ligands("6. Ligand Similarity Search")

        # Dock ligands
        project.Docking = Docking(
            project.Protein,
            list(project.Ligand.analogs.values()),
            project.Specs.Docking,
            project.Specs.OutputPaths.docking,
            frozen_data_filepath["docking_pdbqt_files"],
        )
        project.Ligand.Docking = Docking(
            project.Protein,
            [project.Ligand],
            project.Specs.Docking,
            project.Specs.OutputPaths.ligand,
            frozen_data_filepath["docking_pdbqt_files"],
        )
        project._report_docked_poses("7. Docking Experiment")

        # Analyze interactions
        project.InteractionAnalysis = InteractionAnalysis(
            project.Docking.pdbqt_filepath_extracted_protein,
            project.Docking.pdb_filepath_extracted_protein,
            project.Protein.residue_number_first,
            list(project.Ligand.analogs.values()),
            project.Docking.master_df,
            project.Specs.InteractionAnalysis,
            project.Specs.OutputPaths.interaction_analysis,
        )
        project.Ligand.InteractionAnalysis = InteractionAnalysis(
            project.Docking.pdbqt_filepath_extracted_protein,
            project.Docking.pdb_filepath_extracted_protein,
            project.Protein.residue_number_first,
            [project.Ligand],
            project.Ligand.Docking.master_df,
            project.Specs.InteractionAnalysis,
            project.Specs.OutputPaths.ligand,
        )
        project._report_interactions("8. Protein-Ligand Interaction Analysis")

        # Select optimized ligands
        project.OptimizedLigands = OptimizedLigands(project)
        project._report_optimized_ligands("9. Selecting The Optimized Analog")

        # Report completed pipeline
        project._report_pipeline_status("10. Pipeline Completed")

        return project

    @staticmethod
    def _pprint(markdown_list):
        """
        Display multiple lines in a given color for each line.
        
        Parameters
        ----------
        markdown_list : list of lists/tuples
            List of texts and their respective colors to be displayed.
            Each tuple has two elements: the text, followed by its color.
        
        Returns
        -------
        None
            The texts are displayed in their given colors.
        """
        markdown_command = ""
        for command in markdown_list:
            text, color = command
            markdown_command += f"<span style='color:{color}'>{text}</span>"
        display(Markdown(markdown_command))

    @staticmethod
    def _pprint_header(header):
        """
        Display the report header of each part of the pipeline after its successful completion.
        
        Parameters
        ----------
        header : str
            Name of a process in the pipeline, e.g. "Binding site detection".
        
        Returns
        -------
        None
            The header will be displayed in blue color and bold,
            followed by "successful" in green.
            Example: Binding site detection: Successful
        """
        display(
            Markdown(
                f"<span style='color:blue'>**{header}:** "
                f"</span><span style='color:green'>Successful</span>"
            )
        )

    def _report_initialized_project(self, header):
        """
        Report the results the step where the project is initialized.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self._pprint([(f"&nbsp;&nbsp;&nbsp;&nbsp;Project name: **{self.name}**", "black")])

    def _report_initialized_io(self, header):
        """
        Report the results the step where the input/output is initialized.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Input data read from: "
                    f"**{self.Specs.RawData.filepath}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Output folders created at: "
                    f"**{self.Specs.OutputPaths.root}**",
                    "black",
                )
            ]
        )

    def _report_processed_protein(self, header):
        """
        Report the results the step where the input protein is processed.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        display(self.Protein())

    def _report_processed_ligand(self, header):
        """
        Report the results the step where the input ligand is processed.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        display(self.Ligand())

    def _report_detected_binding_site(self, header):
        """
        Report the results the step where the binding site is detected.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Binding site definition method: "
                    f"**{self.Specs.BindingSite.definition_method.name}**",
                    "black",
                )
            ]
        )
        if (
            self.Specs.BindingSite.definition_method
            is Consts.BindingSite.DefinitionMethods.DETECTION
        ):
            self._pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Binding site detection method: "
                        f"**{self.Specs.BindingSite.detection_method.name}**",
                        "black",
                    )
                ]
            )
            self._pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Selection method for best binding site: "
                        f"**{self.Specs.BindingSite.selection_method.name}**",
                        "black",
                    )
                ]
            )
            self._pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Selection criteria for best binding site: "
                        f"**{self.Specs.BindingSite.selection_criteria}**",
                        "black",
                    )
                ]
            )
            self._pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;"
                        f"Name of selected binding site: "
                        f"**{self.BindingSiteDetection.best_binding_site_name}**",
                        "black",
                    )
                ]
            )
        else:
            raise AttributeError(
                f"Binding site definition tool unknown: {self.Specs.BindingSite.definition_method}"
            )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Binding site coordinates - center: "
                    f"**{self.Protein.binding_site_coordinates['center']}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Binding site coordinates - size: "
                    f"**{self.Protein.binding_site_coordinates['size']}**",
                    "black",
                )
            ]
        )
        # display(self.BindingSiteDetection.visualize_best())

    def _report_similar_ligands(self, header):
        """
        Report the results the step where the similarity search is performed.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Search engine: "
                    f"**{self.Specs.LigandSimilaritySearch.search_engine.name}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Number of fetched analogs with a similarity higher than "
                    f"**{self.Specs.LigandSimilaritySearch.min_similarity_percent}%**: "
                    f"**{len(self.LigandSimilaritySearch.all_analogs)}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Dice-similarity range of fetched analogs: "
                    f"**{self.LigandSimilaritySearch.all_analogs['dice_similarity'].min()} - "
                    f"{self.LigandSimilaritySearch.all_analogs['dice_similarity'].max()}**",
                    "black",
                )
            ]
        )
        dice_similarity = (
            self.LigandSimilaritySearch.all_analogs.sort_values(
                by="dice_similarity", ascending=False
            )
            .head(1)
            .index.values[0]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"CID of analog with the highest Dice-similarity: "
                    f"**{dice_similarity}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Number of selected drug-like analogs: "
                    f"**{len(self.Ligand.analogs)}**",
                    "black",
                )
            ]
        )
        sorted_analogs_df = self.LigandSimilaritySearch.all_analogs.sort_values(
            by="drug_score_total", ascending=False
        ).head(len(self.Ligand.analogs))
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Range of drug-likeness score in selected analogs: "
                    f"**{sorted_analogs_df['drug_score_total'].min()} - "
                    f"{sorted_analogs_df['drug_score_total'].max()}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"CID of analog with the highest drug-likeness score: "
                    f"**{sorted_analogs_df.head(1).index.values[0]}**",
                    "black",
                )
            ]
        )

    def _report_docked_poses(self, header):
        """
        Report the results the step where the docking is performed.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Highest binding affinity of input ligand: "
                    f"**{self.Ligand.binding_affinity_best}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Binding affinity range of analogs: "
                    f"**{self.Docking.results_dataframe['affinity[kcal/mol]'].max()} - "
                    f"{self.Docking.results_dataframe['affinity[kcal/mol]'].min()}**",
                    "black",
                )
            ]
        )
        n_analog_poses = len(
            self.Docking.results_dataframe[
                self.Docking.results_dataframe["affinity[kcal/mol]"]
                < self.Ligand.binding_affinity_best
            ].sort_values(by=["affinity[kcal/mol]"])
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Number of analog docking poses with higher affinity than ligand: "
                    f"**{n_analog_poses}**",
                    "black",
                )
            ]
        )
        n_analogs = len(
            set(
                self.Docking.results_dataframe[
                    self.Docking.results_dataframe["affinity[kcal/mol]"]
                    < self.Ligand.binding_affinity_best
                ]
                .sort_values(by=["affinity[kcal/mol]"])
                .index.get_level_values(0)
            )
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Number of analogs with higher affinity than ligand: "
                    f"**{n_analogs}**",
                    "black",
                )
            ]
        )

        highest_aff_cids = set(
            self.Docking.results_dataframe[
                self.Docking.results_dataframe["affinity[kcal/mol]"]
                < self.Ligand.binding_affinity_best
            ]
            .sort_values(by=["affinity[kcal/mol]"])
            .index.get_level_values(0)
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"CIDs of analogs with higher affinity than ligand: "
                    f"**{highest_aff_cids}**",
                    "black",
                )
            ]
        )
        self.Docking.visualize_all_poses()

    def _report_interactions(self, header):
        """
        Report the results the step where the interactions are analyzed.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        n_interactions = (
            self.Ligand.InteractionAnalysis.results.sort_values(
                by="total_num_interactions", ascending=False
            )
            .head(1)["total_num_interactions"]
            .values[0]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Highest number of total interactions in a docking pose of input ligand: "
                    f"**{n_interactions}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;"
                    f"Range of total number of interactions in docking poses of analogs: "
                    f"**{self.InteractionAnalysis.results['total_num_interactions'].min()} - "
                    f"{self.InteractionAnalysis.results['total_num_interactions'].max()}**",
                    "black",
                )
            ]
        )
        self._pprint(
            [
                (
                    "&nbsp;&nbsp;&nbsp;&nbsp;"
                    "Correlation plot between binding affinity and number of interactions "
                    "in docking poses of analogs:",
                    "black",
                )
            ]
        )
        self.InteractionAnalysis.plot_interaction_affinity_correlation()

        display(self.InteractionAnalysis.visualize_all_interactions())

    def _report_optimized_ligands(self, header):
        """
        Report the results the step where the optimized ligands are selected.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
        self.OptimizedLigands()
        print("\n")
        self._pprint([("**Selected analogs as final output:**", "blue")])
        self.OptimizedLigands.show_final_output()

        cid_pose_nr_list = []
        for final_analog in self.OptimizedLigands.output:
            for docking_pose_nr in range(1, len(final_analog.dataframe_docking) + 1):
                cid_pose_nr_list.append((final_analog.cid, docking_pose_nr))
        display(self.InteractionAnalysis.visualize_docking_poses_interactions(cid_pose_nr_list))

    def _report_pipeline_status(self, header):
        """
        Report the pipeline status at the end.

        Parameters
        ----------
        header : str
            Report header.
        """
        self._pprint_header(header)
