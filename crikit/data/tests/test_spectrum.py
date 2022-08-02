import os
import numpy as np
import numpy.testing

import pytest
import crikit.io.lazy5 as lazy5

from crikit.io.hdf5 import hdf_import_data
from crikit.data.spectra import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.spectra import Hsi

@pytest.fixture(scope="function")
def make_datasets():
    """ Setups and tears down a series of datasets """

    data_m, data_n, data_p = [20, 22, 24]
    spectrum = np.random.randn(data_p)**2 + 1
    spectra = np.random.randn(data_n, data_p)**2 + 1
    hsi = np.random.randn(data_m, data_n, data_p)**2 + 1

    return spectrum, spectra, hsi, np.array([data_m, data_n, data_p])

def test_mean_axes_static(make_datasets):
    """ Import a spectrum into a spectrum """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    Spectrum._mean_axes(3, 2) == [0,1]
    Spectrum._mean_axes(3, -1) == [0,1]
    Spectrum._mean_axes(3, 0) == [1,2]
    Spectrum._mean_axes(3, 1) == [0,2]

def test_spectrum_to_spectrum(make_datasets):
    """ Import a spectrum into a spectrum """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Spectrum()
    new_dataset.data = spectrum

    assert new_dataset.size == spectrum.size
    np.testing.assert_almost_equal(new_dataset.data, spectrum)

def test_spectrum_to_spectrum_rng(make_datasets):
    """ Import a spectrum into a spectrum -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Spectrum()
    new_dataset.freq.data = np.arange(spectrum.size)
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = spectrum

    assert new_dataset.size == spectrum.size
    assert (new_dataset.data != 0).sum() == len(rng)
    np.testing.assert_almost_equal(new_dataset.data[rng], spectrum[rng])

def test_spectra_to_spectrum(make_datasets):
    """ Import spectra into a spectrum """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Spectrum()
    new_dataset.data = spectra

    assert new_dataset.size == spectrum.size
    np.testing.assert_almost_equal(new_dataset.data, spectra.mean(axis=0))

def test_spectra_to_spectrum_rng(make_datasets):
    """ Import spectra into a spectrum -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Spectrum()
    new_dataset.freq.data = np.arange(spectrum.size)
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = spectra

    assert new_dataset.size == spectrum.size
    assert (new_dataset.data != 0).sum() == len(rng)
    np.testing.assert_almost_equal(new_dataset.data[rng], spectra[:,rng].mean(axis=0))

def test_hsi_to_spectrum(make_datasets):
    """ Import hsi into a spectrum """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Spectrum()
    new_dataset.data = hsi

    assert new_dataset.size == spectrum.size
    np.testing.assert_almost_equal(new_dataset.data, hsi.mean(axis=(0,1)))

def test_hsi_to_spectrum_rng(make_datasets):
    """ Import an hsi into a spectrum -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Spectrum()
    new_dataset.freq.data = np.arange(spectrum.size)
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = hsi

    assert new_dataset.size == spectrum.size
    assert (new_dataset.data != 0).sum() == len(rng)

    print('A - B: {}'.format(new_dataset.data[rng] - hsi[..., rng].mean(axis=(0,1))))
    np.testing.assert_almost_equal(new_dataset.data[rng], hsi[..., rng].mean(axis=(0,1)))