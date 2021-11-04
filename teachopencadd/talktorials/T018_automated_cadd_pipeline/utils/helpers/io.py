"""
Contains all the necessary functions for handling the input and output data.
e.g. creating a dataframe from the input CSV file, extracting specific information
from the dataframe, or creating folders for storing the output data.
"""

# Standard library:
from pathlib import Path  # for creating folders and handling local paths

# 3rd-party packages:
import pandas as pd  # for creating dataframes and handling data


def create_dataframe_from_csv_input_file(
    input_data_filepath, list_of_index_column_names, list_of_columns_to_keep
):
    """
    Read a CSV file and create a pandas DataFrame with given specifications.

    Parameters
    ----------
    input_data_filepath : str or pathlib.Path object
        Path of the CSV data file.
    list_of_index_column_names : list of strings
        List of column names in the CSV file to be used as indices for the dataframe.
    list_of_columns_to_keep : list of strings
        List of column names from the CSV file to keep in the dataframe.

    Returns
    -------
        Pandas DataFrame
    """
    input_df = pd.read_csv(input_data_filepath)
    input_df.set_index(list_of_index_column_names, inplace=True)
    input_df.drop(input_df.columns.difference(list_of_columns_to_keep), axis=1, inplace=True)
    return input_df


def copy_series_from_dataframe(input_df, index_name, column_name):
    """
    Take a multi-index dataframe, and make a copy of the data
    corresponding to a given index and column.

    Parameters
    ----------
    input_df : Pandas DataFrame
        The dataframe to extract the data from.
    index_name : str
        The index-value of the needed rows.
    column_name : str
        The column-name of the needed values.
    Returns
    -------
        Pandas Series
        Copy of the data corresponding to given index- and column-name.
    """
    subject_data = input_df.xs(index_name, level=0, axis=0)[column_name].copy()
    return subject_data


def create_folder(folder_name, folder_path=""):
    """
    Create a folder with a given name in a given path.
    Also creates all non-existing parent folders.

    Parameters
    ----------
    folder_name : str
        Name of the folder to be created.

    folder_path : str (optional; default: current path)
        Either relative or absolute path of the folder to be created.

    Returns
    -------
        pathlib.Path object
        Full path of the created folder.
    """
    path = Path(folder_path) / folder_name
    # Creating the folder and all non-existing parent folders.
    path.mkdir(parents=True, exist_ok=True)
    return path
