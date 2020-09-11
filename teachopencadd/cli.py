"""
Command Line Interface for the project.
"""

from pathlib import Path
from . import _version


def main():
    print(f"TeachOpenCADD CLI {_version.get_versions()['version']}")
    talktorials_dir = Path(_version.__file__).parent / "talktorials"
    if talktorials_dir.is_dir():
        print("Available talktorials:")
        for d in sorted(talktorials_dir.glob("*/")):
            if (d / "talktorial.ipynb").exists():
                print("  -", d.name)