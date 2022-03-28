# T002 · Molecular filtering: ADME and lead-likeness criteria

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Michele Wichmann, CADD seminars 2017, Charité/FU Berlin
- Mathias Wajnberg, CADD seminars 2018, Charité/FU Berlin
- Dominique Sydow, 2018-2020, [Volkamer lab](https://volkamerlab.org), Charité
- Andrea Volkamer, 2018-2020, [Volkamer lab](https://volkamerlab.org), Charité


__Talktorial T002__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of talktorials T001-T010.


## Aim of this talktorial

In the context of drug design, it is important to filter candidate molecules by e.g. their physicochemical properties. In this talktorial, the compounds acquired from ChEMBL (__Talktorial T001__) will be filtered by Lipinsik's rule of five to keep only orally bioavailable compounds.


### Contents in _Theory_

* ADME - absorption, distribution, metabolism, and excretion
* Lead-likeness and Lipinski's rule of five (Ro5)
* Radar charts in the context of lead-likeness


### Contents in _Practical_

* Define and visualize example molecules
* Calculate and plot molecular properties for Ro5
* Investigate compliance with Ro5
* Apply Ro5 to the EGFR dataset
* Visualize Ro5 properties (radar plot)


### References

* ADME criteria ([Wikipedia](https://en.wikipedia.org/wiki/ADME) and [<i>Mol Pharm.</i> (2010), <b>7(5)</b>, 1388-1405](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3025274/))
* [SwissADME](https://www.nature.com/articles/srep42717) webserver
* What are lead compounds? ([Wikipedia](https://en.wikipedia.org/wiki/Lead_compound))
* What is the LogP value? ([Wikipedia](https://en.wikipedia.org/wiki/Partition_coefficient))
* Lipinski et al. "Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings." ([<i>Adv. Drug Deliv. Rev.</i> (1997), <b>23</b>, 3-25](https://www.sciencedirect.com/science/article/pii/S0169409X96004231))
* Ritchie et al. "Graphical representation of ADME-related molecule properties for medicinal chemists" ([<i>Drug. Discov. Today</i> (2011), <b>16</b>, 65-72](https://www.ncbi.nlm.nih.gov/pubmed/21074634))
