# TeachOpenCADD

[![DOI](https://img.shields.io/badge/DOI-10.1186%2Fs13321--019--0351--x-blue.svg)](https://doi.org/10.1186/s13321-019-0351-x)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.2600909.svg)](https://doi.org/10.5281/zenodo.2600909)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)

> If you use TeachOpenCADD in a publication,
> please [cite](https://github.com/volkamerlab/TeachOpenCADD/blob/master/README.md#citation) us!
> If you use TeachOpenCADD in class, please include a link back to our repository.
> In any case, please [star](https://help.github.com/en/github/getting-started-with-github/saving-repositories-with-stars)
> (and tell your students to star) those repositories you consider useful for your learning/teaching activities.

Open source programming packages for cheminformatics and structural bioinformatics are powerful tools to build modular, reproducible, and reusable pipelines for computer-aided drug design (CADD). While documentation for such tools is available, only few freely accessible examples teach underlying concepts focused on CADD applications, addressing especially users new to the field.

TeachOpenCADD is a teaching platform developed by students for students, which provides teaching material for central CADD topics. Since we cover both the theoretical as well as practical aspect of these topics, the platform addresses students and researchers with a biological/chemical as well as a computational background.

For each topic, an interactive Jupyter Notebook is offered, using open source packages such as the Python packages `rdkit`, `pypdb`, `biopandas`, `nglview`, and `mdanalysis`. Topics are continuously expanded and open for contributions from the community. Beyond their teaching purpose, the TeachOpenCADD material can serve as starting point for users’ project-directed modifications and extensions.

<p align="center">
  <img src="docs/_static/images/TeachOpenCADD_topics.svg" alt="TeachOpenCADD topics" width="800"/>
  <br>
  <font size="1">
  Figure adapted from Figure 1 in the TeachOpenCADD publication 
  <a href="https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x">
  (D. Sydow <i>et al.</i>, J. Cheminformatics, 2019)</a>.
  </font>
</p>

## Get started

If you can't wait and just want to read through the materials, please go to the read-only version [here](https://projects.volkamerlab.org/teachopencadd/talktorials.html).

If you'd like to execute the provided notebooks, we offer two possibilities:

- 🚧 Online thanks to [Binder](https://mybinder.org/). This takes some minutes, but does not require any kind of setup on your end. Click here to get started: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)
- Locally using our `conda` package. More details in this [section of the documentation](https://projects.volkamerlab.org/teachopencadd/installing.html).

## TeachOpenCADD KNIME workflows

[![DOI](https://img.shields.io/badge/DOI-10.1021%2Facs.jcim.9b00662-blue.svg)](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00662)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3626897.svg)](https://doi.org/10.5281/zenodo.3626897)
[![KNIME Hub](https://img.shields.io/badge/KNIME%20Hub-TeachOpenCADD--KNIME-yellow.svg)](https://hub.knime.com/volkamerlab/spaces/Public/latest/TeachOpenCADD/TeachOpenCADD)

If you prefer to work in the context of a graphical interface, talktorials T001-T008 are also available as [KNIME workflows](https://hub.knime.com/volkamerlab/space/TeachOpenCADD/TeachOpenCADD). Questions regarding this version should be addressed using the "Discussion section" available at [this post](https://forum.knime.com/t/teachopencadd-knime/17174). You might need to create a KNIME account.

## Contact

Please contact us if you have questions or suggestions!

- If you have questions regarding our Jupyter Notebooks, please [open an issue](https://github.com/volkamerlab/teachopencadd/issues) on our GitHub repository.
- If you have ideas for new topics, please fill out our questionnaire: [contribute.volkamerlab.org](http://contribute.volkamerlab.org)
- For all other requests, please send us an email: teachopencadd@charite.de

We are looking forward to hearing from you!

## License

This work is licensed under the Attribution 4.0 International (CC BY 4.0).
To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/.

## Citation

If you make use of the TeachOpenCADD material in scientific publications, please cite our respective articles:

- [TeachOpenCADD Jupyter Notebooks: Talktorials T001-T010](https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x)
- [TeachOpenCADD KNIME workflows](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00662)

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

## Acknowledgments

### External resources

#### Python packages

TODO: Select from `test_env.yml`...

#### Databases

- ChEMBL 
  - Bioactivity database: [Gaulton *et al.*, <i>Nucleic Acids Res.</i> (2017), 45(Database issue), D945–D954](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5210557/)
  - Web services: [Davies *et al.*, <i>Nucleic Acids Res.</i> (2015), <b>43</b>, 612-620](https://academic.oup.com/nar/article/43/W1/W612/2467881) 
- PDB
- KLIFS
- PubMed

### Funding

The authors of the TeachOpenCADD platform receive(d) public funding from the following funding agencies:

- Bundesministerium für Bildung und Forschung (Grant Number 031A262C)
- Deutsche Forschungsgemeinschaft (Grant number VO 2353/1-1)
- HaVo-Stiftung, Ludwigshafen, Germany
- Stiftung Charité (Einstein BIH Visiting Fellow project)
- "SUPPORT für die Lehre" program (Förderung innovativer Lehrvorhaben) of the Freie Universität Berlin
- Open Access Publication Fund of Charité – Universitätsmedizin Berlin

### Contributors

Many thanks to everyone who has contributed in any way to TeachOpenCADD (listed alphabetically).

- Andrea Morger
- Andrea Volkamer
- Andrew Wilkinson
- Angelika Szengel
- Anja Georgi
- Calvinna Caswara
- Daria Goldmann
- David Schaller
- Dominique Sydow
- Florian Gusewski
- Floriane Montanari
- Franziska Fritz
- Gizem Spriewald
- Gregory Landrum
- Jacob Gora
- Jaime Rodríguez-Guerra
- Jan Philipp Albrecht
- Jeff Wagner
- Majid Vafadar
- Mareike Leja
- Marvis Sydow
- Mathias Wajnberg
- Maximilian Driller
- Michele Wichmann
- Oliver Nagel
- Paula Schmiel
- Pratik Dhakal
- Richard Gowers
- Ross Johnstone
- Sakshi Misra
- Sandra Krüger
- Svetlana Leng
- Talia Kimber
- Thomas Holder
- Yonghui Chen
