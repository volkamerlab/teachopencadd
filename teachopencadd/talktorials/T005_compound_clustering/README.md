# T005 · Compound clustering

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Gizem Spriewald, CADD Seminar, 2017, Charité/FU Berlin
- Calvinna Caswara, CADD Seminar, 2018, Charité/FU Berlin
- Jaime Rodríguez-Guerra, 2019-2020, [Volkamer lab](https://volkamerlab.org), Charité


__Talktorial T005__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of talktorials T001-T010.


## Aim of this talktorial

<!-- TODO: The wording of this paragraph is confusing -->

Similar compounds might bind to the same targets and show similar effects. 
Based on this similar property principle, compound similarity can be used to build chemical groups via clustering. 
From such a clustering, a diverse set of compounds can also be selected from a larger set of screening compounds for further experimental testing.


### Contents in _Theory_

* Introduction to clustering and Jarvis-Patrick algorithm
* Detailed explanation of Butina clustering
* Picking diverse compounds


### Contents in _Practical_

* Clustering with the Butina algorithm
* Visualizing the clusters
* Picking the final list of compounds
* Bonus: analysis of run times


### References

* Butina, D. Unsupervised Data Base Clustering Based on Daylight’s Fingerprint and Tanimoto Similarity: A Fast and Automated Way To Cluster Small and Large Data Set. _J. Chem. Inf. Comput. Sci._ (1999)
* Leach, Andrew R., Gillet, Valerie J. An Introduction to Chemoinformatics (2003)
* [Jarvis-Patrick Clustering](http://www.improvedoutcomes.com/docs/WebSiteDocs/Clustering/Jarvis-Patrick_Clustering_Overview.htm)
* [TDT Tutorial](https://github.com/sriniker/TDT-tutorial-2014/blob/master/TDT_challenge_tutorial.ipynb)
* [RDKit clustering documentation](http://rdkit.org/docs/Cookbook.html#clustering-molecules)
