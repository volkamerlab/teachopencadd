# T032 · Compound activity: Proteochemometrics

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Marina Gorostiola González, 2022, [Computational Drug Discovery](https://www.universiteitleiden.nl/en/science/drug-research/drug-discovery-and-safety/computational-drug-discovery), Drug Discovery & Safety Leiden University (The Netherlands)
- Olivier J.M. Béquignon, 2022, Computational Drug Discovery, Drug Discovery & Safety Leiden University (The Netherlands)
- Willem Jespers, 2022, Computational Drug Discovery, Drug Discovery & Safety Leiden University (The Netherlands)


## Aim of this talktorial

While activity data is very abundant for some protein targets, there are still a number of underexplored proteins where the use of machine learning (ML) for activity prediction is very difficult due to the lack of data. This issue can be partially solved by leveraging similarities and differences between proteins. In this talktorial, we use proteochemometrics (PCM) modeling to enrich our activity models with protein data to predict the activity of novel compounds against the four [adenosine receptor](https://journals.physiology.org/doi/full/10.1152/physrev.00049.2017) isoforms (A1, A2A, A2B, A3).


### Contents in *Theory*
* Proteochemometrics (PCM) modeling
* Data preparation
    * Papyrus dataset
    * Molecule encoding: molecular descriptors
    * Protein encoding: protein descriptors
* Machine learning principles: regression
    * Data splitting methods
    * Regression evaluation metrics
    * ML algorithm: Random Forest
* Applications of PCM in drug discovery


### Contents in *Practical*

* Download Papyrus dataset
* Data preparation
    * Filter activity data for targets of interest
    * Align target sequences
    * Calculate protein descriptors
    * Calculate compound descriptors
* Proteochemometrics modeling
    * Helper functions
    * Preprocessing
    * Model training and validation
        * Random split PCM model
        * Random split QSAR models
        * Leave one target out split PCM model


### References

* Papyrus scripts [GitHub](https://github.com/OlivierBeq/Papyrus-scripts)
* Papyrus dataset preprint: [*ChemRvix* (2021)](https://chemrxiv.org/engage/chemrxiv/article-details/617aa2467a002162403d71f0)
* Molecular descriptors (Modred): [*J. Cheminf.*, 10, (2018)](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-018-0258-y)
* Protein descriptors (ProDEC) [GitHub](https://github.com/OlivierBeq/ProDEC)
* Regression metrics [(Scikit learn)](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)
* XGBoost [Documentation](https://xgboost.readthedocs.io/en/stable/index.html)
* Proteochemometrics review: [*Drug Discov.* (2019), **32**, 89-98](https://www.sciencedirect.com/science/article/pii/S1740674920300111?via%3Dihub)


