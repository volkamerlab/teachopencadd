"""
Implementation of the functionalities of PubChem PUG REST API.
It can obtain new information on ligands such as other identifiers (e.g. IUPAC name, SMILES),
physiochemical properties and, descriptions etc.
Ths class has also the ability to perform similarity searches on a given ligand.
"""

from urllib.parse import quote  # for url quoting
import time  # for creating pauses during the runtime (to wait for the response of API requests)
from enum import Enum  # for creating enumeration classes

import requests  # for communicating with web-service APIs
import redo


class APIConsts:
    """
    Contains constants for PubChem API requests.

    Notes
    -----
    Request URLs should have the format:
        APIConsts.URLs.PROLOG + APIConsts.URLs.Inputs.<type>.value + ...
        ... <input_value> + APIConsts.URLs.Operations.GET_<property>.value + ...
        ... APIConsts.URLs.Outputs.<type>.value + <?optional parameters>
    """

    class URLs:
        PROLOG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/"

        class Inputs(Enum):
            CID = "compound/cid/"
            NAME = "compound/name/"
            SMILES = "compound/smiles/"
            INCHI = "compound/inchi/"
            INCHIKEY = "compound/inchikey/"
            SIMILARITY_FROM_SMILES = "compound/similarity/smiles/"
            SIMILARITY_RESULTS = "compound/listkey/"

        class Operations(Enum):
            GET_CID = "/cids/"
            GET_NAME = "/property/title/"
            GET_SMILES = "/property/CanonicalSMILES/"
            GET_INCHI = "/property/InChI/"
            GET_INCHIKEY = "/property/InChIKey/"
            GET_IUPAC_NAME = "/property/IUPACName/"
            GET_DESCRIPTION = "/description/"
            GET_RECORD = "/record/"

        class Outputs(Enum):
            TXT = "TXT"
            JSON = "JSON"
            PNG = "PNG"
            CSV = "CSV"
            SDF = "SDF"
            XML = "XML"

    class ResponseMsgs:
        class SimilaritySearch(Enum):
            JOBKEY_KEY1 = "Waiting"
            JOBKEY_KEY2 = "ListKey"
            RESULT_KEY1 = "PropertyTable"
            RESULT_KEY2 = "Properties"

        class GetRecords(Enum):
            RESPONSE_KEY = "PC_Compounds"

        class GetDescription(Enum):
            RESPONSE_KEY1 = "InformationList"
            RESPONSE_KEY2 = "Information"
            TITLE_KEY = "Title"
            CID_KEY = "CID"
            DESCRIPTION_KEY = "Description"
            DESCRIPTION_SOURCE_NAME_KEY = "DescriptionSourceName"
            DESCRIPTION_SOURCE_URL = "DescriptionURL"
            

@redo.retriable(attempts=20, sleeptime=30)
def send_request(partial_url, response_type="txt", optional_params=""):
    """
    Send an API request to PubChem and get the response data.

    Parameters
    ----------
    partial_url : str
        The URL part of the request consisting of input-type, input-value and operation.
        E.g. 'compound/cid/2244/property/CanonicalSMILES/' requests the SMILES of
        the compound with an CID of 2244.
    response_type : str
        Optional; default: txt.
        Expected response-type of the API request.
        Valid values are 'txt', 'json', 'png', 'csv' and 'sdf'.
        Valid values are stored in: APIConsts.URLs.Outputs
    optional_params : str
        The URL part of the request consisting of optional parameters.

    Returns
    -------
    Datatype depends on the value of input parameter 'response_type'.
        The response data of the API request.
    """
    full_url = (
        APIConsts.URLs.PROLOG
        + partial_url
        + getattr(APIConsts.URLs.Outputs, response_type.upper()).value
        + f"?{optional_params}"
    )
    response = requests.get(full_url)
    response.raise_for_status()
    if response_type == "txt":
        response_data = response.text
    elif response_type == "json":
        response_data = response.json()
    else:
        response_data = response.content
    return response_data


