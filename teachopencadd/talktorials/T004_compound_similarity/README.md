# T004 · Ligand-based screening: compound similarity

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Andrea Morger, 2017-2020, [Volkamer lab](https://volkamerlab.org/), Charité
- Franziska Fritz, CADD seminar, 2018, Charité/FU Berlin
- Yonghui Chen, 2019-2020, [Volkamer lab](https://volkamerlab.org/), Charité
- Dominique Sydow, 2018-2020, [Volkamer lab](https://volkamerlab.org/), Charité


__Talktorial T004__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of **talktorials T001-T010**.


## Aim of this talktorial

In this talktorial, we get familiar with different approaches to encode (descriptors, fingerprints) and compare (similarity measures) molecules. Furthermore, we perform a virtual screening in the form of a similarity search for the EGFR inhibitor Gefitinib against our dataset of EGFR-tested molecules from the ChEMBL database filtered by Lipinski's rule of five (see **Talktorial T002**). 


### Contents in _Theory_

* Molecular similarity
* Molecular descriptors
* Molecular fingerprints
  * Substructure-based fingerprints
  * MACCS fingerprints
  * Morgan fingerprints and circular fingerprints
* Molecular similarity measures
  * Tanimoto coefficient
  * Dice coefficient
* Virtual screening
  * Virtual screening using similarity search
  * Enrichment plots


### Contents in _Practical_

* Import and draw molecules
* Calculate molecular descriptors
  * 1D molecular descriptors: Molecular weight
  * 2D molecular descriptors: MACCS fingerprint
  * 2D molecular descriptors: Morgan fingerprint
* Calculate molecular similarity
  * MACCS fingerprints: Tanimoto and Dice similarity
  * Morgan fingerprints: Tanimoto and Dice similarity
* Virtual screening using similarity search
  * Compare query molecule to all molecules in the data set
  * Distribution of similarity values
  * Visualize most similar molecules
  * Generate enrichment plots
  * Calculate enrichment factors


### References

* Review on "Molecular similarity in medicinal chemistry" ([<i>J. Med. Chem.</i> (2014), <b>57</b>, 3186-3204](http://pubs.acs.org/doi/abs/10.1021/jm401411z))
* [Morgan fingerprints](http://www.rdkit.org/docs/GettingStartedInPython.html#morgan-fingerprints-circular-fingerprints) with `rdkit`
* Description of the extended-connectivity fingerprint ECFP ([<i>J. Chem. Inf. Model.</i> (2010), <b>50</b>,742-754](https://pubs.acs.org/doi/abs/10.1021/ci100050t))
* What is the chemical space?
([<i>ACS Chem. Neurosci.</i> (2012), <b>19</b>, 649-57](https://www.ncbi.nlm.nih.gov/pubmed/23019491))
* List of [molecular descriptors](https://www.rdkit.org/docs/GettingStartedInPython.html#list-of-available-descriptors) in `rdkit`
* List of [fingerprints](https://www.rdkit.org/docs/GettingStartedInPython.html#list-of-available-fingerprints) in `rdkit`
* Introduction to enrichment plots ([Applied Chemoinformatics, Wiley-VCH Verlag GmbH & Co. KGaA, Weinheim, (2018), **1**, 313-31](https://onlinelibrary.wiley.com/doi/10.1002/9783527806539.ch6h))
