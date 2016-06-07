# -*- coding: utf-8 -*-
"""

Subtract baseline

Created on Sat May 28 00:41:41 2016

@author: chc
"""
if __name__ == '__main__':
    import os as _os
    import sys as _sys
    _sys.path.append(_os.path.abspath('../../'))


import numpy as _np



from crikit.preprocess.algorithms.als import (als_baseline as _als_baseline,
                                              als_baseline_redux as
                                              _als_baseline_redux)
import copy as _copy

def sub_baseline_als(data, ret_difference=True, ret_baseline=False,
                     rng=None, overwrite=True, **kwargs):
    """
    Subtract baseline using ALS

    """

    if overwrite == False:
        shp = list(data.shape)
        if rng is not None:
            shp[-1] = rng.size
        baseline_copy = _np.zeros(shp)

    if kwargs.get('redux_factor') is not None:
        als_method = _als_baseline_redux
    else:
        als_method = _als_baseline

    if data.ndim == 1:
        if rng is None:
            baseline1, als_alg = als_method(data, **kwargs)
        else:
            baseline1, als_alg = als_method(data[...,rng], **kwargs)

        if overwrite:
            if rng is None:
                data -= baseline1
                return None
            else:
                data[..., rng] -= baseline1
                return None
        else:
            if rng is None:
                return data - baseline1
            else:
                return data[..., rng] - baseline1

    elif data.ndim == 2:
        for num, sp in enumerate(data):
            if rng is None:
                baseline1, als_alg = als_method(sp, **kwargs)
            else:
                baseline1, als_alg = als_method(sp[..., rng], **kwargs)
            if overwrite:
                if rng is None:
                    data[num, :] -= baseline1
                else:
                    data[num, rng] -= baseline1
            else:
                baseline_copy[num,:] = _copy.deepcopy(baseline1)
        if overwrite:
            return None
        else:
            if rng is None:
                return data - baseline_copy
            else:
                return data[..., rng] - baseline_copy

    elif data.ndim == 3:
        for num_m, sp_line in enumerate(data):
            for num_n, sp in enumerate(sp_line):
                if rng is None:
                    baseline1, als_alg = als_method(sp, **kwargs)
                else:
                    baseline1, als_alg = als_method(sp[..., rng], **kwargs)

                if overwrite:
                    if rng is None:
                        data[num_m,num_n,:] -= baseline1
                    else:
                        data[num_m, num_n, rng] -= baseline1
                else:
                    baseline_copy[num_m,num_n,:] = _copy.deepcopy(baseline1)
        if overwrite:
            return None
        else:
            if rng is None:
                return data - baseline_copy
            else:
                return data[..., rng] - baseline_copy

if __name__ == '__main__':

    from crikit.data.spectrum import Spectrum as _Spectrum
    from crikit.data.spectra import Spectra as _Spectra
    from crikit.data.hsi import Hsi as _Hsi

    import matplotlib.pyplot as _plt
    sp = _Spectrum()
    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)

    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als(sp.data, ret_baseline=True, smoothness_param=1e2, asym_param=1e-4)
    _plt.plot(sp.data, label='Detrended')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()

    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)
    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als(sp.data, redux_factor=10)
    _plt.plot(sp.data, label='Detrended (Redux)')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()

    spa = _Spectra()
    spa.data = _np.dot(_np.ones((2,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])
    _plt.plot(spa.data.T, label='Original')
    out = sub_baseline_als(spa.data, smoothness_param=1e2, asym_param=1e-4)
    _plt.plot(spa.data.T, label='Detrended')
    _plt.title('Spectra')
    _plt.legend(loc='upper right')
    _plt.show()

    hsi = _Hsi()
    hsi.data = _np.dot(_np.ones((1,1,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])

    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original')
    out = sub_baseline_als(hsi.data, redux_factor=10, overwrite=False)
    _plt.plot(out.reshape((-1,1000)).T, label='Detrended (Redux)')
    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original (No Overwrite)')
    _plt.title('HSI')
    _plt.legend(loc='upper right')
    _plt.show()