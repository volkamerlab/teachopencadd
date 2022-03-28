# T006 · Maximum common substructure

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Oliver Nagel, CADD Seminars, 2017, Charité/FU Berlin
- Jaime Rodríguez-Guerra, 2019-2020, [Volkamer lab](https://volkamerlab.org), Charité
- Andrea Volkamer, 2019-2020, [Volkamer lab](https://volkamerlab.org), Charité


__Talktorial T006__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising talktorials T001-T010.


## Aim of this talktorial

Clustering and classification of large scale chemical data is essential for navigation, analysis and knowledge discovery in a wide variety of chemical application domains in drug discovery.

In the last talktorial, we learned how to group molecules (clustering) and found that the molecules in one cluster look similar to each other and share a common scaffold. Besides visual inspection, we will learn here how to calculate the maximum substructure that a set of molecules has in common.


### Contents in *Theory*

* Introduction to identification of maximum common substructure in a set of molecules
* Detailed explanation of the FMCS algorithm


### Contents in *Practical*

* Load and draw molecules
* Run the FMCS algorithm with different input parameters
* A more diverse set: the EGFR compounds downloaded from ChEMBL
* Identification of MCS using interactive cut-off adaption


### References

* Dalke A, Hastings J., FMCS: a novel algorithm for the multiple MCS problem. [*J. Cheminf.* 2013; **5** (Suppl 1): O6](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3606201/)
* Raymond JW., Willet P., Maximum common subgraph isomorphism algorithms for the matching of chemical structures. [*J Comput Aided Mol Des.* 2002 Jul; **16**(7):521-33](https://link.springer.com/article/10.1023/A:1021271615909)
* [Dalke's website with info on algorithm](http://dalkescientific.com/writings/diary/archive/2012/05/12/mcs_background.html)
* [RDKit Cookbook documentation on MCS](http://www.rdkit.org/docs/Cookbook.html#using-custom-mcs-atom-types)
