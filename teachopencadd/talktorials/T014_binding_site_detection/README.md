# T014 · Binding site detection

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

* Adapted from Abishek Laxmanan Ravi Shankar, 2019, internship at Volkamer lab
* Andrea Volkamer, 2020/21, [Volkamer lab, Charité](https://volkamerlab.org/)
* Dominique Sydow, 2020/21, [Volkamer lab, Charité](https://volkamerlab.org/)


## Aim of this talktorial

The binding site of a protein is the key to its function. In this talktorial, we introduce the concepts of computational binding site detection tools using DoGSiteScorer from the [protein.plus](https://proteins.plus/) web server, exemplified on an EGFR structure. 
Additionally, we compare the results to the pre-defined KLIFS binding site by calculating the percentage of residues in accordance between the two sets.


### Contents in *Theory*

* Protein binding sites
* Binding site detection
    * Methods overview
    * DoGSiteScorer
* Comparison to KLIFS pocket


### Contents in *Practical*

* Binding site detection using DoGSiteScorer
    * Job submission of structure of interest
    * Get DoGSiteScorer pocket metadata
    * Pick the most suitable pocket
    * Get best binding site file content
    * Investigate detected pocket
* Comparison between DoGSiteScorer and KLIFS pocket
    * Get DoGSiteScorer pocket residues
    * Get KLIFS pocket residues
    * Overlap of pocket residues


### References
* Prediction, Analysis, and Comparison of Active Sites [Volkamer <i>et al.</i>, (<b>2018</b>)](https://doi.org/10.1002/9783527806539.ch6g), book chapter in Applied Chemoinformatics: Achievements and Future Opportunities, Wiley
* DoGSiteScorer, [Volkamer <i>et al.</i>, <i>J.Chem.Inf.Model</i>, (<b>2012</b>), 52(2):360-372](https://pubmed.ncbi.nlm.nih.gov/22148551/)
* [ProteinsPlus](https://proteins.plus/): a web portal for structure analysis of macromolecules. [Fährrolfes <i>et al.</i>, <i>NAR</i>, (<b>2017</b>), 3;45(W1)](https://pubmed.ncbi.nlm.nih.gov/28472372/)
* [KLIFS](https://klifs.net/): a structural kinase-ligand interaction database, [Kanev <i>et al.</i>, <i>NAR</i>, (<b>2021</b>), 49(D1):D562-D569](https://academic.oup.com/nar/article/49/D1/D562/5934416) 
