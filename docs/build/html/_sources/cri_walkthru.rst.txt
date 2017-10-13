.. _cri_walkthru:

.. image:: _static/CRIkit2_Logo.png
    :align: left

|
|
|
|
|
|
|

Walk-Thru: CRI Processing
=========================

This walk-thru will take you through several steps:

- `Overview`_
- `Loading HDF file Hsi dataset`_
- `Loading Dark dataset`_
    -`Denoise Dark (Optional)`_
- `Loading an NRB dataset`_
    - From HDF
    - From an ROI within the **Hsi** dataset
- `Dark subtraction`_
- `Residual dark subtraction (Optional)`_
- `Variance stabilization`_
- `Denoising via singular value decomposition (SVD)`_
- `Phase retrieval via Kramers-Kronig relation`_
- `Phase error correction`_
- `Scale error correction`_
- `Calibration`_
- `Saving`_
- `Pseudo-color imagery`_

The screenshots within this manual may or may not reflect the exact look of the
version of CRIkit2 UI that you are using.

Overview
--------

.. image:: _static/cri_wt/overview.jpg
    :align: center

Loading HDF file Hsi dataset
-----------------------------
.. image:: _static/cri_wt/load1.jpg
    :align: center

.. image:: _static/cri_wt/load2.png
    :align: center

.. image:: _static/cri_wt/load3.png
    :align: center

Loading Dark dataset
---------------------
.. image:: _static/cri_wt/load_dark.png
    :align: center

Denoise Dark (Optional)
~~~~~~~~~~~~~~~~~~~~~~~

.. image:: _static/cri_wt/denoise_dark.jpg
    :align: center

Loading an NRB dataset
----------------------

Load from HDF file
~~~~~~~~~~~~~~~~~~

.. image:: _static/cri_wt/load_nrb.png
    :align: center

Load from ROI
~~~~~~~~~~~~~

.. image:: _static/cri_wt/load_nrb_roi.jpg
    :align: center

Merge two NRB datasets
~~~~~~~~~~~~~~~~~~~~~~


Dark subtraction
----------------

Residual dark subtraction (Optional)
------------------------------------

Variance stabilization
----------------------
.. image:: _static/cri_wt/Anscombe_action.jpg
    :align: center

.. image:: _static/cri_wt/InverseAnscombe_action.png
    :align: center

Denoising via singular value decomposition (SVD)
------------------------------------------------
.. image:: _static/cri_wt/denoise_action.jpg
    :align: center

.. image:: _static/cri_wt/svd_widget.jpg
    :align: center

Phase retrieval via Kramers-Kronig relation
-------------------------------------------

Phase error correction
----------------------

Scale error correction
-----------------------

Calibration
-----------

Saving
-------

Pseudo-color imagery
--------------------

