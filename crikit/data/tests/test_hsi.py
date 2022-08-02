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

def test_mean_axes_static():
    """ Ensure mean_axes_static raises an error"""

    with pytest.raises(NotImplementedError):
        Hsi._mean_axes()

def test_reshape_axes_static(make_datasets):
    """ Test reshape axes static method """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    Hsi._reshape_axes(shape=hsi.shape, spectral_axis=-1) == (-1, hsi.shape[-1])
    Hsi._reshape_axes(shape=spectra.shape, spectral_axis=-1) == (-1, spectra.shape[-1])
    Hsi._reshape_axes(shape=spectrum.shape, spectral_axis=-1) == (-1, spectrum.shape[-1])

def test_hsi_to_hsi(make_datasets):
    """ Import an hsi into an hsi """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Hsi()
    new_dataset.data = hsi

    assert new_dataset.size == hsi.size
    np.testing.assert_array_equal(new_dataset.data, hsi)

def test_hsi_to_hsi_rng(make_datasets):
    """ Import an hsi into an hsi -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Hsi()
    new_dataset.freq.data = np.arange(hsi.shape[-1])
    new_dataset.data = hsi
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = hsi

    assert new_dataset.size == hsi.size
    assert (new_dataset.data != 0).sum() == len(rng)*np.prod(hsi.shape[:-1])
    np.testing.assert_almost_equal(new_dataset.data[..., rng], hsi[..., rng])

def test_spectrum_to_hsi(make_datasets):
    """ Import a spectrum into an hsi """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Hsi()
    new_dataset.data = spectrum

    assert new_dataset.size == spectrum.size
    np.testing.assert_array_equal(np.squeeze(new_dataset.data), spectrum)

def test_spectrum_to_hsi_rng(make_datasets):
    """ Import a spectrum into an hsi -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Hsi()
    new_dataset.freq.data = np.arange(hsi.shape[-1])
    new_dataset.data = spectrum
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = spectrum

    assert new_dataset.size == spectrum.size
    assert (new_dataset.data != 0).sum() == len(rng)
    np.testing.assert_almost_equal(np.squeeze(new_dataset.data[..., rng]), spectrum[rng])

def test_spectra_to_hsi(make_datasets):
    """ Import spectra into an hsi """

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    new_dataset = Hsi()
    new_dataset.data = spectra

    assert new_dataset.size == spectra.size
    np.testing.assert_array_equal(np.squeeze(new_dataset.data), spectra)

def test_spectra_to_hsi_rng(make_datasets):
    """ Import spectra into an hsi -- defined range"""

    spectrum, spectra, hsi, make_dataset_shape = make_datasets

    rng = [10,11]

    new_dataset = Hsi()
    new_dataset.freq.data = np.arange(hsi.shape[-1])
    new_dataset.data = spectra
    new_dataset.freq.op_list_pix = rng
    new_dataset.data = spectra

    assert new_dataset.size == spectra.size
    assert (new_dataset.data != 0).sum() == len(rng)*spectra.shape[0]
    np.testing.assert_almost_equal(np.squeeze(new_dataset.data[..., rng]), spectra[..., rng])
