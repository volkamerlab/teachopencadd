# T028 · Kinase similarity: Compare different perspectives

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Talia B. Kimber, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Andrea Volkamer, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

We will compare different perspectives on kinase similarity, which were discussed in detail in previous notebooks:

* **Talktorial T024**: Kinase pocket sequences (KLIFS pocket sequences)
* **Talktorial T025**: Kinase pocket structures (KiSSim fingerprint based on KLIFS pocket residues)
* **Talktorial T026**: Kinase-ligand interaction profiles (KLIFS IFPs based on KLIFS pocket residues)
* **Talktorial T027**: Ligand profiling data (using ChEMBL29 bioactivity data)

_Note_: We focus only on similarities between orthosteric kinase binding sites; similarities to allosteric binding sites are not covered (T027 is an exception since the profiling data does not distinguish between binding sites).


### Contents in *Theory*

* Kinase dataset
* Kinase similarity descriptor (considering 4 different methods)
* Distance matrix conditions


### Contents in *Practical*

* Load kinase similarity and distance matrices
* Distance matrix conditions
* Visualize similarity for example perspective
  * Visualize kinase similarity matrix as heatmap
  * Visualize similarity as dendrogram
* Visualize similarities from the four different perspectives
  * Preprocess distance matrices
    * Normalize matrices
    * Define kinase order
  * Visualize kinase similarities
  * Analysis of results


### References

* Kinase dataset: [<i>Molecules</i> (2021), <b>26(3)</b>, 629](https://www.mdpi.com/1420-3049/26/3/629) 
* Clustering and dendrograms with `scipy`: https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html
* Distance matrix:
    * https://en.wikipedia.org/wiki/Distance_matrix
    * Gilbert, A. C. and Jain, L. "If it ain't broke, don't fix it: Sparse metric repair." _2017 55th Annual Allerton Conference on Communication, Control, and Computing (Allerton)_. IEEE, 2017. https://arxiv.org/pdf/1710.10655.pdf
