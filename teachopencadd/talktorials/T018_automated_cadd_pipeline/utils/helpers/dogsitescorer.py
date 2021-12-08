"""
Class containing all the required functions and constants
to communicate with the DoGSiteScorer's Rest-API.
This can be used to submit binding site detection jobs,
either by providing the PDB code of a protein structure,
or by uploading its PDB file.
It returns a table of all detected pockets and sub-pockets
and their corresponding descriptors.
For each detected (sub-)pocket, a PDB file is provided
and a CCP4 map file is generated.
These can be downloaded and used to define the coordinates of
the (sub-)pocket needed for the docking calculation and visualization.
The function `select_best_pocket` is also defined which provides
several methods for selecting the most suitable binding site.
"""

import io  # for creating file-like objects from strings (needed as input for some functions)
import gzip  # for decompressing .gz files downloaded from DoGSiteScorer
import time  # for creating pauses during runtime (e.g. to wait for the response of API requests)
from pathlib import Path # for handling local paths
import re # for filtering floats from a list of strings

import requests  # for communicating with web-service APIs
import pandas as pd  # for creating dataframes and handling data
from biopandas.pdb import PandasPdb  # for working with PDB files
import redo # for retrying API queries if they fail

from . import pdb


class APIConsts:
    """
    Constants for DoGSiteScorer's API.

    Notes
    -----
    API specifications described here:
    - https://proteins.plus/help/
    - https://proteins.plus/help/dogsite_rest
    """

    class FileUpload:
        URL = "https://proteins.plus/api/pdb_files_rest"
        REQUEST_MSG = "pdb_file[pathvar]"
        RESPONSE_MSG = {
            "status": "status_code",
            "status_codes": {"accepted": "accepted", "denied": "bad_request"},
            "message": "message",
            "url_of_id": "location",
        }
        RESPONSE_MSG_FETCH_ID = {"message": "message", "id": "id"}

    class SubmitJob:
        URL = "https://proteins.plus/api/dogsite_rest"
        QUERY_HEADERS = {
            "Content-type": "application/json",
            "Accept": "application/json",
        }

        RESPONSE_MSG = {"url_of_job": "location"}

        RESPONSE_MSG_FETCH_BINDING_SITES = {
            "result_table": "result_table",
            "pockets_pdb_files": "residues",
            "pockets_ccp4_files": "pockets",
        }

@redo.retriable(attempts=30, sleeptime=1, sleepscale=1.1, max_sleeptime=20)
def _send_request_get_results(
    request_type, 
    keys_list, 
    url, 
    task="Fetching results from DoGSiteScorer API", 
    **kwargs
):
    '''
    Send a request and get the keyword values from json response.
    
    Parameters
    ----------
    request_type : str
        Type of request, i.e. name of a function from the `requests` module,
        e.g. "get", "post".
    keys_list : list of strings
        List of keys in the json response to return.
    url : str
        URL to send the request to.
    task : str
        Textual description of the request's purpose to print in the error message if one is raised.
        Optional; default : "Fetching results from DoGSiteScorer API"
    **kwargs
        Additional arguments to send with the request.
    
    Returns
    -------
    list
        List of values in the json response corresponding to the input list of keys. 
    '''
    
    request_function = getattr(requests, request_type)
    response = request_function(url, **kwargs)
    response.raise_for_status()
    response_values = response.json()
    results=[]
    for key in keys_list:
        try:
            results.append(response_values[key])
        except KeyError:
            raise ValueError(
                f"{task} failed.\n"
                +f"Expected key {key} not found in the response.\n"
                +f"The response message is as follows: {response_values}"
            )
    return results
    
