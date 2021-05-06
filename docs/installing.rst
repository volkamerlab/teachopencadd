Installing
==========

Install from the conda package
------------------------------

Eventually, we will have a ``conda`` package, but for now you need to create a new environment manually.

.. note::

    We are assuming you have a working ``conda`` installation in your computer. If this is not the case, please refer to the official documentation `here <https://docs.conda.io/projects/conda/en/latest/user-guide/install/#regular-installation>`_. We recommend using Miniconda.


1. Create a new conda environment for TeachOpenCADD::

    conda env create -f https://raw.githubusercontent.com/volkamerlab/TeachOpenCADD/master/devtools/other-conda-envs/users_env.yml

2. Activate the new environment::

    conda activate teachopencadd

3. Run ``teachopencadd -h`` to test that it works.
4. [WIP 🚧] Run ``teachopencadd start .`` to set up a new workspace. This step is not fully functional yet. Please refer to `Install from the latest development snapshot <https://projects.volkamerlab.org/teachopencadd/installing.html#install-from-the-latest-development-snapshot>`_ for manual steps.


Install from the latest development snapshot
--------------------------------------------

If you have already created a *conda environment* and it has been activated  (see above), the next step is downloading a copy of the current state of the `GitHub repository <https://github.com/volkamerlab/teachopencadd>`_.

1. Download a zipfile of the repository using `this link <https://github.com/volkamerlab/teachopencadd/archive/master.zip>`_.
2. Unzip to your location of choice.
3. Navigate to ``path/to/your/location/teachopencadd-master/talktorials``.
4. Start Jupyter Lab.
5. Double click on the lesson you want to start.


.. Unix instructions

.. raw:: html

    <details>
    <summary>Instructions for Linux / MacOS</summary>

.. code-block:: bash

    wget https://github.com/volkamerlab/teachopencadd/archive/master.zip -O teachopencadd.zip
    mkdir -p ~/Documents
    unzip teachopencadd.zip -d ~/Documents
    cd ~/Documents/teachopencadd-master/talktorials
    jupyter lab

.. raw:: html

    </details>

.. Windows instructions

.. raw:: html

    <details>
    <summary>Instructions for Windows (PowerShell)</summary>

.. code-block::

    wget https://github.com/volkamerlab/teachopencadd/archive/master.zip -O teachopencadd.zip
    mkdir ~/Documents/
    Expand-Archive teachopencadd.zip -d ~/Documents
    cd ~/Documents/teachopencadd-master/talktorials
    jupyter lab

.. raw:: html

    </details>