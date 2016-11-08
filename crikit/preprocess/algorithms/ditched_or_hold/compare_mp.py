# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 00:00:19 2016

@author: chc
"""
import numpy as _np
import timeit as _timeit

from crikit.preprocess.algorithms.als import (als_baseline_cvxopt as als_old,
                                              als_baseline_redux as 
                                              als_old_redux)

from crikit.preprocess.algorithms.als_mp_cvxopt import ALS_Cvxopt
from crikit.cri.kk import KramersKronig
from crikit.cri.error_correction import PhaseErrCorrectALS
from crikit.cri.error_correction_mp import PhaseErrCorrectALS_MP

if __name__ == '__main__':
    import matplotlib.pyplot as _plt
#    import multiprocessing as _mp
#    from multiprocessing.pool import Pool as _Pool
    
    SPECT_LEN = 878
    WN = _np.linspace(4000, 500, SPECT_LEN)
    chi = (1 / ((WN - 1000 - 1j * 10)) +
           1 / ((WN - 1020 - 1j * 10)) +
           1 / ((WN - 2800 - 1j * 10)))
    chiNR = 0*chi + 0.055
    exc = WN
    sig = _np.abs(chi + chiNR)**2

    sigNR = _np.abs(chiNR)**2
    sigRef = chiNR*(WN/1e3)**.5

    kk = KramersKronig()
    kkd = kk.calculate(sig, sigRef)
    
    N = 100
    D = 3
    
    smoothness = 1
    asym = 1e-3
    redux = 10
    
    print('---ALS Test---')
    data = _np.unwrap(_np.angle(kkd))
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    
    print('Data.shape: {}\n'.format(data.shape))
    
    tmr = _timeit.default_timer()
    if redux == 1:
        out_old = als_old(data, smoothness_param=smoothness, asym_param=asym)[0]
    else:
        out_old = als_old_redux(data, smoothness_param=smoothness, asym_param=asym, redux_factor=redux, print_iteration=False)[0]
    tmr -= _timeit.default_timer()
    print('Old ALS Timer: {:.4f} sec'.format(-tmr))
    
    als_new = ALS_Cvxopt(smoothness_param=smoothness, asym_param=asym, redux=redux, print_iteration=False)
    tmr = _timeit.default_timer()
    out_new = als_new.calculate(data)
    tmr -= _timeit.default_timer()
    print('New ALS Timer: {:.4f} sec'.format(-tmr))
    
    print('Old and New ALS are equivalent: {}'.format((out_old==out_new).all()))
    print('Old and New ALS are close: {}'.format(_np.allclose(out_old,out_new,rtol=1e-3)))

        
    if (D <= 2) & (N<21):
        #_plt.plot(data.T,'k')
        _plt.subplot(211)
        _plt.plot(out_old.T,'b')
        _plt.plot(out_new.T,'r')
        _plt.subplot(212)
        _plt.plot((out_new-out_old).T)
        _plt.show()
        
    print('\n')
    print('-----Phase Err Test-----')
    data = kkd
    if D == 3:
        data = _np.dot((_np.random.rand(N,N)*_np.ones((N,N)))[...,None], data[None,:])
    else:
        data = _np.dot((_np.random.rand(N)*_np.ones((N)))[...,None], data[None,:])
    
    print('Data.shape: {}\n'.format(data.shape))
    ph_err_old = PhaseErrCorrectALS(smoothness_param=smoothness, asym_param=asym, redux_factor=redux)
    ph_err_new = PhaseErrCorrectALS_MP(smoothness_param=smoothness, asym_param=asym, redux=redux)
    
    tmr = _timeit.default_timer()
    out_ph_old = ph_err_old.calculate(data)
    tmr -= _timeit.default_timer()
    print('Old PhErr Timer: {:.4f} sec'.format(-tmr))
    
    tmr = _timeit.default_timer()
    out_ph_new = ph_err_new.calculate(data)
    tmr -= _timeit.default_timer()
    print('New PhErr Timer: {:.4f} sec'.format(-tmr))
    print('Old and New PhErr are equivalent: {}'.format((out_ph_old==out_ph_new).all()))
    print('Old and New PhErr are close: {}'.format(_np.allclose(out_ph_old,out_ph_new,rtol=1e-3)))
    
#(signal_input, smoothness_param=1e3, asym_param=1e-4, print_iteration=False)