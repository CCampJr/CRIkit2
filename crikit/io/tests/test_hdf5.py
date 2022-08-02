import os
import numpy as np
import numpy.testing

import pytest
import h5py
import crikit.io.lazy5 as lazy5

from crikit.io.hdf5 import hdf_import_data
from crikit.data.spectra import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.spectra import Hsi

@pytest.fixture(scope="module")
def hdf_dataset():
    """ Setups and tears down a sample HDF5 file """
    filename = 'temp_test.h5'
    fid = h5py.File(filename, 'w')

    data_m, data_n, data_p = [20, 22, 24]
    spectrum = np.random.randn(data_p)
    spectra = np.random.randn(data_n, data_p)
    hsi = np.random.randn(data_m, data_n, data_p)

    fid.create_dataset('hsi', data=hsi)
    fid.create_dataset('spectra', data=spectra)
    fid.create_dataset('spectrum', data=spectrum)

    yield filename, fid, (data_m, data_n, data_p)

    # Tear-down
    if lazy5.utils.hdf_is_open(fid):
        fid.close()
    os.remove(filename)

def test_hdf_import_spectrum_to_spectrum(hdf_dataset):
    """ Import a spectrum into a spectrum """

    filename, fid, hdf_data_shape = hdf_dataset
    hdf_data_shape = np.array(hdf_data_shape)

    dname = 'spectrum'
    dataset = Spectrum()

    out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
    assert out is True
    assert dataset.size == hdf_data_shape[-1]
    np.testing.assert_array_equal(dataset.data, fid[dname][...])

def test_hdf_import_spectra_to_spectra(hdf_dataset):
    """ Import a spectra into a spectra """

    filename, fid, hdf_data_shape = hdf_dataset
    hdf_data_shape = np.array(hdf_data_shape)

    dname = 'spectra'
    dataset = Spectra()

    out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
    assert out is True
    assert dataset.size == hdf_data_shape[1:].prod()
    np.testing.assert_array_equal(dataset.data, fid[dname][...])

def test_hdf_import_hsi_to_hsi(hdf_dataset):
    """ Import an hsi into an hsi """

    filename, fid, hdf_data_shape = hdf_dataset
    hdf_data_shape = np.array(hdf_data_shape)

    dname = 'hsi'
    dataset = Hsi()

    out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
    assert out is True
    assert dataset.size == hdf_data_shape.prod()
    np.testing.assert_array_equal(dataset.data, fid[dname][...])
def test_hdf_import_no_output_cls_given(hdf_dataset):
    """ Import a spectrum, spectra, and hsi when no instantiated class is provided """

    filename, fid, hdf_data_shape = hdf_dataset
    hdf_data_shape = np.array(hdf_data_shape)

    # Spectrum
    dname = 'spectrum'
    dataset, dset_meta = hdf_import_data('.', filename, dname, output_cls_instance=None)
    assert dataset.size == hdf_data_shape[-1]
    np.testing.assert_array_equal(dataset, fid[dname][...])

    # Spectra
    dname = 'spectra'
    dataset, dset_meta = hdf_import_data('.', filename, dname, output_cls_instance=None)
    assert dataset.size == hdf_data_shape[1:].prod()
    np.testing.assert_array_equal(dataset, fid[dname][...])

    # HSI
    dname = 'hsi'
    dataset, dset_meta = hdf_import_data('.', filename, dname, output_cls_instance=None)
    assert dataset.size == hdf_data_shape.prod()
    np.testing.assert_array_equal(dataset, fid[dname][...])
    
# def test_hdf_import_spectra_to_spectrum(hdf_dataset):
#     """ Import spectra into a spectrum """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'spectra'
#     dataset = Spectrum()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape[-1]
#     np.testing.assert_equal(dataset.data, fid[dname][...].mean(axis=0))

# def test_hdf_import_hsi_to_spectrum(hdf_dataset):
#     """ Import hsi into a spectrum """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'hsi'
#     dataset = Spectrum()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape[-1]
#     np.testing.assert_equal(dataset.data, fid[dname][...].mean(axis=(0,1)))


# def test_hdf_import_spectrum_to_spectra(hdf_dataset):
#     """ Import a spectrum into a spectra """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'spectrum'
#     dataset = Spectra()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape[-1]
#     assert dataset.ndim == 2
#     np.testing.assert_equal(dataset.data, fid[dname][...])

# def test_hdf_import_hsi_to_spectra(hdf_dataset):
#     """ Import hsi into spectra """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'hsi'
#     dataset = Spectra()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape.prod()
#     assert dataset.ndim == 2
#     np.testing.assert_equal(dataset.data, fid[dname][...].reshape((-1, hdf_data_shape[-1])))

# def test_hdf_import_spectrum_to_hsi(hdf_dataset):
#     """ Import a spectrum into an hsi """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'spectrum'
#     dataset = Hsi()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape[-1]
#     assert dataset.ndim == 3
#     np.testing.assert_equal(dataset.data, fid[dname][...])

# def test_hdf_import_spectra_to_hsi(hdf_dataset):
#     """ Import spectra into an hsi """

#     filename, fid, hdf_data_shape = hdf_dataset
#     hdf_data_shape = np.array(hdf_data_shape)

#     dname = 'spectra'
#     dataset = Hsi()

#     out = hdf_import_data('.', filename, dname, output_cls_instance=dataset)
#     assert out is True
#     assert dataset.size == hdf_data_shape[1:].prod()
#     assert dataset.ndim == 3
#     np.testing.assert_equal(dataset.data, fid[dname][...].reshape((0, -1, hdf_data_shape[-1])))