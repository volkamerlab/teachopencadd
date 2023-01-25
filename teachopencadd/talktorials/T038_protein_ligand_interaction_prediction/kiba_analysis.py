import os.path
import urllib.request
from typing import Callable

import pandas as pd
import numpy as np
import biotite.database.rcsb as rcsb
import pypdb
from tqdm import tqdm
from chembl_webresource_client.new_client import new_client


def filter_data(kiba_init_filepath, kiba_filter_filepath):
    df = pd.read_csv(kiba_init_filepath, sep="\t")
    print("KiBA originally contains {} ligands and {} proteins.".format(*df.shape))

    row_vals = np.array([row.isna().sum() for index, row in df.iterrows()])

    df = df.drop(df[row_vals > 200].index)
    print("KiBA after dropping sparse rows contains {} ligands and {} proteins.".format(*df.shape))

    col_vals2 = np.array([df[column].isna().sum() for column in df.columns])

    df = df.loc[:, col_vals2 < 10]
    print("KiBA finally contains {} ligands and {} proteins.".format(*df.shape))

    df.to_csv(kiba_filter_filepath, sep="\t", index=None)


def download_ligands(kiba_filepath, ligand_filepath):
    print("Preprocessing ligands")
    df = pd.read_csv(kiba_filepath, sep="\t")
    mol_finder = new_client.molecule
    not_found = []
    with open(ligand_filepath, "w") as ligands:
        print("ChEMBL_ID", "SMILES", sep="\t", file=ligands)
        for _, row in df.iterrows():
            try:
                print(
                    row[0],
                    pd.DataFrame.from_records(
                        mol_finder.filter(chembl_id=row[0]).only(["molecule_structures"])
                    ).iloc[0, 0]["canonical_smiles"],
                    sep="\t",
                    file=ligands,
                )
                not_found.append(False)
            except Exception as e:
                not_found.append(True)
    df = df.drop(df[not_found].index)
    print("After ligand availability analysis KiBA contains {} ligands and {} proteins.".format(*df.shape))
    df.to_csv(kiba_filepath, sep="\t", index=None)
    print("Preprocessing ligands finished")


def describe_one_pdb_id(pdb_id):
    """Fetch meta information from PDB."""
    described = pypdb.describe_pdb(pdb_id)
    if described is None:
        print(f"! Error while fetching {pdb_id}, retrying ...")
        raise ValueError(f"Could not fetch PDB id {pdb_id}")
    return described


def query_uniprot(
        uniprot_id: str = "O00444",
        before_deposition_date: str = "2020-01-01T00:00:00Z",
        experimental_method: str = "X-RAY DIFFRACTION",
        max_resolution: float = 3.0,
        n_chains: int = 1,
        min_ligand_molecular_weight: float = 100.0,
):
    try:
        query_by_uniprot_id = rcsb.FieldQuery(
            "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
            exact_match=uniprot_id,
        )
        query_by_deposition_date = rcsb.FieldQuery(
            "rcsb_accession_info.deposit_date", less=before_deposition_date
        )
        query_by_experimental_method = rcsb.FieldQuery("exptl.method", exact_match=experimental_method)
        # query_by_resolution = rcsb.FieldQuery(
        #     "rcsb_entry_info.resolution_combined", less_or_equal=max_resolution
        # )
        # query_by_polymer_count = rcsb.FieldQuery(
        #     "rcsb_entry_info.deposited_polymer_entity_instance_count", equals=n_chains
        # )
        # query_by_ligand_mw = rcsb.FieldQuery(
        #     "chem_comp.formula_weight", molecular_definition=True, greater=min_ligand_molecular_weight
        # )
        query = rcsb.CompositeQuery(
            [
                query_by_uniprot_id,
                query_by_deposition_date,
                query_by_experimental_method,
                # query_by_resolution,
                # query_by_polymer_count,
                # query_by_ligand_mw,
            ],
            "and",
        )
        pdb_ids = rcsb.search(query)
        pdbs_data = [(pdb_id, describe_one_pdb_id(pdb_id)) for pdb_id in pdb_ids]
        pdb = sorted(pdbs_data, key=lambda x: x[1]["rcsb_entry_info"]["resolution_combined"][0])[0][0]
        return uniprot_id, pdb
    except:
        return uniprot_id, ""


def download_proteins(kiba_filepath, structure_folder):
    print("Preprocessing proteins")
    df = pd.read_csv(kiba_filepath, sep="\t")
    if os.path.exists("data/tmp.txt"):
        results = []
        with open("data/tmp.txt", "r") as data:
            for line in data.readlines():
                parts = line.strip().split("\t")[:2]
                if len(parts) == 1:
                    results.append((parts[0], ""))
                else:
                    results.append((parts[0], parts[1]))
    else:
        results = [query_uniprot(uniprot_id) for uniprot_id in tqdm(list(df.columns)[1:])]
        with open("data/tmp.txt", "w") as output:
            for uniprot, pdb in results:
                print(uniprot, pdb, sep="\t", file=output)

    flags = [True]
    for uniprot_id, pdb_id in results:
        if pdb_id == "":
            flags.append(False)
            continue
        if os.path.exists(structure_folder + uniprot_id):
            flags.append(True)
            continue
        try:
            urllib.request.urlretrieve("https://files.rcsb.org/download/" + pdb_id + ".pdb", structure_folder + uniprot_id + ".pdb")
            print(f"\rDownload {pdb_id} -> {uniprot_id}", end="")
            flags.append(True)
        except:
            flags.append(False)

    df = df.loc[:, flags]
    print("\rAfter protein availability analysis KiBA contains {} ligands and {} proteins.".format(*df.shape))
    df.to_csv(kiba_filepath, sep="\t", index=None)
    print("Preprocessing proteins finished")


def process_interactions(kiba_filepath, inter_filepath, threshold_fn: Callable):
    print("Preprocessing interactions")
    inter_count = 0
    with open(kiba_filepath, "r") as data, open(inter_filepath, "w") as inter:
        print("UniProt_ID", "ChEMBL_ID", "Y", sep="\t", file=inter)
        uniprot_ids = []
        values = []
        for i, line in enumerate(data.readlines()):
            if i == 0:
                uniprot_ids = line.strip().split("\t")[1:]
            else:
                parts = line.strip().split("\t")
                ligand = parts[0]
                for val, p_id in zip(parts[1:], uniprot_ids):
                    if len(val) > 0:
                        inter_count += 1
                        values.append(float(val.replace(",", ".")))
                        print(p_id, ligand, threshold_fn(float(val.replace(",", "."))), sep="\t", file=inter)
    print(f"Finally, KiBA comprises {inter_count} interactions.")
    print("Preprocessing interactions finished")


def kiba_preprocessing(
        kiba_init_filepath: str = "data/kiba/KIBA.csv",
        database: str = "data/resources/"
):
    os.makedirs(os.path.join(database, "tables"), exist_ok=True)
    os.makedirs(os.path.join(database, "proteins"), exist_ok=True)

    filter_data(kiba_init_filepath, database + "tables/kiba.tsv")
    download_ligands(database + "tables/kiba.tsv", database + "tables/ligands.tsv")
    download_proteins(database + "tables/kiba.tsv", database + "proteins/")
    process_interactions(database + "tables/kiba.tsv", database + "tables/inter.tsv", lambda x: "1" if x < 3.6122 else "0")


def main():
    kiba_preprocessing()


if __name__ == '__main__':
    main()
