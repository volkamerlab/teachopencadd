# T037 · An introduction to $\text{E}(3)$-invariant graph neural networks

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Joschka Groß, 2022, Chair for Modelling and Simulation, Saarland University

## Aim of this talktorial

This talktorial is supposed to serve as an introduction to machine learning on point cloud representations of molecules with 3D conformer information, i.e., molecular graphs that are embedded into euclidean space (see **Talktorial 033**). You will learn why euclidean equivariance and invariance are important properties of neural networks (NNs) that take point clouds as input and learn how to implement and train such NNs. In addition to discussing them in theory, this notebook also aims to demonstrate the shortcomings of plain graph neural networks (GNNs) when working with point clouds practically.

### Contents in *Theory*

* Why 3D coordinates?
* Representing molecules as point clouds
* Equivariance and invariance in euclidean space and why we care
* How to construct $\text{E}(n)$-invariant and equivariant models
* The QM9 dataset

### Contents in *Practical*

* Visualization of point clouds
* Set up and inspect the QM9 dataset
  * Preprocessing
  * Atomic number distribution and point cloud size
  * Data split, distribution of regression target electronic spatial extent
* Model implementation
  * Plain "naive euclidean" GNN
  * Demo: Plain GNNs are not E(3)-invariant
  * EGNN model
  * Demo: Our EGNN is E(3)-invariant
* Training and evaluation
  * Setup
  * Training the EGNN
  * Training the plain GNN
  * Comparative evaluation

### References

#### Theoretical
* **Quantum chemistry structures and properties of 134k molecules (QM9)**: [<i>Scientific data</i> (2014)](https://www.nature.com/articles/sdata201422/?ref=https://githubhelp.com)
* **MoleculeNet: a benchmark for molecular machine learning**: [<i>Chem. Sci.</i>, 2018, <b>9</b>, 513-530](https://pubs.rsc.org/en/content/articlehtml/2018/sc/c7sc02664a)
* **$\text{E}(n)$ Equivariant Graph Neural Networks**: [<i>International conference on machine learning</i> (2021), <b>139</b>, 99323-9332](https://proceedings.mlr.press/v139/satorras21a.html)
* **SE(3)-transformers: 3D roto-translation equivariant attention networks**: [<i>Advances in Neural Information Processing Systems</i> (2021), <b>33</b>, 1970-1981](https://proceedings.neurips.cc/paper/2020/file/15231a7ce4ba789d13b722cc5c955834-Paper.pdf)
* **TorchMD-NET: Equivariant Transformers for Neural Network based Molecular Potentials**: [<i>arXiv preprint (2022)</i>](https://arxiv.org/abs/2202.02541)
* **DiffDock**: [<i> arXiv preprint</i> (2022)](https://arxiv.org/abs/2210.01776)

#### Practical
* [Pytorch Geometric QM9 version](https://pytorch-geometric.readthedocs.io/en/latest/modules/datasets.html#torch_geometric.datasets.QM9)
