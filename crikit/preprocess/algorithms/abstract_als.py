"""
Created on Mon Dec  5 13:44:58 2016

@author: chc
"""
import timeit as _timeit

import numpy as _np
from scipy.interpolate import UnivariateSpline as _USpline


class AbstractBaseline:
    
    def setup(self, redux=1, verbose=False, order=2, rng=None, 
              fix_end_points=False, fix_rng=None, fix_const=1, 
              max_iter=100, min_diff=1e-5, use_prev=True):
        self.redux = redux
        self.order = order
        self.rng = rng
        self.fix_end_points = fix_end_points
        self._fix_rng = fix_rng

        self.fix_const = fix_const
        self.max_iter = max_iter
        self.min_diff = min_diff
        self.use_prev = use_prev
        
        self.verbose = verbose
        self.t = None
        self.t_per_iter = None

        # Rng applied, then redux
        self.full_sig_shape = None
        self.full_sig_spectral_size = None
        self.n_sig_to_detrend = None
        self.rng_sig_shape = None
        self.rng_sig_spectral_size = None
        self.redux_sig_shape = None
        self.redux_sig_spectral_size = None
        
    def calculate(self, signal):
        self.full_sig_shape = signal.shape # Shape of input signal
        self.full_sig_spectral_size = signal.shape[-1]  # Length of spectral axis

        if self.rng is None:
            self.rng = _np.arange(self.full_sig_spectral_size)
        
        self.rng_sig_shape = signal[..., self.rng].shape
        self.rng_sig_spectral_size = self.rng_sig_shape[-1]

        # N signals to detrend
        self.n_sig_to_detrend = int(signal.size/self.full_sig_spectral_size)
        
        tmr = _timeit.default_timer()
        if self.redux == 1:
            self.redux_sig_shape = self.rng_sig_shape
            self.redux_sig_spectral_size = self.redux_sig_shape[-1]

            output = _np.zeros(self.full_sig_shape, dtype=signal.dtype)
            output[..., self.rng] = self._calc(signal[..., self.rng])

        else:  # Sub-sample
            # Dummy indep variable
            x = _np.arange(self.rng.size)
            x_sub = _np.linspace(x[0], x[-1], _np.round(x.size / 
                                 self.redux).astype(_np.integer))
            self.redux_sig_shape = list(self.full_sig_shape)
            self.redux_sig_shape[-1] = x_sub.size
            self.redux_sig_spectral_size = self.redux_sig_shape[-1]

            signal_sampled = _np.zeros(self.redux_sig_shape)
            
            # Spline interpolation/sub-sampling
            for coords in _np.ndindex(signal.shape[:-1]):
                spl = _USpline(x,signal[coords][self.rng],s=0)
                signal_sampled[coords] = spl(x_sub)
            
            # Baseline from sub-sampled signal
            output_sampled = self._calc(signal_sampled)
            
            output = _np.zeros(signal.shape)
            # Spline interpolation/super-sampling
            for coords in _np.ndindex(output_sampled.shape[0:-1]):
                spl2 = _USpline(x_sub,output_sampled[coords],s=0)
                output[[*coords, self.rng]] = spl2(x)
            
        tmr -= _timeit.default_timer()
        self.t = -tmr
        self.t_per_iter = self.t/self.n_sig_to_detrend
        
        return output

    def _calc(self, signal):
        raise NotImplementedError

    @property
    def fix_rng(self):
        if (self.redux == 1) | (self._fix_rng is None):
            return self._fix_rng
        else:
            redux_fix_rng = self._fix_rng / self.redux
            redux_fix_rng = _np.unique(redux_fix_rng).astype(_np.integer)
            return redux_fix_rng
