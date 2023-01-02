For contributors
================

You are welcome to contribute to the project either by requesting new topics, proposing ideas or
getting involved in the development!

- Engage with the maintainers and other TeachOpenCADD users in our `GitHub Discussions forum <https://github.com/volkamerlab/teachopencadd/discussions>`_!
- Submit new talktorials (see `Submitting new talktorials`_).
- Update existing talktorials by fixing bugs or extending the content (see `Updating talktorials`_).
- Help us maintain TeachOpenCADD (see `Maintaining talktorials`_).


Submitting new talktorials
--------------------------

This is a step-by-step guide on how to submit new talktorials.

1. Fork the repository: https://docs.github.com/en/get-started/quickstart/fork-a-repo

2. Ask us for your talktorial index (our notebooks are indexed with T001, T002, ...).

3. Clone your fork::

    git clone git@github.com:your-github-name/teachopencadd.git

4. Change into the cloned/downloaded ``teachopencadd`` folder::

    cd teachopencadd

5. Checkout a new branch with your initials, talktorial index, and talktorial short title (e.g. ``ab-t099-fingerprints``)::

    git checkout -b ab-t099-fingerprints

6. Create ``toc-dev`` environment::

    # Create environment with dependencies
    mamba env create -f devtools/test_env.yml -n toc-dev
    # On MacOS with M1 chip you may need
    CONDA_SUBDIR=osx-64 mamba env create -f devtools/test_env.yml -n toc-dev

    # Activate enviroment
    conda activate toc-dev

    # Pip install teachopencadd in editable mode
    cd ..
    pip install -e teachopencadd
    cd teachopencadd

    # Interact with the talktorials via e.g. Jupyter Lab
    jupyter lab

   If you add new dependencies to ``devtools/test_env.yml``, you will need to redo **step 6**.

