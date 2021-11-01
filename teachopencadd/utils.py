"""
Helper functions and constants for the TeachOpenCADD talktorials
"""

from pathlib import Path
import sys

from . import _version


def seed_everything(seed=22):
    """Set the RNG seed in Python and Numpy"""
    import random
    import os
    import numpy as np

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)


def show_pdf(pdf_url):
    """PDF viewer in notebook

    Parameters
    ----------
    pdf_url : str
            URL to the PDF file.
    Notes
    -----
    You might need to click "File> Trust this notebook for this live PDF preview to work".
    """
    from IPython.display import display, HTML

    display(
        HTML(
            f"""
    <iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true"
        frameborder="0" webkitallowfullscreen mozallowfullscreen
        allowfullscreen width="900" height="600">
    </iframe>
    """
        )
    )


def pdbqt_to_pdbblock(pdbqt):
    """File converter

    Parameters
    ----------
    pdbqt :
        pdbqt file.

    """
    lines = []
    with open(pdbqt) as f:
        for line in f:
            if line[:6] in ("ATOM  ", "HETATM"):
                lines.append(line[:67].strip())
    return "\n".join(lines)


def _greeting_string():
    """
    Print TeachOpenCADD greeting.

    Notes
    -----
    Generated with https://manytools.org/hacker-tools/ascii-banner/ (Font: Mini)
    """

    message = f"""
 ___                _               _       _   _  
  |  _   _.  _ |_  / \ ._   _  ._  /   /\  | \ | \ 
  | (/_ (_| (_ | | \_/ |_) (/_ | | \_ /--\ |_/ |_/ 
                       |                           

    version {_version.get_versions()['version']}
    by @volkamerlab
    """

    return message


def _run_jlab_string(talktorials_dst_dir):
    """
    Print command for starting JupyterLab from workspace folder.

    Parameters
    ----------
    talktorials_dst_dir : str or pathlib.Path
        Path to directory containing the talktorial folders.
    """

    talktorials_dst_dir = Path(talktorials_dst_dir)

    message = f"""
To start working with the talktorials in JupyterLab run:

    jupyter lab {talktorials_dst_dir}

Enjoy!
"""

    return message


def _talktorial_list_string(talktorials_dst_dir):
    """
    Print a list of all talktorials.

    Parameters
    ----------
    talktorials_dst_dir : str or pathlib.Path
        Path to directory containing the talktorial folders.
    """

    talktorials_dst_dir = Path(talktorials_dst_dir)

    message = []

    if talktorials_dst_dir.is_dir():
        message.append("\nTalktorials available in your workspace:\n")
        for d in sorted(talktorials_dst_dir.glob("**/*")):
            if (d / "talktorial.ipynb").exists():
                message.append(f"  - {d.name}")
        message = "\n".join(message)
        return message
    else:
        print(f"Could not find talktorials at expected location `{talktorials_dst_dir}`")
        sys.exit()
