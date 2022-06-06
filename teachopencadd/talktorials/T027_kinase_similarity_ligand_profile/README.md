# T027 · Kinase similarity: Ligand profile

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Talia B. Kimber, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Dominique Sydow, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)
- Andrea Volkamer, 2021, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

The aim of this talktorial is to investigate kinase similarity through ligand profiling data (ChEMBL29). In the context of drug design, the following assumption is often made: if a compound was tested active on two different kinases, it is suspected that these two kinases may have some degree of similarity. We will use this assumption in this talktorial. The concept of kinase promiscuity is also covered.


### Contents in *Theory*

* Kinase dataset
* Bioactivity data
* Kinase similarity descriptor: Ligand profile
    * Kinase similarity
    * Kinase promiscuity
* From similarity matrix to distance matrix


### Contents in *Practical*

* Define the kinases of interest
* Retrieve the data
* Preprocess the data
    * Hit or non-hit
* Kinase promiscuity
* Kinase similarity
    * Visualize similarity as kinase matrix
    * Save kinase similarity matrix
* Kinase distance matrix
    * Save kinase distance matrix


### References

* Kinase dataset: [<i>Molecules</i> (2021), <b>26(3)</b>, 629](https://www.mdpi.com/1420-3049/26/3/629) 
* ChEMBL database
  * Website: https://www.ebi.ac.uk/chembl/
  * Paper: [<i>Nucleic Acid Research</i> (2017), <b>45(D1)</b>, D945-D954](https://doi.org/10.1093/nar/gkw1074) 
* KinMap
  * Website: http://www.kinhub.org/kinmap/
  * Paper: [<i>BMC Bioinformatics</i> (2017), <b>18(1)</b>, 16](https://doi.org/10.1186/s12859-016-1433-7) 
