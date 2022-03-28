# T010 · Binding site similarity and off-target prediction

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Angelika Szengel, CADD seminar 2017, Charité/FU Berlin
- Marvis Sydow, CADD seminar 2018, Charité/FU Berlin
- Richard Gowers, RDKit UGM hackathon 2019
- Jaime Rodríguez-Guerra, 2020, [Volkamer lab](https://volkamerlab.org), Charité
- Dominique Sydow, 2018-2020, [Volkamer lab](https://volkamerlab.org), Charité
- Mareike Leja, 2020, [Volkamer lab](https://volkamerlab.org), Charité


__Talktorial T010__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of talktorials T001-T010.


**Note**: Please run this notebook cell by cell. Running all cells in one is possible also, however, part of the `nglview` 3D representations might be missing.


## Aim of this talktorial

In this talktorial, we use the structural similarity of full proteins and binding sites to predict off-targets, i.e. proteins that are not intended targets of a drug. This may lead to unwanted side effects or enable desired alternate applications of a drug (drug repositioning).
We discuss the main steps for binding site comparison and implement a basic method, i.e. the geometrical variation between structures (the root mean square deviation between two structures).


### Contents in *Theory*

* Off-target proteins
* Computational off-target prediction: binding site comparison
* Pairwise RMSD as simple measure for similarity
* Imatinib, a tyrosine kinase inhibitor


### Contents in *Practical*

* Load and visualize the ligand of interest (Imatinib/STI)
* Get all protein-STI complexes from the PDB
* Visualize the PDB structures
* Align the PDB structures (full protein)
* Get pairwise RMSD (full protein)
* Align the PDB structures (binding site)
* Get pairwise RMSD (binding site)
* Filter out outliers


### References

* Binding site superposition + comparison 
  * Binding site comparison reviews: 
    * [<i>Curr. Comput. Aided Drug Des. </i> (2008), <b>4</b>, 209-20](https://www.eurekaselect.com/67606/article/how-measure-similarity-between-protein-ligand-binding-sites)
    * [<i>J. Med. Chem. </i> (2016), <b>9</b>, 4121-51](https://pubs.acs.org/doi/10.1021/acs.jmedchem.6b00078)
  * Molecular superposition with Python: `opencadd` package (`structure.superposition` module) ([GitHub repository](https://github.com/volkamerlab/opencadd))
  * Wikipedia article on root mean square deviation ([RMSD](https://en.wikipedia.org/wiki/Root-mean-square_deviation_of_atomic_positions)) and [structural superposition](https://en.wikipedia.org/wiki/Structural_alignment)
  * Structural superposition: [Book chapter: Algorithms, Applications, and Challenges of Protein Structure Alignment in *Advances in Protein Chemistry and Structural Biology* (2014), **94**, 121-75](https://www.sciencedirect.com/science/article/pii/B9780128001684000056?via%3Dihub)
* Imatinib  
  * Review on Imatinib: [<i>Nat. Rev. Clin. Oncol.</i> (2016), <b>13</b>, 431-46](https://www.nature.com/articles/nrclinonc.2016.41)
  * Promiscuity of imatinib: 
[<i>J. Biol.</i> (2009), <b>8</b>, 30](https://jbiol.biomedcentral.com/articles/10.1186/jbiol134)
  * [ChEMBL information on Imatinib](https://www.ebi.ac.uk/chembl/compound/inspect/CHEMBL941)
  * [PDB information on Imatinib](https://www3.rcsb.org/ligand/STI)
  * Side effects of Imatinib
    * [MedFacts Consumer Drug Information](https://www.drugs.com/cdi/imatinib.html)
    * [DrugBank](https://go.drugbank.com/drugs/DB00619)
    * [<i>BMC Struct. Biol.</i> (2009), <b>9</b>](https://bmcstructbiol.biomedcentral.com/articles/10.1186/1472-6807-9-7)
* PDB queries
  * `pypdb` Python package 
[_Bioinformatics_ (2016), **1**, 159-60](https://academic.oup.com/bioinformatics/article-lookup/doi/10.1093/bioinformatics/btv543); [documentation](http://www.wgilpin.com/pypdb_docs/html/)
  * `biotite` Python package [_BMC Bioinformatics_ (2018), **19**](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2367-z); [documentation](https://www.biotite-python.org/)
  * Check out **Talktorial T008** for more details on PDB queries
