# T008 · Protein data acquisition: Protein Data Bank (PDB) 

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Anja Georgi, CADD seminar, 2017, Charité/FU Berlin
- Majid Vafadar, CADD seminar, 2018, Charité/FU Berlin
- Jaime Rodríguez-Guerra, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, [Volkamer lab, Charité](https://volkamerlab.org/)


__Talktorial T008__: This talktorial is part of the TeachOpenCADD pipeline described in the first TeachOpenCADD publication ([_J. Cheminform._ (2019), **11**, 1-7](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x)), comprising of talktorials T001-T010.


## Aim of this talktorial

In this talktorial, we conduct the groundwork for the next talktorial where we will generate a ligand-based ensemble pharmacophore for EGFR. Therefore, we 
(i) fetch all PDB IDs for EGFR from the PDB database that fullfil certain criteria (e.g. ligand-bound structures with high resolution), 
(ii) retrieve protein-ligand structures with the best structural quality, 
(iii) align all structures, and 
(iv) extract and save the ligands to be used in the next talktorial.


### Contents in Theory

* Protein Data Bank (PDB)
* Query the PDB using the Python packages `biotite` and `pypdb`


### Contents in Practical

* Select a query protein
* Get the number of PDB entries for a query protein
* Find PDB entries fullfilling certain conditions
* Select PDB entries with the highest resolution
* Get metadata of ligands from top structures
* Draw top ligand molecules
* Create protein-ligand ID pairs
* Align PDB structures and extract ligands


### References

* Protein Data Bank 
([PDB website](http://www.rcsb.org/))
* `pypdb` Python package 
([_Bioinformatics_ (2016), **1**, 159-60](https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btv543); [documentation](http://www.wgilpin.com/pypdb_docs/html/))
* `biotite` Python package ([_BMC Bioinformatics_ (2018), **19**](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2367-z); [documentation](https://www.biotite-python.org/))
* Molecular superposition with the Python package `opencadd` ([repository](https://github.com/volkamerlab/opencadd))
