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

from crikit.utils.gen_utils import find_nearest as _find_nearest

def sub_mean_over_range(data, rng, freq=None, overwrite=True):
    """
    Subtract the mean intensity over a frequency range (rng). The \
    calculated mean is per spectrum.


    Parameters
    ----------
    data : ndarray
        Input data.

    rng : list or tuple
        Frequency range span [start, end]

    freq : ndarray (1D), optional
        Frequency vector to find range (rng). Pixel numbers used if freq is \
        None

    overwrite : bool, optional (default=True)
        Overwrite data with new values or simply return result as ndarray.

    Returns
    -------
    ndarray
        Altered data if overwrite is False

    None
        Return None if overwrite is True

    """

    # Check that rng is list or tuple
    if isinstance(rng, (list, tuple)) == False:
        raise TypeError('rng should be a list/tuple with 2 elements')
    if len(rng) != 2:
        raise TypeError('rng should be a list/tuple with 2 elements')

    if freq is None:
        freq = _np.arange(data.shape[-1])

    pixrange = _find_nearest(freq,rng)[-1]
    pixrange[-1] += 1 # To make inclusive

    # Mean over frequency range
    meaner = data[...,pixrange].mean(axis=-1)

    if overwrite:
        data -= meaner[...,None]
        return None
    else:
        return meaner

if __name__ == '__main__': # pragma: no cover

    from crikit.data.spectrum import Spectrum as _Spectrum
    from crikit.data.spectra import Spectra as _Spectra
    from crikit.data.hsi import Hsi as _Hsi

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
    out = sub_mean_over_range(hs.data, [5,8], overwrite=True)
    print('Final mean: {}\n'.format(hs.data.mean()))

    print('2D----------')
    print('Initial mean: {}'.format(spa.data.mean()))
    out = sub_mean_over_range(spa.data, [5,8], overwrite=True)
    print('Final mean: {}\n'.format(spa.data.mean()))

    print('1D----------')
    print('Initial mean: {}'.format(sp.data.mean()))
    out = sub_mean_over_range(sp.data, [5,8], overwrite=True)
    print('Final mean: {}'.format(sp.data.mean()))
