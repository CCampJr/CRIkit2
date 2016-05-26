# -*- coding: utf-8 -*-
"""
Subtract mean value (optionally, over a range from all spectrum/spectra/hsi)

Created on Thu May 26 14:31:39 2016

@author: chc
"""
if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

import numpy as _np

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

def sub_mean_over_range(data_obj, rng, overwrite=True):
    """
    Subtract the mean intensity over a frequency range (rng). The \
    calculated mean is per spectrum.


    Parameters
    ----------
    data_obj : object of class or subclass crikit.data.Spectrum
        Class instance containing data.

    rng : list
        Frequency range span [start, end]

    overwrite : bool, optional (default=True)
        Overwrite data_cls with new values or simply return result as ndarray.

    Returns
    -------
    ndarray
        Altered data if overwrite is False

    None
        Return None if overwrite is True

    """

    if isinstance(rng, list) == False:
        raise TypeError('rng should be a list with 2 elements')
    elif len(rng) != 2:
        raise TypeError('rng should be a list with 2 elements')
    else:
        pass

    if not isinstance(data_obj,_Spectrum):
        print('data_obj is not of class or subclass _Spectrum')
        return None

    pixrange = data_obj.freq.get_index_of_closest_freq(rng)
    meaner = data_obj.mean(extent=pixrange,over_space=False)

    if overwrite:
        # NOTE order is important
        if isinstance(data_obj, _Hsi):
            data_obj.data -= meaner[:,:,None]
        elif isinstance(data_obj, _Spectra):
            data_obj.data -= meaner[:,None]
        elif isinstance(data_obj, _Spectrum):
            data_obj.data -= meaner
        return None
    else:
        return meaner

if __name__ == '__main__': # pragma: no cover

    import copy as _copy

    x = _np.linspace(0,100,10)
    y = _np.linspace(0,100,10)
    freq = _np.arange(20)
    data = _np.ones((10,10,20))


    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
    spa = _Spectra(data=_copy.deepcopy(data), freq=freq)
    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)

    print('\n3D----------')
    print('Initial mean: {}'.format(hs.data.mean()))
    #out = sub_mean_over_range(hs, [5,8], overwrite=False)
    #print('Initial mean over range shape: {}'.format(out.shape))
    out = sub_mean_over_range(hs, [5,8], overwrite=True)
    print('Final mean: {}\n'.format(hs.data.mean()))

    print('2D----------')
    print('Initial mean: {}'.format(spa.data.mean()))
    out = sub_mean_over_range(spa, [5,8], overwrite=True)
    print('Final mean: {}\n'.format(spa.data.mean()))

    print('1D----------')
    print('Initial mean: {}'.format(sp.data.mean()))
    out = sub_mean_over_range(sp, [5,8], overwrite=True)
    print('Final mean: {}'.format(sp.data.mean()))
#
#    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
#    spa = _Spectra(data=_copy.deepcopy(data), freq=freq)
#    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)
#
#    print('')
#    print('Minuend mean: {}'.format(hs.data.mean()))
#    print('Subtraend mean: {}'.format(sp.data.mean()))
#    out = sub_spect(hs,sp,overwrite=False)
#    print('Difference mean: {}'.format(out.mean()))
#
#    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
#    spa = _Spectra(data=_copy.deepcopy(data), freq=freq)
#    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)
#
#    print('\n3D----------')
#    print('Initial mean: {}'.format(hs.data.mean()))
#    out = sub_mean_over_range(hs, [5,8], overwrite=False)
#    print('Final mean: {}\n'.format(hs.data.mean()))
#
#    print('2D----------')
#    print('Initial mean: {}'.format(spa.data.mean()))
#    out = sub_mean_over_range(spa, [5,8], overwrite=False)
#    print('Final mean: {}\n'.format(spa.data.mean()))
#
#    print('1D----------')
#    print('Initial mean: {}'.format(sp.data.mean()))
#    out = sub_mean_over_range(sp, [5,8], overwrite=False)
#    print('Final mean: {}'.format(sp.data.mean()))