def upload_pdb_file(filepath):
    """
    Upload a PDB file to the DoGSiteScorer webserver using their API
    and get back a dummy PDB code, which can be used to submit a detection job.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Relative or absolute path of the PDB file.

    Returns
    -------
    str
        Dummy PDB code of the uploaded structure, which can be used instead of a PDB code.
    """

    # Open the local PDB file for reading in binary mode
    with open(Path(filepath).with_suffix(".pdb"), "rb") as f:
        # Post API query and get the response
        url_of_id = _send_request_get_results(
            "post",
            [APIConsts.FileUpload.RESPONSE_MSG["url_of_id"]],
            APIConsts.FileUpload.URL, 
            files={APIConsts.FileUpload.REQUEST_MSG: f}
        )[0]
    
    protein_id = _send_request_get_results(
        "get",
        [APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"]],
        url_of_id
    )[0]
    return protein_id

def submit_job(pdb_id, ligand_id="", chain_id=""):
    """
    Submit a protein structure to DoGSiteScorer webserver using their API
    and get back all the information on the detected binding sites.

    Parameters
    ----------
    pdb_id : str
        Either a valid 4-letter PDB code (e.g. '3w32'),
        or a dummy PDB code of an uploaded PDB file.
    ligand_id : str
        DogSiteScorer-name of the co-crystallized ligand of interest, e.g. 'W32_A_1101'.
        DogSiteScorer's naming convention is:
        <PDB ligand-ID>_<chain-ID>_<PDB residue number of the ligand>
    chain_id : str (optional; default: none)
        Chain ID to limit the binding site detection to.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing all the information on all detected binding sites.
    """
    
    url_of_job = _send_request_get_results(
        "post",
        [APIConsts.SubmitJob.RESPONSE_MSG["url_of_job"]],
        APIConsts.SubmitJob.URL, 
        json={
            "dogsite": {
                "pdbCode": pdb_id,  # PDB code of protein
                "analysisDetail": "1",  # 1 = include subpockets in results
                "bindingSitePredictionGranularity": "1",  # 1 = include drugablity scores
                "ligand": ligand_id,  # if name is specified, ligand coverage is calculated
                "chain": chain_id,  # if specified, calculation is only performed on this chain
            }
        },
        headers=APIConsts.SubmitJob.QUERY_HEADERS
    )[0]

    (binding_site_data_url, 
     binding_sites_pdb_files_urls, 
     binding_sites_ccp4_files_urls) = _send_request_get_results(
        "get",
        [APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["result_table"],
         APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["pockets_pdb_files"],
         APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["pockets_ccp4_files"]
        ],
        url_of_job)
    
    response = requests.get(binding_site_data_url)
    response.raise_for_status()
    binding_site_data_file = io.StringIO(response.text)
    binding_site_df = pd.read_csv(binding_site_data_file, sep="\t").set_index("name")
    binding_site_df["pdb_file_url"] = binding_sites_pdb_files_urls
    binding_site_df["ccp4_file_url"] = binding_sites_ccp4_files_urls
    return binding_site_df


def save_binding_sites_to_file(binding_site_df, output_path):
    """
    Download and save the PDB and CCP4 files corresponding to the calculated binding sites.

    Parameters
    ----------
    binding_site_df : pandas.DataFrame
        Binding site data retrieved from the DoGSiteScorer webserver.
    output_path : str or pathlib.Path
        Local folder path to save the files in.
    """

    for binding_site in binding_site_df.index:
        for column in ["pdb_file_url", "ccp4_file_url"]:
            response = requests.get(binding_site_df.loc[binding_site, column])
            response.raise_for_status()
            if column == "pdb_file_url":
                response_file_content = response.content
                file_extension = ".pdb"
            else:
                response_file_content = gzip.decompress(response.content)
                file_extension = ".ccp4"

            file_name = binding_site + file_extension
            with open(Path(output_path) / file_name, "wb") as f:
                f.write(response_file_content)
    return


def select_best_pocket(binding_site_df, selection_method, selection_criteria, ascending=False):
    """
    Select the best binding site from the table of all detected binding sites,
    either by sorting the binding sites based on a set of properties in the table,
    or by applying a function on the property values.

    Parameters
    ----------
    binding_site_df : pandas.DataFrame
        Binding site data retrieved from the DoGSiteScorer webserver.
    selection_method : str
        Selection method for selecting the best binding site.
        Either 'sorting' or 'function'.
    selection_criteria : str or list
        If 'selection_method' is 'sorting':
            List of one or more property names.
        If 'selection_method' is 'function':
            Any valid python syntax that generates a list-like object
            with the same length as the number of detected binding sites.
    ascending : bool
        Optional; default: False.
        If set to True, the binding site with the lowest value will be selected,
        otherwise, the binding site with the highest value is selected.

    Returns
    -------
    str
        Name of the selected binding site.
    """
    df = binding_site_df

    if selection_method == "sorting":
        sorted_df = df.sort_values(by=selection_criteria, ascending=ascending)
    elif selection_method == "function":
        df["function_score"] = eval(selection_criteria)
        sorted_df = df.sort_values(by="function_score", ascending=ascending)
    else:
        raise ValueError(f"Binding site selection method unknown: {selection_method}")

    selected_pocket_name = sorted_df.iloc[0].name
    return selected_pocket_name


def calculate_pocket_coordinates_from_pocket_pdb_file(filepath):
    """
    Calculate the coordinates of a binding site using the binding site's PDB file
    downloaded from DoGSiteScorer.

    Parameters
    ----------
    filepath : str or pathlib.Path
        Local filepath of the binding site's PDB file.

    Returns
    -------
    dict of list of int
        Binding site coordinates in format:
        `{'center': [x, y, z], 'size': [x, y, z]}`
    """
    with open(Path(filepath).with_suffix(".pdb")) as f:
        pdb_file_text_content = f.read()
    pdb_file_df = pdb.load_pdb_file_as_dataframe(pdb_file_text_content)
    pocket_coordinates_data = pdb_file_df["OTHERS"].loc[5, "entry"]
    coordinates_data_as_list = pocket_coordinates_data.split()
    # select strings representing floats from a list of strings
    coordinates = [float(element) for element in coordinates_data_as_list if re.compile(r'\d+(?:\.\d*)').match(element)]
    pocket_coordinates = {
        "center": coordinates[:3],
        "size": [coordinates[-1] * 2 for dim in range(3)],
    }
    return pocket_coordinates


def get_pocket_residues(pocket_pdb_filepath):
    """
    Get residue-IDs and names of a specified pocket.

    Parameters
    ----------
    pocket_pdb_filepath : str or pathlib.Path
        Path of pocket's PDB file.

    Returns
    -------
    pandas.DataFrame
        Table of residues names and IDs for the selected binding site.
    """
    
    with open(Path(pocket_pdb_filepath).with_suffix(".pdb")) as f:
        pdb_content = f.read()
    atom_info = pdb.load_pdb_file_as_dataframe(pdb_content)["ATOM"]
    # Drop duplicates, since the PDB file contains one entry per atom,
    # but we only need one entry per residue
    atom_info.sort_values("residue_number", inplace=True)
    atom_info.drop_duplicates(subset="residue_number", keep="first", inplace=True)
    atom_info.reset_index(drop=True, inplace=True)
    atom_info.index += 1
    return atom_info[["residue_number", "residue_name"]]
