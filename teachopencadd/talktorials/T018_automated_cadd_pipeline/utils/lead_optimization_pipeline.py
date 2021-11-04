# 3rd-party packages:
from IPython.display import display, Markdown  # for more display options in the Jupyter Notebook


from .specs import Specs
from .protein import Protein
from .ligand import Ligand
from .binding_site_detection import BindingSiteDetection
from .ligand_similarity_search import LigandSimilaritySearch
from .docking import Docking
from .interaction_analysis import InteractionAnalysis
from .optimized_ligands import OptimizedLigands


class LeadOptimizationPipeline:
    def __init__(self, project_name):
        self.name = project_name

    @classmethod
    def run(cls, project_name, input_data_filepath, output_data_root_folder_path):
        """
        Automatically run the whole lead optimization pipeline to completion,
        and print out a summary in real-time.

        Parameters
        ----------
        project_name : str
            Name of the lead optimization project.
        input_data_filepath : str or pathlib.Path object
            Filepath of the input CSV file containing all the specifications of the project.
        output_data_root_folder_path : str or pathlib.Path object
            Root folder path to save the pipeline's data in.

        Returns
        -------
            LeadOptimizationPipeline object
            Object containing all the information about the pipeline.
        """

        def pprint(markdown_list):
            markdown_command = ""
            for command in markdown_list:
                text, color = command
                markdown_command += f"<span style='color:{color}'>{text}</span>"
            display(Markdown(markdown_command))

        def pprint_header(header):
            display(
                Markdown(
                    f"<span style='color:blue'>**{header}:** </span><span style='color:green'>Successful</span>"
                )
            )

        project = cls(project_name=project_name)
        pprint_header("1. Initializing Project")
        pprint([(f"&nbsp;&nbsp;&nbsp;&nbsp;Project name: **{project.name}**", "black")])

        project.Specs = Specs(
            input_data_filepath=input_data_filepath,
            output_data_root_folder_path=f"{output_data_root_folder_path}/{project.name}",
        )
        pprint_header("2. Initializing Input/Output")
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Input data read from: **{input_data_filepath}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Output folders created at: **{output_data_root_folder_path}/{project.name}**",
                    "black",
                )
            ]
        )

        project.Protein = Protein(
            identifier_type=project.Specs.Protein.input_type,
            identifier_value=project.Specs.Protein.input_value,
            protein_output_path=project.Specs.OutputPaths.protein,
        )
        pprint_header("3. Processing Protein Data")
        display(project.Protein())

        project.Ligand = Ligand(
            identifier_type=project.Specs.Ligand.input_type,
            identifier_value=project.Specs.Ligand.input_value,
            ligand_output_path=project.Specs.OutputPaths.ligand,
        )
        pprint_header("4. Processing Ligand Data")
        display(project.Ligand())

        """
        project.BindingSiteDetection = BindingSiteDetection(
            project.Protein,
            project.Specs.BindingSite,
            project.Specs.OutputPaths.binding_site_detection,
        )
        pprint_header("5. Binding Site Detection")
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Binding site definition method: **{project.Specs.BindingSite.definition_method.name}**",
                    "black",
                )
            ]
        )
        if (
            project.Specs.BindingSite.definition_method
            is Consts.BindingSite.DefinitionMethods.DETECTION
        ):
            pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;Binding site detection method: **{project.Specs.BindingSite.detection_method.name}**",
                        "black",
                    )
                ]
            )
            pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;Selection method for best binding site: **{project.Specs.BindingSite.selection_method.name}**",
                        "black",
                    )
                ]
            )
            pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;Selection criteria for best binding site: **{project.Specs.BindingSite.selection_criteria}**",
                        "black",
                    )
                ]
            )
            pprint(
                [
                    (
                        f"&nbsp;&nbsp;&nbsp;&nbsp;Name of selected binding site: **{project.BindingSiteDetection.best_binding_site_name}**",
                        "black",
                    )
                ]
            )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Binding site coordinates - center: **{project.Protein.binding_site_coordinates['center']}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Binding site coordinates - size: **{project.Protein.binding_site_coordinates['size']}**",
                    "black",
                )
            ]
        )

        # display(project.BindingSiteDetection.visualize_best())
        """
        # TODO once ProteinsPlus is back
        # Remove line below and remove comment block above
        project.Protein.binding_site_coordinates = {
            "center": [16.55, 23.34, 1.31],
            "size": [26.14, 26.14, 26.14],
        }

        project.LigandSimilaritySearch = LigandSimilaritySearch(
            project.Ligand,
            project.Specs.LigandSimilaritySearch,
            project.Specs.OutputPaths.similarity_search,
        )
        pprint_header("6. Ligand Similarity Search")
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Search engine: **{project.Specs.LigandSimilaritySearch.search_engine.name}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Number of fetched analogs with a similarity higher than **{project.Specs.LigandSimilaritySearch.min_similarity_percent}%**: **{len(project.LigandSimilaritySearch.all_analogs)}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Dice-similarity range of fetched analogs: **{project.LigandSimilaritySearch.all_analogs['dice_similarity'].min()} - {project.LigandSimilaritySearch.all_analogs['dice_similarity'].max()}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;CID of analog with the highest Dice-similarity: **{project.LigandSimilaritySearch.all_analogs.sort_values(by='dice_similarity', ascending=False).head(1).index.values[0]}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Number of selected drug-like analogs: **{len(project.Ligand.analogs)}**",
                    "black",
                )
            ]
        )
        sorted_analogs_df = project.LigandSimilaritySearch.all_analogs.sort_values(
            by="drug_score_total", ascending=False
        ).head(len(project.Ligand.analogs))
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Range of drug-likeness score in selected analogs: **{sorted_analogs_df['drug_score_total'].min()} - {sorted_analogs_df['drug_score_total'].max()}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;CID of analog with the highest drug-likeness score: **{sorted_analogs_df.head(1).index.values[0]}**",
                    "black",
                )
            ]
        )

        project.Docking = Docking(
            project.Protein,
            list(project.Ligand.analogs.values()),
            project.Specs.Docking,
            project.Specs.OutputPaths.docking,
        )
        project.Ligand.Docking = Docking(
            project.Protein,
            [project.Ligand],
            project.Specs.Docking,
            project.Specs.OutputPaths.ligand,
        )
        pprint_header("7. Docking Experiment")
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Highest binding affinity of input ligand: **{project.Ligand.binding_affinity_best}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Binding affinity range of analogs: **{project.Docking.results_dataframe['affinity[kcal/mol]'].max()} - {project.Docking.results_dataframe['affinity[kcal/mol]'].min()}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Number of analog docking poses with higher affinity than ligand: **{len(project.Docking.results_dataframe[project.Docking.results_dataframe['affinity[kcal/mol]']<project.Ligand.binding_affinity_best].sort_values(by=['affinity[kcal/mol]']))}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Number of analogs with higher affinity than ligand: **{len(set(project.Docking.results_dataframe[project.Docking.results_dataframe['affinity[kcal/mol]']<project.Ligand.binding_affinity_best].sort_values(by=['affinity[kcal/mol]']).index.get_level_values(0)))}**",
                    "black",
                )
            ]
        )

        highest_aff_cids = set(
            project.Docking.results_dataframe[
                project.Docking.results_dataframe["affinity[kcal/mol]"]
                < project.Ligand.binding_affinity_best
            ]
            .sort_values(by=["affinity[kcal/mol]"])
            .index.get_level_values(0)
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;CIDs of analogs with higher affinity than ligand: **{highest_aff_cids}**",
                    "black",
                )
            ]
        )

        project.Docking.visualize_all_poses()

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
        pprint_header("8. Protein-Ligand Interaction Analysis")
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Highest number of total interactions in a docking pose of input ligand: **{project.Ligand.InteractionAnalysis.results.sort_values(by='total_num_interactions',ascending=False).head(1)['total_num_interactions'].values[0]}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Range of total number of interactions in docking poses of analogs: **{project.InteractionAnalysis.results['total_num_interactions'].min()} - {project.InteractionAnalysis.results['total_num_interactions'].max()}**",
                    "black",
                )
            ]
        )
        pprint(
            [
                (
                    f"&nbsp;&nbsp;&nbsp;&nbsp;Correlation plot between binding affinity and number of interactions in docking poses of analogs:",
                    "black",
                )
            ]
        )
        project.InteractionAnalysis.plot_interaction_affinity_correlation()

        display(project.InteractionAnalysis.visualize_all_interactions())

        pprint_header("9. Selecting The Optimized Analog")
        project.OptimizedLigands = OptimizedLigands(project)
        project.OptimizedLigands()
        print("\n")
        pprint([("**Selected analogs as final output:**", "blue")])
        project.OptimizedLigands.show_final_output()

        cid_pose_nr_list = []
        for final_analog in project.OptimizedLigands.output:
            for docking_pose_nr in range(1, len(final_analog.dataframe_docking) + 1):
                cid_pose_nr_list.append((final_analog.cid, docking_pose_nr))
        display(project.InteractionAnalysis.visualize_docking_poses_interactions(cid_pose_nr_list))

        pprint_header("10. Pipeline Completed")

        return project
