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

def sub_dark(data_obj, dark_obj, overwrite=True):
    """
    Subtract dark spectrum.


    Parameters
    ----------
    data_obj : object of class or subclass crikit.data.Spectrum
        Class instance containing data.

    dark_obj : object of class or subclass crikit.data.Spectrum or ndarray
        Class or ndarray containing data.

    overwrite : bool, optional (default=True)
        Overwrite data_cls with new values or simply return result as ndarray.

    Returns
    -------
    ndarray
        Altered data if overwrite is False

    None
        Return None if overwrite is True

    """
    out = data_obj.subtract(dark_obj, overwrite=overwrite)
    return out


if __name__ == '__main__': # pragma: no cover

    import copy as _copy

    x = _np.linspace(0,100,10)
    y = _np.linspace(0,100,10)
    freq = _np.arange(20)
    data = _np.ones((10,10,20))


    hs = _Hsi(data=_copy.deepcopy(data), freq=freq, x=x, y=y)
    spa = _Spectra(data=_copy.deepcopy(data)[0,:,:], freq=freq)
    sp = _Spectrum(data=_copy.deepcopy(data)[0,0,:], freq=freq)

    dark = 0.5*_copy.deepcopy(data)

    print('\n3D----------')
    print('Initial mean: {}'.format(hs.data.mean()))
    #out = sub_mean_over_range(hs, [5,8], overwrite=False)
    #print('Initial mean over range shape: {}'.format(out.shape))
    out = sub_dark(hs, dark, overwrite=True)
    print('Final mean: {}\n'.format(hs.data.mean()))

    print('2D----------')
    print('Initial mean: {}'.format(spa.data.mean()))
    out = sub_dark(spa, dark[0,:,:], overwrite=True)
    print('Final mean: {}\n'.format(spa.data.mean()))

    print('1D----------')
    print('Initial mean: {}'.format(sp.data.mean()))
    out = sub_dark(sp, dark[0,0,:], overwrite=True)
    print('Final mean: {}'.format(sp.data.mean()))
