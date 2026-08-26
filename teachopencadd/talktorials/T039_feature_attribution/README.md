# T039 · Explaining molecular property prediction models with feature attribution methods

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Joschka Groß, 2026, NMM@DFKI, Saarland University



## Aim of this talktorial

Explaining why a machine learning model makes a certain prediction is an important step towards building trust in the model. 

The aim of this talktorial is to introduce basic concepts of explainability and demonstrate how to apply feature attribution methods to molecular property prediction models.


### Contents in *Theory*

* Prerequisites
    * Case study: predicting EGFR binding affinities
    * Property prediction models
* Explainable artificial intelligence (XAI) theory
    * Definitions
    * Basic concepts
        * Local vs. global explanations
        * Faithfulness
        * Plausibility
        * Applications of XAI in drug discovery
        * Other concepts and further reading
    * Feature attribution methods
        * Shapley values and TreeSHAP
        * Input x Gradient



### Contents in *Practical*

* Held-out type I inhibitors
* Model training
    * Load and split raw data
    * Chemprop: data preparation
    * Chemprop: model training and testing
    * Random forest: data preparation
    * Random forest: model training and testing
* Explaining model predictions
    * Attribution abstractions
    * Visualization code
    * Random forest: TreeSHAP
    * Chemprop: Input x Gradient
    * Comparing explanations across models
        * Visually on random molecules
        * Quantifying overall agreement
        * Quinazoline-based type I inhibitors



### References

### Setting of this talktorial
* [Sydow et al., 2019, doi:10.1186/s13321-019-0351-x](https://doi.org/10.1186/s13321-019-0351-x), "TeachOpenCADD: a teaching platform for computer-aided drug design using open source packages and data"
* [Zdrazil et al., 2024, doi:10.1093/nar/gkad1004](https://doi.org/10.1093/nar/gkad1004), "The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods"
* [Stamos et al., 2002, doi:10.1074/jbc.M207135200](https://doi.org/10.1074/jbc.M207135200), "Structure of the epidermal growth factor receptor kinase domain alone and in complex with a 4-anilinoquinazoline inhibitor"
* [van Linden et al., 2014, doi:10.1021/jm400378w](https://doi.org/10.1021/jm400378w), "KLIFS: a knowledge-based structural database to navigate kinase-ligand interaction space"
* [Kanev et al., 2021, doi:10.1093/nar/gkaa895](https://doi.org/10.1093/nar/gkaa895), "KLIFS: an overhaul after the first 5 years of supporting kinase research"
* [Sigismund et al., 2018, doi:10.1002/1878-0261.12155](https://doi.org/10.1002/1878-0261.12155), "Emerging functions of the EGFR in cancer"
* [Kalliokoski et al., 2013, doi:10.1371/journal.pone.0061007](https://doi.org/10.1371/journal.pone.0061007), "Comparability of mixed IC50 data - a statistical analysis"
* [Landrum & Riniker, 2024, doi:10.1021/acs.jcim.4c00049](https://doi.org/10.1021/acs.jcim.4c00049), "Combining IC50 or Ki values from different sources is a source of significant noise"

### Models and representations

* [Breiman, 2001, doi:10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324), "Random forests"
* [Rogers & Hahn, 2010, doi:10.1021/ci100050t](https://doi.org/10.1021/ci100050t), "Extended-connectivity fingerprints" (Morgan/ECFP)
* [Yang et al., 2019, doi:10.1021/acs.jcim.9b00237](https://doi.org/10.1021/acs.jcim.9b00237), "Analyzing learned molecular representations for property prediction"
* [Heid et al., 2024, doi:10.1021/acs.jcim.3c01250](https://doi.org/10.1021/acs.jcim.3c01250), "Chemprop: a machine learning package for chemical property prediction"
* [Burns et al., 2026, doi:10.1021/acs.jcim.6c01546](https://doi.org/10.1021/acs.jcim.6c01546), "Deep learning foundation models for low-data regimes from classical molecular descriptors" (CheMeleon), [preprint arXiv:2506.15792](https://arxiv.org/abs/2506.15792), [code](https://github.com/JacksonBurns/chemeleon), [weights doi:10.5281/zenodo.15426600](https://doi.org/10.5281/zenodo.15426600)

### XAI: concepts and surveys

* [Jimenez-Luna et al., 2020, doi:10.1038/s42256-020-00236-4](https://doi.org/10.1038/s42256-020-00236-4), "Drug discovery with explainable artificial intelligence"
* [Wellawatte et al., 2023, doi:10.1021/acs.jctc.2c01235](https://doi.org/10.1021/acs.jctc.2c01235), "A perspective on explanations of molecular prediction models"
* [Rudin, 2019, doi:10.1038/s42256-019-0048-x](https://doi.org/10.1038/s42256-019-0048-x), "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead"
* [Jacovi & Goldberg, 2020, arXiv:2004.03685](https://arxiv.org/abs/2004.03685), "Towards faithfully interpretable NLP systems: how should we define and evaluate faithfulness?"

### Feature attribution methods

* [Shapley, 1953](https://doi.org/10.1515/9781400881970-018), "A value for n-person games", in *Contributions to the Theory of Games II*
* [Lundberg & Lee, 2017, arXiv:1705.07874](https://arxiv.org/abs/1705.07874), "A unified approach to interpreting model predictions" (SHAP)
* [Lundberg et al., 2018, arXiv:1802.03888](https://arxiv.org/abs/1802.03888), "Consistent individualized feature attribution for tree ensembles" (TreeSHAP)
* [Lundberg et al., 2020, doi:10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9), "From local explanations to global understanding with explainable AI for trees"
* [Simonyan et al., 2014, arXiv:1312.6034](https://arxiv.org/abs/1312.6034), "Deep inside convolutional networks: visualising image classification models and saliency maps" (gradient saliency)
* [Shrikumar et al., 2016, arXiv:1605.01713](https://arxiv.org/abs/1605.01713), "Not just a black box: learning important features through propagating activation differences" (Input x Gradient)
* [Sundararajan et al., 2017, arXiv:1703.01365](https://arxiv.org/abs/1703.01365), "Axiomatic attribution for deep networks" (Integrated Gradients)
* [Ying et al., 2019, arXiv:1903.03894](https://arxiv.org/abs/1903.03894), "GNNExplainer: generating explanations for graph neural networks"
* [Wellawatte et al., 2022, doi:10.1039/D1SC05259D](https://doi.org/10.1039/D1SC05259D), "Model agnostic generation of counterfactual explanations for molecules"

### Evaluating and distrusting explanations

* [Hooker et al., 2019, arXiv:1806.10758](https://arxiv.org/abs/1806.10758), "A benchmark for interpretability methods in deep neural networks" (ROAR)
* [DeYoung et al., 2020, arXiv:1911.03429](https://arxiv.org/abs/1911.03429), "ERASER: a benchmark to evaluate rationalized NLP models" (comprehensiveness)
* [Chen et al., 2020, arXiv:2006.16234](https://arxiv.org/abs/2006.16234), "True to the model or true to the data?"
* [Janzing et al., 2020, arXiv:1910.13413](https://arxiv.org/abs/1910.13413), "Feature relevance quantification in explainable AI: a causal problem"
* [McCloskey et al., 2019, doi:10.1073/pnas.1820657116](https://doi.org/10.1073/pnas.1820657116), "Using attribution to decode binding mechanism in neural network models for chemistry"