7. Make a copy of the following template folder using your talktorial index and short name (example here is ``T099_fingerprints``::

    cp -r teachopencadd/talktorials/T000_template/ teachopencadd/talktorials/T099_fingerprints

8. Replace all instances of ``T000_template`` or "T000 · Talktorial topic title" with your talktorial index and title.

   a. ``T099_fingerprints/talktorial.ipynb`` is the talktorial template (`see the example here <https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T000_template/talktorial.ipynb>`_), within which you develope your new talktorial. Please read through the template before you start as it contains a lot of information about the content and style requirements.

   b. You do not need to worry about updating ``T099_fingerprints/README.md`` as we are autogenerating these READMEs with the first couple of sections of the notebook (see more details in `Maintaining talktorials`_).

   c. As the names suggest, the folders ``T099_fingerprints/data/`` and ``T099_fingerprints/images/`` can be used to store input/output data and images. Whenever possible, avoid adding files and instead fetch data/images by URL. Ask us if in doubt.

9. Push your new talktorial folder skeleton to your GitHub repository (replace ``T099_fingerprints`` and ``ab-t099-fingerprints`` with your own)::

    # Add folder
    git add teachopencadd/talktorials/T099_fingerprints/
    # Commit changes
    git commit -m "T099: Add talktorial folder skeleton"
    # Push changes
    git push origin ab-t099-fingerprints

10. Create the pull request (PR) with our PR template:

    a. Go to your fork ``https://github.com/your-github-name/teachopencadd/pulls`` and click "New pull request".

    b. Select the following:

       - ``base repository: volkamberlab/teachopencadd`` and ``base: master``

       - ``head repository: your-github-name/teachopencadd`` and ``compare: ab-t099-fingerprints``

    c. Click "Create pull request".

    d. When the PR description window opens, please copy-paste `the content of this PR template <https://github.com/volkamerlab/teachopencadd/blob/master/.github/PULL_REQUEST_TEMPLATE/talktorial_review.md>`_ into it.

11. Read through the PR description TODOs and check in with us if you have questions. Note: Many bullet points have to do with our maintenance efforts (see more details in `Maintaining talktorials`_).

12. Get started with developing your talktorials. Add your changes to the PR by following the procedure in **step 9**.

13. Ping us if you need help or are ready for the PR review. Thanks!


Updating talktorials
--------------------

This is a step-by-step guide on how to update existing talktorials.

If you find an error in a talktorial or wish to extend the content of one, please follow these steps (example: updating talktorial ``T002_compound_adme``):

1. Fork and clone the ``teachopencadd`` repository and checkout a new branch as described in  **steps 1-5** in `Submitting new talktorials`_, while **step 2** refers to the index of the talktorial you wish to update, e.g. ``T002_compound_adme``, and your new branch should be something descriptive like ``ab-t002-extend-adme-theory``.

3. Set up environment as described in **step 6** in `Submitting new talktorials`_.

2. Push your new branch to your GitHub repository (replace ``T002_compound_adme`` and ``ab-t002-extend-adme-theory`` with your own)::

    # Add folder
    git add teachopencadd/talktorials/T002_compound_adme/
    # Commit changes
    git commit -m "T002: Extend ADME theory"
    # Push changes
    git push origin ab-t002-extend-adme-theory

3. Create PR as described in **steps 10 and 11** in `Submitting new talktorials`_. Some PR bullet points might not apply to your case, please use ``~`` (e.g. ``~some bullet point~``) to strike those through.

4. Ping us if you need help or are ready for the PR review. Thanks!


Maintaining talktorials
-----------------------

This is an overview about our TeachOpenCADD maintenance efforts.

- Our `environment file <https://github.com/volkamerlab/teachopencadd/tree/master/devtools>`_ satisfies the dependencies for all TeachOpenCADD talktorials. This format might change in the future as discussed `here <https://github.com/volkamerlab/teachopencadd/discussions/277>`_.

- Our `GitHub Actions CI setup file <https://github.com/volkamerlab/teachopencadd/blob/master/.github/workflows/ci.yml>`_ contains:

  - Notebook tests (``pytest``), which check if the notebook runs without errors and if cells flagged with ``# NBVAL_CHECK_OUTPUT`` produce the same output in the CI run as saved within the ``talktorial.ipynb`` file. Check under ``jobs.test`` the tested operating systems and Python versions.

  - Notebook formatting (``black-nb``), check under ``jobs.format``::

        # Apply formatting to all talktorials
        black-nb -l 99 teachopencadd/talktorials/T*/talktorial.ipynb

  - Autogenerated READMEs, check under ``jobs.readmes``::

        # Autogenerate all talktorials' README
        for path in teachopencadd/talktorials/T*/talktorial.ipynb; do
            python devtools/regenerate_readmes.py --output README.md $path
        done

- Our `TeachOpenCADD website <https://projects.volkamerlab.org/teachopencadd/>`_:

  - You can render the website locally (including your changes) as described in `our documentation README <https://github.com/volkamerlab/teachopencadd/blob/master/docs/README.md>`_.

  - Please follow `these steps <https://github.com/volkamerlab/teachopencadd/blob/master/.github/PULL_REQUEST_TEMPLATE/talktorial_review.md#website>`_ if you wish to add new content.

- We are cutting new releases as described in this `Discussion entry <https://github.com/volkamerlab/teachopencadd/discussions/197>`_.

- Our ``teachopencadd`` package lives with ``conda-forge``: https://anaconda.org/conda-forge/teachopencadd

  - Whenever we cut a new GitHub release, we have to also cut a new ``conda`` release.

  - Refer to `"Maintaining packages" <https://conda-forge.org/docs/maintainer/updating_pkgs.html>`_  and `these notes <https://github.com/volkamerlab/teachopencadd/discussions/184>`_ for instructions on how to do this and ask @dominiquesydow for help. In order to cut a new ``conda`` release, you will need to update the recipe within our `teachopencadd feedstock <https://github.com/conda-forge/teachopencadd-feedstock>`_.




