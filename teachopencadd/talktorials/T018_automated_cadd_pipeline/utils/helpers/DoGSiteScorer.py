"""
Class Containing all the required functions and constants
to communicate with the DoGSiteScorer's Rest-API.
This can be used to submit binding-site detection jobs, 
either by providing the PDB-code of protein structure, 
or by uploading its PDB file. 
It returns a table of all detected pockets and sub-pockets
and their corresponding descriptors. 
For each detected (sub-)pocket, a PDB file is provided 
and a CCP4 map file is generated. 
These can be downloaded and used to define the coordinates of 
the (sub-)pocket needed for the docking calculation and visualization. 
The function ***select_best_pocket*** is also defined which provides 
several methods for selecting the most suitable binding-site.
"""

# Standard library:
import io  # for creating file-like objects from strings of data (needed as input for some functions)
import gzip  # for decompressing .gz files downloaded from DoGSiteScorer

# 3rd-party packages:
import requests  # for communicating with web-service APIs
import pandas as pd  # for creating dataframes and handling data


class APIConsts:
    # See https://proteins.plus/help/
    # and https://proteins.plus/help/dogsite_rest
    # for API specifications.

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


def upload_pdb_file(filepath):
    """
    Upload a PDB file to DoGSiteScorer webserver using their API
    and get back a dummy PDB-code, which can be used to submit a detection job.

    Parameters
    ----------
    filepath : str
        Relative or absolute path of the PDB file.

    Returns
    -------
        str
        Dummy PDB-code of the uploaded structure,
        which can then be used instead of a real PDB-code.
    """
    url = APIConsts.FileUpload.URL  # Read API URL from Constants
    request_msg = APIConsts.FileUpload.REQUEST_MSG  # Read API request message from Constants
    with open(filepath, "rb") as f:  # Open the local PDB file for reading in binary mode
        response = requests.post(
            url, files={request_msg: f}
        )  # Post API query and get the response
    response.raise_for_status()  # Raise HTTPError if one occured during query
    if response.ok:
        response_values = response.json()  # Turn the response values into a dict
        # If the request is accepted, the response will contain a URL,
        # from which the needed ID of the uploaded protein can be obtained.
        # Here, we store this URL from the response values in the url_of_id variable.
        url_of_id = response_values[APIConsts.FileUpload.RESPONSE_MSG["url_of_id"]]
    else:
        raise ValueError(
            "Uploading PDB file failed.\n"
            + f"The response values are as follows: {response_values}"
        )
    # After getting the URL, it may take some time for the server to process the uploaded file
    # and return an ID. Thus, we try 30 times in intervals of 5 seconds to query the URL,
    # until we get the ID
    for try_nr in range(30):
        id_response = requests.get(url_of_id)  # Query the URL containing the ID
        id_response_values = id_response.json()  # Turn the response values into a dict
        # The response should contain the ID keyword:
        if id_response.ok & (
            APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"] in id_response_values
        ):
            id_response_values = id_response.json()
            protein_id = id_response_values[APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"]]
            break
        else:
            time.sleep(5)
    if not (
        id_response.ok & (APIConsts.FileUpload.RESPONSE_MSG_FETCH_ID["id"] in id_response_values)
    ):
        raise ValueError(
            "Fetching the ID of uploaded protein failed.\n"
            + f"The response values are as follows: {id_response_values}"
        )
    return protein_id


def submit_job(pdb_id, ligand_id="", chain_id="", num_attempts=30):
    """
    Submit a protein structure to DoGSiteScorer webserver using their API
    and get back all the information on the detected binding-sites.

    Parameters
    ----------
    pdb_id : str
        Either a valid 4-letter PDB-code (e.g. '3w32'),
        or a dummy PDB-code of an uploaded PDB file.
    ligand_id : str
        DogSiteScorer-name of the co-crystallized ligand of interest, e.g. 'W32_A_1101'.
        DogSiteScorer naming convention is: <PDB ligand-ID>_<chain-ID>_<PDB residue number of the ligand>
    chain_id : str (optional; default: none)
        Chain-ID to limit the binding-site detection to.
    num_attempts : int (optional; default: 30)
        Number of times to attempt to fetch the results after the job has been submitted.
        After each failed attempt there is a 10-second pause.

    Returns
    -------
        Pandas DataFrame
        Dataframe containing all the information on all detected binding-sites.
    """
    response = requests.post(
        APIConsts.SubmitJob.URL,
        json={
            "dogsite": {
                "pdbCode": pdb_id,  # PDB code of protein
                "analysisDetail": "1",  # 1 = include subpockets in results
                "bindingSitePredictionGranularity": "1",  # 1 = include drugablity scores
                "ligand": ligand_id,  # if name is specified, ligand coverage is calculated
                "chain": chain_id,  # if chain is specified, calculation is only performed on this chain
            }
        },
        headers=APIConsts.SubmitJob.QUERY_HEADERS,
    )
    response.raise_for_status()
    response_values = response.json()
    url_of_job = response_values[APIConsts.SubmitJob.RESPONSE_MSG["url_of_job"]]

    attempt_count = 0
    while attempt_count <= num_attempts:
        job_response = requests.get(url_of_job)
        job_response.raise_for_status()
        job_response_values = job_response.json()

        if (
            APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["result_table"]
            in job_response_values
        ):
            binding_site_data_url = job_response_values[
                APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["result_table"]
            ]
            binding_sites_pdb_files_urls = job_response_values[
                APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["pockets_pdb_files"]
            ]
            binding_sites_ccp4_files_urls = job_response_values[
                APIConsts.SubmitJob.RESPONSE_MSG_FETCH_BINDING_SITES["pockets_ccp4_files"]
            ]
            break
        attempt_count += 1
        time.sleep(10)
    else:
        raise ValueError(
            "Fetching the binding-site data failed.\n"
            + f"The response values are as follows: {job_response_values}"
        )

    binding_site_data_table = requests.get(binding_site_data_url).text
    binding_site_data_file = io.StringIO(binding_site_data_table)
    binding_site_df = pd.read_csv(binding_site_data_file, sep="\t").set_index("name")
    binding_site_df["pdb_file_url"] = binding_sites_pdb_files_urls
    binding_site_df["ccp4_file_url"] = binding_sites_ccp4_files_urls
    return binding_site_df


def save_binding_sites_to_file(binding_site_df, output_path):
    """
    download and save the PDB and CCP4 files corresponding to the calculated binding-sites.

    Parameters
    ----------
    binding_site_df : Pandas DataFrame
        Binding-site data retrieved from the DoGSiteScorer webserver.
    output_path : str or pathlib.Path object
        Local file path to save the files in.

    Returns
    -------
        None
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
            with open(output_path / file_name, "wb") as f:
                f.write(response_file_content)
    return


def select_best_pocket(binding_site_df, selection_method, selection_criteria, ascending=False):
    """
    Select the best binding-site from the table of all detected binding-sites,
    either by sorting the binding-sites based on a set of properties in the table,
    or by applying a function on the property values.

    Parameters
    ----------
    binding_site_df : Pandas DataFrame
        Binding-site data retrieved from the DoGSiteScorer webserver.
    selection_method : str
        Selection method for selecting the best binding-site.
        Either 'sorting' or 'function'.
    selection_criteria : str or list
        When 'selection_method' is 'sorting':
            List of one or several property names.
        When 'selection_method' is 'function':
            Any valid python syntax that generates a list-like object
            with the same length as the number of detected binding-sites.
    ascending : bool (optional; default: False)
        If set to True, the binding-site with the lowest value will be selected,
        otherwise, the binding-site with the highest value is selected.

    Returns
    -------
        str
        Name of the selected binding-site.
    """
    df = binding_site_df
    if selection_method == "sorting":
        sorted_df = df.sort_values(by=selection_criteria, ascending=ascending)
    elif selection_method == "function":
        df["function_score"] = eval(selection_criteria)
        sorted_df = df.sort_values(by="function_score", ascending=ascending)

    selected_pocket_name = sorted_df.iloc[0].name
    return selected_pocket_name


def calculate_pocket_coordinates_from_pocket_pdb_file(filepath):
    """
    Calculate the coordinates of a binding-site using the binding-site's PDB file
    downloaded from DoGSiteScorer.

    Parameters
    ----------
    filepath : str or pathlib.Path object
        Local filepath (including filename, without extension) of the binding-site's PDB file.

    Returns
    -------
        dict of lists of integers
        Binding-site coordinates in format:
        {'center': [x, y, z], 'size': [x, y, z]}
    """
    with open(str(filepath) + ".pdb") as f:
        pdb_file_text_content = f.read()
    pdb_file_df = PDB.load_pdb_file_as_dataframe(pdb_file_text_content)
    pocket_coordinates_data = pdb_file_df["OTHERS"].loc[5, "entry"]
    coordinates_data_as_list = pocket_coordinates_data.split(" ")
    coordinates = []
    for elem in coordinates_data_as_list:
        try:
            coordinates.append(float(elem))
        except:
            pass
    pocket_coordinates = {
        "center": coordinates[:3],
        "size": [coordinates[-1] * 2 for dim in range(3)],
    }
    return pocket_coordinates


def get_pocket_residues(pocket_residues_url):
    """
    Gets residue IDs and names of a specified pocket (via URL).

    Parameters
    ----------
    pocket_residues_url : str
        URL of selected pocket file on the DoGSiteScorer web server.

    Returns
    -------
        pandas.DataFrame
        Table of residues names and IDs for the selected binding site.
    """
    # Retrieve PDB file content from URL
    result = requests.get(pocket_residues_url)
    # Get content of PDB file
    pdb_residues = result.text
    # Load PDB format as DataFrame
    ppdb = PandasPdb()
    # TODO: Change _construct_df to read_pdb_from_lines once biopandas
    # cuts a new release (currently: 0.2.7), see https://github.com/rasbt/biopandas/pull/72
    pdb_df = ppdb._construct_df(pdb_residues.splitlines(True))["ATOM"]
    # Drop duplicates
    # PDB file contains per atom entries, we only need per residue info
    pdb_df.sort_values("residue_number", inplace=True)
    pdb_df.drop_duplicates(subset="residue_number", keep="first", inplace=True)
    return pdb_df[["residue_number", "residue_name"]]
