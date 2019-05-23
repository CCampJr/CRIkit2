.. _api:

.. image:: _static/CRIkit2_Logo.png
    :align: left

|
|
|
|
|
|
|

API Reference
=============

This is not an exhaustive list of classes and functions,
but rather those most likely to be of interest to users and developer.
See :ref:`genindex` and :ref:`modindex` for a full list.

:mod:`crikit.cri`: Coherent Raman Imagery (CRI) classes and functions
---------------------------------------------------------------------

.. automodule:: crikit.cri

Classes
~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    

    cri.kk.KramersKronig
    cri.error_correction.PhaseErrCorrectALS
    cri.error_correction.ScaleErrCorrectSG

Functions
~~~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    

    cri.algorithms.kk.kkrelation
    cri.algorithms.kk.hilbertfft
   
:mod:`crikit.data`: Data container classes
------------------------------------------

.. automodule:: crikit.data

Classes
~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    data.frequency.Frequency
    data.replicate.Replicate

    data.spectrum.Spectrum
    data.spectra.Spectra
    data.hsi.Hsi

:mod:`crikit.io`: Input/Output (IO) functions
----------------------------------------------

.. automodule:: crikit.io

Functions
~~~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    io.csv_nist.csv_nist_import_data
    io.hdf5.hdf_import_data
    io.meta_configs.special_nist_bcars1_sample_scan
    io.meta_configs.special_nist_bcars2
    io.meta_process.meta_process
    io.meta_process.rosetta_query

:mod:`crikit.measurement`: Measurement classes
----------------------------------------------

.. automodule:: crikit.measurement

Classes
~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    measurement.fftspatialnoise.FFTSignalMetric
    measurement.peakamps.MeasurePeak
    measurement.peakamps.MeasurePeakAdd
    measurement.peakamps.MeasurePeakBWTroughs
    measurement.peakamps.MeasurePeakMinus
    measurement.peakamps.MeasurePeakDivide
    measurement.peakamps.MeasurePeakMultiply
    measurement.peakamps.MeasurePeakSummation
    measurement.peakfind.PeakFinder

:mod:`crikit.preprocess`: Preprocessing classes and functions
-------------------------------------------------------------

.. automodule:: crikit.preprocess

Classes
~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    preprocess.algorithms.als.AlsCvxopt
    preprocess.algorithms.anscombe.anscombe_inverse_exact_unbiased
    preprocess.algorithms.anscombe.gen_anscombe_forward
    preprocess.algorithms.anscombe.gen_anscombe_inverse_closed_form
    preprocess.algorithms.anscombe.gen_anscombe_inverse_exact_unbiased
    preprocess.algorithms.arpls.ArPlsCvxopt
    preprocess.crop.ZeroColumn
    preprocess.crop.ZeroRow
    preprocess.denoise.SVDDecompose
    preprocess.denoise.SVDRecompose
    preprocess.standardize.Anscombe
    preprocess.standardize.AnscombeInverse
    preprocess.subtract_baseline.SubtractBaselineALS
    preprocess.subtract_dark.SubtractDark
    preprocess.subtract_mean.SubtractMeanOverRange

:mod:`crikit.utils`: Utility functions
---------------------------------------

.. automodule:: crikit.utils

Classes
~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    utils.breadcrumb.BCPre

Functions
~~~~~~~~~
.. currentmodule:: crikit

.. autosummary::
    
    utils.general.arange_nonzero
    utils.general.expand_1d_to_ndim
    utils.general.expand_1d_to_ndim_data
    utils.general.find_nearest
    utils.general.lin_from_row_col
    utils.general.mean_nd_to_1d
    utils.general.np_fcn_nd_to_1d
    utils.general.row_col_from_lin
    utils.general.std_nd_to_1d

