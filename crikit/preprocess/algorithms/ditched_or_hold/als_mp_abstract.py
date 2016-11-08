# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:54:08 2016

@author: chc
"""
import numpy as _np
import multiprocessing as _mp

from multiprocessing.pool import Pool as _Pool

from scipy.interpolate import UnivariateSpline as _USpline

class ALS_Abstract:
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1, 
                 redux_interp=True, print_iteration=False):
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param
        self.redux = redux
        self.redux_interp = redux_interp
        self.print_iteration = print_iteration
        self.cholesky_type = None
        
        self.initial_setup()
                
    def initial_setup(self):
        
        self._data = None
        
        self.baseline = None
    
        self._max_iter = 100  # Maximum iterations
        self._min_diff = 1e-5  # Minimum difference b/w iterations
        self._order = 2  # Difference filter order
        
        self._baseline_last = None
        self._baseline_current = None
        self._sigsize = None
        self._penalty = None
        self._penalty_mat = None
        self._min_mat = None
        self._factor = None
        
        self.setup()
        
    def _diff_mat_calc(self):
        raise NotImplementedError
        
    def setup(self):
        if self._data is None:
            self._penalty = None
            self.baseline = None
            self._baseline_last = None
            self._sigsize = None
            self._penalty = None
            self._penalty_mat = None
            self._min_mat = None
            self._factor = None
            self._difference_mat = self._diff_mat_calc()
        elif (self._sigsize is None) | (self._sigsize != self._data.size):
            self._sigsize = self._data.size
            self._penalty = _np.ones(self._sigsize)
            self.baseline = _np.zeros(self._sigsize)
            self._baseline_last = _np.zeros(self._sigsize)
            self._penalty_mat = _np.zeros((self._sigsize, self._sigsize))
            self._min_mat = _np.zeros((self._sigsize, self._sigsize))
            self._factor = _np.zeros((self._sigsize, self._sigsize))
            self._difference_mat = self._diff_mat_calc()
        else:
            #self._sigsize = self._data.size
            self._penalty *= 0
            self._penalty += 1
            
            self.baseline *= 0
            self._baseline_last *= 0
            
            self._penalty_mat *= 0
            
            self._min_mat *= 0
            self._factor *= 0
            self._difference_mat = self._diff_mat_calc()

    def _spline_subsample_calc(self, data):
        spl = _USpline(self._x,data,s=0)
        return spl(self._sampled_x)
        
    def _spline_supersample_calc(self, data):
        spl = _USpline(self._sampled_x,data,s=0)
        return spl(self._x)
        
    def calculate(self, data):
        ndim = data.ndim
        if ndim > 1:
            p = _Pool(_mp.cpu_count())

        # No sub-sample/interpolation of data
        if self.redux == 1:
            if ndim == 1:
                out = self._calc(data)
            elif ndim == 2:
                out = _np.array(p.map(self._calc, data, chunksize=1))
#                for count in out:
#                    print(_np.allclose(count,0))
            elif ndim == 3:
                out = _np.zeros(data.shape)
                for num_row, col in enumerate(data):
                    temp = _np.array(p.map(self._calc, col, chunksize=1))
                    out[num_row,:,:] = temp
            return out
        # Sub-sample OR interpolate
        else:
            self._x = _np.arange(0, data.shape[-1], 1)  # dummy indep variable
            
        # Sub-sample
        if self.redux_interp == False: # Sub-sample
            self._sampled_x = self._x[::self.redux]
                
        # Interpolate
        elif self.redux_interp == True: # Interpolation
            self._sampled_x = _np.linspace(self._x[0], self._x[-1],
                         _np.round(self._x.size/self.redux).astype(int))
        
        if ndim == 1:
            sampled_data = self._spline_subsample_calc(data)
            sampled_baseline = self._calc(sampled_data)
            out = self._spline_supersample_calc(sampled_baseline)
        elif ndim == 2:
            sampled_data = _np.zeros((data.shape[0],self._sampled_x.size))
            out = _np.zeros(data.shape)
            
            sampled_data = _np.array(p.map(self._spline_subsample_calc, data))
            sampled_baseline = _np.array(p.map(self._calc, sampled_data,
                                               chunksize=1))
            out = _np.array(p.map(self._spline_supersample_calc, sampled_baseline))
        elif ndim == 3:
            sampled_data = _np.zeros((data.shape[0], 
                                      data.shape[1], 
                                      self._sampled_x.size))
            out = _np.zeros(data.shape)
            sampled_baseline = _np.zeros(sampled_data.shape)
            
            for num_row, blk in enumerate(data):
                sampled_data[num_row, :, :] = _np.array(p.map(self._spline_subsample_calc, blk))

            for num_row, col in enumerate(sampled_data):
                temp = _np.array(p.map(self._calc, col, chunksize=1))
                sampled_baseline[num_row,:,:] = temp
            for num_row, blk in enumerate(sampled_baseline):
                out[num_row, :, :] = _np.array(p.map(self._spline_supersample_calc, blk))

        return out
            
            
        
            
    def _calc(self, data):
        raise NotImplementedError

        