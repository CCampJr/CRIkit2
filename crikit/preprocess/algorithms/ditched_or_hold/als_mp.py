# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 17:40:58 2016

@author: chc
"""

import numpy as _np
import scipy as _scipy
from scipy.interpolate import UnivariateSpline as _USpline
import timeit as _timeit


from crikit.utils.general import row_col_from_lin as _row_col_from_lin

ALS = None

try:
    from crikit.preprocess.algorithms.als_mp_cvxopt import ALS_Cvxopt
except ImportError:
    print('No cvxopt.cholmod module found. Trying scikits.sparse instead.\n\
    You may want to install cvxopt with CHOLMOD for [potentially]\n\
    significant performance enhancement')
else:
    ALS = ALS_Cvxopt
    
try:
    from crikit.preprocess.algorithms.als_mp_scipy import ALS_Scipy
except ImportError:
    if ALS is None:
        print('No scipy.linalg module found. Your Python does not meet the requirements for this module.')
else:
    if ALS is None:
        ALS = ALS_Scipy


if __name__ == '__main__':
    import matplotlib.pyplot as _plt
#    import multiprocessing as _mp
#    from multiprocessing.pool import Pool as _Pool
    
    x = _np.linspace(0,1000,800)
    data = _np.exp(-(x-500)**2/300**2) + _np.abs(5/(300 - x -1j*10) + .005)
    
    N = 50
    D = 2
    
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.ones((N)))[...,None], data[None,:])
    
    print('Data.shape: {}\n'.format(data.shape))
    
#    als = ALS()
    
    
    als = ALS(smoothness_param=1e3, asym_param=1e-3, 
              redux=1, print_iteration=False)
    tmr = _timeit.default_timer()
    out = als.calculate(data)
    tmr -= _timeit.default_timer()
    print('Timer: {:.4f} sec'.format(-tmr))
    
    if (D <= 2) & (N<51):
        _plt.plot(data.T,'k')
        _plt.plot(out.T,'r')
        _plt.show()