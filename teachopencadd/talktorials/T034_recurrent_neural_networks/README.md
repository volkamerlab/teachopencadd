# T034 · RNN-based molecular property prediction

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Azat Tagirdzhanov, 2022, [Chair for Clinical Bioinformatics](https://www.ccb.uni-saarland.de/), member of the [NextAID](https://nextaid.cs.uni-saarland.de/) project, Saarland University


## Aim of this talktorial

Molecular representation by a SMILES string paved the way for applying natural language processing techniques to a broad range of molecule-related tasks. In this talktorial we will dive deeper into one of these techniques: recurrent neural networks (RNNs). First, we will describe different RNN architectures and then apply them to a regression task using the QM9 dataset.


### Contents in *Theory*

* Molecules as text
    * Tokenization and one-hot encoding
* Recurrent Neural Networks (RNNs)
    * Vanilla RNN
    * Training an RNN
    * Vanishing gradients
    * Gated Recurrent Unit


### Contents in *Practical*

* Dataset
* Model definition
* Training
* Evaluation


### References

#### Talktorials
* __Talktorial T021__: One-Hot Encoding
* __Talktorial T022__: Ligand-based screening: neural networks
* __Talktorial T033__: Molecular Representations
* __Talktorial T034__: GNN based property prediction


#### Theoretical background
* Michael Phi, <i>Illustrated Guide to Recurrent Neural Networks</i>, [towardsdatascience](https://towardsdatascience.com/illustrated-guide-to-recurrent-neural-networks-79e5eb8049c9)
* Michael Phi, <i>Illustrated Guide to LSTM’s and GRU’s: A step by-step explanation</i>, [towardsdatascience](https://towardsdatascience.com/illustrated-guide-to-lstms-and-gru-s-a-step-by-step-explanation-44e9eb85bf21)
* [Modern Recurrent Neural Networks](https://d2l.ai/chapter_recurrent-modern/index.html), <i>D2L.ai: Interactive Deep Learning Book with Multi-Framework Code, Math, and Discussions</i>
* Denny Britz, <i>Recurrent Neural Networks Tutorial</i>, [dennybritz.com](https://dennybritz.com/posts/wildml/recurrent-neural-networks-tutorial-part-1/)
* Andrej Karpathy, <i>The Unreasonable Effectiveness of Recurrent Neural Networks</i>, [Andrej Karpathy blog](https://karpathy.github.io/2015/05/21/rnn-effectiveness/)
