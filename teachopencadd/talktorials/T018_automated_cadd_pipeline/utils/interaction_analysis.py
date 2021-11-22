"""
Contains interaction analysis class.
"""

from pathlib import Path

import pandas as pd  # for creating dataframes and handling data
import matplotlib.pyplot as plt  # for plotting of data
import matplotlib as mpl  # for changing the display settings of plots (see Settings below)

from .consts import Consts
from .helpers import plip, nglview

# Settings:
mpl.rcParams["figure.dpi"] = 300  # for plots with higher resolution
mpl.rcParams["agg.path.chunksize"] = 10000  # for handling plots with large number of data points


class InteractionAnalysis:
    """
    Automated protein-ligand interaction analysis process of the pipeline.

    Attributes
    ----------
    TODO
    results
    master_df
    _analogs
    _pdb_filepath_extracted_protein
    """

    def __init__(
        self,
        separated_protein_pdbqt_filepath,
        separated_protein_pdb_filepath,
        protein_first_residue_number,
        list_ligand_obj,
        docking_master_df,
        interaction_analysis_specs_obj,
        interaction_analysis_output_path,
    ):
        """
        Initialize the interaction analysis.

        Parameters
        ----------
        separated_protein_pdbqt_filepath : str or pathlib.Path
            Filepath of the separated protein PDBQT file used in docking.
        separated_protein_pdb_filepath : str or pathlib.Path
            Filepath of the separated protein PDB file.
        protein_first_residue_number : int
            First residue number in the protein.
        list_ligand_obj : list of utils.Ligand
            List of ligands to analyze their interactions with the protein.
        docking_master_df : pandas.DataFrame
            Summary dataframe created by the docking class.
        interaction_analysis_specs_obj : utils.Specs.InteractionAnalysis
            Specifications for the interaction analysis processes.
        interaction_analysis_output_path : str or pathlib.Path
            Output folder path to store the analyzed data in.
        """

        separated_protein_pdbqt_filepath = Path(separated_protein_pdbqt_filepath)
        separated_protein_pdb_filepath = Path(separated_protein_pdb_filepath)
        interaction_analysis_output_path = Path(interaction_analysis_output_path)

        self._analogs = list_ligand_obj
        self._pdb_filepath_extracted_protein = separated_protein_pdb_filepath

        if interaction_analysis_specs_obj.program is Consts.InteractionAnalysis.Programs.PLIP:
            results_df = docking_master_df.copy()
            results_df.drop("filepath", axis=1, inplace=True)
            results_df["total_num_interactions"] = 0

            interaction_master_df = docking_master_df.copy()

            for analog in list_ligand_obj:
                analog.dataframe.loc["average_num_total_interactions", "Value"] = 0
                for interaction_type in plip.Consts.InteractionTypes:
                    analog.dataframe.loc[
                        f"average_num_{interaction_type.name.lower()}", "Value"
                    ] = 0

                for index, docking_pose_filepath in zip(
                    range(len(analog.docking_poses_split_filepaths)),
                    analog.docking_poses_split_filepaths,
                ):
                    analog.protein_complex_filepath = plip.create_protein_ligand_complex(
                        separated_protein_pdbqt_filepath,
                        docking_pose_filepath,
                        analog.cid,
                        interaction_analysis_output_path / f"CID_{analog.cid}_{index + 1}",
                    )

                    # interaction_data will be dict of dicts, where each of the
                    # outer dict's items correspond to a ligand found in the pdb file
                    interaction_data = plip.calculate_interactions(analog.protein_complex_filepath)

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
                    ligand_interaction_data = plip.correct_protein_residue_numbers(
                        ligand_interaction_data,
                        protein_first_residue_number)

                    interaction_master_df.loc[(analog.cid, index + 1), "plip_dict"] = [
                        interaction_data[list(interaction_data.keys())[0]]
                    ]

                    for interaction_type in plip.Consts.InteractionTypes:
                        df = plip.create_dataframe_of_ligand_interactions(
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
                analog.dataframe.loc["average_num_total_interactions", "Value"] = round(
                    analog.dataframe.loc["average_num_total_interactions", "Value"]
                    / len(analog.docking_poses_split_filepaths),
                    1,
                )
                analog.num_total_interactions_mean = analog.dataframe.loc[
                    "average_num_total_interactions", "Value"
                ]
                for interaction_type in plip.Consts.InteractionTypes:
                    analog.dataframe.loc[
                        f"average_num_{interaction_type.name.lower()}", "Value"
                    ] = round(
                        analog.dataframe.loc[
                            f"average_num_{interaction_type.name.lower()}", "Value"
                        ]
                        / len(analog.docking_poses_split_filepaths),
                        1,
                    )

            results_df["total_num_interactions"] = pd.to_numeric(
                results_df["total_num_interactions"], downcast="integer"
            )
            self.results = results_df
            self.master_df = interaction_master_df

        else:
            raise AttributeError(
                f"Interaction analysis tool unknown: {interaction_analysis_specs_obj.program}"
            )

    def find_poses_with_specific_interactions(self, list_interaction_data, all_or_any):
        """
        Find docking poses containing a specific set of interactions.

        Parameters
        ----------
        list_interaction_data : list of lists
            List of desired interactions. Each sub-list should have the following format:
            [interaction_type, residue_number]
            Example: [["h_bond", 793], ["hydrophobic", 860]]
            interaction_type : str
                Type of desired interaction. Allowed values are:
                'h_bond', 'hydrophobic', 'salt_bridge', 'water_bridge',
                'pi_stacking', 'pi_cation', 'halogen', 'metal'
            residue_nr : int
                Residue number involved in the given interaction_type
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
        Visualize docking poses of all analogs, using NGLView.
        The docking poses are sorted by their binding affinities in a menu.

        Returns
        -------
        nglview.widget.NGLWidget
            NGLView viewer for all interactions.
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
        nglview.widget.NGLWidget
            NGLView viewer for analog interactions.
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
        nglview.widget.NGLWidget
            NGLView viewer for docking poses interactions.
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
        fitted_master_df : pandas.DataFrame
            Any section of the master InteractionAnalysis dataframe,
            stored under self.master_df.

        Returns
        -------
        nglview.widget.NGLWidget
            NGLView viewer.
        """
        list_docking_poses_labels = list(
            map(lambda x: f"{x[0]} - {x[1]}", fitted_master_df.index.tolist())
        )

        view = nglview.interactions(
            self._pdb_filepath_extracted_protein,
            fitted_master_df["filepath"].tolist(),
            list_docking_poses_labels,
            fitted_master_df["affinity[kcal/mol]"].tolist(),
            fitted_master_df["plip_dict"].tolist(),
        )
        return view

    def plot_interaction_affinity_correlation(self):
        """
        View a correlation plot between binding affinity and number of interactions
        in each docking pose.
        """
        df = self.results.sort_values(by="affinity[kcal/mol]", ascending=True)

        _, ax1 = plt.subplots()
        color = "tab:red"
        ax1.set_xlabel(
            "Docking pose count (sorted by binding affinity)", color="black", fontsize=9
        )
        ax1.set_ylabel(
            "Estimated binding affinity (absolute value) [kcal/mol]", color=color, fontsize=9
        )
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
        ax2.set_ylabel("Number of Interactions", color=color, fontsize=9)
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
