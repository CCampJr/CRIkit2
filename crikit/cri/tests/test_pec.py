"""
Testing Phase error correction

"""

import numpy as np
import numpy.testing

from crikit.cri.error_correction import PhaseErrCorrectALS

def test_basic():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    assert np.sum((phi_peak-phi)**2) > 265.0
    
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                             redux=1, fix_end_points=False, fix_rng=None, 
                             verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    # RSS
    assert np.sum((phi_peak-phi_pec)**2) < 4.7

def test_basic2D():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)
    y = np.dot(np.ones((10,1)), y[None,:])
    # RSS
    assert np.sum((phi_peak-phi)**2) > 265.0
    
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=False, fix_rng=None, 
                                verbose=True, use_prev=False)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    # RSS
    np.testing.assert_array_less(np.sum((phi_peak-phi_pec)**2, axis=-1), 4.7)

def test_basic3D():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)
    y = np.dot(np.ones((9,1)), y[None,:]).reshape((3,3,-1))

    # RSS
    assert np.sum((phi_peak-phi)**2) > 265.0
    
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=False, fix_rng=None, 
                                verbose=True, use_prev=False)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    # RSS
    np.testing.assert_array_less(np.sum((phi_peak-phi_pec)**2, axis=-1), 4.7)


def test_fix_ends():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    assert np.sum((phi_peak-phi)**2) > 265.0
    
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=True, fix_rng=None, 
                                verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    # RSS
    assert np.sum((phi_peak-phi_pec)**2) < 3.3

def test_rng():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    rng = np.arange(200, 800)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=True, rng=rng, 
                                verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    
    assert np.allclose(np.sum(phi_pec[:200]),0)
    # RSS
    assert np.sum((phi_peak-phi_pec)**2) < 3.1

def test_transform_rng():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    rng = np.arange(200, 800)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=True, rng=rng, 
                                verbose=True)

    pec.transform(y)
    phi_pec = np.unwrap(np.angle(y))

    
    assert np.allclose(np.sum(phi_pec[:200]),0)
    # RSS
    assert np.sum((phi_peak-phi_pec)**2) < 3.1
    
def test_fix_rng():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    fix_rng = np.arange(x.size)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-8, 
                                redux=1, fix_end_points=True, fix_rng=fix_rng, 
                                verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    assert np.max(np.abs(phi_pec)) < 0.015

def test_rng_redux():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)

    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    rng = np.arange(200,800)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-4, 
                             redux=10, fix_end_points=True, rng=rng, 
                             verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    assert np.allclose(np.sum(phi_pec[:200]),0)
    # RSS
    assert np.sum((phi_peak-phi_pec)**2) < 3.1

def test_rng_redux2D():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)
    y = np.dot(np.ones((10,1)), y[None,:])
    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    rng = np.arange(200,800)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-4, 
                             redux=10, fix_end_points=True, rng=rng, 
                             verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    assert np.allclose(np.sum(phi_pec[...,:200], axis=-1),0)
    # RSS
    np.testing.assert_array_less(np.sum((phi_peak-phi_pec)**2, axis=-1), 3.1)


def test_rng_redux3D():
    x = np.linspace(-100, 100, 1000)

    phi_peak = 10*np.imag(1/(25-x-1j*2))
    phi_bg = np.exp(-x**2/(2*30**2))
    phi =  phi_peak + phi_bg
    y = 1*np.exp(1j*phi)
    y = np.dot(np.ones((9,1)), y[None,:]).reshape((3,3,-1))
    # RSS
    # assert np.sum((phi_peak-phi)**2) > 265.0
    
    rng = np.arange(200,800)
    pec = PhaseErrCorrectALS(smoothness_param=1, asym_param=1e-4, 
                             redux=10, fix_end_points=True, rng=rng, 
                             verbose=True)

    y_pec = pec.calculate(y)
    phi_pec = np.unwrap(np.angle(y_pec))

    assert np.allclose(np.sum(phi_pec[...,:200], axis=-1),0)
    # RSS
    np.testing.assert_array_less(np.sum((phi_peak-phi_pec)**2, axis=-1), 3.1)
    
