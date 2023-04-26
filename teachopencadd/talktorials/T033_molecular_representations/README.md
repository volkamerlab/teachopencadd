# Feedback formatting:


# T033 · Molecular representations

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

**<span style="color:red">Important</span>:** Currently, this talkturial uses Datamol which has to be installed using `conda install -c conda-forge datamol`.


Authors:

- [Gerrit Großmann](https://mosi.uni-saarland.de/people/gerrit/), 2022, Saarland University


__Talktorial T033__: This talktorial is part of the TeachOpenCADD pipeline described in the TeachOpenCADD publication (TODO), comprising of talktorials T033 to T038.


## Aim of this talktorial

In this talktorial, we conduct the groundwork for the deep learning talktorials (<span style="color:pink">add references: 034, 035, 036, 037, 038</span>).
Specifically, we learn about molecular representations and find that representing a molecule in a computer is not a trivial task. Different representations come with their specific implications and (dis-)advantages.


### Contents in Theory

* What is a molecule?
* Molecular representations
* Molecular representations for humans
* Computer-age molecular representations


### Contents in Practical

* Conformers
* Molecular graphs
* Fingerprints


### References

* Databases: 
  * [UniProt Protein Database](https://www.uniprot.org/)
  * [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/)
* Papers: 
  * [Molecular representations in AI-driven drug discovery: a review and practical guide](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-020-00460-5#:~:text=Traditionally%2C%20molecules%20are%20represented%20as,of%20chemical%20structures%20in%20cheminformatics.)
  * [A review of molecular representation in the age of machine learning](https://wires.onlinelibrary.wiley.com/doi/full/10.1002/wcms.1603)
  * [Point-based molecular representation learning from conformers](https://openreview.net/pdf?id=pjePBJjlBby)
  * [Learning 3D Representations of Molecular Chirality with Invariance to Bond Rotations](https://openreview.net/pdf?id=hm2tNDdgaFK)
* Talkturials: 
  * [T008 - Protein data acquisition: Protein Data Bank (PDB)](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T008_query_pdb/talktorial.ipynb)
  * [T017 - Advanced NGLview usage](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T017_advanced_nglview_usage/talktorial.ipynb)
  * Deep learning talkturials T033 to T038
* [Tutorial on chirality](https://chem.libretexts.org/Bookshelves/Organic_Chemistry/Map%3A_Organic_Chemistry_(Vollhardt_and_Schore)/05._Stereoisomers/5.1%3A_Chiral__Molecules)
