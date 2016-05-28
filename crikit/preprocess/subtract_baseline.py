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

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

from crikit.preprocess.algorithms.als import (als_baseline as _als_baseline,
                                              als_baseline_redux as
                                              _als_baseline_redux)
import copy as _copy

def sub_baseline_als(data_obj, ret_difference=True, ret_baseline=False, overwrite=True, **kwargs):
    """
    Subtract baseline using ALS

    """

    if overwrite == False:
        baseline_copy = _np.zeros(data_obj.shape)

    if kwargs.get('redux_factor') is not None:
        als_method = _als_baseline_redux
    else:
        als_method = _als_baseline

    if isinstance(data_obj,_Spectrum):  # Spectrum, Spectra, Hsi
        if data_obj.ndim == 1:
            baseline1, als_alg = als_method(data_obj.data, **kwargs)
            if overwrite:
                data_obj.data -= baseline1
                if ret_baseline:
                    return baseline1
                else:
                    return None
            else:
                if ret_difference == True and ret_baseline == False:
                    return data_obj.data - baseline1
                elif ret_difference == False and ret_baseline == True:
                    return baseline1
                elif ret_difference == True and ret_baseline == True:
                    return (data_obj.data - baseline1, baseline1)
                else:
                    return data_obj.data - baseline1

        elif data_obj.ndim == 2:
            for num, sp in enumerate(data_obj.data):
                baseline1, als_alg = als_method(sp, **kwargs)
                if overwrite:
                    data_obj.data[num,:] -= baseline1
                else:
                    baseline_copy[num,:] = _copy.deepcopy(baseline1)
            if overwrite:
                if ret_baseline:
                    return baseline_copy
                else:
                    return None
            else:
                if ret_difference == True and ret_baseline == False:
                    return data_obj.data - baseline_copy
                elif ret_difference == False and ret_baseline == True:
                    return baseline_copy
                elif ret_difference == True and ret_baseline == True:
                    return (data_obj.data - baseline_copy, baseline_copy)
                else:
                    return data_obj.data - baseline_copy

        elif data_obj.ndim == 3:
            for num_m, sp_line in enumerate(data_obj.data):
                for num_n, sp in enumerate(sp_line):
                    baseline1, als_alg = als_method(sp, **kwargs)
                    if overwrite:
                        data_obj.data[num_m,num_n,:] -= baseline1
                    else:
                        baseline_copy[num_m,num_n,:] = _copy.deepcopy(baseline1)
            if overwrite:
                if ret_baseline:
                    return baseline_copy
                else:
                    return None
            else:
                if ret_difference == True and ret_baseline == False:
                    return data_obj.data - baseline_copy
                elif ret_difference == False and ret_baseline == True:
                    return baseline_copy
                elif ret_difference == True and ret_baseline == True:
                    return (data_obj.data - baseline_copy, baseline_copy)
                else:
                    return data_obj.data - baseline_copy

    elif isinstance(data_obj,_np.ndarray):  # Numpy ndarray
        if data_obj.ndim == 1:
            baseline1, als_alg = als_method(data_obj, **kwargs)
            if overwrite:
                data_obj -= baseline1
                return None
            else:
                return data_obj - baseline1

        elif data_obj.ndim == 2:
            for num, sp in enumerate(data_obj):
                baseline1, als_alg = als_method(sp, **kwargs)
                if overwrite:
                    data_obj[num,:] -= baseline1
                else:
                    baseline_copy[num,:] = _copy.deepcopy(baseline1)
            if overwrite:
                return None
            else:
                return data_obj - baseline_copy

        elif data_obj.ndim == 3:
            for num_m, sp_line in enumerate(data_obj):
                for num_n, sp in enumerate(sp_line):
                    baseline1, als_alg = als_method(sp, **kwargs)
                    if overwrite:
                        data_obj[num_m,num_n,:] -= baseline1
                    else:
                        baseline_copy[num_m,num_n,:] = _copy.deepcopy(baseline1)
            if overwrite:
                return None
            else:
                return data_obj - baseline_copy


if __name__ == '__main__':

    import matplotlib.pyplot as _plt
    sp = _Spectrum()
    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)

    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als(sp, ret_baseline=True, smoothness_param=1e2, asym_param=1e-4)
    _plt.plot(sp.data, label='Detrended')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()
    print('Out.shape: {}'.format(out.shape))

    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)
    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als(sp, redux_factor=10)
    _plt.plot(sp.data, label='Detrended (Redux)')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()

    spa = _Spectra()
    spa.data = _np.dot(_np.ones((2,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])
    _plt.plot(spa.data.T, label='Original')
    out = sub_baseline_als(spa, smoothness_param=1e2, asym_param=1e-4)
    _plt.plot(spa.data.T, label='Detrended')
    _plt.title('Spectra')
    _plt.legend(loc='upper right')
    _plt.show()

    hsi = _Hsi()
    hsi.data = _np.dot(_np.ones((1,1,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])

    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original')
    out = sub_baseline_als(hsi, redux_factor=10, overwrite=False)
    _plt.plot(out.reshape((-1,1000)).T, label='Detrended (Redux)')
    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original (No Overwrite)')
    _plt.title('HSI')
    _plt.legend(loc='upper right')
    _plt.show()