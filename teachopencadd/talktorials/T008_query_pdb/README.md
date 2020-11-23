# T008 · Protein data acquisition: Protein Data Bank (PDB) 

Authors:

- Anja Georgi, CADD seminar, 2017, Charité/FU Berlin
- Majid Vafadar, CADD seminar, 2018, Charité/FU Berlin
- Jaime Rodríguez-Guerra, Volkamer lab, Charité
- Dominique Sydow, Volkamer lab, Charité


__Talktorial T008__: This talktorial is part of the TeachOpenCADD pipeline described in the first TeachOpenCADD publication ([_J. Cheminform._ (2019), **11**, 1-7](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x)), comprising of talktorials T001-T010.


## Aim of this talktorial

In this talktorial, we conduct the groundwork for the next talktorial where we will generate a ligand-based ensemble pharmacophore for EGFR. Therefore, we 
(i) fetch all PDB IDs for EGFR from the PDB database, 
(ii) retrieve five protein-ligand structures, which have the best structural quality and are derived from X-ray crystallography, and 
(iii) align all structures to each in 3D as well as extract and save the ligands to be used in the next talktorial.


### Contents in Theory

* Protein Data Bank (PDB)
* Python package `pypdb`


### Contents in Practical

* Select query protein
* Get all PDB IDs for query protein
* Get statistic on PDB entries for query protein
* Get meta information on PDB entries
* Filter and sort meta information on PDB entries
* Get meta information of ligands from top structures
* Draw top ligand molecules
* Create protein-ligand ID pairs
* Get the PDB structure files
* Align PDB structures


### References

* Protein Data Bank 
([PDB website](http://www.rcsb.org/))
* `pypdb` python package 
([_Bioinformatics_ (2016), **1**, 159-60](https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btv543), [documentation](http://www.wgilpin.com/pypdb_docs/html/))
* Molecular superposition with the python package `opencadd` ([repository](https://github.com/volkamerlab/opencadd))
