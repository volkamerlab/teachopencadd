Installing
==========

.. note::

    We are assuming you have a working ``mamba`` installation in your computer. 
    If this is not the case, please refer to their `official documentation <https://mamba.readthedocs.io/en/latest/installation.html#mamba>`_. 

    If you installed ``mamba`` into an existing ``conda`` installation, also make sure that the ``conda-forge`` channel is configured by running ``conda config --add channels conda-forge``. 

    If you prefer to work with ``conda``, please use ``conda`` in place of ``mamba`` in the instructions below. 
    Please note that the TeachOpenCADD setup with ``conda`` takes much longer than with ``mamba``.


Install from the conda package
------------------------------
.. note::

    The conda package does not yet include all packages necessary to run the deep learning edition talktorials (T033-T038).

    We are working on it and will post an update as soon as the new package is available.

1. Create a new conda environment for TeachOpenCADD::

    # Linux / MacOS
    mamba create -n teachopencadd teachopencadd

    # Windows
    mamba create -n teachopencadd teachopencadd -c conda-forge -c defaults

    # When using a MacBook Air 12.4 with an M1 chip you may need:
    CONDA_SUBDIR=osx-64 mamba create -n teachopencadd teachopencadd

2. Activate the new environment::

    conda activate teachopencadd

3. Run ``teachopencadd -h`` to test that it works.
4. Run ``teachopencadd start .`` to set up a new workspace with the TeachOpenCADD material. Follow the instructions printed in your terminal to open the material (Jupyter notebooks) with Jupyter Lab.
   In this example command, you are setting up your workspace in the current directory ``.``; you can use any other path.

You can always return to your TeachOpenCADD material with ``jupyter lab /path/to/your/teachopencadd/workspace``.
If you need an introduction to Jupyter notebooks, please check out the suggested resources :ref:`here<jupyter_tutorial>`.

Install from the latest development snapshot
--------------------------------------------

1. Create a new conda environment and activate it::

    mamba env create -f https://raw.githubusercontent.com/volkamerlab/TeachOpenCADD/master/devtools/test_env.yml
    conda activate teachopencadd
   
   Note: If you are working on MacOS with an M1 chip and the above command is not working, e.g. "The environment can't be solved, aborting the operation", prefix the command with ``CONDA_SUBDIR=osx-64`` and try again::
    
    CONDA_SUBDIR=osx-64 mamba env create -f https://raw.githubusercontent.com/volkamerlab/TeachOpenCADD/master/devtools/test_env.yml
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
