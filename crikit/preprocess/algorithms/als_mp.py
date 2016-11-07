# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:54:08 2016

@author: chc
"""
import numpy as _np
import scipy as _scipy
import timeit as _timeit
import cvxopt as _cvxopt
import cvxopt.cholmod as _cvxopt_cholmod
from scipy.interpolate import UnivariateSpline as _USpline

#if __name__ == '__main__':
#    import os as _os
#    import sys as _sys
#    _sys.path.append(_os.path.abspath('../../../'))

class ALS_Abstract:
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1, 
                 redux_interp=True, print_iteration=False):
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param
        self.redux = redux
        self.redux_interp = redux_interp
        self.print_iteration = print_iteration
        
        self.inital_setup()
        
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
                out = _np.array(p.map(self._calc, data))
            elif ndim == 3:
                out = _np.zeros(data.shape)
                for num_row, col in enumerate(data):
                    temp = _np.array(p.map(als._calc, col))
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
            sampled_baseline = _np.array(p.map(self._calc, sampled_data))
            out = _np.array(p.map(self._spline_supersample_calc, sampled_baseline))
        elif ndim == 3:
            sampled_data = _np.zeros((data.shape[0], 
                                      data.shape[1], 
                                      self._sampled_x.size))
            out = _np.zeros(data.shape)
            sampled_baseline = _np.zeros(sampled_data.shape)
            
            for num_row, blk in enumerate(data):
                sampled_data[num_row, :, :] = _np.array(p.map(self._spline_subsample_calc, blk))
#                for num_col, sp in enumerate(blk):
#                    spl = _USpline(x,sp,s=0)
#                    sampled_data[num_row, num_col,:] = spl(self._sampled_x)
            for num_row, col in enumerate(sampled_data):
                temp = _np.array(p.map(als._calc, col))
                sampled_baseline[num_row,:,:] = temp
            for num_row, blk in enumerate(sampled_baseline):
                out[num_row, :, :] = _np.array(p.map(self._spline_supersample_calc, blk))
#                for num_col, sp in enumerate(blk):
#                    spl2 = _USpline(self._sampled_x,sp,s=0)
#                    out[num_row, num_col,:] = spl2(self._x) 
        return out
            
            
        
            
    def _calc(self, data):
        if data.ndim > 1:
            print('Input data must be 1D')
            return None
        
        self._data = data
        self.setup()
            
        for count_iterate in range(self._max_iter):
            self._penalty_mat = _cvxopt.spdiag(list(self._penalty))
            self._min_mat = self._penalty_mat + \
                _cvxopt.mul(self.smoothness_param,self._difference_mat.T)*\
                self._difference_mat
            x = _cvxopt.matrix(self._penalty[:]*data);
            
            # Cholesky factorization A = LL'
            # Solve A * baseline_current = w_sp * Signal
            _cvxopt_cholmod.linsolve(self._min_mat,x,uplo='U')
        
            if count_iterate > 0:
                self._baseline_last = self.baseline

            self.baseline = _np.array(x).squeeze()

            if count_iterate > 0: # Difference check b/w iterations
                differ = _np.abs(_np.sum(self.baseline - self._baseline_last, 
                                         axis=0))
                if differ < self._min_diff:
                    break
            # Apply asymmetric penalization
            self._penalty = _np.squeeze(self.asym_param*(data >=
                                                         self.baseline) + 
                                                         (1-self.asym_param) * 
                                                         (data < 
                                                          self.baseline))
        return self.baseline
    
class ALS_Cvxopt:
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1, 
                 redux_interp=True, print_iteration=False):
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param
        self.redux = redux
        self.redux_interp = redux_interp
        self.print_iteration = print_iteration
        
        self.inital_setup()
        
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
            self._difference_mat = None
        elif (self._sigsize is None) | (self._sigsize != self._data.size):
            self._sigsize = self._data.size
            self._penalty = _np.ones(self._sigsize)
            self.baseline = _np.zeros(self._sigsize)
            self._baseline_last = _np.zeros(self._sigsize)
            self._penalty_mat = _np.zeros((self._sigsize, self._sigsize))
            self._min_mat = _np.zeros((self._sigsize, self._sigsize))
            self._factor = _np.zeros((self._sigsize, self._sigsize))
            self._difference_mat = _cvxopt.sparse(_cvxopt.matrix(_scipy.diff(_np.eye(self._sigsize),n=self._order,axis=0)))
        else:
            #self._sigsize = self._data.size
            self._penalty *= 0
            self._penalty += 1
            
            self.baseline *= 0
            self._baseline_last *= 0
            
            self._penalty_mat *= 0
            
            self._min_mat *= 0
            self._factor *= 0
            self._difference_mat = _cvxopt.sparse(_cvxopt.matrix(_scipy.diff(_np.eye(self._sigsize),n=self._order,axis=0)))

    class _Spline:
        def __init__(self, x, x_sampled, s=0):
            self._x = x
            self._x_sampled = x_sampled
            self.s = s
     
        def calculate(self,data):
            spl = _USpline(self._x,data,s=self.s)
            return spl(self._x_sampled)
        
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
                out = _np.array(p.map(self._calc, data))
            elif ndim == 3:
                out = _np.zeros(data.shape)
                for num_row, col in enumerate(data):
                    temp = _np.array(p.map(als._calc, col))
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
            sampled_baseline = _np.array(p.map(self._calc, sampled_data))
            out = _np.array(p.map(self._spline_supersample_calc, sampled_baseline))
        elif ndim == 3:
            sampled_data = _np.zeros((data.shape[0], 
                                      data.shape[1], 
                                      self._sampled_x.size))
            out = _np.zeros(data.shape)
            sampled_baseline = _np.zeros(sampled_data.shape)
            
            for num_row, blk in enumerate(data):
                sampled_data[num_row, :, :] = _np.array(p.map(self._spline_subsample_calc, blk))
#                for num_col, sp in enumerate(blk):
#                    spl = _USpline(x,sp,s=0)
#                    sampled_data[num_row, num_col,:] = spl(self._sampled_x)
            for num_row, col in enumerate(sampled_data):
                temp = _np.array(p.map(als._calc, col))
                sampled_baseline[num_row,:,:] = temp
            for num_row, blk in enumerate(sampled_baseline):
                out[num_row, :, :] = _np.array(p.map(self._spline_supersample_calc, blk))
#                for num_col, sp in enumerate(blk):
#                    spl2 = _USpline(self._sampled_x,sp,s=0)
#                    out[num_row, num_col,:] = spl2(self._x) 
        return out
            
            
        
            
    def _calc(self, data):
        if data.ndim > 1:
            print('Input data must be 1D')
            return None
        
        self._data = data
        self.setup()
            
        for count_iterate in range(self._max_iter):
            self._penalty_mat = _cvxopt.spdiag(list(self._penalty))
            self._min_mat = self._penalty_mat + \
                _cvxopt.mul(self.smoothness_param,self._difference_mat.T)*\
                self._difference_mat
            x = _cvxopt.matrix(self._penalty[:]*data);
            
            # Cholesky factorization A = LL'
            # Solve A * baseline_current = w_sp * Signal
            _cvxopt_cholmod.linsolve(self._min_mat,x,uplo='U')
        
            if count_iterate > 0:
                self._baseline_last = self.baseline

            self.baseline = _np.array(x).squeeze()

            if count_iterate > 0: # Difference check b/w iterations
                differ = _np.abs(_np.sum(self.baseline - self._baseline_last, 
                                         axis=0))
                if differ < self._min_diff:
                    break
            # Apply asymmetric penalization
            self._penalty = _np.squeeze(self.asym_param*(data >=
                                                         self.baseline) + 
                                                         (1-self.asym_param) * 
                                                         (data < 
                                                          self.baseline))
        return self.baseline
        
if __name__ == '__main__':
    import matplotlib.pyplot as _plt
    import multiprocessing as _mp
    from multiprocessing.pool import Pool as _Pool
    
    x = _np.linspace(0,1000,800)
    data = _np.exp(-(x-500)**2/300**2) + _np.abs(5/(300 - x -1j*10) + .005)

    N = 100
    D = 3
    
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    data = _np.squeeze(data)
    
    print('Data.shape: {}\n'.format(data.shape))

    print('Cores: {}\n'.format(_mp.cpu_count()))
    
    # NO Redux
    als = ALS_Cvxopt(smoothness_param=1e3, asym_param=1e-3, redux=1)
    tmr = _timeit.default_timer()
    out_mp = als.calculate(data)
    tmr -= _timeit.default_timer()
    print('No REDUX: MP als: {:.4f} sec\n'.format(-tmr))
   
    
    # Redux
    redux = 10
    als = ALS_Cvxopt(smoothness_param=1e-1, asym_param=1e-3, redux=redux)
    tmr = _timeit.default_timer()
    out_mp_redux = als.calculate(data)
    tmr -= _timeit.default_timer()
    print('REDUX: MP als: {:.4f} sec\n'.format(-tmr))
    
    print('Redux and Non-redux are close: {}'.format(_np.allclose(out_mp, out_mp_redux,rtol=.05)))
    
    if (D == 2) & (N < 21):
        _plt.plot(data.T,'k', label='Data')
        _plt.plot(out_mp.T,'b', label='No Redux')
        _plt.plot(out_mp_redux.T,'r', label='Redux')
        if N == 1:
            _plt.legend()
        _plt.show()
        
    