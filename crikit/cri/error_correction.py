# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 11:20:35 2016

@author: chc
"""

if __name__ == '__main__':
    import os as _os
    import sys as _sys
    _sys.path.append(_os.path.abspath('../../'))


import numpy as _np
import numexpr as _ne
from scipy.signal import savgol_filter as _sg

from crikit.cri.algorithms.kk import hilbertfft as _hilbert

from crikit.preprocess.algorithms.als import (als_baseline as _als_baseline,
                                              als_baseline_redux as
                                              _als_baseline_redux)
import copy as _copy


def phase_err_correct_als(data, overwrite=True, **kwargs):
    """
    Phase error correction using alternating least squares (ALS)

    Reference
    ---------
    * C H Camp Jr, Y J Lee, and M T Cicerone, JRS (2016).
    """
    assert issubclass(data.dtype.type, _np.complex)

    if kwargs.get('redux_factor') is not None:
        als_method = _als_baseline_redux
    else:
        als_method = _als_baseline

    ph = _np.unwrap(_np.angle(data))
    err_phase,_ = als_method(ph, **kwargs)

    h = _hilbert(err_phase)
    correction_factor = _ne.evaluate('1/exp(imag(h)) * exp(-1j*err_phase)')

    if overwrite:
        data *= correction_factor
        return None
    else:
        return data*correction_factor

def scale_err_correct_sg(data, win_size=601, order=2, overwrite=True, **kwargs):
    """
    Scale error correction using Savitky-Golay

    Reference
    ---------
    * C H Camp Jr, Y J Lee, and M T Cicerone, JRS (2016).
    """
    correction_factor = (1/_sg(data.real, window_length=win_size,
                               polyorder=order, axis=-1))

    if overwrite:
        data *= correction_factor
        return None
    else:
        return data * correction_factor


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from crikit.cri.kk import kk
    import timeit

    SPECT_LEN = 878
    WN = _np.linspace(4000,500,SPECT_LEN)
    chi = 1/((WN - 1000 -1j*10)) + 1/((WN - 1020 -1j*10)) + \
            1/((WN - 2800 -1j*10))
    chiNR = 0*chi + 0.055
    exc = WN
    sig = _np.abs(chi + chiNR)**2

    sigNR = _np.abs(chiNR)**2
    sigRef = chiNR*(WN/1e3)**.5

    NUM_REPS = 10
    sig = _np.dot(_np.ones((NUM_REPS,NUM_REPS, 1)),sig[None,:])

    kkd = kk(sig, sigRef)
    kkd2 = kk(sig, sigRef)

    start = timeit.default_timer()
    phase_err_correct_als(kkd)
    stop = timeit.default_timer()
    print((stop-start)/NUM_REPS**2)

    start = timeit.default_timer()
    ph2 = phase_err_correct_als(kkd2, redux_factor=10)
    stop = timeit.default_timer()
    print((stop-start)/NUM_REPS**2)

#    plt.plot(ph1.real.T)
#    plt.plot(ph2.real.T)
#    plt.show()
