"""
Contains docking class.
"""

from pathlib import Path

import pandas as pd  # for creating dataframes and handling data

from .helpers import obabel, smina, pdb, nglview


class Docking:
    """
    Automated docking process of the pipeline.
    Take in a Protein and a list of ligands, and
    dock each ligand on the protein, using the given specifications.

    Attributes
    ----------
    TODO
    """

    def __init__(
        self,
        protein_obj,
        list_ligand_obj,
        docking_specs_obj,
        docking_output_path,
        frozen_data_filepath=None,
    ):
        """
        Initialize docking.

        Parameters
        ----------
        protein_obj : utils.Protein
            The protein to perform docking on.
        list_ligand_obj : list of utils.Ligand
            List of ligands to dock on the protein.
        docking_specs_obj : utils.Specs.Docking
            Specifications for the docking experiment.
        docking_output_path : str or pathlib.Path
            Output folder path to store the docking data in.
        frozen_data_filepath : str or pathlib.Path
            If existing data is to be used, provide the path to a folder
            containing the pdbqt files for
            (a) the protein `<PDBcode>_extracted_protein_ready_for_docking.pdbqt` and
            (b) all previously defined ligands/analogs `CID_<CID>.pdbqt`.
        """

        docking_output_path = Path(docking_output_path)
        if frozen_data_filepath is not None:
            frozen_data_filepath = Path(frozen_data_filepath)

        self.pdb_filepath_extracted_protein = docking_output_path / (
            f"{protein_obj.pdb_code}_extracted_protein.pdb"
        )
        protein_obj.Universe = pdb.extract_molecule_from_pdb_file(
            "protein", protein_obj.pdb_filepath, self.pdb_filepath_extracted_protein
        )

        if frozen_data_filepath is not None:
            # Set path to frozen PDBQT files
            self.pdbqt_filepath_extracted_protein = frozen_data_filepath / (
                f"{protein_obj.pdb_code}_extracted_protein_ready_for_docking.pdbqt"
            )
        else:
            # Generate PDBQT files
            self.pdbqt_filepath_extracted_protein = docking_output_path / (
                f"{protein_obj.pdb_code}_extracted_protein_ready_for_docking.pdbqt"
            )
            obabel.create_pdbqt_from_pdb_file(
                self.pdb_filepath_extracted_protein, self.pdbqt_filepath_extracted_protein
            )

        temp_list_results_df = []
        temp_list_master_df = []

        for ligand in list_ligand_obj:

            if frozen_data_filepath is not None:
                # Set path to frozen PDBQT files
                ligand.pdbqt_filepath = frozen_data_filepath / (f"CID_{ligand.cid}.pdbqt")
            else:
                # Generate PDBQT files
                ligand.pdbqt_filepath = docking_output_path / (f"CID_{ligand.cid}.pdbqt")
                obabel.create_pdbqt_from_smiles(ligand.remove_counterion(), ligand.pdbqt_filepath)

            ligand.docking_poses_filepath = docking_output_path / (
                f"CID_{ligand.cid}_docking_poses.pdbqt"
            )

            raw_log = smina.dock(
                ligand.pdbqt_filepath,
                self.pdbqt_filepath_extracted_protein,
                protein_obj.binding_site_coordinates["center"],
                protein_obj.binding_site_coordinates["size"],
                str(ligand.docking_poses_filepath).split(".")[0],
                output_format="pdbqt",
                num_poses=docking_specs_obj.num_poses_per_ligand,
                exhaustiveness=docking_specs_obj.exhaustiveness,
                random_seed=docking_specs_obj.random_seed,
                log=True,
            )

            ligand.docking_poses_split_filepaths = obabel.split_multistructure_file(
                "pdbqt", ligand.docking_poses_filepath
            )

            # Assigning the the dataframe of the Smina output
            # to the ligand's attribute 'dataframe_docking'
            df = smina.convert_log_to_dataframe(raw_log)
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
        nglview.widget.NGLWidget
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
        nglview.widget.NGLWidget
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
        fitted_master_df : pandas.DataFrame
            Any section of the master docking dataframe,
            stored under self.master_df.

        Returns
        -------
        nglview.widget.NGLWidget
            Interactive viewer of given analog's docking poses,
            sorted by their binding affinities.
        """
        list_docking_poses_labels = list(
            map(lambda x: f"{x[0]} - {x[1]}", fitted_master_df.index.tolist())
        )
        nglview.docking(
            self.pdb_filepath_extracted_protein,
            fitted_master_df["filepath"].tolist(),
            list_docking_poses_labels,
            fitted_master_df["affinity[kcal/mol]"].tolist(),
        )
        return
