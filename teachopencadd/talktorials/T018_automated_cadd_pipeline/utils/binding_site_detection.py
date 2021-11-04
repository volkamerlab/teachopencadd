# Standard library:
from enum import Enum  # for creating enumeration classes

# Modules in the util folder:
from .helpers import dogsitescorer, pdb, nglview


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
        ligand_object = pdb.extract_molecule_from_pdb_file(
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
            self.dogsitescorer_pdb_id = dogsitescorer.upload_pdb_file(Protein.pdb_filepath)

        # try to get the chain_id for binding-site detection if it's available in input data
        if BindingSiteSpecs.protein_chain_id != "":
            if hasattr(Protein, "chains") and BindingSiteSpecs.protein_chain_id in Protein.chains:
                self.dogsitescorer_chain_id = BindingSiteSpecs.protein_chain_id
            else:
                raise ValueError(
                    f"The input protein chain-ID ({BindingSiteSpecs.protein_chain_id}) "
                    f"does not exist in the input protein. Existing chains are: {Protein.chains}"
                )
        else:
            # if chain_id is not in input data, try to set it to the first chain found in PDB file
            try:
                self.dogsitescorer_chain_id = Protein.chains[0]
            # if no chain is found in PDB file either, leave the chain_id empty
            except:
                self.dogsitescorer_chain_id = ""

        # create a list of ligand ids in the DoGSiteScorer format
        list_dogsitescorer_ligand_ids = []
        list_ligands_heavy_atom_count = []
        for ligand in Protein.ligands:
            list_ligands_heavy_atom_count.append(ligand[-1])
            if len(ligand) == 3:
                list_dogsitescorer_ligand_ids.append(
                    ligand[0] + "_" + ligand[1][0] + "_" + ligand[1][1:]
                )
            else:
                list_dogsitescorer_ligand_ids.append(ligand[0] + "_" + ligand[1] + "_" + ligand[2])

        # try to get the ligand_id for detection calculation if it's available in input data
        if BindingSiteSpecs.protein_ligand_id != "":
            ligand_id = BindingSiteSpecs.protein_ligand_id
            # check if the given ligand_id is already given in the DoGSiteScorer format
            if "_" in ligand_id:
                if ligand_id in list_dogsitescorer_ligand_ids:
                    self.dogsitescorer_ligand_id = ligand_id
                    self.dogsitescorer_chain_id = ligand_id.split("_")[1][0]
                else:
                    raise ValueError(
                        f"The input ligand-ID ({BindingSiteSpecs.protein_ligand_id}) "
                        f"does not exist in the input protein. Existing ligand-IDs are: "
                        f"{[ligand[0] for ligand in Protein.ligands]}"
                    )
            else:
                self.dogsitescorer_ligand_id = None
                for ligand in list_dogsitescorer_ligand_ids:
                    if ligand.split("_")[0] == ligand_id and (
                        ligand.split("_")[1][0] == self.dogsitescorer_chain_id
                    ):
                        self.dogsitescorer_ligand_id = ligand
                        break
                if self.dogsitescorer_ligand_id == None:
                    raise ValueError(
                        f"The input ligand-ID ({BindingSiteSpecs.protein_ligand_id}) "
                        f"does not exist in the input protein. Existing ligand-IDs are: "
                        f"{[ligand[0] for ligand in Protein.ligands]}"
                    )

        else:
            index_of_heaviest_ligand = list_ligands_heavy_atom_count.index(
                max(list_ligands_heavy_atom_count)
            )
            self.dogsitescorer_ligand_id = list_dogsitescorer_ligand_ids[index_of_heaviest_ligand]

        self.dogsitescorer_binding_sites_df = dogsitescorer.submit_job(
            self.dogsitescorer_pdb_id,
            self.dogsitescorer_ligand_id,
            self.dogsitescorer_chain_id,
        )
        dogsitescorer.save_binding_sites_to_file(
            self.dogsitescorer_binding_sites_df, binding_site_output_path
        )

        self.best_binding_site_name = dogsitescorer.select_best_pocket(
            self.dogsitescorer_binding_sites_df,
            BindingSiteSpecs.selection_method.value,
            BindingSiteSpecs.selection_criteria,
        )

        self.best_binding_site_data = self.dogsitescorer_binding_sites_df.loc[
            self.best_binding_site_name
        ]

        self.best_binding_site_coordinates = (
            dogsitescorer.calculate_pocket_coordinates_from_pocket_pdb_file(
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
            viewer = nglview.binding_site(
                "pdb_code",
                self.Protein.pdb_code,
                str(self.output_path / pocket_name) + ".ccp4",
            )
        else:
            viewer = nglview.protein(
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
