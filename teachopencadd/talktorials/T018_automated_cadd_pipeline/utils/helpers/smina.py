"""
Set of functions for communicating with the Smina docking program,
and extracting data from its log file.
"""

import subprocess  # for creating shell processes (needed to communicate with Smina program)

import pandas as pd  # for creating dataframes and handling data


def dock(
    ligand_path,
    protein_path,
    pocket_center,
    pocket_size,
    output_path,
    output_format="pdbqt",
    num_poses=10,
    exhaustiveness=10,
    random_seed=None,
    log=True,
):
    """
    Perform docking with Smina.

    Parameters
    ----------
    ligand_path : str or pathlib.Path
        Path to ligand PDBQT file that should be docked.
    protein_path : str or pathlib.Path
        Path to protein PDBQT file that should be docked to.
    pocket_center : iterable of float or int
        Coordinates defining the center of the binding site.
    pocket_size : iterable of float or int
        Lengths of edges defining the binding site.
    output_path : str or pathlib.Path
        Path to which docking poses should be saved, SDF or PDB format.
    output_format : str
        Output format (default: pdbqt).
    num_poses : int or str
        Maximum number of poses to generate.
    exhaustiveness : int or str
        Accuracy of docking calculations.
    random_seed : int or str
        Seed number to make the docking deterministic for reproducibility.
    log : bool
        Optional; default: True.
        Whether to also write a log-file in the same output path for each docking.

    Returns
    -------
    output_text : str
        The output log of the docking calculation.
    """
    smina_command = (
        [
            "smina",
            "--ligand",
            str(ligand_path),
            "--receptor",
            str(protein_path),
            "--out",
            str(output_path) + "." + output_format,
            "--center_x",
            str(pocket_center[0]),
            "--center_y",
            str(pocket_center[1]),
            "--center_z",
            str(pocket_center[2]),
            "--size_x",
            str(pocket_size[0]),
            "--size_y",
            str(pocket_size[1]),
            "--size_z",
            str(pocket_size[2]),
            "--num_modes",
            str(num_poses),
            "--exhaustiveness",
            str(exhaustiveness),
        ]
        + (["--log", str(output_path) + "_log.txt"] if log else [])
        + (["--seed", str(random_seed)] if random_seed is not None else [])
    )

    output_text = subprocess.check_output(
        smina_command,
        universal_newlines=True,
    )
    return output_text


def convert_log_to_dataframe(raw_log):
    """
    Convert docking's raw output log into a pandas.DataFrame.

    Parameters
    ----------
    raw_log : str
        Raw output log generated after docking.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing columns 'mode', 'affinity[kcal/mol]',
        'dist from best mode_rmsd_l.b', and 'dist from best mode_rmsd_u.b'
        for each generated docking pose.
    """

    # Remove the unnecessary parts and extract the results table as list of lines
    # The table starts after the line containing: -----+------------+----------+----------
    # and ends before the word "Refine"
    log = (
        raw_log.split("-----+------------+----------+----------")[1]
        .split("Refine")[0]
        .strip()
        .split("\n")
    )

    # parse each line and remove everything except the numbers
    for index in range(len(log)):
        # turn each line into a list
        log[index] = log[index].strip().split(" ")
        # First element is the mode, which is an int.
        # The rest of the elements are either empty strings, or floats
        # Elements that are not empty strings should be extracted
        # (first element as int and the rest as floats)
        log[index] = [int(log[index][0])] + [
            float(value) for value in log[index][1:] if value != ""
        ]

    df = pd.DataFrame(
        log,
        columns=[
            "mode",
            "affinity[kcal/mol]",
            "dist from best mode_rmsd_l.b",
            "dist from best mode_rmsd_u.b",
        ],
    )
    df.index = df["mode"]
    df.drop("mode", axis=1, inplace=True)
    return df
