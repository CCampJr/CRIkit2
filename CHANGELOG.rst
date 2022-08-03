=========
Changelog
=========

This document records all notable changes to 
`CRIkit2 <https://github.com/CCampJr/CRIkit2>`_.

This project adheres to `PEP 440 -- Version Identification 
and Dependency Specification <https://www.python.org/dev/peps/pep-0440/>`_.

0.4.3 (22-08-03)
----------------
- Spectrum and Hsi now moved to **data.spectra**. **This could break your fork if you have custom code.**
- LazyHDF5 now within CRIkit2 instead of external library
- Import macrostage raster images (NIST) from multiple datasets

0.4.2 (22-03-24)
----------------
- Changes to Phase Error Correction UI and some quality of life improvements

0.4.1 (22-03-24)
----------------
- The UI for Phase Error Correction now incorporates the wavenumber-increased parameter of 0.4 release

0.4 (22-03-11)
---------------
- **Important**: PhaseErrCorrectALS now has parameter for whether wavenumber is increasing left-to-right. This is important to set correctly. This should match the `conjugate` parameter in the KramersKronig.

0.3.1 (21-11-29)
-----------------
- Updated h5py deprecated syntax from .value to [:] (@XavierAutier)
- Minor updates

0.3.0 (21-10-21)
----------------
-   H5 files with problematic X- or Y- assigned scales will revert to pixel units
-   Upgraded to LazyHDF5 0.3.0 nuances.
-   Added option to hilbertfft to return full padded results
-   Bug fixes

0.2.5 (20-03-05)
----------------
-   Significant performance improvement to ALS-detrending (15-50%)

0.2.4 (20-02-19)
----------------
-   Added more unit tests
-   Performance improvements (especially related to ROI-spectra)
-   Bug fix: Phantom dataset now included in pip installation

0.2.3 (20-02-06)
----------------
-   Added more tests
    -   Algorithms: KK, hilbert
-   KK (class) uses less memory but at a slight decrease to speed using iteration. 'no_iter' flag to disable.
-   Visualize the real part of the KK in interactive mode
-   Conjugate the KK (function, class, and GUI)
    -   Support for spectra that are high-to-low wavenumber oriented (left-to-right)
    -   Auto-checks for this in the KK dialog (UI), though not in interactive mode
-   Crop (or some other options) m spectra every n spectra
    -   In preprocess.crop
    -   Added GUI as well (Preprocess header) -- separate for NRB and Dark
-   Updated KK GUI to incorporate edge-averaging (n_edge KK parameter)

0.2.2 (19-11-20)
----------------

-   Added a calculate Anscombe parameters function (calc_anscombe_parameters) to crikit.preprocess.standardize
    -   Added an associated GUI dialog for calculating based on NRB and Dark spectra (Preprocess>Standardize submenu)
    -   Note: you will need to perform Dark subtraction before performing the Anscombe transform (though the calculation of parameters can handle either scenario)
    -   Added unittest for calculation function (not the GUI itself)
    -   Added Jupyter Notebook (Calculating Anscombe Parameters.ipynb) to demonstrate use of calc_anscombe_parameters
-   Added a function that will take the respective RGB images + composite and de-mosaic them into TIFFs (NIST Special > DeMosaic RGB Images)
-   Fixes
    -   Closing Mosaic tool doesn't close CRIkit UI as well

0.2.1 (19-09-17)
------------------

-   New toolbar ribbon setup scheme and default
-   New kkrelation and hilbertfft function
    -   Select axis
    -   Performs on N-dimensional arrays (not limited to 1- or 2D)
    -   Removed pyFFTW support
    -   Set min values
    -   Set value to set Inf's and NaN's
    -   Note: Does consume more RAM during computation (user may iteratively apply)

-   New KramersKronig incorporating new kkrelation/hilbertfft features
    -   Does not iterate through data, which can require a lot more memory
    
-   New padding function pad_edge_mean
    -   Pads along specified axis with edge values
    -   Edge values can be a mean of n neighboring values as well
    -   Now the default padding function for hilbert and kkrelation

-   Tweaks and bug fixes
    -   Fixed sign error in PhaseErrorCorrectALS that mainly affected real part of spectra

0.2.0 (19-05-23)
----------------

-   Initial version
