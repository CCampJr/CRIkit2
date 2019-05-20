"""
Subtract mean value (optionally, over a range from all spectrum/spectra/hsi)

Note: If dark > 1D, averaged -- even if data has same shape.
"""

import numpy as _np
import copy as _copy

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

from crikit.utils.general import (expand_1d_to_ndim as _expand_1d_to_ndim,
                                  mean_nd_to_1d as _mean_nd_to_1d)

class SubtractDark:
    def __init__(self, dark):
        self.dark = dark

    def transform(self, data):
        """
        Subtract dark spectrum (overwrite original data).


        Parameters
        ----------
        data : ndarray
            Data from which dark is subtracted.

        Returns
        -------
        bool
            Returns the success state (True=success)

        """

        if not _np.can_cast(self.dark.dtype, data.dtype):
            err_str1 = 'Cannot transform input data type {}'.format(data.dtype)
            err_str2 = ' with dark type {}'.format(self.dark.dtype)
            raise TypeError(err_str1 + err_str2)

        success = self._calc(data, ret_obj=data)
        return success


    def calculate(self, data):
        """
        Subtract dark spectrum (return copy).

        Parameters
        ----------
        data : ndarray
            Data from which dark is subtracted.

        Returns
        -------
        ndarray
            Returns data with dark subtracted (or None if fails)

        """
        data_copy = _copy.deepcopy(data)
        success = self._calc(data, ret_obj=data_copy)
        if success:
            return data_copy
        else:
            return None

    def _calc(self, data, ret_obj):
        # Assume that an nD dark should be averaged to be 1D
        self.dark = _mean_nd_to_1d(self.dark, axis=-1)

        # Expand dark dimensionality to match data.ndim
        self.dark = _expand_1d_to_ndim(self.dark, data.ndim)

        ret_obj -= self.dark
        return True


if __name__ == '__main__': # pragma: no cover

    x = _np.linspace(0,100,10)
    y = _np.linspace(0,100,10)
    freq = _np.arange(20)
    data = _np.ones((10,10,20))

    # OVERWRITE TEST
    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
    spa = _Spectra(data=_copy.deepcopy(data)[0,:,:], freq=freq)
    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)

    dark=0.5 * _copy.deepcopy(data)
    dark_sub = SubtractDark(dark)

    print('\n---------TRANSFORM TEST----------\n')
    print('\n3D----------')
    print('Initial mean: {}'.format(hs.data.mean()))
    out = dark_sub.transform(hs.data)
    print('Success?: {}'.format(out))
    print('Final mean: {}\n'.format(hs.data.mean()))

    print('2D----------')
    print('Initial mean: {}'.format(spa.data.mean()))
    out = dark_sub.transform(spa.data)
    print('Success?: {}'.format(out))
    print('Final mean: {}\n'.format(spa.data.mean()))

    print('1D----------')
    print('Initial mean: {}'.format(sp.data.mean()))
    out = dark_sub.transform(sp.data)
    print('Success?: {}'.format(out))
    print('Final mean: {}'.format(sp.data.mean()))

    # NOT-OVERWRITE TEST
    print('\n---------CALCULATE TEST----------\n')

    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
    spa = _Spectra(data=_copy.deepcopy(data)[0,:,:], freq=freq)
    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)

    dark=0.5 * _copy.deepcopy(data)
    dark_sub = SubtractDark(dark)

    print('\n3D----------')
    print('Initial Data Mean: {}'.format(hs.data.mean()))
    out = dark_sub.calculate(hs.data)
    print('Returned Mean: {}'.format(out.mean()))
    print('Final Data Mean: {}'.format(hs.data.mean()))

    print('2D----------')
    print('Initial Data Mean: {}'.format(spa.data.mean()))
    out = dark_sub.calculate(spa.data)
    print('Returned Mean: {}'.format(out.mean()))
    print('Final Data Mean: {}'.format(spa.data.mean()))

    print('1D----------')
    print('Initial Data Mean: {}'.format(sp.data.mean()))
    out = dark_sub.calculate(sp.data)
    print('Returned Mean: {}'.format(out.mean()))
    print('Final Data Mean: {}'.format(sp.data.mean()))
