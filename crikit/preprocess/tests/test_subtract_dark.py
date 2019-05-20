import os
import numpy as np
import numpy.testing

import pytest

from crikit.preprocess.subtract_dark import SubtractDark

@pytest.fixture(scope="function")
def make_datasets():
    """ Setups and tears down a series of datasets """

    data_m, data_n, data_p = [20, 22, 24]
    spectrum = np.random.randn(data_p)**2 + 1
    spectra = np.random.randn(data_n, data_p)**2 + 1
    hsi = np.random.randn(data_m, data_n, data_p)**2 + 1

    return spectrum, spectra, hsi, np.array([data_m, data_n, data_p])

def test_sub_spectrum_from_spectrum(make_datasets):
    """ Dark is spectrum. Data is spectrum. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectrum
    dark = 1*spectrum

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, 0.0)
    np.testing.assert_array_almost_equal(out, data - dark)

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_spectra_from_spectrum(make_datasets):
    """ Dark is spectra. Data is spectrum. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectrum
    dark = 1*spectra

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=0))

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_hsi_from_spectrum(make_datasets):
    """ Dark is HSI. Data is spectrum. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectrum
    dark = 1*hsi

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=(0,1)))

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_spectrum_from_spectra(make_datasets):
    """ Dark is spectrum. Data is spectra. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectra
    dark = 1*spectrum

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, data - dark[None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_spectra_from_spectra(make_datasets):
    """ Dark is spectra. Data is spectra. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectra
    dark = 1*spectra

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    
    # * Even though the data and dark have same dimensions, the dark is averaged
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=0)[None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_hsi_from_spectra(make_datasets):
    """ Dark is HSI. Data is spectrum. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*spectra
    dark = 1*hsi

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=(0,1))[None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_spectrum_from_hsi(make_datasets):
    """ Dark is spectrum. Data is HSI. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*hsi
    dark = 1*spectrum

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    np.testing.assert_array_almost_equal(out, data - dark[None,None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_spectra_from_hsi(make_datasets):
    """ Dark is spectra. Data is HSI. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*hsi
    dark = 1*spectra

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size
    
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=0)[None,None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_hsi_from_hsi(make_datasets):
    """ Dark is HSI. Data is HSI. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = 1*hsi
    dark = 1*hsi

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size

    # * Even though the data and dark have same dimensions, the dark is averaged
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=(0,1))[None,None,:])

    # Transform
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_sub_hsi_int_from_hsi_float(make_datasets):
    """ Dark is HSI. Data is HSI. """
    
    spectrum, spectra, hsi, shape = make_datasets
    data = (1*hsi).astype(np.float)
    dark = (1*hsi).astype(np.int)

    subdark = SubtractDark(dark)

    # Calculate
    meaner = data.mean()
    out = subdark.calculate(data)
    assert meaner == data.mean()
    assert out.mean() != data.mean()
    assert out.size == data.size

    # * Even though the data and dark have same dimensions, the dark is averaged
    np.testing.assert_array_almost_equal(out, data - dark.mean(axis=(0,1))[None,None,:])

    # Transform
    dark = (1*hsi).astype(np.int)
    subdark = SubtractDark(dark)
    success = subdark.transform(data)
    np.testing.assert_array_almost_equal(data, out)
    assert meaner != data.mean()
    assert success is True

def test_transform_incompatible_dtypes(make_datasets):
    """
    Test that TypeError is raised when Dark and Data have incompatible
    dtypes for in-place transformation

    Note: if spectra or hsi is used for dark, will convert to float due to mean
    """
    
    spectrum, spectra, hsi, shape = make_datasets
    
    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.int)
    dark = (1*spectrum).astype(np.int)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.float)
    dark = (1*spectrum).astype(np.int)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.complex)
    dark = (1*spectrum).astype(np.int)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    # DOES RAISE ERROR
    data = (1*hsi).astype(np.int)
    dark = (1*spectrum).astype(np.float)
    subdark = SubtractDark(dark)
    with pytest.raises(TypeError):
        subdark.transform(data)

    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.float)
    dark = (1*spectrum).astype(np.float)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.complex)
    dark = (1*spectrum).astype(np.float)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    # DOES RAISE ERROR
    data = (1*hsi).astype(np.int)
    dark = (1*spectrum).astype(np.complex)
    subdark = SubtractDark(dark)
    with pytest.raises(TypeError):
        subdark.transform(data)

    # DOES RAISE ERROR
    data = (1*hsi).astype(np.float)
    dark = (1*spectrum).astype(np.complex)
    subdark = SubtractDark(dark)
    with pytest.raises(TypeError):
        subdark.transform(data)

    # DOES NOT RAISE ERROR
    data = (1*hsi).astype(np.complex)
    dark = (1*spectrum).astype(np.complex)
    subdark = SubtractDark(dark)
    subdark.transform(data)

    