# T042 ·  Inductive Conformal Prediction

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Lisa-Marie Rolli, 2026, Saarland University



## Aim of this talktorial

Traditional machine learning models output a point value (regression) or class (classification) but do not provide rigorous guarantees about uncertainty. Inductive conformal prediction (CP) addresses this limitation by transforming model outputs into prediction intervals (regression) or sets (classification) with statistical coverage guarantees, given specific assumptions.

The aim of this talktorial is to introduce basic concepts of inductive CP and demonstrate how to apply it to toxicity prediction models.


### Contents in *Theory*

* Prerequisites
    * Property prediction models
* Inductive Conformal Prediction Theory
    * Data split
    * Prediction probabilities
    * (Non-)conformity scores
    * Efficiency and coverage evaluation of CP 



### Contents in *Practical*


* Model training
    * Load and split raw data
    * Data preparation
    * Random forest: model training, calibration and testing
* Conformal prediction
    * Calibrating the model
    * Calculating (Non-)conformity scores with the `morgoth` package
    * Evaluate efficiency and coverage


### References

### Setting of this talktorial
* [Sydow et al., 2019, doi:10.1186/s13321-019-0351-x](https://doi.org/10.1186/s13321-019-0351-x), "TeachOpenCADD: a teaching platform for computer-aided drug design using open source packages and data"



### Models

* [Breiman, 2001, doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324), "Random forests"


### Conformal prediction

* [Jimenez-Luna et al., 2020, doi:10.1038/s42256-020-00236-4](https://doi.org/10.1038/s42256-020-00236-4), "Drug discovery with explainable artificial intelligence"
* [Angelopoulos and Bates, 2022, doi:10.48550/arXiv.2107.07511](https://arxiv.org/abs/2107.07511), "A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification"
* [Vovk et al., 2022, doi:10.1007/978-3-031-06649-8_3](https://link.springer.com/chapter/10.1007/978-3-031-06649-8_3), "Conformal Prediction: Classification and General Case"
* [Rolli et al., 2026, doi:10.1039/d5dd00284b](https://pubs.rsc.org/dd/article/5/4/1746/1229659/Increasing-trustworthiness-of-machine-learning), "Increasing trustworthiness of machine learning-based drug sensitivity prediction with a multivariate random forest approach"
* [Morger et al., 2020, doi:10.1186/s13321-020-00422-x](https://link.springer.com/article/10.1186/s13321-020-00422-x), "KnowTox: pipeline and case study for confident prediction of potential toxic effects of compounds in early phases of development"
