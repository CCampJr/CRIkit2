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

from numpy.linalg import svd as _svd

def svd_decompose(data, rng=None, rng_list=None):
    """
    Compute the SVD of a signal (just wraps numpy.linalg.svd) i.e., decompose \
    the input into components.

    Parameters
    ----------
    data : ndarray (2D or 3D).
        Input array.

    rng : ndarray (1D), optional
        Range of pixels to perform operation over. Note rng has priority over \
        rng_list

    rng_list : list/tuple, optional
        List (2-elements) of first through last pixel to perform operation over

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

    data = _np.squeeze(data)
    sh = data.shape

    if rng is not None:
        span = rng
    elif rng_list:
        span = _np.arange(rng_list[0],rng_list[1]+1)
    else:
        span = _np.arange(0,sh[-1])

    if data.ndim == 2:
        U,s,Vh = _svd(data[..., span], full_matrices=False)
    elif data.ndim == 3:
        U,s,Vh = _svd(data.reshape((-1,data.shape[-1]))[..., span], full_matrices=False)
    else:
        raise TypeError('ndarray should be 2D or 3D')

    return [U, s, Vh]

def svd_recompose(U,s,Vh, data=None, svs=None, rng=None, rng_list=None,
                  overwrite=False):
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

    data : ndarray (2D or 3D)
        Original data (for overwrite if selected).

    rng : ndarray (1D), optional
        Range of pixels to perform operation over. Note rng has priority over \
        rng_list

    rng_list : list/tuple, optional
        List (2-elements) of first through last pixel to perform operation over

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
    out = _np.dot(U, _np.dot(_np.diag(s_vec_final), Vh))

    # See if data was originally 3D. If out (2D) -> out (3D)
    if data is not None:
        if out.ndim == 2 and data.ndim == 3:
            out = out.reshape(list(data.shape[0:-1]) + [-1])

    # See if range info was provided and create span vector
    if rng is not None:
        span = rng
    elif rng_list is not None:
        span = _np.arange(rng_list[0],rng_list[1]+1)
    else:
        span = None

    # no data = no overwrite or resize
    if data is None:
        return out
    # data and out are the same shape: no further reshaping needed
    elif data.shape == out.shape:
        if overwrite:
            data *= 0
            data += out
            return None
        else:
            return out
    # data and out shape disagree AND no range info given-- can't overwrite
    elif rng is None and rng_list is None:
        if overwrite:
            print('Data and SVD recompose shape disagree. Cannot overwrite.')
#            data *= 0
#            data += out
            return out
        else:
            return out
    # range info given: reshape
    elif span is not None:
        if overwrite:
            data *= 0
            data[...,rng] += out
        else:
            out2 = _np.zeros(data.shape)
            out2[...,rng] += out
            return out2
    else:
        print('Something weird. Returning recomposed.')
        return out


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
    y2 = svd_recompose(U,s,Vh, data=y, svs=[])
    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,1000)
    y_copy = _copy.deepcopy(y)

    [U,s,Vh] = svd_decompose(y)
    y2 = svd_recompose(U,s,Vh, data=y, svs=[], overwrite=True)
    print('\nOverwrite input data...')
    print('0 singular values selected...')
    print('Input is NOT same as output: {}'.format(not _np.allclose(y,y_copy)))
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y,0) == True))
