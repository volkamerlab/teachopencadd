.. teachopencadd documentation master file, created by
   sphinx-quickstart on Thu Mar 15 13:55:56 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to TeachOpenCADD's documentation!
=========================================================

A teaching platform for computer-aided drug design (CADD)
using open source packages and data.

.. toctree::
   :maxdepth: 1
   :caption: Getting started

   installing

.. toctree::
   :maxdepth: 1
   :caption: Talktorials

   talktorials

.. toctree::
   :maxdepth: 1
   :caption: Developers

   api

.. code-block:: python

   # Input: Fingerprints and a threshold for the clustering
   def ClusterFps(fps,cutoff=0.2):
      # Calculate Tanimoto distance matrix
      distance_matr = Tanimoto_distance_matrix(fps)
      # Now cluster the data with the implemented Butina algorithm:
      clusters = Butina.ClusterData(distance_matr,len(fps),cutoff,isDistData=True)
      return clusters