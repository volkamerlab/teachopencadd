# T020 · Analyzing molecular dynamics simulations

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Mareike Leja, 2020/21, Internship at [Volkamer Lab, Charité](https://volkamerlab.org/) 
- David Schaller, 2020/21, [Volkamer Lab, Charité](https://volkamerlab.org/) 
- Andrea Volkamer, 2021, [Volkamer Lab, Charité](https://volkamerlab.org/) 


## Aim of this talktorial

In this talktorial, we will introduce methods for the analysis of molecular dynamics (MD) simulations. The introduced methods include animated visualization, structural alignment, RMSD calculation as well as selected atom distances and hydrogen bond analysis. 
Note, we will work with the simulation results (1ns, 100 frames) generated with **Talktorial T019** on the EGFR kinase ([PDB: 3POZ](https://www.rcsb.org/structure/3poz)) bound to inhibitor [03P](https://www.rcsb.org/ligand/03P). 


### Contents in *Theory*

- MD simulations
    - Application in the drug discovery process
    - Flexible vs. static structures
- Analyzing MD simulations
  - Visualization
  - RMSD
  - Hydrogen bond analysis


### Contents in *Practical*

- Load and visualize the system
- Alignment
- RMSD of protein and ligand
  - RMSD over time
  - RMSD between frames
- Interaction analysis
  - Atomic distances
  - Hydrogen bond analysis


### References

Theoretical Background:

- Review on the impact of MD simulations in drug discovery ([_J Med Chem_ (2016), **59**(9), 4035‐4061](https://doi.org/10.1021/acs.jmedchem.5b01684))
- Review on force fields ([_J Chem Inf Model_ (2018), **58**(3), 565-578](https://doi.org/10.1021/acs.jcim.8b00042))
- Review on hydrogen bonding ([_PLoS One._ (2010), **5(8)**, e12029](https://doi.org/10.1371%2Fjournal.pone.0012029))
- Guide to molecular interactions ([_J. Med. Chem._ 2010, **53(14)**, 5061-84](https://doi.org/10.1021/jm100112j))
- Wikipedia Article about [root-mean-square deviation](https://en.wikipedia.org/wiki/Root-mean-square_deviation)
- Repositories of [MDAnalysis](https://www.mdanalysis.org/) and [NGL View](https://github.com/arose/nglview)
