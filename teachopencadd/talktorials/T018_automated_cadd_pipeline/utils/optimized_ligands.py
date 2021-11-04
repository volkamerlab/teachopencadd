# 3rd-party packages:
from IPython.display import display, Markdown  # ror more display options in the Jupyter Notebook
import pandas as pd  # for creating dataframes and handling data

# Modules in the util folder:
from .consts import Consts


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
            # TODO should this be project.Specs.OptimizedLigands.selection_criteria?
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
