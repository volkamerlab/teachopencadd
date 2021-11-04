"""
Contains the ligand similarity search class.
"""

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
            analogs_info = pubchem.similarity_search(
                Ligand_obj.smiles,
                SimilaritySearchSpecs.min_similarity_percent,
                SimilaritySearchSpecs.max_num_results,
            )

        # create dataframe from initial results
        all_analog_identifiers_df = pd.DataFrame(analogs_info)
        all_analog_identifiers_df["Mol"] = all_analog_identifiers_df["CanonicalSMILES"].apply(
            lambda smiles: rdkit.create_molecule_object("smiles", smiles)
        )
        all_analog_identifiers_df["dice_similarity"] = all_analog_identifiers_df["Mol"].apply(
            lambda mol: rdkit.calculate_similarity_dice(Ligand_obj.rdkit_obj, mol)
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
            .head(SimilaritySearchSpecs.max_num_druglike)
            .index
        ):
            new_analog_object = Ligand(
                Consts.Ligand.InputTypes.CID,
                analog_cid,
                similarity_search_output_path,
            )

            new_analog_object.dice_similarity = rdkit.calculate_similarity_dice(
                Ligand_obj.rdkit_obj, new_analog_object.rdkit_obj
            )

            new_analog_object.dataframe.loc["similarity"] = new_analog_object.dice_similarity

            analogs_dict[new_analog_object.cid] = new_analog_object

        Ligand_obj.analogs = analogs_dict
