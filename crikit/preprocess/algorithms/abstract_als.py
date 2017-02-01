"""
Created on Mon Dec  5 13:44:58 2016

@author: chc
"""
import numpy as _np
import timeit as _timeit

from scipy.interpolate import UnivariateSpline as _USpline

class AbstractBaseline:
    
    def setup(self, redux=1, verbose=False, order=2, fix_end_points=False, 
              max_iter=100, min_diff=1e-5):
        self.redux = redux
        self.order = order
        self.fix_end_points = fix_end_points
        self.max_iter = max_iter
        self.min_diff = min_diff
        
        self.verbose = verbose
        self.t = None
        self.t_per_iter = None
        
    def calculate(self, signal):
        sig_shape = signal.shape  # Shape of input signal
        sig_size = signal.shape[-1]  # Length of spectral axis
        
        # N signals to detrend
        sig_n_to_detrend = int(signal.size/signal.shape[-1])
        
        tmr = _timeit.default_timer()
        if self.redux == 1:
            output = self._calc(signal)
        else:  # Sub-sample
            # Dummy indep variable
            x = _np.arange(sig_size)
            x_sub = _np.linspace(x[0], x[-1], _np.round(x.size / 
                                 self.redux).astype(_np.integer))

            sub_shape = list(sig_shape)
            sub_shape[-1] = x_sub.size
            
            signal_sampled = _np.zeros(sub_shape)
            
            # Spline interpolation/sub-sampling
            for coords in _np.ndindex(signal.shape[0:-1]):
                spl = _USpline(x,signal[coords],s=0)
                signal_sampled[coords] = spl(x_sub)
            
            # Baseline from sub-sampled signal
            output_sampled = self._calc(signal_sampled)
            
            output = _np.zeros(signal.shape)
            # Spline interpolation/super-sampling
            for coords in _np.ndindex(output_sampled.shape[0:-1]):
                spl2 = _USpline(x_sub,output_sampled[coords],s=0)
                output[coords] = spl2(x)
            
        tmr -= _timeit.default_timer()
        self.t = -tmr
        self.t_per_iter = self.t/sig_n_to_detrend
        
        return output

    def _calc(self, signal):
        raise NotImplementedError
