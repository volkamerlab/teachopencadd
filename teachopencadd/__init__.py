"""
TeachOpenCADD is a collection of Jupyter Notebooks
to help you learn or teach computer aided drug design concepts.

The notebooks themselves are located under ``talktorials/``.
"""

# Handle versioneer
from ._version import get_versions

versions = get_versions()
__version__ = versions["version"]
__git_revision__ = versions["full-revisionid"]
del get_versions, versions
