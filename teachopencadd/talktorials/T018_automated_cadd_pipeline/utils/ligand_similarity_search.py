"""
Contains the ligand similarity search class.
"""

from pathlib import Path

from typing_extensions import ParamSpecKwargs
import pandas as pd  # for creating dataframes and handling data

from .consts import Consts
from .ligand import Ligand
from .helpers import pubchem, rdkit


class LigandSimilaritySearch:
    """
    Automated ligand similarity-search process of the pipeline.
    Take in input Ligand object, Specs.LigandSimilaritySearch object,
    and the corresponding output path, and automatically run all the necessary
    processes to output a set of analogs with the highest drug-likeness scores.

    Attributes
    ----------
    TODO
    all_analogs
    """

    def __init__(
        self,
        ligand_obj,
        similarity_search_specs_obj,
        similarity_search_output_path,
        frozen_data_filepath=None,
    ):
        """
        Initialize the ligand similarity search.

        Parameters
        ----------
        ligand_obj : utils.Ligand
            The Ligand object of the project.
        similarity_search_specs_obj : utils.Specs.LigandSimilaritySearch
            The similarity search specification data-class of the project.
        similarity_search_output_path : str or pathlib.Path
            Output path of the project's similarity search information.
        frozen_data_filepath : str or pathlib.Path
            If existing data is to be used, provide the path to a csv file
            containing the columns "CID" and "CanonicalSMILES" for the analogs.
        """

        similarity_search_output_path = Path(similarity_search_output_path)

        if not frozen_data_filepath is None:
            all_analog_identifiers_df = pd.read_csv(frozen_data_filepath)
        elif (
            similarity_search_specs_obj.search_engine
            is Consts.LigandSimilaritySearch.SearchEngines.PUBCHEM
        ):
            analogs_info = pubchem.similarity_search(
                ligand_obj.smiles,
                similarity_search_specs_obj.min_similarity_percent,
                similarity_search_specs_obj.max_num_results,
            )
            all_analog_identifiers_df = pd.DataFrame(analogs_info)
        else:
            raise ValueError(f"Search engine unknown: {similarity_search_specs_obj.search_engine}")

        # create dataframe from initial results
        all_analog_identifiers_df["Mol"] = all_analog_identifiers_df["CanonicalSMILES"].apply(
            lambda smiles: rdkit.create_molecule_object("smiles", smiles)
        )
        all_analog_identifiers_df["dice_similarity"] = all_analog_identifiers_df["Mol"].apply(
            lambda mol: rdkit.calculate_similarity_dice(ligand_obj.rdkit_obj, mol)
        )
        all_analog_properties_df = pd.DataFrame(
            (
                all_analog_identifiers_df["Mol"].apply(
                    lambda mol: rdkit.calculate_druglikeness(mol)
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
            .head(similarity_search_specs_obj.max_num_druglike)
            .index
        ):
            new_analog_object = Ligand(
                Consts.Ligand.InputTypes.CID,
                analog_cid,
                similarity_search_output_path,
            )

            new_analog_object.dice_similarity = rdkit.calculate_similarity_dice(
                ligand_obj.rdkit_obj, new_analog_object.rdkit_obj
            )

            new_analog_object.dataframe.loc["similarity"] = new_analog_object.dice_similarity

            analogs_dict[new_analog_object.cid] = new_analog_object

        ligand_obj.analogs = analogs_dict
