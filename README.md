# TeachOpenCADD

A teaching platform for computer-aided drug design (CADD) using open source packages and data.

![TOC](https://img.shields.io/badge/Project-TeachOpenCADD-pink)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1486226.svg)](https://doi.org/10.5281/zenodo.1486226)

<!-- markdown-link-check-disable-next-line -->
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/volkamerlab/teachopencadd)
[![GH Actions CI ](https://github.com/volkamerlab/teachopencadd/workflows/CI/badge.svg)](https://github.com/volkamerlab/teachopencadd/actions?query=branch%3Amaster+workflow%3ACI)
[![GH Actions Docs](https://github.com/volkamerlab/teachopencadd/workflows/Docs/badge.svg)](https://projects.volkamerlab.org/teachopencadd/)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/teachopencadd/badges/downloads.svg)](https://anaconda.org/conda-forge/teachopencadd)

![GitHub closed pr](https://img.shields.io/github/issues-pr-closed-raw/volkamerlab/teachopencadd) ![GitHub open pr](https://img.shields.io/github/issues-pr-raw/volkamerlab/teachopencadd) ![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/volkamerlab/teachopencadd) ![GitHub open issues](https://img.shields.io/github/issues/volkamerlab/teachopencadd)

> If you use TeachOpenCADD in a publication,
> please [cite](https://projects.volkamerlab.org/teachopencadd/citation.html) us!
> If you use TeachOpenCADD in class, please include a link back to our repository.
<!-- markdown-link-check-disable-next-line -->
> In any case, please [star](https://docs.github.com/en/get-started/exploring-projects-on-github/saving-repositories-with-stars)
> (and tell your students to star) those repositories you consider useful for your learning/teaching activities.

## Description

<p align="center">
  <img src="docs/_static/images/TeachOpenCADD_topics.png" alt="TeachOpenCADD topics" width="800"/>
  <br>
  <font size="1">
  Figure adapted from Figure 1 in the TeachOpenCADD publication
  <a href="https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x">
  (D. Sydow <i>et al.</i>, J. Cheminformatics, 2019)</a>.
  </font>
</p>

Open source programming packages for cheminformatics and structural bioinformatics are powerful tools to build modular, reproducible, and reusable pipelines for computer-aided drug design (CADD). While documentation for such tools is available, only few freely accessible examples teach underlying concepts focused on CADD applications, addressing especially users new to the field.

TeachOpenCADD is a teaching platform developed by students for students, which provides teaching material for central CADD topics. Since we cover both the theoretical as well as practical aspect of these topics, the platform addresses students and researchers with a biological/chemical as well as a computational background.

Each topic is covered in an interactive Jupyter Notebook, using open source packages such as the Python packages `rdkit`, `pypdb`, `biopandas`, `nglview`, and `mdanalysis` (find the full list [here](https://projects.volkamerlab.org/teachopencadd/external_dependencies.html)). Topics are continuously expanded and open for contributions from the community. Beyond their teaching purpose, the TeachOpenCADD material can serve as starting point for users’ project-directed modifications and extensions.


**New edition**: we have extended the TeachOpenCADD platform with 6 notebooks introducing deep learning and its application to CADD related topics. 

## Get started

<!-- markdown-link-check-disable -->
[![GH Actions Docs](https://github.com/volkamerlab/teachopencadd/workflows/Docs/badge.svg)](https://projects.volkamerlab.org/teachopencadd/)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master)
<!-- markdown-link-check-enable -->

If you can't wait and just want to read through the materials, please go to the read-only version [here](https://projects.volkamerlab.org/teachopencadd/talktorials.html).

If you'd like to execute the provided notebooks, we offer two possibilities:

<!-- markdown-link-check-disable-next-line -->
- Online thanks to [Binder](https://mybinder.org/). This takes around 10 minutes to get ready, but does not require any kind of setup on your end. Click here to get started: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/volkamerlab/TeachOpenCADD/master). Once it has loaded, you can navigate to `teachopencadd/talktorials/` to find the executable notebooks.
- Locally using our `conda` package. More details in this [section of the documentation](https://projects.volkamerlab.org/teachopencadd/installing.html).

## TeachOpenCADD KNIME workflows

<!-- markdown-link-check-disable-next-line -->
[![DOI](https://img.shields.io/badge/DOI-10.1021%2Facs.jcim.9b00662-blue.svg)](https://pubs.acs.org/doi/10.1021/acs.jcim.9b00662)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3626897.svg)](https://doi.org/10.5281/zenodo.3626897)
[![KNIME Hub](https://img.shields.io/badge/KNIME%20Hub-TeachOpenCADD--KNIME-yellow.svg)](https://hub.knime.com/-/spaces/-/~xYhrR1mfFcGNxz7I/current-state/)

If you prefer to work in the context of a graphical interface, talktorials T001-T008 are also available as [KNIME workflows](https://hub.knime.com/-/spaces/-/~xYhrR1mfFcGNxz7I/current-state/). Questions regarding this version should be addressed using the "Discussion section" available at [this post](https://forum.knime.com/t/teachopencadd-knime/17174). You need to create a KNIME account to use the forum.

## About TeachOpenCADD

- [Contact](https://projects.volkamerlab.org/teachopencadd/contact.html)
- [Acknowledgments](https://projects.volkamerlab.org/teachopencadd/acknowledgments.html)
- [Citation](https://projects.volkamerlab.org/teachopencadd/citation.html)
- [License](https://projects.volkamerlab.org/teachopencadd/license.html)
- [Funding](https://projects.volkamerlab.org/teachopencadd/funding.html)


## External resources

Please refer to our TeachOpenCADD website to find a list of external resources:
- [External packages and webservices](https://projects.volkamerlab.org/teachopencadd/external_dependencies.html) that are used in the TeachOpenCADD material
- [Further reading material](https://projects.volkamerlab.org/teachopencadd/external_tutorials_collections.html) on Python programming, cheminformatics, structural bioinformatics, and more.
