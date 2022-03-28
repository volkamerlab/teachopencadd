# T007 · Ligand-based screening: machine learning

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

* Jan Philipp Albrecht, CADD seminar 2018, Charité/FU Berlin
* Jacob Gora, CADD seminar 2018, Charité/FU Berlin
* Talia B. Kimber, 2019-2020, [Volkamer lab](https://volkamerlab.org)
* Andrea Volkamer, 2019-2020, [Volkamer lab](https://volkamerlab.org)


__Talktorial T007__: This talktorial is part of the TeachOpenCADD pipeline described in the [first TeachOpenCADD paper](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x), comprising of talktorials T001-T010.


## Aim of this talktorial

Due to larger available data sources, machine learning (ML) gained momentum in drug discovery and especially in ligand-based virtual screening. In this talktorial, we learn how to use different supervised ML algorithms to predict the activity of novel compounds against our target of interest (EGFR).


### Contents in _Theory_

* Data preparation: Molecule encoding
* Machine learning (ML)
    * Supervised learning
* Model validation and evaluation
    * Validation strategy: K-fold cross-validation
    *  Performance measures


### Contents in _Practical_

* Load compound and activity data
* Data preparation
    * Data labeling
    * Molecule encoding
* Machine learning
    * Helper functions
    * Random forest classifier
    * Support vector classifier
    * Neural network classifier
    * Cross-validation


### References

* "Fingerprints in the RDKit" [slides](https://www.rdkit.org/UGM/2012/Landrum_RDKit_UGM.Fingerprints.Final.pptx.pdf), G. Landrum, RDKit UGM 2012
* Extended-connectivity fingerprints (ECFPs): Rogers, David, and Mathew Hahn. "Extended-connectivity fingerprints." [_Journal of chemical information and modeling_ 50.5 (2010): 742-754.](https://doi.org/10.1021/ci100050t)
* Machine learning (ML):
  * Random forest (RF): Breiman, L. "Random Forests". [_Machine Learning_ **45**, 5–32 (2001).](https://link.springer.com/article/10.1023%2FA%3A1010933404324)
  * Support vector machines (SVM): Cortes, C., Vapnik, V. "Support-vector networks". [_Machine Learning_ **20**, 273–297 (1995).](https://link.springer.com/article/10.1007%2FBF00994018)
  * Artificial neural networks (ANN): Van Gerven, Marcel, and Sander Bohte. "Artificial neural networks as models of neural information processing." [_Frontiers in Computational Neuroscience_ 11 (2017): 114.](https://doi.org/10.3389/fncom.2017.00114)
* Performance: 
  * Sensitivity and specificity ([Wikipedia](https://en.wikipedia.org/wiki/Sensitivity_and_specificity))
  * ROC curve and AUC ([Wikipedia](https://en.wikipedia.org/wiki/Receiver_operating_characteristic#Area_under_the_curve))
* See also [github notebook by B. Merget](https://github.com/Team-SKI/Publications/tree/master/Profiling_prediction_of_kinase_inhibitors) from [*J. Med. Chem.*, 2017, 60, 474−485](https://pubs.acs.org/doi/10.1021/acs.jmedchem.6b01611) 
* Activity cutoff $pIC_{50} = 6.3$ used in this talktorial
  * Profiling Prediction of Kinase Inhibitors: Toward the Virtual Assay [<i>J. Med. Chem.</i> (2017), <b>60</b>, 474-485](https://doi.org/10.1021/acs.jmedchem.6b01611)
  * Notebook accompanying the publication mentioned before: [Notebook](https://github.com/Team-SKI/Publications/blob/master/Profiling_prediction_of_kinase_inhibitors/Build_ABL1_model.ipynb)
