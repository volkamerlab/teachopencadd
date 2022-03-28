# T019 · Molecular dynamics simulation

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Pietro Gerletti, CADD seminar 2020, Charité/FU Berlin
- Mareike Leja, 2020/21, Internship at [Volkamer Lab, Charité](https://volkamerlab.org/)
- Jeffrey R Wagner, 2020, [Open Force Field Consortium](https://openforcefield.org/)
- David Schaller, 2020/21, [Volkamer Lab, Charité](https://volkamerlab.org/)
- Andrea Volkamer, 2020/21, [Volkamer Lab, Charité](https://volkamerlab.org/)


__Note__

This talktorial was designed to be used with [Google Colab](https://colab.research.google.com/github/volkamerlab/teachopencadd/blob/1bd7cb0c9f6379aebc0c1a0b1c7413685910cffa/teachopencadd/talktorials/019_md_simulation/talktorial.ipynb). It is also possible to use it on a local computer. However, performing the molecular dynamics simulation may take a considerably long time if no GPU is available.

Also, note that this talktorial **will not run on Windows** for the time being (check progress in [this issue](https://github.com/volkamerlab/teachopencadd/issues/136)).


## Aim of this talktorial


In this talktorial, we will learn why molecular dynamics (MD) simulations are important for drug design and which steps are necessary to perform an MD simulation of a protein in complex with a ligand. The kinase EGFR will serve as sample system for simulation.


### Contents in *Theory*

- Molecular dynamics
- Force fields
- Boundary conditions
- MD simulations and drug design
- EGFR kinase


### Contents in *Practical*

- Installation on Google Colab
- Adjust environment for local installations running on Linux or MacOS
- Import dependencies
- Download PDB file
- Prepare the protein ligand complex
  - Protein preparation
  - Ligand preparation
  - Merge protein and ligand
- MD simulation set up
  - Force field
  - System
- Perform the MD simulation
- Download results


### References

- Review on the impact of MD simulations in drug discovery ([_J Med Chem_ (2016), **59**(9), 4035‐4061](https://doi.org/10.1021/acs.jmedchem.5b01684))
- Review on the physics behind MD simulations and best practices ([_Living J Comp Mol Sci_ (2019), **1**(1), 5957](https://doi.org/10.33011/livecoms.1.1.5957))
- Review on force fields ([_J Chem Inf Model_ (2018), **58**(3), 565-578](https://doi.org/10.1021/acs.jcim.8b00042))
- Review on EGFR in cancer ([_Cancers (Basel)_ (2017), **9**(5), 52](https://dx.doi.org/10.3390%2Fcancers9050052))
- Summarized statistical knowledge from Pierre-Simon Laplace ([Théorie Analytique des Probabilités _Gauthier-Villars_ (1820), **3**)](https://archive.org/details/uvrescompltesde31fragoog/page/n15/mode/2up)
- Inspired by a notebook form Jaime Rodríguez-Guerra ([github](https://github.com/jaimergp/uab-msc-bioinf/blob/master/MD%20Simulation%20and%20Analysis%20in%20a%20Notebook.ipynb))
- Repositories of [OpenMM](https://github.com/openmm/openmm) and [OpenMM Forcefields](https://github.com/openmm/openmmforcefields), [RDKit](https://github.com/rdkit/rdkit), [PyPDB](https://github.com/williamgilpin/pypdb), [MDTraj](https://github.com/mdtraj/mdtraj), [PDBFixer](https://github.com/openmm/pdbfixer)
- Wikipedia articles about [MD simulations](https://en.wikipedia.org/wiki/Molecular_dynamics), [AMBER](https://en.wikipedia.org/wiki/AMBER) and [force fields](https://en.wikipedia.org/wiki/Force_field_(chemistry)) in general
