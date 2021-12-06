"""
Defines paths to frozen datasets.
- PubChem similarity search results
- Docking starting structures (PDBQT files)
"""

from pathlib import Path

FROZEN_DATA_FILEPATH = Path(__file__).parent / "../data/FrozenData"


class FrozenData:
    """
    Defines paths to frozen data.

    Parameters
    ----------
    project : str
        Name of folder containing frozen data for one project.
    is_frozen : bool
        By default, this is set to `True` and will set all paths to the frozen datasets.
        This is only useful for maintenance reasons.
        For all other use cases, set this to `False`; all paths are set to `None` in order to run
        the pipeline or individual pipeline steps without frozen data.

    Attributes
    ----------
    pubchem_similarity_search : pathlib.Path
        Path to frozen similarity search results from PubChem.
    docking_pdbqt_files : pathlib.Path
        Path to frozen PDBQT structure files as input for docking.

    Properties
    ----------
    pipeline : dict of pathlib.Path
        Dictionary containing all paths to frozen datasets needed to run the full pipeline.
    """

    def __init__(self, project, is_frozen=True):
        self.pubchem_similarity_search = self._set_pubchem_similarity_search(project, is_frozen)
        self.docking_pdbqt_files = self._set_docking_pdbqt_files(project, is_frozen)

    @property
    def pipeline(self):
        return {
            "pubchem_similarity_search": self.pubchem_similarity_search,
            "docking_pdbqt_files": self.docking_pdbqt_files,
        }

    def _set_pubchem_similarity_search(self, project, is_frozen):
        if is_frozen:
            return FROZEN_DATA_FILEPATH / project / "FrozenPubchemQuery.csv"
        else:
            return None

    def _set_docking_pdbqt_files(self, project, is_frozen):
        if is_frozen:
            return FROZEN_DATA_FILEPATH / project / "DockingPdbqt"
        else:
            return None
