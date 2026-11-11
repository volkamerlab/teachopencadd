# Data
## `models/`
This folder should contain the NeuralPLexer model (weights, ...) that can be obtained from (https://doi.org/10.5281/zenodo.10373581)[https://doi.org/10.5281/zenodo.10373581] (see `models/README.md`).
## `6np5/`
This folder comprises the input protein structure 6np5 (`protein.pdb` for the templated task), as well as, the input ligand (`ligand.sdf`/-`.mol2`, originally cocrystallized). This data was also obtained from (https://doi.org/10.5281/zenodo.10373581)[https://doi.org/10.5281/zenodo.10373581], and originates from PDBind.
## `results_*`
These folders (`_felxible_receptor/`, `_rigid_reseptor/`, and `_trajectory/`) contain the precalculated NeuralPLexer results for the respective tasks.