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
