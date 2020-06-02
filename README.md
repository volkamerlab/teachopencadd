# TeachOpenCADD

#### A teaching platform for computer-aided drug design (CADD) using open source packages and data

Volkamer Lab 

*In Silico* Toxicology and Structural Bioinformatics <br>
Institute of Physiology <br>
Charité - Universitätsmedizin Berlin <br>
[volkamerlab.org](https://physiologie-ccm.charite.de/en/research_at_the_institute/volkamer_lab/)

[![DOI](https://img.shields.io/badge/DOI-10.1186%2Fs13321--019--0351--x-blue.svg)](https://doi.org/10.1186/s13321-019-0351-x)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2600909.svg)](https://doi.org/10.5281/zenodo.2600909)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)

If you use TeachOpenCADD in a publication, 
please  [cite](https://github.com/volkamerlab/TeachOpenCADD/blob/master/README.md#citation) us! 
If you use TeachOpenCADD in class, please include a link back to our repository. 
In any case, please [star](https://help.github.com/en/github/getting-started-with-github/saving-repositories-with-stars) 
(and tell your students to star) those repositories you consider useful for your learning/teaching activities.

## Table of contents  

* [Objective](#objective)
* [Topics](#topics)
* [Usage](#usage)
* [Contact](#contact)
* [License](#license)
* [Citation](#citation)
* [Funding](#funding)

## Objective

(Back to [Table of contents](#table-of-contents).)

Open source programming packages for cheminformatics and structural bioinformatics are powerful tools to build modular, 
reproducible, and reusable pipelines for computer-aided drug design (CADD). 
While documentation for such tools is available, only few freely accessible examples teach underlying concepts focused on 
CADD applications such as the TDT initiative [1], addressing especially users new to the field.

TeachOpenCADD [2] is a teaching platform developed by students for students, which provides teaching material for 
central CADD topics. Since we cover both the theoretical as well as practical aspect of these 
topics, the platform addresses students and researchers with a biological/chemical as well as a computational background.

For each topic, an interactive Jupyter Notebook [3] was developed, using open source packages such as the 
Python packages RDKit [4], PyPDB [5], and PyMol [6]. Additionally, we offer topics 1-8 in the form of KNIME workflows 
[7], which allow to perform the same tasks using a graphical user interface instead of coding.

With this platform, we aim to introduce interested users to the ease and benefit of using open source tools for 
cheminformatics and structural bioinformatics.
Topics will be continuously expanded and are open for contributions from the community. 
Beyond their teaching purpose, the TeachOpenCADD material can serve as starting point for 
users’ project-directed modifications and extensions. 

[1] [S. Riniker et al., F1000Research, 2017, 6, 1136](https://f1000research.com/articles/6-1136/v1) <br>
[2] [D. Sydow et al., J Chem, 2019, 11, 29](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x) <br>
[3] [T. Kluyver et al., IOS Press, 2016, 87-90.](http://ebooks.iospress.com/publication/42900) <br>
[4] [G. Landrum, RDKit](http://www.rdkit.org) <br>
[5] [W. Gilpin, Bioinform, 2016, 32, 156-60](https://academic.oup.com/bioinformatics/article/32/1/159/1743800) <br>
[6] [The PyMOL Molecular Graphics System, Version 1.8, Schrödinger, LLC](https://pymol.org) <br>
[7] [A. Fillbrunn et al., J Biotechnol, 2017, 261, 149–156](https://www.sciencedirect.com/science/article/pii/S0168165617315651)

## Topics

(Back to [Table of contents](#table-of-contents).)

<p align="center">
  <img src="README_figures/TeachOpenCADD_topics.svg" alt="TeachOpenCADD topics" width="800"/>
  <br>
  <font size="1">
  Figure adapted from Figure 1 in the TeachOpenCADD publication,
  <a href="https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x">
  D. Sydow et al., J Chem, 2019, 11, 29</a>.
  </font>
</p>


TeachOpenCADD offers teaching material on common tasks in computer-aided drug design. 
Currently, the following topics are available:

**Cheminformatics**

* Topic 1. Compound data acquisition: ChEMBL
* Topic 2. Molecular filtering: ADME and lead-likeness criteria
* Topic 3. Molecular filtering: Unwanted substructures
* Topic 4. Ligand-based screening: Compound similarity
* Topic 5. Compound clustering
* Topic 6. Maximum common substructures
* Topic 7. Ligand-based screening: Machine learning
   
**Structural bioinformatics**

* Topic 8. Protein data acquisition: Protein Data Bank (PDB)
* Topic 9. Ligand-based pharmacophores
* Topic 10. Binding site similarity
* Topic 11. Structure-based CADD using online APIs/servers
  * 11a. Querying KLIFS & PubChem for potential kinase inhibitors
  * 11b. Docking the candidates against the target 
  * 11c. Visualizing the results and comparing against known data


The teaching material is offered in the following formats: 
* Coding-based *Jupyter Notebooks* (topics 1-11) here on GitHub, so called *talktorials* (talk + tutorial), i.e. tutorials that can also be used in presentations
* GUI-based *KNIME workflows* (topics 1-8) on the [KNIME Hub](https://hub.knime.com/volkamerlab/space/TeachOpenCADD/TeachOpenCADD)

## Usage

(Back to [Table of contents](#table-of-contents).)

You can use Binder to host the repository and all needed dependencies, or 
you can use our talktorials locally (download repository and install dependencies).


### Use Binder (for talktorials T1-T8)

Use binder to host the repository and all needed dependencies by following this link:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)

The setup will take a few minutes.

### Install locally (for all talktorials)

#### Linux

1.  Get your local copy of the TeachOpenCADD repository (including the talktorials) by

    a. ... either downloading it as zip archive and unzipping it: 
    
    ![Download repository](https://github.com/volkamerlab/TeachOpenCADD/blob/master/README_figures/download_repo.png)
   
    b. ... or cloning it to your computer using the package `git`:

        ```bash
        git clone https://github.com/volkamerlab/TeachOpenCADD.git
        ```
        
2.  Use the Anaconda software for a clean package version management. 
   
    Install Anaconda2 or Anaconda3. In theory, it should not matter which Anaconda version you install. However, we only tested it for Anaconda2, so we cannot guarantee the same behaviour for Anaconda3.

    https://docs.anaconda.com/anaconda/install/

3.  Use the package management system conda to create an environment (called `teachopencadd`) for the talktorials. 
   
    We provide an environment file (yml file) containing all required packages.

    ```bash
    conda env create -f environment.yml
    ```

    Note: You can also create this environment manually. 
    Check ["Alternatively create conda environment manually"](#Alternatively-create-conda-environment-manually) for this.

4.  Activate the conda environment.
    
    ```bash
    conda activate teachopencadd
    ```
    
    Now you can work within the conda environment. 
    
5.  Link the conda environment to the Jupyter notebook.
    
    ```bash
    python -m ipykernel install --user --name teachopencadd
    
    # FYI, uninstall this link again with this command:
    #jupyter kernelspec uninstall teachopencadd
    ``` 

6.  Start the Jupyter notebook.

    ```bash
    jupyter notebook
    ```
    
7.  Change the Jupyter kernel to the conda environment via the menu:

    `Kernel > Change kernel > teachopencadd`
    
    ![Change Jupyter kernel](https://github.com/volkamerlab/TeachOpenCADD/blob/master/README_figures/jupyter_kernel_teachopencadd.png)
    
8.  Now you can get started with your first talktorial. Enjoy!



##### Alternatively create conda environment manually

**Note**: This is the alternative to creating the conda environment using the yml file as described in step 3 above. 

```bash
# Create and activate an environment called `teachopencadd`
conda create -n teachopencadd python=3.6
conda activate teachopencadd

# Install packages via conda
conda install jupyter  # Installs also ipykernel
conda install -c conda-forge rdkit  # Installs also numpy and pandas
conda install -c samoturk pymol  # Linux: Installs also freeglut and glew
conda install -c conda-forge pmw  # Necessary for PyMol terminal window to pop up
conda install -c conda-forge scikit-learn  # Installs also scipy
conda install -c conda-forge seaborn  # Installs also matplotlib
conda install -c conda-forge chembl_webresource_client
conda install -c conda-forge biopandas
conda install -c conda-forge pypdb
```

#### Windows

Generally, the installation works the same under Linux and Windows without problems.

The only difference, we encountered, is the installation of PyMol:

* Download PyMol from http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymol 
* Put it where Anaconda2 is installed (e.g. C:\Anaconda2)
* Open a command prompt as administrator (Windows > accessories > command prompt, "right-click" > open as administrator)
* Go to the Anaconda directory by typing the correct path on the prompt:

```bash
cd C:/Anaconda2
set path=%path%;C:\Anaconda2
pip install pymol‑2.3.0a0‑cp36‑cp36m‑win_amd64.whl
pip install pymol_launcher‑2.1‑cp36‑cp36m‑win_amd64.whl
# or whatever pymol_XXXX.whl you have downloaded
```
#### MacOS

The installation works the same as under Linux, however we could not install `pymol` from the open source `samoturk` conda channel. You can use the `schrodinger` channel. Unfortunately a Schrödinger license is needed to run PyMOL (the license is free for academic use).

For the installation done manually, replace the command:

```
conda install -c samoturk pymol  # Installs also freeglut and glew
```

with the following

```
conda install -c schrodinger pymol  # Installs also freeglut and glew
```

## Contact
(Back to [Table of contents](#table-of-contents).)

Please contact us if you have questions or suggestions!

* If you have questions regarding our Jupyter Notebooks, please open an issue on our GitHub repository: https://github.com/volkamerlab/teachopencadd/issues
* If you have questions regarding our KNIME workflows, please make a post on our KNIME Hub page in the "Discussion" section: https://hub.knime.com/volkamerlab/space/TeachOpenCADD/TeachOpenCADD
* If you have ideas for new topics, please fill out our questionnaire: [contribute.volkamerlab.org](contribute.volkamerlab.org)
* For all other requests, please send us an email: teachopencadd@charite.de

We are looking forward to hearing from you!


## License
(Back to [Table of contents](#table-of-contents).)

This work is licensed under the Attribution 4.0 International (CC BY 4.0).
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.


## Citation
(Back to [Table of contents](#table-of-contents).)

If you make use of the TeachOpenCADD material in scientific publications, please cite our respective articles:
* [TeachOpenCADD Jupyter Notebooks: Talktorials 1-10](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x). 
* [TeachOpenCADD KNIME workflows](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00662)

It will help measure the impact of the TeachOpenCADD platform and future funding!

```
@article{TeachOpenCADD2019,
    author = {Sydow, Dominique and Morger, Andrea and Driller, Maximilian and Volkamer, Andrea},
    title = {{TeachOpenCADD: a teaching platform for computer-aided drug design using open source packages and data}},
    doi = {10.1186/s13321-019-0351-x},
    url = {https://doi.org/10.1186/s13321-019-0351-x},
    journal = {J. Cheminform.},
    volume = {11},
    number = {1},
    pages = {29},
    year = {2019}
}

@article{TeachOpenCADDKNIME2019,
    author = {Sydow, Dominique and Wichmann, Michele and Rodríguez-Guerra, Jaime and Goldmann, Daria and Landrum, Gregory and Volkamer, Andrea},
    title = {{TeachOpenCADD-KNIME: A Teaching Platform for Computer-Aided Drug Design Using KNIME Workflows}},
    doi = {10.1021/acs.jcim.9b00662},
    url = {https://doi.org/10.1021/acs.jcim.9b00662},
    journal = {Journal of Chemical Information and Modeling},
    volume = {59},
    number = {10},
    pages = {4083-4086},
    year = {2019}
}
```

## Funding
(Back to [Table of contents](#table-of-contents).)

The authors of the TeachOpenCADD platform receive(d) public funding from the following funding agencies:
* Bundesministerium für Bildung und Forschung (Grant Number 031A262C) 
* Deutsche Forschungsgemeinschaft (Grant number VO 2353/1-1)
* HaVo-Stiftung, Ludwigshafen, Germany
* Stiftung Charité (Einstein BIH Visiting Fellow project)
* "SUPPORT für die Lehre" program (Förderung innovativer Lehrvorhaben) of the Freie Universität Berlin
* Open Access Publication Fund of Charité – Universitätsmedizin Berlin