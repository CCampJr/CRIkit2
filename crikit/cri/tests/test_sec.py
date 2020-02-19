"""
Testing scale error correction

"""

import numpy as np
import numpy.testing

from crikit.cri.error_correction import ScaleErrCorrectSG

def test_basic():
    x = np.linspace(-100, 100, 1000)
    y = 1/(-x-1j*2) + 0.055
    y /= (0.055/2)

    assert np.allclose(y.real.mean(), 2)

    sec = ScaleErrCorrectSG(win_size=401, order=1, rng=None)

    assert np.abs(sec.calculate(y).real.mean()) < 1.1

def test_basic_transform():
    x = np.linspace(-100, 100, 1000)
    y = 1/(-x-1j*2) + 0.055
    y /= (0.055/2)

    assert np.allclose(y.real.mean(), 2)

    sec = ScaleErrCorrectSG(win_size=401, order=1, rng=None)
    sec.transform(y)
    assert np.abs(y.real.mean()) < 1.1
 
def test_rng():
    x = np.linspace(-100, 100, 1000)
    y = 1/(-x-1j*2) + 0.055
    y /= (0.055/2)

    assert np.allclose(y.real.mean(), 2)

    rng = np.arange(200,800)

    sec = ScaleErrCorrectSG(win_size=401, order=1, rng=rng)
    y_sec = sec.calculate(y)
    assert np.abs(y_sec.real.mean()) < 1.1
    assert np.allclose(y_sec.real[:200], 0)
