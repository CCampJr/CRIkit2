.. CRIKit2 documentation master file, created by
   sphinx-quickstart on Wed Jul 20 22:31:57 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: _static/CRIkit2_Logo.png
    :align: left


|
|
|
|
|
|
|

Welcome to CRIKit2's documentation!
===================================

CRIkit2 is a numerical and graphical package for processing hyperspectral 
imagery (HSI). Originally developed for coherent Raman imaginery (CRI),
CRIkit2 is appropriate for all HSI.

The main components of CRIkit2:

- **CRIkitUI_process** : the [graphical] user interface (UI) for (pre-)processing 
  HSI.
- **CRIkitUI_analyze** : *Coming soon*. A UI for analysis and visualization. Out-of-core 
  computation enabled. Does not alter the original data.
- Numerical packages that can be used from the command line.

Contents:

.. toctree::
  :maxdepth: 2
  :caption: User Documentation

  installing
  running
  cri_walkthru
  algorithms
  io
  nonlicense

.. toctree::
  :maxdepth: 2
  :caption: Developer Documentation

  api
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
