# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 11:54:08 2016

@author: chc
"""
import numpy as _np
import timeit as _timeit

from scipy import linalg as _linalg

from crikit.preprocess.algorithms.als_mp_abstract import (ALS_Abstract as 
                                                          _ALS_Abstract)

class ALS_Scipy(_ALS_Abstract):
    def __init__(self, smoothness_param=1e3, asym_param=1e-4, redux=1, 
                 redux_interp=True, print_iteration=False):
        self.smoothness_param = smoothness_param
        self.asym_param = asym_param
        self.redux = redux
        self.redux_interp = redux_interp
        self.print_iteration = print_iteration
        self.cholesky_type = 'scipy.linalg'
        
        self.initial_setup()
    
    def _diff_mat_calc(self):
        if self._data is None:
            return None
        else:
            return _np.diff(_np.eye(self._sigsize),n=self._order,axis=0)

        
    def _calc(self, data):
        if data.ndim > 1:
            print('Input data must be 1D')
            return None
        
        self._data = data
        self.setup()
            
        for count_iterate in range(self._max_iter):
            self._penalty_mat = _np.diag(self._penalty)
            self._min_mat = self._penalty_mat + \
                _np.dot((self.smoothness_param*self._difference_mat.T),
                        self._difference_mat)
            
            # Cholesky factorization A = LL'
            self._factor = _linalg.cholesky(self._min_mat, 
                                            lower=True, 
                                            overwrite_a=False, 
                                            check_finite=True)
            
            if count_iterate > 0:
                self._baseline_last = self.baseline

            # Solve A * baseline_current = penalty_vector * Signal
            self.baseline = _linalg.solve(self._factor.T,
                                          _linalg.solve(self._factor, 
                                                        self._penalty * data))
            
            
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
    
    x = _np.linspace(0,1000,800)
    data = _np.exp(-(x-500)**2/300**2) + _np.abs(5/(300 - x -1j*10) + .005)

    N = 2 # Number of spectra
    D = 2 # Dimension 2 or 3
    
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    data = _np.squeeze(data)
    
    print('Data.shape: {}\n'.format(data.shape))

    print('Cores: {}\n'.format(_mp.cpu_count()))
      
    #### SCIPY
    print('\n----SCIPY----')
    if D*N < 10:
        
        # NO Redux
        als = ALS_Scipy(smoothness_param=1e3, asym_param=1e-3, redux=1)
        tmr = _timeit.default_timer()
        out_scipy_mp = als.calculate(data)
        tmr -= _timeit.default_timer()
        print('No REDUX: MP als: {:.4f} sec\n'.format(-tmr))
   
    
    if D*N < 500:
        # Redux
        redux = 10
        als = ALS_Scipy(smoothness_param=1e-1, asym_param=1e-3, redux=redux)
        tmr = _timeit.default_timer()
        out_scipy_mp_redux = als.calculate(data)
        tmr -= _timeit.default_timer()
        print('REDUX: MP als: {:.4f} sec\n'.format(-tmr))
    
    if D*N < 10:
        print('Redux and Non-redux are close: {}'.format(_np.allclose(out_scipy_mp, out_scipy_mp_redux,rtol=.05)))
    
    if (D == 2) & (D*N < 10):
        _plt.plot(data.T,'k', label='Data')
        _plt.plot(out_scipy_mp.T,'b', label='No Redux')
        _plt.plot(out_scipy_mp_redux.T,'r', label='Redux')
        if N == 1:
            _plt.legend()
        _plt.show()
        
    