.. teachopencadd documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TeachOpenCADD
=============

   This website is free and open to all users and there is no login requirement!

Open source programming packages for cheminformatics and structural bioinformatics are powerful tools to build modular, reproducible, and reusable pipelines for computer-aided drug design (CADD). While documentation for such tools is available, only few freely accessible examples teach underlying concepts focused on CADD applications, addressing especially users new to the field.

TeachOpenCADD is a teaching platform developed by students for students, which provides teaching material for central CADD topics. Since we cover both the theoretical as well as practical aspect of these topics, the platform addresses students and researchers with a biological/chemical as well as a computational background.

For each topic, an interactive Jupyter Notebook is offered, using open source packages such as the Python packages ``rdkit``, ``pypdb``, ``biopandas``, ``nglview``, and ``mdanalysis``. Topics are continuously expanded and open for contributions from the community. Beyond their teaching purpose, the TeachOpenCADD material can serve as starting point for users’ project-directed modifications and extensions.

.. raw:: html

   <p align="center">
   <img src="_static/images/TeachOpenCADD_topics.png" alt="TeachOpenCADD topics" width="800"/>
   <br>
   <font size="1">
   Figure adapted from Figure 1 in the TeachOpenCADD publication 
   <a href="https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x">
   (D. Sydow <i>et al.</i>, J. Cheminformatics, 2019)</a>.
   </font>
   </p>

Table of contents
-----------------

.. toctree::
   :maxdepth: 1
   :caption: Our talktorials

   all_talktorials
   talktorials

.. toctree::
   :maxdepth: 1
   :caption: Run locally

   installing

.. toctree::
   :maxdepth: 1
   :caption: Contributors

   contribute
   api

.. toctree::
   :maxdepth: 1
   :caption: External resources

   external_dependencies
   external_tutorials_collections


Citation
--------

If you make use of the TeachOpenCADD material in scientific publications, please cite our respective articles:

- `TeachOpenCADD Jupyter Notebooks: Talktorials T001-T010 <https://jcheminf.biomedcentral.com/articles/10.1186/s13321-019-0351-x>`_
- `TeachOpenCADD KNIME workflows <https://pubs.acs.org/doi/10.1021/acs.jcim.9b00662>`_
- `How to use the TeachOpenCADD material for teaching? <https://pubs.acs.org/doi/abs/10.1021/bk-2021-1387.ch010>`_

It will help measure the impact of the TeachOpenCADD platform and future funding!

.. code-block::

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

   @inbook{doi:10.1021/bk-2021-1387.ch010,
      author = {Sydow, Dominique and Rodríguez-Guerra, Jaime and Volkamer, Andrea},
      title = {Teaching Computer-Aided Drug Design Using TeachOpenCADD},
      booktitle = {Teaching Programming across the Chemistry Curriculum},
      chapter = {10},
      pages = {135-158},
      doi = {10.1021/bk-2021-1387.ch010},
      URL = {https://pubs.acs.org/doi/abs/10.1021/bk-2021-1387.ch010},
   }


Funding
-------

Volkamer Lab's projects are supported by several public funding sources
(for more info see our `webpage <https://volkamerlab.org/>`_).


License
-------

This work is licensed under the `Attribution 4.0 International (CC BY 4.0) <http://creativecommons.org/licenses/by/4.0/>`_.
