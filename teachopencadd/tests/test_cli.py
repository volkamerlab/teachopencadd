"""
Unit tests for Command Line Interface.
"""

from pathlib import Path
import shutil
import subprocess
import warnings

from teachopencadd.utils import (
    _greeting_string,
    _run_jlab_string,
    _talktorial_list_string,
)
from teachopencadd.cli import TALKTORIAL_FOLDER_NAME


def capture(command):
    """
    Run input command as subprocess and caputure the subprocess' exit code, stdout and stderr.

    Parameters
    ----------
    command : list of str
        Command to be run as subprocess.

    Returns
    -------
    out : str
        Standard output message.
    err : str
        Standard error message.
    exitcode : int
        Exit code.
    """

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_start_workspace():
    """
    Test `teachopencadd start` (exit code, stdout, and stderr) for existing user-defined workspace
    - Run #1: Talktorials do not exist, yet, and are therefore copied
    - Run #2: Talktorials do already exist, and are therefore NOT copied again
    - Check if number of copied files equals number of files in repository
    - At the end: Remove talktorial copy
    """

    command = "teachopencadd start ."

    # Start workspace #1
    out, err, exitcode = capture(command.split())
    # Check exit code, stdout, and stderr
    assert exitcode == 0
    assert out == (
        _greeting_string()
        + "\n"
        + _talktorial_list_string(TALKTORIAL_FOLDER_NAME)
        + "\n"
        + _run_jlab_string(TALKTORIAL_FOLDER_NAME)
        + "\n"
    )
    assert not err

    # Start workspace #2 (this time the talktorial folder already exists)
    out, err, exitcode = capture(command.split())
    # Check exit code, stdout, and stderr
    assert exitcode == 0
    assert out == (
        _greeting_string()
        + "\n"
        + f"Workspace exists already at location `{TALKTORIAL_FOLDER_NAME}`."
        + "\n"
        + _talktorial_list_string(TALKTORIAL_FOLDER_NAME)
        + "\n"
        + _run_jlab_string(TALKTORIAL_FOLDER_NAME)
        + "\n"
    )
    assert not err

    # Check if all files were transferred to workspace
    # Set path to template (repository) and test (copy) talktorial directories
    talktorials_path_template = Path(__name__).parent / "teachopencadd/talktorials"
    talktorials_path_test = Path(TALKTORIAL_FOLDER_NAME)
    # Fetch all files in directories
    files_list_template = sorted(talktorials_path_template.glob("**/*"))
    files_list_test = sorted(talktorials_path_test.glob("**/*"))
    # Remove checkpoint files that may be present
    files_list_template = [
        file
        for file in files_list_template
        if ("checkpoint" not in str(file)) and ("__pycache__" not in str(file))
    ]
    files_list_test = [
        file
        for file in files_list_test
        if ("checkpoint" not in str(file)) and ("__pycache__" not in str(file))
    ]
    # The same number of files?
    # assert files_list_test == files_list_template
    assert len(files_list_test) == len(files_list_template)

    # At the very end: Delete TeachOpenCADD talktorial folder
    shutil.rmtree(TALKTORIAL_FOLDER_NAME)


def test_start_incorrect_workspace():
    """
    Test `teachopencadd start` for non-existing user-defined workspace.
    """

    command = "teachopencadd start xxx"
    out, err, exitcode = capture(command.split())

    assert exitcode == 0
    assert out == _greeting_string() + "\n" + "Could not find user-defined location `xxx`.\n"
    assert not err


def test_jlab_import():
    """
    Add warning if JupyterLab cannot be imported.
    """

    try:
        import jupyterlab
    except ImportError:
        warnings.warn(
            "JupyterLab cannot be imported; install with `mamba install jupyterlab`.",
            ImportWarning,
        )


def test_incomplete_signature():
    """
    Test behavior when the user enters an incomplete CLI command.
    """

    command = "teachopencadd"
    out, err, exitcode = capture(command.split())

    assert exitcode == 0
    # Since the output will change whenever new subcommands are added to the CLI,
    # Check only the beginning and end of the message, which will stay the same.
    assert out.startswith("usage")
    assert out.endswith("show this help message and exit\n")
    assert not err
