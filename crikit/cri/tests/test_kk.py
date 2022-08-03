"""
Testing for Kramers-Kronig Phase Retrieval Method

Using the math relation a^2 / (a^2 + x^2) (Lorentz/Cauchy) has an 
analytical Hilbert transform: x^2 / (a^2 + x^2)-- and how that plays into
the KK

"""

import numpy as np
from numpy.testing import assert_array_almost_equal

from crikit.cri.kk import KramersKronig


def test_kk():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    hilb_y_analytical = x/(2**2 + x**2)
    
    kk = KramersKronig(pad_factor=10)
    kkd = kk.calculate(np.exp(2*y), 0*y + 1)
    
    kkd_angle = np.angle(kkd)
    assert_array_almost_equal(hilb_y_analytical, kkd_angle, decimal=4)

def test_kk_no_bg_norm():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)

    kk = KramersKronig(norm_to_nrb=False)
    kkd = kk.calculate(y, 0*y + 1)

    assert_array_almost_equal(np.abs(kkd), np.sqrt(y))

def test_kk_rng():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)

    rng = np.arange(5, x.size)

    kk = KramersKronig(norm_to_nrb=False, rng=rng)
    kkd = kk.calculate(y, 0*y + 1)

    assert_array_almost_equal(np.abs(kkd[rng]), np.sqrt(y[rng]))

def test_kk_transform():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    y_complex = y.astype(complex)

    kk = KramersKronig(norm_to_nrb=False)
    success = kk._transform(y_complex, 0*y_complex + 1)

    assert success
    assert_array_almost_equal(np.abs(y_complex), np.sqrt(y))

def test_kk_transform_fail():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    y_complex = y.astype(complex)

    kk = KramersKronig(norm_to_nrb=False)
    
    success = kk._transform(y, 0*y + 1)
    assert not success


def test_kk_properties_read():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    hilb_y_analytical = x/(2**2 + x**2)
    
    kk = KramersKronig(pad_factor=10, norm_to_nrb=True, phase_offset=3.0)

    assert kk.pad_factor == 10
    assert kk.norm_to_nrb
    assert kk.phase_offset == 3.0
    
def test_kk_properties_setter():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    hilb_y_analytical = x/(2**2 + x**2)
    
    kk = KramersKronig()
    kk.pad_factor=10
    kk.norm_to_nrb=True
    kk.phase_offset=3.0

    assert kk.pad_factor == 10
    assert kk.norm_to_nrb
    assert kk.phase_offset == 3.0
