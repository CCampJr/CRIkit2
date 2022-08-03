"""

Subtract baseline

Created on Sat May 28 00:41:41 2016

@author: chc
"""

import copy as _copy

import numpy as _np

from crikit.preprocess.algorithms.als import (AlsCvxopt as _AlsCvxopt)

from crikit.utils.datacheck import _rng_is_pix_vec


class SubtractBaselineALS:
    """
    Subtract baseline using asymmetric least squares algorithm
    
    Parameters
    ----------
    smoothness_param : float, optional (default=1.0)
        Smoothness parameter aka 'lambda'
        
    asym_param : float, optional (default=1e-2)
        Asymmetry parameter aka 'p'
        
    redux_factor : int, optional (default=10)
        Down-sampling factor (more down-sampling leads to faster detrending,
        but with more chance of non-optimal detrending)
        
    rng : ndarray (1D), optional (default=None)
        Range in pixels to perform action over
    
    use_imag : bool, optional (default=True)
        If spectrum(a) are complex-values, use the imaginary portion?
    """
    def __init__(self, smoothness_param=1, asym_param=1e-2,
                 redux=10, order=2, rng=None, fix_end_points=False, 
                 fix_rng=None, fix_const=1,
                 max_iter=100, min_diff=1e-5, use_imag=True, 
                 **kwargs):

        self.rng = _rng_is_pix_vec(rng)
        self._k = kwargs
        
        self._k.update({'smoothness_param' : smoothness_param,
                        'asym_param' : asym_param,
                        'redux' : redux,
                        'order' : order,
                        'rng' : rng,
                        'fix_end_points' : fix_end_points,
                        'fix_rng' : fix_rng,
                        'fix_const' : fix_const,
                        'max_iter' : max_iter,
                        'min_diff' : min_diff})
        
        self.use_imag = use_imag
        
    def _calc(self, data, ret_obj, **kwargs):
        
        self._inst_als = _AlsCvxopt(**kwargs)
        
        try:
            # Get the subarray shape
            shp = data.shape[0:-2]
            total_num = _np.array(shp).prod()
   
            # Iterate over the sub-array -- super slick way of doing it
            for num, idx in enumerate(_np.ndindex(shp)):
                print('Detrended iteration {} / {}'.format(num+1, total_num))
                # Imaginary portion set
                if self.use_imag and _np.iscomplexobj(data):
                    # if self.rng is None:
                    #     ret_obj[idx] -= 1j*self._inst_als.calculate(data[idx].imag)
                    # else:
                    ret_obj[idx] -= 1j*self._inst_als.calculate(data[idx].imag)
                else:  # Real portion set or real object
                    # if self.rng is None:
                    #     ret_obj[idx] -= self._inst_als.calculate(data[idx].real)
                    # else:
                    ret_obj[idx] -= self._inst_als.calculate(data[idx].real)
        except Exception:
            return False
        else:
#            print(self._inst_als.__dict__)
            return True

    def transform(self, data, **kwargs):
        if self.rng is None:
            self.rng = _np.arange(data.shape[-1])

        total_rng = _np.arange(data.shape[-1])

        not_in_rng = list(set(total_rng).difference(self.rng))
        not_in_rng.sort()
        not_in_rng = _np.array(not_in_rng)

        if not_in_rng.size != 0:
            data[..., not_in_rng] *= 0
            
        self._k.update(kwargs)
        
        success = self._calc(data, ret_obj=data, **self._k)
        return success

    def calculate(self, data, **kwargs):
        if self.rng is None:
            self.rng = _np.arange(data.shape[-1])
            
        data_copy = _np.zeros(data.shape, dtype=data.dtype)
        data_copy[..., self.rng] = 1*data[..., self.rng]

        self._k.update(kwargs)
        
        success = self._calc(data, ret_obj=data_copy, **self._k)
        if success:
            return data_copy
        else:
            return None


if __name__ == '__main__':  # pragma: no cover

    x = _np.linspace(-100, 100, 1000)
    y = 10*_np.exp(-(x**2/(2*20**2)))

    rng = _np.arange(200,800)
    als = SubtractBaselineALS(smoothness_param=1, asym_param=1e-3, rng=rng,
                                redux=1, fix_end_points=False, fix_rng=None, 
                                verbose=True)

    y_als = als.calculate(y)
