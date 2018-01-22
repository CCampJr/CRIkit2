"""
Testing the aysmmetric least-squares detrending algorithm

"""

import numpy as np
import numpy.testing

from crikit.preprocess.subtract_baseline import SubtractBaselineALS

def test_basic():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-3, 
                              redux=1, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    assert y_als.max() < 0.0004

def test_fix_ends():
    x = np.linspace(-100, 100, 1000)
    y = 1000*np.exp(-x**2/(2*20**2)) + 200*np.exp(-(x+99)**2/(2*1**2))

    als = SubtractBaselineALS(smoothness_param=1e2, asym_param=1e-3, 
                              redux=1, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    assert y_als[0] > 20

    als = SubtractBaselineALS(smoothness_param=1e1, asym_param=1e-3, 
                              redux=1, fix_end_points=True, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    assert y_als[0] < 2

def test_fix_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))
    fix_rng = np.arange(200,800)

    als = SubtractBaselineALS(smoothness_param=1e3, asym_param=1e-5, 
                              redux=1, fix_end_points=False, fix_rng=None, 
                              verbose=True)
    y_als = als.calculate(y)

    assert np.max((y_als)[200:800]) > 0.002

    als = SubtractBaselineALS(smoothness_param=1e3, asym_param=1e-5, 
                              redux=1, fix_end_points=False, fix_rng=fix_rng, 
                              verbose=True)
    y_als = als.calculate(y)
    assert np.max((y_als)[200:800]) < 0.002

def test_vec_asym_param():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    asym_param = 1e-6*np.ones((x.size))

    als = SubtractBaselineALS(smoothness_param=1e3, asym_param=asym_param, 
                    redux=1, fix_end_points=False, fix_rng=None, 
                    verbose=True)
    y_als = als.calculate(y)

    assert np.max((y_als)[250:750]) > 7 

    asym_param[200:800] = 1e-2

    als = SubtractBaselineALS(smoothness_param=1e3, asym_param=asym_param, 
                    redux=1, fix_end_points=False, fix_rng=None, 
                    verbose=True)
    y_als = als.calculate(y)

    assert np.max((y_als)[250:750]) < 0.03

def test_basic_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    rng = np.arange(200,800)
    als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-3, rng=rng,
                                redux=1, fix_end_points=False, fix_rng=None, 
                                verbose=True)

    y_als = als.calculate(y)

    np.testing.assert_almost_equal(y_als[...,rng], 0, decimal=2)
    np.testing.assert_allclose(y_als[:200],0)
    np.testing.assert_allclose(y_als[800:],0)

def test_basic_redux():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    als = SubtractBaselineALS(smoothness_param=1e-2, asym_param=1e-1, 
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    np.testing.assert_almost_equal(y_als, 0, decimal=3)

def test_basic_redux_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    rng = np.arange(200,800)
    als = SubtractBaselineALS(smoothness_param=1e-2, asym_param=1e-1, rng=rng,
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    np.testing.assert_allclose(y_als[:200],0)
    np.testing.assert_allclose(y_als[800:],0)
    np.testing.assert_almost_equal(y_als[...,rng], 0, decimal=3)

def test_2Dbasic_redux_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))
    y = np.dot(np.ones((10,1)), y[None,:])

    rng = np.arange(200,800)
    als = SubtractBaselineALS(smoothness_param=1e-2, asym_param=1e-1, rng=rng,
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    y_als = als.calculate(y)

    np.testing.assert_allclose(y_als[..., :200],0)
    np.testing.assert_allclose(y_als[..., 800:],0)
    np.testing.assert_almost_equal(y_als[...,rng], 0, decimal=3)

def test_2Dbasic_transform_redux_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))
    y = np.dot(np.ones((10,1)), y[None,:])

    rng = np.arange(200,800)
    als = SubtractBaselineALS(smoothness_param=1e-2, asym_param=1e-1, rng=rng,
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)

    als.transform(y)

    np.testing.assert_allclose(y[..., :200],0)
    np.testing.assert_allclose(y[..., 800:],0)
    np.testing.assert_almost_equal(y[...,rng], 0, decimal=3)


def test_vec_asym_param_rng_redux():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    asym_param = 1e-7*np.ones((x.size))

    als = SubtractBaselineALS(smoothness_param=1, asym_param=asym_param, 
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)
    y_als = als.calculate(y)

    assert np.max((y_als)[250:750]) > 7 

    asym_param[200:800] = 1e-1

    als = SubtractBaselineALS(smoothness_param=1, asym_param=asym_param, 
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)
    y_als = als.calculate(y)

    assert np.max((y_als)[250:750]) < 0.03

def test_rng_redux_fix_rng():
    x = np.linspace(-100, 100, 1000)
    y = 10*np.exp(-(x**2/(2*20**2)))

    als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-7, 
                              redux=10, fix_end_points=False, fix_rng=None, 
                              verbose=True)
    y_als = als.calculate(y)

    assert np.max(y_als[250:750]) > 9

    fix_rng = np.arange(200,800)
    
    als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-7, 
                              redux=10, fix_end_points=False, fix_rng=fix_rng, 
                              verbose=True)
    y_als = als.calculate(y)
    assert np.max(y_als[250:750]) < 0.004
    