def convert_compound_identifier(
    input_id_type, input_id_value, output_id_type, output_data_type="txt"
):
    """
    Convert an identifier to another identifier, e.g. CID to SMILES, SMILES to IUPAC-name etc.

    Parameters
    ----------
    input_id_type : str
        Type of the input identifier.
        Valid values are: 'name', 'cid', 'smiles', 'inchi' and 'inchikey'.
        Valid values are stored in: `APIConsts.URLs.Inputs`
    input_id_value : str or int or list of str or list of int
        Value of the input identifier.
        For CIDs, multiple values can be entered as a list.
    output_id_type : str
        Type of the output identifier.
        Valid values are: 'name', 'cid', 'smiles', 'inchi', 'inchikey', 'iupac_name'.
        Valid values are stored in: `APIConsts.URLs.Operations`
    output_data_type : str
        Optional; default: 'txt'.
        Datatype of the output data.
        Valid values are 'txt', 'json', 'csv'.
        A list of all valid values are stored in: `APIConsts.URLs.Outputs`

    Returns
    -------
    Datatype depends on the value of input parameter 'response_type'
        The response data of the API request.
    """

    if isinstance(input_id_value, list):
        if input_id_type == "cid":
            input_id_value = ",".join(map(str, input_id_value))
        else:
            raise ValueError("Only CIDs can be entered as a list.")
    else:
        escaped_input_id_value = quote(str(input_id_value)).replace("/", ".")

    url = (
        getattr(APIConsts.URLs.Inputs, input_id_type.upper()).value
        + str(escaped_input_id_value)
        + getattr(APIConsts.URLs.Operations, f"GET_{output_id_type}".upper()).value
    )
    response_data = send_request(url, output_data_type)

    if isinstance(input_id_value, list):
        response_data = response_data.strip().split("\n")
    else:
        response_data = response_data.strip()
    return response_data


def get_compound_record(input_id_type, input_id_value, output_data_type="json"):
    """
    Get a full record of all physiochemical properties of the compound.

    Parameters
    ----------
    input_id_type : str
        Type of the input identifier.
        Valid values are: 'name', 'cid', 'smiles', 'inchi' and 'inchikey'.
        Valid values are stored in: `APIConsts.URLs.Inputs`
    input_id_value : str or int
        Value of the input identifier.
    output_data_type : str
        Optional; default: 'json'.
        Datatype of the output data.
        Valid values are 'txt', 'json', 'csv'.
        A list of all valid values are stored in: `APIConsts.URLs.Outputs`

    Returns
    -------
    dict
        Dictionary keys are: 'id', 'atoms', 'bonds', 'coords', 'charge', 'props', 'count'
    """
    
    escaped_input_id_value = quote(input_id_value).replace("/", ".")
    url = (
        getattr(APIConsts.URLs.Inputs, input_id_type.upper()).value
        + str(escaped_input_id_value)
        + getattr(APIConsts.URLs.Operations, "GET_RECORD").value
    )
    response_data = send_request(url, output_data_type)[
        APIConsts.ResponseMsgs.GetRecords.RESPONSE_KEY.value
    ][0]

    return response_data


