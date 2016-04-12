# -*- coding: utf-8 -*-
"""
Spectral preprocessing

Created on Tue Apr 12 16:13:15 2016

@author: chc
"""
if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))

import numpy as _np

#from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi
from crikit.utils.gen_utils import find_nearest as _find_nearest

def sub_mean_over_range(data_obj, rng, overwrite=True, f = None):
    """
    Subtract the mean intensity over a frequency range (rng). The \
    calculated mean is per spectrum.


    Parameters
    ----------
    data_obj : object or ndarray
        Class or ndarray containing data. Compatible object types given in \
        Notes. If data_obj is ndarray, f must be provided.

    rng : list
        Frequency range span [start, end]

    overwrite : bool, optional
        Overwrite data_cls with new values or simply return result as ndarray

    f : 1D ndarray
        Frequency (or other) 1D ndarray from which rng will be selected.

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

    if isinstance(data_obj,_Spectrum):  # True if type Spectrum **OR** a subclass of Spectrum
        ndim = data_obj.ndim
        pixrange = [data_obj.freq.get_index_of_closest_freq(rng[0]),
                    data_obj.freq.get_index_of_closest_freq(rng[1])]

        if ndim == 1:
            meaner1 = data_obj.data[pixrange].mean(axis=-1)
            if overwrite == True:
                data_obj.data -= meaner1
                return None
            else:
                return data_obj.data - meaner1
        elif ndim == 2:
            meaner2 = data_obj.data[:,pixrange].mean(axis=-1)
            if overwrite == True:
                data_obj.data -= meaner2[:,None]
                return None
            else:
                return data_obj.data - meaner2[:,None]
        elif ndim == 3:
            meaner3 = data_obj.data[:,:,pixrange].mean(axis=-1)
            if overwrite == True:
                data_obj.data -= meaner3[:,:,None]
                return None
            else:
                return data_obj.data - meaner3[:,:,None]
        else:
            raise NotImplementedError('Only 1D to 3D data_obj is currently \
            supported')

    elif isinstance(data_obj, _np.ndarray):
        if isinstance(f, _np.ndarray):
            ndim = data_obj.ndim
            pixrange = [_find_nearest(f,rng[0])[1],_find_nearest(f,rng[1])[1]]

            if ndim == 1:
                meaner1 = data_obj[pixrange].mean(axis=-1)
                if overwrite == True:
                    data_obj -= meaner1
                    return None
                else:
                    return data_obj - meaner1
            elif ndim == 2:
                meaner2 = data_obj[:,pixrange].mean(axis=-1)
                if overwrite == True:
                    data_obj -= meaner2[:,None]
                    return None
                else:
                    return data_obj - meaner2[:,None]
            elif ndim == 3:
                meaner3 = data_obj[:,:,pixrange].mean(axis=-1)
                if overwrite == True:
                    data_obj -= meaner3[:,:,None]
                    return None
                else:
                    return data_obj - meaner3[:,:,None]
            else:
                raise NotImplementedError('Only 1D to 3D data_obj is currently \
                supported')
        else:
            raise TypeError('f parameter required if data_obj is ndarray')
    else:
        raise TypeError('data_obj should be a supported class instance or of type ndarray')

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
