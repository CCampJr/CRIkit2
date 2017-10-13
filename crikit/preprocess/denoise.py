"""
Denoising

Created on Fri Apr 22 23:55:22 2016

@author: chc
"""

import copy as _copy

import numpy as _np

from numpy.linalg import svd as _svd

from crikit.utils.datacheck import _rng_is_pix_vec

__all__ = ['SVDDecompose', 'SVDRecompose']


class SVDDecompose:
    """
    Compute the SVD of a signal (just wraps numpy.linalg.svd) i.e., decompose \
    the input into components.

    Parameters
    ----------
    data : ndarray (2D or 3D).
        Input array.

    rng : ndarray (1D), optional
        Range of pixels to perform operation over.

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
    def __init__(self, rng=None):
        self._U = None
        self._s = None
        self._Vh = None

        self.rng = _rng_is_pix_vec(rng)


    def _calc(self, data, ret_obj):
        """
        Calculate SVD (wrap numpy SVD).
        """
        try:
            if self.rng is None:
                self._U, self._s, self._Vh = _svd(data, full_matrices=False)
            else:
                self._U, self._s, self._Vh = _svd(data[..., self.rng],
                                               full_matrices=False)
        except:
            return False
        else:
            return True

    def calculate(self, data):
        """
        Calculate SVD and return U, s, and Vh.
        """

        # If 3D -> 2D
        if data.ndim == 3:
            success = self._calc(data.reshape((-1,data.shape[-1])), ret_obj=None)
        else:
            success = self._calc(data, ret_obj=None)
        if success:
            return self._U, self._s, self._Vh
        else:
            return None


class SVDRecompose:
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
        Range of pixels to perform operation over.

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
    def __init__(self, rng=None):
        self.rng = _rng_is_pix_vec(rng)
        self.svs = None
        self.s_keep = None


    def _calc(self, U, s, Vh, ret_obj):
        """
        Perform data reconstruction from U*S*Vh with selected s-values.
        """

        try:
            ret_obj *= 0
            if ret_obj.ndim == 2:
                if self.rng is None:
                # out = U*S*Vh
                    # ret_obj += _np.dot(U, _np.dot(_np.diag(s), Vh))
                    ret_obj += _np.dot(U[:, self.svs], _np.dot(_np.diag(s[self.svs]), Vh[self.svs, :]))
                else:
                    # ret_obj[..., self.rng] += _np.dot(U, _np.dot(_np.diag(s), Vh))
                    ret_obj[..., self.rng] += _np.dot(U[:, self.svs], _np.dot(_np.diag(s[self.svs]), Vh[self.svs, :]))
            elif ret_obj.ndim == 3:
                # If 3D (calculate is performed in 2D), reshape.
                if self.rng is None:
                    # out = U*S*Vh
                    # ret_obj += _np.reshape(_np.dot(U, _np.dot(_np.diag(s), Vh)),
                    #                        ret_obj.shape)
                    ret_obj += _np.reshape(_np.dot(U[:, self.svs], 
                                                   _np.dot(_np.diag(s[self.svs]),
                                                           Vh[self.svs, :])), ret_obj.shape)               
                else:
                    shp = list(ret_obj.shape)
                    shp[-1] = self.rng.size
                    # ret_obj[..., self.rng] += _np.reshape(_np.dot(U, _np.dot(_np.diag(s), Vh)),
                    #                        shp)
                    ret_obj[..., self.rng] += _np.reshape(_np.dot(U[:, self.svs], _np.dot(_np.diag(s[self.svs]),Vh[self.svs, :])), shp)

        except:
            return False
        else:
            return True

    def _set_s_keep(self, s, svs):
        """
        Set the singular value vector (s_keep) based on svs list/ndarray
        """
        if svs is not None:
            self.svs = svs
        if self.svs is None:
            self.svs = _np.arange(s.size)
        
        self.s_keep = 0*s
        self.s_keep[self.svs] = s[self.svs]
        # print(self.s_keep)
        # self.s_keep = s[svs]

    def transform(self, data, U, s, Vh, svs=None):
        # Set what singular values to keep
        self._set_s_keep(s, svs)


        success = self._calc(U, self.s_keep, Vh, ret_obj=data)
        return success

    def calculate(self, data, U, s, Vh, svs=None):
        # Set what singular values to keep
        self._set_s_keep(s, svs)

        data_copy = _copy.deepcopy(data)
        success = self._calc(U, self.s_keep, Vh, ret_obj=data_copy)
        if success:
            return data_copy
        else:
            return None


if __name__ == '__main__':  # pragma: no cover

    y = _np.random.randn(100,1000)

    svd_decompose = SVDDecompose()
    svd_recompose = SVDRecompose()

    U, s, Vh = svd_decompose.calculate(y)

    y2 = svd_recompose.calculate(y,U,s,Vh,svs=[])
    print('0 singular values selected...')
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y2,0) == True))
    
    [U,s,Vh] = svd_decompose.calculate(y)
    y2 = svd_recompose.calculate(y, U, s, Vh, svs=[1])
    print('\n1 singular value selected...')
    print('Returns matrix is NOT all 0\'s: {}'.format(_np.allclose(y2,0) == False))
    print('Return matrix is all based on 1 component: {}'.format(_np.isclose(\
        _np.median(y2[0,:]/y2[50,:]),y2[0,0]/y2[50,0])))

    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,10,1600)
    rng = _np.arange(300,600)
    svd_decompose = SVDDecompose(rng=rng)
    svd_recompose = SVDRecompose(rng=rng)
    U, s, Vh = svd_decompose.calculate(y)

    y2 = svd_recompose.calculate(y, U, s, Vh, svs=[])
    print('\nReturned matrix is same shape {} as that entered: {}'.format(y.shape, y.shape == y2.shape))

    y = _np.random.randn(10,1000)
    y_copy = _copy.deepcopy(y)

    [U,s,Vh] = svd_decompose.calculate(y)
    y2 = svd_recompose.transform(y, U, s, Vh, svs=[])
    print('\nOverwrite input data...')
    print('0 singular values selected...')
    print('Input is NOT same as output: {}'.format(not _np.allclose(y,y_copy)))
    print('Returns matrix is all 0\'s: {}'.format(_np.allclose(y,0) == True))

