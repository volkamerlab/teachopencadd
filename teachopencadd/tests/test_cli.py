"""
Unit tests for Command Line Interface.
"""

from pathlib import Path
import subprocess

from teachopencadd.utils import (
    _greeting_string,
    _run_jlab_string,
    _talktorial_list_string,
)
from teachopencadd.cli import TALKTORIAL_FOLDER_NAME


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_start_workspace():
    """
    Test `teachopencadd start` (exit code, stdout, and stderr) for existing user-defined workspace
    - Run #1: Talktorials do not exist, yet, and are therefore copied
    - Run #2: Talktorials do already exist, and are therefor NOT copied again
    - Check if number of copied files equals number of files in repository
    - At the end: Remove talktorial copy
    """

    command = "teachopencadd start ."

    # Start workspace #1
    out, err, exitcode = capture(command.split())
    # Check exit code, stdout, and stderr
    assert exitcode == 0
    assert (
        out
        == (
            _greeting_string()
            + "\n"
            + _talktorial_list_string(TALKTORIAL_FOLDER_NAME)
            + "\n"
            + _run_jlab_string(TALKTORIAL_FOLDER_NAME)
            + "\n"
        ).encode()
    )
    assert err == b""

    # Start workspace #2 (this time the talktorial folder already exists)
    out, err, exitcode = capture(command.split())
    # Check exit code, stdout, and stderr
    assert exitcode == 0
    assert (
        out
        == (
            _greeting_string()
            + "\n"
            + f"Workspace exists already at location {TALKTORIAL_FOLDER_NAME}."
            + "\n"
            + _talktorial_list_string(TALKTORIAL_FOLDER_NAME)
            + "\n"
            + _run_jlab_string(TALKTORIAL_FOLDER_NAME)
            + "\n"
        ).encode()
    )
    assert err == b""

    # Check if all files were transferred to workspace
    # Set path to template (repository) and test (copy) talktorial directories
    talktorials_path_template = Path(__name__).parent / "teachopencadd/talktorials"
    talktorials_path_test = Path(TALKTORIAL_FOLDER_NAME)
    # Fetch all files in directories
    files_list_template = sorted(talktorials_path_template.glob("**/*"))
    files_list_test = sorted(talktorials_path_test.glob("**/*"))
    # Remove checkpoint files that may be present
    files_list_template = [
        file for file in files_list_template if "checkpoint" not in str(file)
    ]
    files_list_test = [
        file for file in files_list_test if "checkpoint" not in str(file)
    ]
    # The same number of files?
    assert len(files_list_test) == len(files_list_template)

    # At the very end: Delete TeachOpenCADD talktorial folder
    subprocess.run(f"rm -r {TALKTORIAL_FOLDER_NAME}".split())


def test_start_incorrect_workspace():
    """
    Test `teachopencadd start` for non-existing user-defined workspace.
    """

    command = "teachopencadd start xxx"
    out, err, exitcode = capture(command.split())

    assert exitcode == 1
    # Keep console output without the trailing "\n"
    out_template = (_greeting_string() + "\n").encode()
    assert out == out_template
    # Keep console error without traceback
    err = err.split(b"\n")[-2]
    err_template = b"RuntimeError: Could not find user-defined location `xxx`"
    assert err == err_template
