# T024 · Kinase similarity: Sequence

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Talia B. Kimber, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Andrea Volkamer, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

In this talktorial, we investigate sequence similarity for kinases of interest. KLIFS API is used to retrieve the $85$ residues of the pocket sequence for each kinase. 

Two similarity measures are implemented:

   1. Sequence identity, i.e., the similarity which is based on character-wise discrepancy.
   2. Sequence similarity, i.e., the similarity which is based on a substitution matrix, thus, reflecting similarities between amino acids.
   
_Note_: We focus on similarities between orthosteric kinase binding sites; similarities to allosteric binding sites are not covered.


### Contents in *Theory*

* Kinase dataset
* Kinase similarity descriptor: Sequence
    * Identity score
    * Substitution score
* From similarity matrix to distance matrix


### Contents in *Practical*

* Define the kinases of interest
* Retrieve sequences from KLIFS
* Sequence similarity
    * Identity score
    * Substitution score
* Kinase similarity
  * Visualize similarity as kinase matrix
  * Save kinase similarity matrix
* Kinase distance matrix
  * Save kinase distance matrix


### References

* Kinase dataset: [<i>Molecules</i> (2021), <b>26(3)</b>, 629](https://www.mdpi.com/1420-3049/26/3/629) 
* KLIFS
  * KLIFS URL: https://klifs.net/
  * KLIFS database: [<i>Nucleic Acid Res.</i> (2020), <b>49(D1)</b>, D562-D569](https://doi.org/10.1093/nar/gkaa895)
* Sequence-based kinase clustering: Manning _et al._ [<i>Science</i> (2002), <b>298(5600)</b>, 1912-1934](https://doi.org/10.1126/science.1075762)
* Substitution matrix: [<i>PNAS</i> (1992), <b>89(22)<b>, 10915-10919](https://doi.org/10.1073/pnas.89.22.10915)
* Biotite
    * Documentation: https://www.biotite-python.org/index.html
    * [Blosum matrix](https://www.biotite-python.org/examples/gallery/sequence/blosum_dendrogram.html?highlight=blosum)
* Sequence logo: http://www.cbs.dtu.dk/biotools/Seq2Logo/    
