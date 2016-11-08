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

import copy as _copy

import numpy as _np

from crikit.preprocess.algorithms.als import (als_baseline as _als_baseline,
                                              als_baseline_redux as
                                              _als_baseline_redux)

from crikit.utils.datacheck import _rng_is_pix_vec


class SubtractBaselineALS:
    """
    Subtract baseline using asymmetric least squares algorithm
    
    Parameters
    ----------
    smoothness_param : float, optional (default=1.0)
        Smoothness parameter aka 'lambda'
        
    asym_param : float, optional (default=1e-2)
        Asymmetry parameter aka 'p'
        
    redux_factor : int, optional (default=10)
        Down-sampling factor (more down-sampling leads to faster detrending,
        but with more chance of non-optimal detrending)
        
    rng : ndarray (1D), optional (default=None)
        Range in pixels to perform action over
    
    use_imag : bool, optional (default=True)
        If spectrum(a) are complex-values, use the imaginary portion?
    """
    def __init__(self, smoothness_param=1.0, asym_param=1e-2,
                 redux_factor=10, rng=None, use_imag=True, **kwargs):

        self.smoothness_param = smoothness_param
        self.asym_param = asym_param
        self.redux_factor = redux_factor

        self.rng = _rng_is_pix_vec(rng)
        self.use_imag = use_imag
        
        self._k = {}
        self._k.update(kwargs)

    @property
    def redux_factor(self):
        return self._rf

    @redux_factor.setter
    def redux_factor(self, value):
        if value is None or value <= 1:
            self._rf = None
            self._als_method = _als_baseline
        else:
            self._rf = value
            self._als_method = _als_baseline_redux

    def _calc(self, data, ret_obj, **kwargs):
        try:
            # Get the subarray shape
            shp = data.shape[0:-1]
#            print('kwargs: {}'.format(kwargs))
            # Iterate over the sub-array -- super slick way of doing it
            for idx in _np.ndindex(shp):
                # Imaginary portion set
                if self.use_imag and _np.iscomplexobj(data):
                    ret_obj[idx] -= 1j*self._als_method(data[idx].imag, smoothness_param=self.smoothness_param,
                                                asym_param=self.asym_param,
                                                redux_factor=self.redux_factor,
                                                **kwargs)[0]
                else:  # Real portion set or real object
                    ret_obj[idx] -= self._als_method(data[idx].real, smoothness_param=self.smoothness_param,
                                                asym_param=self.asym_param,
                                                redux_factor=self.redux_factor,
                                                **kwargs)[0]
        except:
            return False
        else:
            return True

    def transform(self, data, **kwargs):
        success = self._calc(data, ret_obj=data, **kwargs)
        return success

    def calculate(self, data, **kwargs):

        data_copy = _copy.deepcopy(data)
        success = self._calc(data, ret_obj=data_copy, **kwargs)
        if success:
            return data_copy
        else:
            return None


if __name__ == '__main__':

    from crikit.data.spectrum import Spectrum as _Spectrum
    from crikit.data.spectra import Spectra as _Spectra
    from crikit.data.hsi import Hsi as _Hsi

    import matplotlib.pyplot as _plt
    sp = _Spectrum()
    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)

    sub_baseline_als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-1)

    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als.transform(sp.data)
    _plt.plot(sp.data, label='Detrended')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()

    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)
    _plt.plot(sp.data, label='Original')
    sub_baseline_als.redux_factor = 10
    out = sub_baseline_als.transform(sp.data)
    _plt.plot(sp.data, label='Detrended (Redux)')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()
#
    spa = _Spectra()
    sub_baseline_als = SubtractBaselineALS(smoothness_param=1e2, asym_param=1e-4)
    spa.data = _np.dot(_np.ones((2,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])
    _plt.plot(spa.data.T, label='Original')
    out = sub_baseline_als.transform(spa.data)
    _plt.plot(spa.data.T, label='Detrended')
    _plt.title('Spectra')
    _plt.legend(loc='upper right')
    _plt.show()

    hsi = _Hsi()
    sub_baseline_als.redux_factor = 10
    hsi.data = _np.dot(_np.ones((1,1,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])

    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original')
    out = sub_baseline_als.calculate(hsi.data)
    _plt.plot(out.reshape((-1,1000)).T, label='Detrended (Redux)')
    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original (No Overwrite)')
    _plt.title('HSI')
    _plt.legend(loc='upper right')
    _plt.show()