"""
Testing Spectrum class

"""


import numpy as np
import numpy.testing as np_testing

from crikit.data.spectra import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.spectra import Hsi
from crikit.utils.general import find_nearest

def test_spectrum():
    N = 101
    data = np.linspace(0,100,N)
    f = np.arange(N)
    spectrum = Spectrum(data=data, freq=f)
    np_testing.assert_allclose(spectrum._data_idx_freq[0],spectrum._data[0])

    # Note: _data_idx_freq is INCLUSIVE-- normal indexing is NOT
    # This the :11 and not 10
    np_testing.assert_allclose(spectrum._data_idx_freq[0:10],
                               spectrum._data[0:11])
    np_testing.assert_allclose(spectrum._data_idx_freq[0.0:10.1:.1],
                               spectrum._data[0:11])
    np_testing.assert_allclose(spectrum._data_idx_freq[0.0:10.1],
                               spectrum._data[0:11])
    np_testing.assert_equal(spectrum._data_idx_freq[10], spectrum._data[10])
    np_testing.assert_allclose(spectrum._data_idx_freq[[10,11]], spectrum._data[[10,11]])
    
    
def test_spectra():
    N = 101
    data = np.dot(np.ones((10,1)), np.linspace(0,100,N)[None,:])
    f = np.arange(N)
    spectra = Spectra(data=data, freq=f)
    np_testing.assert_allclose(spectra._data_idx_freq[0],spectra._data[...,0])

    # Note: _data_idx_freq is INCLUSIVE-- normal indexing is NOT
    # This the :11 and not 10
    np_testing.assert_allclose(spectra._data_idx_freq[0:10],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[0.0:10.1:.1],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[0.0:10.1],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[10], spectra._data[...,10])
    np_testing.assert_allclose(spectra._data_idx_freq[[10,11]], spectra._data[...,[10,11]])
    
    # Slice the spatial dimension as well:
    np_testing.assert_allclose(spectra._data_idx_freq[:,0:10],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[:,0.0:10.1:.1],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[:,0.0:10.1],
                               spectra._data[...,0:11])
    np_testing.assert_allclose(spectra._data_idx_freq[10,11], spectra._data[...,[10,11]])
    np_testing.assert_allclose(spectra._data_idx_freq[:,10], spectra._data[...,10])
    # np_testing.assert_allclose(spectra._data_idx_freq[:,[10,11]], spectrum._data[...,[10,11]])

def test_hsi():
    N = 101
    data = np.dot(np.ones((10,11,1)), np.linspace(0,100,N)[None,:])
    f = np.arange(N)
    hsi = Hsi(data=data, freq=f)
    np_testing.assert_allclose(hsi._data_idx_freq[0],hsi._data[...,0])

    # Note: _data_idx_freq is INCLUSIVE-- normal indexing is NOT
    # This the :11 and not 10
    np_testing.assert_allclose(hsi._data_idx_freq[0:10],
                               hsi._data[...,0:11])
    np_testing.assert_allclose(hsi._data_idx_freq[0.0:10.1:.1],
                               hsi._data[...,0:11])
    np_testing.assert_allclose(hsi._data_idx_freq[0.0:10.1],
                               hsi._data[...,0:11])
    np_testing.assert_allclose(hsi._data_idx_freq[...,10], hsi._data[...,10])
    np_testing.assert_allclose(hsi._data_idx_freq[...,[10,11]], hsi._data[...,[10,11]])
    
    # Slice the spatial dimension as well:
    np_testing.assert_allclose(hsi._data_idx_freq[:,:,0:10],
                               hsi._data[...,0:11])
    np_testing.assert_allclose(hsi._data_idx_freq[:,:,0.0:10.1:.1],
                               hsi._data[...,0:11])
    np_testing.assert_allclose(hsi._data_idx_freq[:,:,0.0:10.1],
                               hsi._data[...,0:11])
    

if __name__ == '__main__':
    print('Here')
    test_spectra()