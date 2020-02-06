"""
Testing for Kramers-Kronig Phase Retrieval Method

Using the math relation a^2 / (a^2 + x^2) (Lorentz/Cauchy) has an 
analytical Hilbert transform: x^2 / (a^2 + x^2)-- and how that plays into
the KK

"""

import numpy as np
from numpy.testing import assert_array_almost_equal

from crikit.cri.algorithms.kk import kkrelation


def test_kk():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    hilb_y_analytical = x/(2**2 + x**2)
    kkd = kkrelation(0*y + 1, np.exp(2*y), pad_factor=10)
    kkd_angle = np.angle(kkd)
    assert_array_almost_equal(hilb_y_analytical, kkd_angle, decimal=4)

def test_kk_conjugate():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    hilb_y_analytical = -1 * (x/(2**2 + x**2))
    kkd = kkrelation(0*y + 1, np.exp(2*y), pad_factor=10, conjugate=True)
    kkd_angle = np.angle(kkd)
    assert_array_almost_equal(hilb_y_analytical, kkd_angle, decimal=4)

def test_kk_no_bg_norm():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)

    kkd = kkrelation(0*y + 1, y, norm_to_nrb=False)
    assert_array_almost_equal(np.abs(kkd), np.sqrt(y))

def test_kk_3d():
    x = np.linspace(-100, 100, 1000)
    y = 2/(2**2 + x**2)
    y = y[:, None, None]

    kkd = kkrelation(0*y + 1, y, norm_to_nrb=False)
    assert_array_almost_equal(np.abs(kkd), np.sqrt(y))
