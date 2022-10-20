# T032 · Compound activity: Proteochemometrics

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Marina Gorostiola González, 2022, Computational Drug Discovery, Drug Discovery & Safety Leiden University (The Netherlands)
- Olivier J.M. Béquignon, 2022, Computational Drug Discovery, Drug Discovery & Safety Leiden University (The Netherlands)
- Willem Jespers, 2022, Computational Drug Discovery, Drug Discovery & Safety Leiden University (The Netherlands)



## Aim of this talktorial

While activity data is very abundant for some protein targets, there are still a number of underexplored proteins where the use of machine learning (ML) for activity prediction is very difficult due to the lack of data. This issue can be solved leveraging similarities and differences between proteins. In this talktorial, we use Proteochemometrics modelling (PCM) to enrich our activity models with protein data to predict the activity of novel compounds against the four adenosine receptor isoforms (A1, A2A, A2B, A3).


### Contents in *Theory*

* Data preparation
    * Papyrus dataset
    * Molecule encoding: molecular descriptors
    * Protein encoding: protein descriptors

* Proteochemometrics (PCM)
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
* Proteochemometrics modelling
    * Helper functions
        * Preprocessing
    * Model training and validation
        * Random split PCM model
        * Random split QSAR models
        * Leave one target out split PCM model


### References

* Papyrus scripts [github](https://github.com/OlivierBeq/Papyrus-scripts)
* Papyrus dataset preprint: [<i>ChemRvix</i> (2021)](https://chemrxiv.org/engage/chemrxiv/article-details/617aa2467a002162403d71f0)
* Molecular descriptors (Modred): [<i>J. Cheminf.</i>, 10, (2018)](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-018-0258-y)
* Protein descriptors (ProDEC) [github](https://github.com/OlivierBeq/ProDEC)
* Regression metrics [(Scikit learn)](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics)
* XGBoost [Documentation](https://xgboost.readthedocs.io/en/stable/index.html)
* Proteochemometrics review: [<i>Drug Discov.</i> (2019), <b>32</b>, 89-98](https://www.sciencedirect.com/science/article/pii/S1740674920300111?via%3Dihub)
