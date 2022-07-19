Installing
==========

.. note::

    We are assuming you have a working ``mamba`` installation in your computer. 
    If this is not the case, please refer to their `official documentation <https://mamba.readthedocs.io/en/latest/installation.html#mamba>`_. 

    If you installed ``mamba`` into an existing ``conda`` installation, also make sure that the ``conda-forge`` channel is configured by running ``conda config --add channels conda-forge``. 


Install from the conda package
------------------------------

1. Create a new conda environment for TeachOpenCADD::

    # Linux / MacOS
    mamba create -n teachopencadd teachopencadd

    # Windows
    mamba create -n teachopencadd teachopencadd -c conda-forge -c defaults

    # When using a MacBook Air 12.4 with an M1 chip (2020)
    CONDA_SUBDIR=osx-64 mamba create -n teachopencadd teachopencadd

2. Activate the new environment::

    conda activate teachopencadd

3. Run ``teachopencadd -h`` to test that it works.
4. Run ``teachopencadd start .`` to set up a new workspace with the TeachOpenCADD material. Follow the instructions printed in your terminal to open the material (Jupyter notebooks) with Jupyter Lab.
   In this example command, you are setting up your workspace in the current directory ``.``; you can use any other path.

You can always return to your TeachOpenCADD material with ``jupyter lab /path/to/your/teachopencadd/workspace``.


Install from the latest development snapshot
--------------------------------------------

1. Create a new conda environment and activate it::

    mamba env create -f https://raw.githubusercontent.com/volkamerlab/TeachOpenCADD/master/devtools/test_env.yml
    conda activate teachopencadd

2. Download a zipfile of the repository using `this link <https://github.com/volkamerlab/teachopencadd/archive/master.zip>`_.
3. Unzip to your location of choice.
4. Navigate to your location.
5. Start Jupyter Lab.
6. Double click on the lesson you want to start.

Steps 2 to 5 are summarized below.

.. Unix instructions

.. raw:: html

    <details>
    <summary>Instructions for Linux / MacOS</summary>

.. code-block:: bash

    wget https://github.com/volkamerlab/teachopencadd/archive/master.zip -O teachopencadd.zip
    mkdir -p ~/Documents
    unzip teachopencadd.zip -d ~/Documents
    cd ~/Documents/teachopencadd-master/teachopencadd/talktorials
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
    cd ~/Documents/teachopencadd-master/teachopencadd/talktorials
    jupyter lab

.. raw:: html

    </details>
