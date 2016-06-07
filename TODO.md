# Major initiatives
* Add rng functionality to all fcns
* Implement and test dask/out-of-core processing
* Remove references to Spectrum subclasses in unittests
* Implement logging
* ~~Test-out Change all inputs to type numpy rather than class~~

# Numerical performance

# Process functionality enhancements

# Frequency class
* Accept calib dict or list with only n_pix, returning pixel vector
* Implement op_range_pix, op_range_freq, plot_range_pix, plot_range_freq

# Spectra class
* ~~Implement Replicate class container~~
* ~~If writing back data the size of op_range_\*, correctly pad~~

# Spectrum class
* ~~If writing back data the size of op_range_\*, correctly pad~~

# Hsi class
* ~~If writing back data the size of op_range_\*, correctly pad~~

# denoise
* Implement plugin framework

# io package
* Implement out-of-core processing system with temporary HDF file-as-data solution
* Make into plugin system to make custom import modules more streamline
* Make tests for meta and hdf after artificial test hdf file is created
* special create list of filename
* Handle list of HSI image imaports
* Redo frequency calibration meta config and meta process
* hdf_import_data needs to return something
* ~~HDF5 import~~

# preprocess package
* tests for subtract_mean
* tests for subtract_dark
* tests for subtract_baseline
* docstring for subtract_baseline
* docstring for als algorithms
* docstring for arpls algorithms
* make sub_baseline_arpls

# From crikit to crikit2
* Denoise with SVD
* KK
* Phase-error correction
* Scaling
* Subtract from ROI (maybe)
* Grayscale image return
* RGB color return and math (maybe)
* Save functionality

# Etc
~~Make layout SVG~~