import os
import numpy as np
import numpy.testing

import pytest

from crikit.preprocess.standardize import calc_anscombe_parameters

@pytest.fixture(scope="function")
def make_datasets():
    """ Setups and tears down a series of datasets """
    np.random.seed(0)
    n_spectra = 1000  # number of indep. spectra
    n_lambda = 901  # number of wavelengths in each spectrum

    f = np.linspace(0,4000,n_lambda)  # Frequency (au)
    y = 40e2*np.exp(-f**2/(2*350**2)) + 50e1*np.exp(-(f-2900)**2/(2*250**2))   # signal

    g_mean = 100
    g_std = 25
    p_alpha = 10

    y_array = np.dot(np.ones((n_spectra,1)),y[None,:])
    y_noisy = p_alpha*np.random.poisson(y_array) + g_std*np.random.randn(*y_array.shape) + g_mean
    dark = g_std*np.random.randn(*y_array.shape) + g_mean

    return y_noisy, dark, g_mean, g_std, p_alpha

def test_calc_ansc_params(make_datasets):
    """ Calculate Anscombe Parameters """
    
    y_noisy, dark, g_mean, g_std, p_alpha = make_datasets
    out = calc_anscombe_parameters(dark, y_noisy, axis=0, rng=None, dark_subtracted=False)

    assert np.allclose(out['g_mean'].mean(), g_mean, rtol=1e-2)
    assert np.allclose(out['g_std'].mean(), g_std, rtol=1e-2)
    assert np.allclose(out['weighted_mean_alpha'].mean(), p_alpha, rtol=1e-2)