def get_description_from_smiles(smiles, output_data_type="json", printout=False):
    """
    Get a textual description of a molecule, including its usage, properties, source etc.

    Parameters
    ----------
    smiles : str
        SMILES of the molecule.
    output_data_type : str
        Optional; default: 'txt'.
        Datatype of the output data.
        Valid values are 'txt', 'json', 'csv'.
        A list of all valid values are stored in: `APIConsts.URLs.Outputs`
    printout : bool
        Whether to print the descriptions, or return the data.

    Returns
    -------
    list of dict
        When the parameter printout is set to False, the raw data is
        returned as a list of dicts, where each element of the list
        corresponds to a description from a specific source (e.g. a journal article).
    """
    
    escaped_smiles = quote(smiles).replace("/", ".")
    url = (
        APIConsts.URLs.Inputs.SMILES.value
        + escaped_smiles
        + APIConsts.URLs.Operations.GET_DESCRIPTION.value
    )
    response_data = send_request(url, output_data_type)[
        APIConsts.ResponseMsgs.GetDescription.RESPONSE_KEY1.value
    ][APIConsts.ResponseMsgs.GetDescription.RESPONSE_KEY2.value]

    if printout:
        print(
            f"Name: {response_data[0][APIConsts.ResponseMsgs.GetDescription.TITLE_KEY.value]}\n"
            f"CID: {response_data[0][APIConsts.ResponseMsgs.GetDescription.CID_KEY.value]}\n"
        )
        if len(response_data) == 1:
            print("No description available.")
        else:
            for entry in response_data[1:]:
                print(
                    f"{entry[APIConsts.ResponseMsgs.GetDescription.DESCRIPTION_KEY.value]}\n"
                    f"Source: {entry[APIConsts.ResponseMsgs.GetDescription.DESCRIPTION_SOURCE_NAME_KEY.value]}, {entry[APIConsts.ResponseMsgs.GetDescription.DESCRIPTION_SOURCE_URL.value]}\n\n"
                )
    else:
        return response_data


def similarity_search(
    smiles,
    min_similarity=80,
    max_num_results=100,
    output_data_type="json",
    max_num_attempts=30,
):
    """
    Run a similarity search on a molecule and get all the similar ligands.

    Parameters
    ----------
    smiles : str
        The canonical SMILES string for the given compound.
    min_similarity : int
        Optional; default: 80.
        The threshold of similarity in percent.
    max_num_results : int
        Optional; default: 100.
        The maximum number of feedback records.
    output_data_type : str
        Optional; default: 'json'.
        Datatype of the output data.
        Valid values are 'txt', 'json', 'csv'.
        A list of all valid values are stored in: APIConsts.URLs.Outputs
    max_num_attempts : int
        Optional; default: 30.
        Maximum number of attempts to fetch the API response, after the job has been submitted.
        Each failed attempt is followed by a 10 second pause.

    Returns
    -------
    Datatype depends on the 'output_data_type' parameter
        E.g. when set to "json", returns a list of dicts
        Each dictionary in the list corresponds to a similar compound,
        which has a 'CID' and a 'CanonicalSMILES' key.
    """
    escaped_smiles = quote(smiles).replace("/", ".")
    url = APIConsts.URLs.Inputs.SIMILARITY_FROM_SMILES.value + escaped_smiles + "/"
    response_data = send_request(
        url,
        output_data_type,
        f"Threshold={min_similarity}&MaxRecords={max_num_results}",
    )
    job_key = response_data[APIConsts.ResponseMsgs.SimilaritySearch.JOBKEY_KEY1.value][
        APIConsts.ResponseMsgs.SimilaritySearch.JOBKEY_KEY2.value
    ]

    url = (
        APIConsts.URLs.Inputs.SIMILARITY_RESULTS.value
        + job_key
        + APIConsts.URLs.Operations.GET_SMILES.value
    )

    # Wait until the request has been processed
    # While the request is still running, `response_data` looks like this:
    # `{'Waiting': {'ListKey': '3270344311506161039', 'Message': 'Your request is running'}}`
    num_attempts = 0
    while num_attempts < max_num_attempts:
        response_data = send_request(url, output_data_type)
        if APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY1.value in response_data:
            similar_compounds = response_data[
                APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY1.value
            ][APIConsts.ResponseMsgs.SimilaritySearch.RESULT_KEY2.value]
            break
        time.sleep(30)
        num_attempts += 1
    else:
        raise ValueError(f"Could not find matches in the response URL: {url}")

    return similar_compounds
