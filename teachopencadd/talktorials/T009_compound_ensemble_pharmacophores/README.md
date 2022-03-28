# T009 · Ligand-based pharmacophores

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Pratik Dhakal, CADD seminar, 2017, Charité/FU Berlin
- Florian Gusewski, CADD seminar, 2018, Charité/FU Berlin
- Jaime Rodríguez-Guerra, [Volkamer lab](https://volkamerlab.org/), Charité
- Dominique Sydow, [Volkamer lab](https://volkamerlab.org/), Charité


__Talktorial T009__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of talktorials T001-T010.


**Note**: Please run this notebook cell by cell. Running all cells in one is possible also, however, part of the nglview 3D representations might be missing.


## Aim of this talktorial

In this talktorial, we use known EGFR ligands, which were selected and aligned in the previous talktorial, to identify donor, acceptor, and hydrophobic pharmacophoric features for each ligand. Those features are then clustered to define an ensemble pharmacophore, which represents the properties of the set of known EGFR ligands and can be used to search for novel EGFR ligands via virtual screening.


## Learning goals


### Contents in *Theory*

* Pharmacophore modeling
  * Structure- and ligand-based pharmacophore modeling
* Virtual screening with pharmacophores
* Clustering: k-means


### Contents in *Practical*

* Get pre-aligned ligands from previous talktorial
* Show ligands with NGLView
* Extract pharmacophore features
* Show the pharmacophore features of all ligands
  * Hydrogen bond donors
  * Hydrogen bond acceptors
  * Hydrophobic contacts
* Collect coordinates of features per feature type
* Generate ensemble pharmacophores
  * Set static parameters for k-means clustering
  * Set static parameters for cluster selection
  * Define k-means clustering and cluster selection functions
  * Cluster features
  * Select relevant clusters
  * Get selected cluster coordinates
* Show clusters
  * Hydrogen bond donors
  * Hydrogen bond acceptors
  * Hydrophobic contacts
* Show ensemble pharmacophore


### References

* IUPAC pharmacophore definition 
([<i>Pure & Appl. Chem</i> (1998), <b>70</b>, 1129-43](https://www.degruyter.com/view/journals/pac/70/5/article-p1129.xml))
* 3D pharmacophores in LigandScout 
([<i>J. Chem. Inf. Model.</i> (2005), <b>45</b>, 160-9](http://pubs.acs.org/doi/pdf/10.1021/ci049885e))
* Book chapter: Pharmacophore Perception and Applications 
([Applied Chemoinformatics, Wiley-VCH Verlag GmbH & Co. KGaA, Weinheim, (2018), **1**, 259-82](https://onlinelibrary.wiley.com/doi/10.1002/9783527806539.ch6f))
* Book chapter: Structure-Based Virtual Screening ([Applied Chemoinformatics, Wiley-VCH Verlag GmbH & Co. KGaA, Weinheim, (2018), **1**, 313-31](https://onlinelibrary.wiley.com/doi/10.1002/9783527806539.ch6h)).
* Monty Kier and the origin of the pharmacophore concept 
([<i>Internet Electron. J. Mol. Des.</i> (2007), <b>6</b>, 271-9](http://biochempress.com/Files/iejmd_2007_6_0271.pdf))
* Nik Stiefl's demonstration of pharmacophore modeling with RDKit 
([RDKit UGM 2016 on GitHub](https://github.com/rdkit/UGM_2016/blob/master/Notebooks/Stiefl_RDKitPh4FullPublication.ipynb)) 
