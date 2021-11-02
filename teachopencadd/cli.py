"""
Command Line Interface for the project.
"""

from pathlib import Path
import argparse
import subprocess
import shutil
import sys

from teachopencadd.utils import _greeting_string, _run_jlab_string, _talktorial_list_string
from . import _version

TALKTORIAL_FOLDER_NAME = "teachopencadd-talktorials"


def main():
    """
    Main CLI function enabling the following signatures:
    - teachopencadd start path/to/workspace
    """

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    # Subcommand `start`
    subparser_start = subparsers.add_parser("start")
    subparser_start.add_argument(
        "workspace", type=str, help="Path to directory for user workspace"
    )
    subparser_start.set_defaults(func=_start)

    # For future additional subcommands (e.g. `teachopencadd test`),
    # - copy the `subparser_start` code block above,
    # - replace `start` with `test`, and
    # - add a function called `test` that implements the behavior you want.

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        # Run help if no arguments were given
        subprocess.run(["teachopencadd", "-h"])


def _start(args):
    """
    Starts a new TeachOpenCADD workspace.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments for start subcommand.

    Notes
    -----
    Procedure:
    - copy all talktorial folders to a folder called `TALKTORIAL_FOLDER_NAME` in a user-defined
      directory
    - if such a folder already exists, do nothing but print message
    - print list of talktorials in workspace
    - print instructions on how to fire up the talktorials in JupyterLab
    """

    print(_greeting_string())

    # Source and destination directories for talktorials
    talktorials_src_dir = Path(_version.__file__).parent / "talktorials"
    talktorials_dst_dir = Path(args.workspace) / TALKTORIAL_FOLDER_NAME

    if not Path(args.workspace).is_dir():
        print(f"Could not find user-defined location `{args.workspace}`.")
        sys.exit()

    if not talktorials_src_dir.is_dir():
        print(f"Could not find talktorials at expected location `{talktorials_src_dir}`.")
        sys.exit()

    try:
        shutil.copytree(talktorials_src_dir, talktorials_dst_dir)
    except FileExistsError:
        print(f"Workspace exists already at location `{talktorials_dst_dir}`.")

    print(_talktorial_list_string(talktorials_dst_dir))
    print(_run_jlab_string(talktorials_dst_dir))
