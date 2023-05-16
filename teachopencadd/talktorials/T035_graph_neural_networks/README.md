# T035 · GNN-based molecular property prediction


**Note**: This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:
* Paula Linh Kramer, 2022, [Volkamer Lab](https://volkamerlab.org/), Saarland University


## Aim of this talktorial
In this tutorial, we will first explain the basic concepts of graph neural networks (GNNs) and present two different GNN architectures. We apply our neural networks to the `QM9` dataset, which is a dataset containing small molecules. With this dataset, we want to predict molecular properties. We demonstrate how to train and evaluate GNNs step by step using PyTorch Geometric.


### Contents in *Theory*

* GNN Tasks
* Message Passing
* Graph Convolutional Network (GCN)
* Graph Isomorphism Network (GIN)
* Training a GNN
* Applications of GNNs


### Contents in *Practical*

* Dataset
* Defining a GCN and GIN
* Training a GNN
* Evaluating the model


### References

* Articles:
    * Atz, Kenneth, Francesca Grisoni, and Gisbert Schneider. *Geometric Deep Learning on Molecular Representations*, [Nature Machine Intelligence 3.12 (2021): 1023-1032](https://arxiv.org/pdf/2107.12375.pdf)
    * Xu, Keyulu, Weihua Hu, Jure Leskovec, and Stefanie Jegelka. *How Powerful are Graph Neural Networks?*, [International Conference on Learning Representations (ICLR 2019)](https://arxiv.org/abs/1810.00826v3)
    * Welling, Max, and Thomas N. Kipf. *Semi-supervised classification with graph convolutional networks*, [International Conference on Learning Representations (ICLR 2017)](https://arxiv.org/pdf/1609.02907.pdf)
    * Gilmer, Justin, Samuel S. Schoenholz, Patrick F. Riley, Oriol Vinyals, and George E. Dahl. *Neural Message Passing for Quantum Chemistry*, [International conference on machine learning. PMLR, 2017](https://arxiv.org/pdf/1704.01212.pdf)


* Blog posts:
    * Maxime Labonne, *Graph Convolutional Networks: Introduction to GNNs*, [Maxime Labonne](https://mlabonne.github.io/blog/intrognn/)
    * Maxime Labonne, *GIN: How to Design the Most Powerful Graph Neural Network*, [Maxime Labonne](https://mlabonne.github.io/blog/gin/)
    * Vortana Say, *How To Save and Load Model In PyTorch With A Complete Example*, [towardsdatascience](https://towardsdatascience.com/how-to-save-and-load-a-model-in-pytorch-with-a-complete-example-c2920e617dee)
    * Michael Bronstein, *Expressive power of graph neural networks and the Weisfeiler-Lehman test*, [towardsdatascience](https://towardsdatascience.com/expressive-power-of-graph-neural-networks-and-the-weisefeiler-lehman-test-b883db3c7c49)
    * Benjamin Sanchez-Lengeling,  Emily Reif, *A Gentle Introduction to Graph Neural Networks*, [Distill](https://distill.pub/2021/gnn-intro/)


* Tutorials:
    * *Pytorch Geometric Documentation*, [Colab Notebooks and Video Tutorials](https://pytorch-geometric.readthedocs.io/en/latest/notes/colabs.html)
    * *Pytorch Geometric Documentation*, [Introduction by Example](https://pytorch-geometric.readthedocs.io/en/latest/notes/introduction.html#learning-methods-on-graphs)
