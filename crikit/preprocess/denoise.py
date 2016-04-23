# -*- coding: utf-8 -*-
"""
Denoising

Created on Fri Apr 22 23:55:22 2016

@author: chc
"""

__all__ = ['anscombe, anscombe_inverse']

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))

import timeit as _timeit
import copy as _copy

import numpy as _np
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

from numpy.linalg import svd as _svd

def svd(data_obj, svs=None, overwrite=False):
    """
    Compute the SVD of a signal and return the exact or de-noised version

    Parameters
    ----------
    data_obj : Spectra or Hsi object or (2D or 3D) ndarray.
        Spectral data object or ndarray.

    svs : list, ndarray (1D)
        List of singular values (sv's) to keep

    Returns
    -------
    [ndarray, ndarray, ndarray]
        U, s, Vh from SVD if overwrite is True
        data_obj.data will be overwritten by U*S*Vh

    ndarray, [ndarray, ndarray, ndarray]
        U*S*Vh, [U, s, Vh] from SVD if overwrite is False. See Notes.

    Notes
    -----

    U : ndarray (2D)
        U-component from SVD decomposition (spatial componenet with crikit)

    Vh : ndarray (2D)
        Vh-component from SVD decomposition (spectral componenet with crikit).
        NOTE: this is the Hermitial/conjugate transpose of the normal
        V-component in SVD

    s : ndarray (1D)
        Diagonal elements of S-matrix describing the relative contributions
        of each singular value

    S : ndarray (2D)
        S-matrix derived from s

    References
    ----------

    """
    if isinstance(data_obj,_Spectrum):
        if type(data_obj) == _Spectra:
            U,s,Vh = _svd(data_obj.data, full_matrices=False)
        elif type(data_obj) == _Hsi:
            U,s,Vh = _svd(data_obj.data.reshape((-1,data_obj.f_pix)), full_matrices=False)
        else:
            raise TypeError('data_obj should be of Spectra or Hsi classes or an ndarray')

    elif isinstance(data_obj, _np.ndarray):
        data_obj = _np.squeeze(data_obj)
        if data_obj.ndim == 2:
            U,s,Vh = _svd(data_obj.data, full_matrices=False)
        elif data_obj.ndim == 3:
            U,s,Vh = _svd(data_obj.reshape((-1,data_obj.shape[-1])), full_matrices=False)
        else:
            raise TypeError('ndarray should be 2D or 3D')
    else:
        raise TypeError('data_obj should be of Spectra or Hsi classes or an ndarray')

    if svs is None: # Keep all s-entries
        s_ret = _copy.deepcopy(s)
        S = _np.diag(s_ret)
        print('Here')
    else:  # Certain s-entries specified to keep
        s_ret = _np.zeros(s.shape)
        s_ret[svs] = s[svs]
        S = _np.diag(s_ret)

    # Note: one could just reshape all objects, but that is actually slower
    # than just testing
    if isinstance(data_obj, _np.ndarray):
        if overwrite == False:
            if data_obj.ndim == 2:
                return _np.dot(U,_np.dot(S,Vh)), [U, s_ret, Vh]
            else:
                return _np.reshape(_np.dot(U,_np.dot(S,Vh)), data_obj.shape), [U, s_ret, Vh]
        else:
            if data_obj.ndim == 2:
                # NOTE: In a pass-by-value situation, like this, need to perform
                # in-line math to overwrite the variable
                data_obj *= 0
                data_obj += _np.dot(U,_np.dot(S,Vh))
                return [U, s_ret, Vh]
            else:
                data_obj *= 0
                data_obj += _np.reshape(_np.dot(U,_np.dot(S,Vh)), data_obj.shape)
                return [U, s_ret, Vh]
    else:  # Is a _Spectrum sub-class
        if overwrite == False:
            if type(data_obj) == _Spectra:
                return _np.dot(U,_np.dot(S,Vh)), [U, s_ret, Vh]
            elif type(data_obj) == _Hsi:
                return _np.reshape(_np.dot(U,_np.dot(S,Vh)), data_obj.shape), [U, s_ret, Vh]
#            else:
#                raise TypeError('data_obj should be of Spectra or Hsi classes or an ndarray')
        else:
            if type(data_obj) == _Spectra:
                data_obj.data = _np.dot(U,_np.dot(S,Vh))
                return [U, s_ret, Vh]
            elif type(data_obj) == _Hsi:
                data_obj.data = _np.reshape(_np.dot(U,_np.dot(S,Vh)), data_obj.shape)
                return [U, s_ret, Vh]
#            else:
#                raise TypeError('data_obj should be of Spectra or Hsi classes or an ndarray')

if __name__ == '__main__':  # pragma: no cover
    y = _np.random.randn(100,1000)
    y2, [U,s,Vh] = svd(y,svs=[])
    print('0 singular values selected...')
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y2,0) == True))
    y2, [U,s,Vh] = svd(y,svs=[0])
    print('\n1 singular value selected...')
    print('Returns matrix is NOT all 0\'s: {}'.format(_np.allclose(y2,0) == False))
    print('Return matrix is all based on 1 component: {}'.format(_np.isclose(\
        _np.median(y2[0,:]/y2[50,:]),y2[0,0]/y2[50,0])))

    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,10,1000)
    y2, [U,s,Vh] = svd(y,svs=[])
    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,1000)
    y_copy = _copy.deepcopy(y)

    [U,s,Vh] = svd(y,svs=[],overwrite=True)

    print('\nOverwrite input data...')
    print('0 singular values selected...')
    print('Input is same as output: {}'.format(_np.allclose(y,y_copy)))
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y,0) == True))

#    y = _np.random.randn(100,1000)
#    y_obj = _Spectra(y)
#    print(y_obj.data)
#    [U,s,Vh] = svd(y_obj,svs=[],overwrite=True)
#    print(y_obj.data)
