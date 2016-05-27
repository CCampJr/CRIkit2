# -*- coding: utf-8 -*-
"""
Denoising

Created on Fri Apr 22 23:55:22 2016

@author: chc
"""

__all__ = ['svd_decompose', 'svd_recompose']

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

import copy as _copy

import numpy as _np
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

from numpy.linalg import svd as _svd

def svd_decompose(data_obj):
    """
    Compute the SVD of a signal (just wraps numpy.linalg.svd) i.e., decompose \
    the input into components.

    Parameters
    ----------
    data_obj : Spectra or Hsi object or (2D or 3D) ndarray.
        Spectral data object or ndarray.

    Returns
    -------
    ndarray, ndarray, ndarray
        U, s, Vh

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

    return [U, s, Vh]

def svd_recompose(U,s,Vh, data_obj=None, svs=None, overwrite=False):
    """
    Reconstruct the original data using the SVD components. The reconstructed \
    signal shape is 2D (or if provided) or matches data_obj.

    Parameters
    ----------
    U : ndarray (2D)
        U-component from SVD decomposition (spatial componenet with crikit)

    s : ndarray (1D)
        Diagonal elements of S-matrix describing the relative contributions
        of each singular value

    Vh : ndarray (2D)
        Vh-component from SVD decomposition (spectral componenet with crikit).
        NOTE: this is the Hermitial/conjugate transpose of the normal
        V-component in SVD

    data_obj : Spectra or Hsi object or (2D or 3D) ndarray.
        Spectral data object or ndarray.

    overwrite : bool, optional (default=True)
        Overwrite the original data in data_obj

    Returns
    -------
    ndarray (2D or 3D)
        Recomposed data (U*S*Vh). If data_obj is not None, returned object \
        shape matches data_obj. Else 2D.

    None
        Returns None if overwrite is True and overwrites input data_obj.

    Notes
    -----

    S : ndarray (2D)
        S-matrix derived from s

    References
    ----------

    """
    if not isinstance(U, _np.ndarray):
        raise TypeError('U should be of type ndarray')
    if not isinstance(Vh, _np.ndarray):
        raise TypeError('Vh should be of type ndarray')
    if not isinstance(s, _np.ndarray):
        raise TypeError('s should be of type ndarray')
    if data_obj is not None:
        if isinstance(data_obj, _Spectrum):
            pass
        elif isinstance(data_obj, _np.ndarray):
            pass
        else:
            raise TypeError('data_obj should be of type ndarray or a subclass of Spectrum')

    if _np.squeeze(s).ndim == 2:
        s_vec = _np.diag(s)
    elif _np.squeeze(s).ndim == 1:
        s_vec = s
    else:
        raise TypeError('s should be 1D or 2D ndarray')

    if svs is None:
        s_vec_final = s_vec
    else:
        s_vec_final = 0*s_vec
        s_vec_final[svs] = s_vec[svs]

    out = _np.dot(U, _np.dot(_np.diag(s_vec_final),Vh))

    # Get out to the right shape and return or overwrite
    if data_obj is None or data_obj.shape == out.shape:
        return out
    else:
        out = _np.reshape(out, data_obj.shape)

    if overwrite == False:
        return out
    else:
        if isinstance(data_obj, _Spectrum):
            data_obj.data = out
        elif isinstance(data_obj, _np.ndarray):
            data_obj *= 0
            data_obj += out
#        else:
#            raise TypeError('data_obj should be a subclass of Spectrum or ndarray')

if __name__ == '__main__':  # pragma: no cover
    y = _np.random.randn(100,1000)
    [U,s,Vh] = svd_decompose(y)
    y2 = svd_recompose(U,s,Vh,svs=[])
    print('0 singular values selected...')
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y2,0) == True))
    [U,s,Vh] = svd_decompose(y)
    y2 = svd_recompose(U,s,Vh,svs=[0])

    print('\n1 singular value selected...')
    print('Returns matrix is NOT all 0\'s: {}'.format(_np.allclose(y2,0) == False))
    print('Return matrix is all based on 1 component: {}'.format(_np.isclose(\
        _np.median(y2[0,:]/y2[50,:]),y2[0,0]/y2[50,0])))

    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,10,1000)
    [U,s,Vh] = svd_decompose(y)
    y2 = svd_recompose(U,s,Vh, data_obj=y, svs=[])
    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,1000)
    y_copy = _copy.deepcopy(y)

    [U,s,Vh] = svd_decompose(y)
    y2 = svd_recompose(U,s,Vh, data_obj=y, svs=[], overwrite=True)

    print('\nOverwrite input data...')
    print('0 singular values selected...')
    print('Input is same as output: {}'.format(_np.allclose(y,y_copy)))
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y,0) == True))
