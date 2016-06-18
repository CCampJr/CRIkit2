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
    def __init__(self, rng=None):
        self.rng = _rng_is_pix_vec(rng)
        self.redux_factor = None
        self.smoothness_param = None
        self.asym_param = None

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

            # Iterate over the sub-array -- super slick way of doing it
            for count in _np.ndindex(shp):
                ret_obj[count] -= self._als_method(data[count], smoothness_param=self.smoothness_param,
                                                asym_param=self.asym_param,
                                                redux_factor=self.redux_factor,
                                                **kwargs)[0]
        except:
            return False
        else:
            return True

    def transform(self, data, smoothness_param=1, asym_param=1e-2,
                  redux_factor=10, **kwargs):
        self.redux_factor = redux_factor
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param

        success = self._calc(data, ret_obj=data, **kwargs)
        return success

    def calculate(self, data, smoothness_param=1, asym_param=1e-2,
                  redux_factor=10, **kwargs):
        self.redux_factor = redux_factor
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param

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

    sub_baseline_als = SubtractBaselineALS()

    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als.transform(sp.data, smoothness_param=1, asym_param=1e-1)
    _plt.plot(sp.data, label='Detrended')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()

    sp.data = _np.exp(-(_np.arange(1000)-500)**2/100**2)
    _plt.plot(sp.data, label='Original')
    out = sub_baseline_als.transform(sp.data, redux_factor=10)
    _plt.plot(sp.data, label='Detrended (Redux)')
    _plt.title('Spectrum')
    _plt.legend(loc='best')
    _plt.show()
#
    spa = _Spectra()
    spa.data = _np.dot(_np.ones((2,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])
    _plt.plot(spa.data.T, label='Original')
    out = sub_baseline_als.transform(spa.data, smoothness_param=1e2, asym_param=1e-4)
    _plt.plot(spa.data.T, label='Detrended')
    _plt.title('Spectra')
    _plt.legend(loc='upper right')
    _plt.show()

    hsi = _Hsi()
    hsi.data = _np.dot(_np.ones((1,1,1)),_np.exp(-(_np.arange(1000)-500)**2/100**2)[None,:])

    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original')
    out = sub_baseline_als.calculate(hsi.data, redux_factor=10)
    _plt.plot(out.reshape((-1,1000)).T, label='Detrended (Redux)')
    _plt.plot(hsi.data.reshape((-1,1000)).T, label='Original (No Overwrite)')
    _plt.title('HSI')
    _plt.legend(loc='upper right')
    _plt.show()