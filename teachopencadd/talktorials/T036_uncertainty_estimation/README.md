# T036 · Uncertainty estimation

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Michael Backenköhler, 2022, [Volkamer lab](https://volkarmerlab.org), Saarland University


*The predictive setting (and the model class) used in this talktorial is adapted from [__Talktorial T022__](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T022_ligand_based_screening_neural_network/talktorial.ipynb).*


## Aim of this talktorial

Researchers often focus on prediction quality alone. However,when applying a predictive model, researchers are also interested in how certain they can be in a specific prediction. Estimating and providing such information is the goal of uncertainty estimation. In this talktorial, we discuss some common methodologies and showcase ensemble methods in practice.


### Contents in *Theory*

* Why a model can't and shouldn't be certain
* Calibration
* Methods overview
    * Single deterministic methods
    * Ensemble methods
    * Test-time data augmentation


### Contents in *Practical*
* Data
* Model
    * Training
    * Evaluation
* Ensembles - Training a model multiple times
    * Coverage of confidence intervals
    * Calibration
    * Ranking-based evaluation
* Bagging ensemble - Training a model with varying data
    * Ranking-based evaluation
* Test-time data augmentation


### References
* [Gawlikowski, Jakob, et al. "A survey of uncertainty in deep neural networks." _arXiv preprint_ (2021), arXiv:__2107.03342__](https://arxiv.org/abs/2107.03342)
* [Scalia, Gabriele, et al. "Evaluating scalable uncertainty estimation methods for deep learning-based molecular property prediction." _Journal of chemical information and modeling_ __60.6__ (2020): 2697-2717](https://pubs.acs.org/doi/pdf/10.1021/acs.jcim.9b00975)
* [__Talktorial T022__](https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T022_ligand_based_screening_neural_network/talktorial.ipynb)
