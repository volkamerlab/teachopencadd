Acknowledgments
===============

TeachOpenCADD has been initiated by the members of `Volkamer Lab <https://volkamerlab.org/>`_,
Charité - Universitätsmedizin Berlin, with special thanks to
`@dominiquesydow <https://github.com/dominiquesydow/>`_,
`@jaimergp <https://github.com/jaimergp/>`_ and
`@AndreaVolkamer <https://github.com/andreavolkamer>`_.
The platform has been filled with life by our students from the CADD courses taught in the
bioinformatics program at Freie Universität Berlin.

Many thanks to everyone who has contributed and is contributing to TeachOpenCADD
by working on talktorials (check out the talktorial READMEs for author information)
and/or by helping in any other way
(see `GitHub contributors <https://github.com/volkamerlab/teachopencadd/graphs/contributors>`_).

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

1. Fork the repository: https://docs.github.com/en/get-started/quickstart/fork-a-repo

2. Ask us for your talktorial index (our notebooks are indexed with T001, T002, ...)

3. Clone your fork::

    git clone git@github.com:your-github-name/teachopencadd.git

4. Change into the cloned/downloaded `teachopencadd` folder::

    cd teachopencadd

5. Checkout a new branch with your initials, talktorial index, and talktorial short title (e.g. ``ab-t099-fingerprints``)::

    git checkout -b ab-t099-fingerprints

6. Make a copy of the following template folder using your talktorial index and short name (example here is ``T099_fingerprints``::

    cp -r teachopencadd/talktorials/T000_template/ teachopencadd/talktorials/T099_fingerprints

7. Replace all instances of ``T000_template`` or "T000 · Talktorial topic title" with your talktorial index and title.

  - ``T099_fingerprints/talktorial.ipynb`` is the talktorial template (`see the example here <https://github.com/volkamerlab/teachopencadd/blob/master/teachopencadd/talktorials/T000_template/talktorial.ipynb>`_), within which you develope your new talktorial. Please read through the template completely before you start as it contains a lot of information about the content and style requirements.

  - You do not need to worry about updating ``T099_fingerprints/README.md`` as we are syncing these READMEs with the first couple of sections of the notebook (see more details in `Maintaining talktorials`_).

  - As the names suggest, the folders ``T099_fingerprints/data/`` and ``T099_fingerprints/images/`` can be used to store input/output data and images. Whenever possible, avoid adding files and instead fetch data/images by URL. Ask us if in doubt.

8. Push your new talktorial folder skeleton to your GitHub repository (replace ``T099_fingerprints`` and ``ab-t099-fingerprints`` with your own)::

    # Add folder
    git add teachopencadd/talktorials/T099_fingerprints/
    # Commit changes
    git commit -m "T099: Add talktorial folder skeleton"
    # Push changes
    git push origin ab-t099-fingerprints

9. Create the pull request (PR) with our PR template:

  - Go to your fork ``https://github.com/your-github-name/teachopencadd/pulls`` and click "New pull request"

  - Select the following:

    - ``base repository: volkamberlab/teachopencadd`` and ``base: master``

    - ``head repository: your-github-name/teachopencadd`` and ``compare: ab-t099-fingerprints``

  - Click "Create pull request"

  - When the PR description window opens, please copy-paste `the content of this PR template <https://github.com/volkamerlab/teachopencadd/blob/master/.github/PULL_REQUEST_TEMPLATE/talktorial_review.md>`_ into it.

10. Read through the PR description TODOs and check in with us if you have questions. Note: Many bullet points have to do with our maintenance efforts (see more details in `Maintaining talktorials`_).

11. Get started with developing your talktorials. Add your changes to the PR by following the procedure in step 8.

12. Ping us if you need help or are ready for the PR review. Thanks!


Updating talktorials
--------------------

If you find an error in a talktorial or wish to extend the content of one, please follow these steps (example: updating talktorial ``T002_compound_adme``):

1. Fork and clone the ``teachopencadd`` repository and checkout a new branch as described in steps 1-5 in `Submitting new talktorials`_, while step 2 refers to the index of the talktorial you wish to update, e.g. ``T002_compound_adme``, and your new branch should be something descriptive like ``ab-t002-fix-kekuli``.

2. Push your new branch to your GitHub repository (replace ``T002_compound_adme`` and ``ab-t002-extend-adme-theory`` with your own)::

    # Add folder
    git add teachopencadd/talktorials/T002_compound_adme/
    # Commit changes
    git commit -m "T002: Extend ADME theory"
    # Push changes
    git push origin ab-t002-extend-adme-theory

3. Create PR as described in step 9 in `Submitting new talktorials`_. Some PR bullet points might not apply to your case, please use `~some bullet point~` to strike it through.

4. Ping us if you need help or are ready for the PR review. Thanks!


.. _contrib_maintain:

Maintaining talktorials
-----------------------

- Our `environment file <https://github.com/volkamerlab/teachopencadd/tree/master/devtools>`_ satisfies the dependencies for all TeachOpenCADD talktorials. This format might change in the future as discussed `here <https://github.com/volkamerlab/teachopencadd/discussions/277>`_.

- Our `GitHub Actions CI setup file <https://github.com/volkamerlab/teachopencadd/blob/master/.github/workflows/ci.yml>`_ contains:

  - Notebook tests (``pytest``), which check if the notebook runs without errors and if cells flagged with ``# NBVAL_CHECK_OUTPUT`` produce the same output in the CI as saved within the ``.ipynb``file. Check under ``jobs.test`` the tested operating systems and Python versions.

  - Notebook formatting (``black-nb``), check under ``jobs.format``::

        black-nb -l 99 --check teachopencadd/talktorials/T*/talktorial.ipynb

  - Autogenerated READMEs, check under ``jobs.readmes``::

        for path in teachopencadd/talktorials/T*/talktorial.ipynb; do
            python devtools/regenerate_readmes.py --output README.md $path
        done

- Our `TeachOpenCADD website <https://projects.volkamerlab.org/teachopencadd/>`_:

  - You can render the website locally (including your changes) as described in `our documentation README <https://github.com/volkamerlab/teachopencadd/blob/master/docs/README.md>`_
  - Please follow `these steps <https://github.com/volkamerlab/teachopencadd/blob/master/.github/PULL_REQUEST_TEMPLATE/talktorial_review.md#website>`_ if you wish to add new content.

- We are cutting new releases as described in this `Discussion entry <https://github.com/volkamerlab/teachopencadd/discussions/197>`_.

- Our ``teachopencadd`` package lives with ``conda-forge``: https://anaconda.org/conda-forge/teachopencadd

  - Whenever we cut a new GitHub release, we have to also cut a new ``conda`` release.

  - Refer to `"Maintaining packages" <https://conda-forge.org/docs/maintainer/updating_pkgs.html>`_  and `these notes <https://github.com/volkamerlab/teachopencadd/discussions/184>`_ for instructions how to do this and ask @dominiquesydow for help.

  - In order to cut a new ``conda`` release, you will need to update the recipe within our `teachopencadd feedstock <https://github.com/conda-forge/teachopencadd-feedstock>`_.