# def test_fix_rng():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))
#     fix_rng = np.arange(200,800)

#     als = AlsCvxopt(smoothness_param=1e3, asym_param=1e-5, 
#                     redux=1, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max((y - y_als)[200:800]) > 0.002

#     als = AlsCvxopt(smoothness_param=1e3, asym_param=1e-5, 
#                     redux=1, fix_end_points=False, fix_rng=fix_rng, 
#                     verbose=True)
#     y_als = als.calculate(y)
#     assert np.max((y - y_als)[200:800]) < 0.002

# def test_vec_asym_param():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     asym_param = 1e-6*np.ones((x.size))

#     als = AlsCvxopt(smoothness_param=1e3, asym_param=asym_param, 
#                     redux=1, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max((y - y_als)[250:750]) > 7 

#     asym_param[200:800] = 1e-2

#     als = AlsCvxopt(smoothness_param=1e3, asym_param=asym_param, 
#                     redux=1, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max((y - y_als)[250:750]) < 0.03

# def test_basic_rng():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     rng = np.arange(200,800)
#     als = AlsCvxopt(smoothness_param=1, asym_param=1e-3, rng=rng,
#                     redux=1, fix_end_points=False, fix_rng=None, 
#                     verbose=True)

#     y_als = als.calculate(y)

#     np.testing.assert_almost_equal(y[...,rng], y_als[...,rng], decimal=2)
#     np.testing.assert_allclose(y_als[:200],0)
#     np.testing.assert_allclose(y_als[800:],0)

# def test_basic_redux():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     als = AlsCvxopt(smoothness_param=1e-2, asym_param=1e-1, 
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)

#     y_als = als.calculate(y)

#     np.testing.assert_almost_equal(y, y_als, decimal=3)

# def test_basic_redux_rng():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     rng = np.arange(200,800)
#     als = AlsCvxopt(smoothness_param=1e-2, asym_param=1e-1, rng=rng,
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)

#     y_als = als.calculate(y)

#     np.testing.assert_allclose(y_als[:200],0)
#     np.testing.assert_allclose(y_als[800:],0)
#     np.testing.assert_almost_equal(y[...,rng], y_als[...,rng], decimal=3)

# def test_2Dbasic_redux_rng():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))
#     y = np.dot(np.ones((10,1)), y[None,:])

#     rng = np.arange(200,800)
#     als = AlsCvxopt(smoothness_param=1e-2, asym_param=1e-1, rng=rng,
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)

#     y_als = als.calculate(y)

#     np.testing.assert_allclose(y_als[..., :200],0)
#     np.testing.assert_allclose(y_als[..., 800:],0)
#     np.testing.assert_almost_equal(y[...,rng], y_als[...,rng], decimal=3)


# def test_vec_asym_param_rng_redux():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     asym_param = 1e-7*np.ones((x.size))

#     als = AlsCvxopt(smoothness_param=1, asym_param=asym_param, 
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max((y - y_als)[250:750]) > 7 

#     asym_param[200:800] = 1e-1

#     als = AlsCvxopt(smoothness_param=1, asym_param=asym_param, 
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max((y - y_als)[250:750]) < 0.03

# def test_rng_redux_fix_rng():
#     x = np.linspace(-100, 100, 1000)
#     y = 10*np.exp(-(x**2/(2*20**2)))

#     als = AlsCvxopt(smoothness_param=1, asym_param=1e-7, 
#                     redux=10, fix_end_points=False, fix_rng=None, 
#                     verbose=True)
#     y_als = als.calculate(y)

#     assert np.max(y[250:750] - y_als[250:750]) > 9

#     fix_rng = np.arange(200,800)
    
#     als = AlsCvxopt(smoothness_param=1, asym_param=1e-7, 
#                     redux=10, fix_end_points=False, fix_rng=fix_rng, 
#                     verbose=True)
#     y_als = als.calculate(y)
#     assert np.max(y[250:750] - y_als[250:750]) < 0.004
    
