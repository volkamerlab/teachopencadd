# T021 · One-Hot Encoding

Developed in the CADD seminar 2020, Volkamer Lab, Charité/FU Berlin 

**Note:** This talktorial is a part of TeachOpenCADD, a platform that aims to teach domain-specific skills and to provide pipeline templates as starting points for research projects.

Authors:

- Sakshi Misra, CADD seminar 2020, Charité/FU Berlin
- Talia B. Kimber, 2020, [Volkamer lab](https://volkamerlab.org), Charité
- Yonghui Chen, 2020, [Volkamer lab](https://volkamerlab.org), Charité
- Andrea Volkamer, 2020, [Volkamer lab](https://volkamerlab.org), Charité


## Aim of this talktorial

The aim of the talktorial is to perform one-hot encoding of SMILES structures on a subset of the ChEMBL data set to gain a deeper understanding on the one-hot encoding concept and why it is useful as a pre-processing step in various machine learning algorithms.


### Contents in *Theory*

- Molecular data and representation
    - ChEMBL database
    - SMILES structures and rules
- What is categorical data?
     - What is the problem with categorical data?
     - How to convert categorical data to numerical data?
- The One-Hot Encoding (OHE) concept
     - Why using one-hot encoding?
     - Example of one-hot encoding
     - Advantages and disadvantages of one-hot encoding
- Similar: Integer or label encoding
- What is *padding*?
- Further readings


### Contents in *Practical*

- Import necessary packages
- Read the input data
- Process the data
     - Double digit replacement
     - Compute longest (& shortest) SMILES
- Python one-hot encoding implementation
     - One-hot encode (padding=True)
     - Visualization
          - Shortest SMILES
          - Longest SMILES 
- Supplementary material
   - Scikit learn implementation
   - Keras implementation


## References

- Theoretical background:
     - ChEMBL database: "The ChEMBL bioactivity database: an update." ([<i>Nucleic acids research<i> (2014), <b>42.D1</b>, D1083-D1090](https://doi.org/10.1093/nar/gkt1031))
     - Allen Chieng Hoon Choong, Nung Kion Lee, "*Evaluation of Convolutionary Neural Networks Modeling of DNA Sequences using Ordinal versus one-hot Encoding Method*", [bioRxiv, October 25, 2017](https://doi.org/10.1101/186965).
     - Patricio Cerda, Gael Varoquaux, "*Encoding high-cardinality string categorical variables*", [arXiv:1907, 18 May 2020](https://arxiv.org/pdf/1907.01860v5.pdf).
     - Blogpost: Jason Brownlee, *How to One Hot Encode Sequence Data in Python*, [Machine Learning Mastery, accessed November 9th, 2020](https://machinelearningmastery.com/how-to-one-hot-encode-sequence-data-in-python/).
     - Blogpost: Krishna Kumar Mahto, *One-Hot-Encoding, Multicollinearity and the Dummy Variable Trap*, towardsdatascience, Available from [one-hot-encoding-multicollinearity](https://towardsdatascience.com/one-hot-encoding-multicollinearity-and-the-dummy-variable-trap-b5840be3c41a/), accessed July 8th, 2019.
     - Blogpost: Chris, *What is padding in a neural network?*, MachineCurve, [Padding](https://www.machinecurve.com/index.php/2020/02/07/what-is-padding-in-a-neural-network/#:~:text=Padding%20avoids%20the%20loss%20of%20spatial%20dimensions,-Sometimes%2C%20however%2C%20you&text=You%20need%20the%20output%20images,in%20order%20to%20generate%20them.) section, accessed February 7th, 2020
     

- Packages and functions:
     - [**RDKit**](https://www.rdkit.org/docs/GettingStartedInPython.html): Greg Landrum,  *RDKit Documentation*, [PDF](https://buildmedia.readthedocs.org/media/pdf/rdkit/latest/rdkit.pdf), Release on 2019.09.1.
     - [**Scikit-learn**](https://scikit-learn.org/stable/): 
        - [Scikit-learn: Machine Learning in Python](https://jmlr.csail.mit.edu/papers/v12/pedregosa11a.html), Pedregosa *et al.*, JMLR 12, pp. 2825-2830, 2011.
        - Jiangang Hao, et al. "A Review of Scikit-learn Package in Python Programming Language." [*Journal of Education and Behavioral Statistics* **Volume: 44 issue: 3** (2019), page(s): 348-361](https://doi.org/10.3102/1076998619832248)
     - [**Keras**](https://keras.io/): Book chapter: "An Introduction to Deep Learning and Keras" in [*Learn Keras for Deep Neural Networks* (2019), **page(s):1-16**](https://doi.org/10.1007/978-1-4842-4240-7).
     - [**Matplotlib**](https://matplotlib.org/)
     - `smiles encoder` function: Blogpost by iwatobipen, *encode and decode SMILES strings* , [Wordpress, accessed November 9th, 2020](https://iwatobipen.wordpress.com/2017/01/22/encode-and-decode-smiles-strings/)
