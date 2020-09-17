Installing
==========

Eventually, we will have a ``conda`` package, but for now you need to create a new environment manually.

1. Install Miniconda for your OS if you don't have it already.
2. Create new conda environment::

    conda env create -n teachopencadd -f https://raw.githubusercontent.com/volkamerlab/TeachOpenCADD/master/environment.yml

3. Activate the new environment::

    conda activate teachopencadd

4. Install the package with ``pip``::

    python -m pip install https://github.com/volkamerlab/teachopencadd/archive/master.tar.gz

5. Run ``teachopencadd -h`` to test it works.
