"""
Created on Tue Mar  1 11:12:12 2016

@author: chc
"""

from crikit.ui.helper_plugin_categories import ErrorCorrect
from crikit.ui.subui_ploteffect import DialogPlotEffect
from crikit.ui.widget_ploteffect import widgetALS

from crikit.process.maths.als_methods import als_baseline_redux as _als
from crikit.process.maths.kk import hilbertfft as _hilbert

import numpy as _np
import numexpr as _ne
import timeit as _ti
#import copy as _copy

class ErrCorrectPhaseALS(ErrorCorrect):
    name = 'Phase Error: ALS'
    
    def errorCorrectHSData(self, hsdatacls):
        temp_spectra = hsdatacls._get_rand_spectra_phase(10, pt_sz=3, quads=True)
        
        plugin = widgetALS()
        
        result = DialogPlotEffect.dialogPlotEffect(temp_spectra, x=hsdatacls.freqvec,
                                                   plugin=plugin, xlabel='Wavenumber (cm$^{-1}$)',
                                                   ylabel='Imag. {$\chi_R$} (au)', show_difference=True)
        if result is not None:
            p = result.p
            lam = result.lam
            redux = result.redux
            
            data_out = _np.zeros(hsdatacls.spectra.shape, dtype=complex)
            
            detrend_ct = 0
            detrend_tot = hsdatacls.mlen * hsdatacls.nlen
            
            for count_col in _np.arange(0, hsdatacls.nlen):
                start = _ti.default_timer()
                for count_row in _np.arange(0, hsdatacls.mlen):
#                    start2 = _ti.default_timer()
                    
                    # Most efficient system
                    if len(hsdatacls.pixrange) != 0:
                        ph = _np.angle(hsdatacls.spectrafull[count_row, count_col, hsdatacls.pixrange[0]:hsdatacls.pixrange[1]+1])
                    else:
                        ph = _np.angle(hsdatacls.spectrafull[count_row, count_col,:])
                    
                    # MUCH LESS EFFICIENT
                    #ph = hsdatacls.spectraphase[count_row, count_col,:]
                        
#                    stop2 = _ti.default_timer()
                    
#                    start3 = _ti.default_timer()
                    err_phase, als_type = _als(ph, redux_factor=redux, redux_full=False,
                                   smoothness_param=lam, asym_param=p, print_iteration=False)
#                    stop3 = _ti.default_timer()
                    
#                    start4 = _ti.default_timer()
                    h = _hilbert(err_phase)
#                    stop4 = _ti.default_timer()
                    #err_amp = _np.exp(_hilbert(err_phase).imag)
                    #err_amp = _ne.evaluate('exp(imag(h))')
                    #correction_factor = 1/err_amp * _np.exp(-1j*err_phase)
                    
#                    start5 = _ti.default_timer()
                    correction_factor = _ne.evaluate('1/exp(imag(h)) * exp(-1j*err_phase)')
#                    stop5 = _ti.default_timer()
                    
                    
                    data_out[count_row, count_col, :] = hsdatacls.spectracomplex[count_row, count_col, :]*correction_factor
                    
                    detrend_ct += 1
                stop = _ti.default_timer()
#                print('2: {}'.format(stop2-start2))
#                print('3: {}'.format(stop3-start3))
#                print('4: {}'.format(stop4-start4))
#                print('5: {}'.format(stop5-start5))
#                
                print('Detrended {} / {} ({:.5f} sec/spect)'.format(detrend_ct, detrend_tot, (stop-start)/hsdatacls.mlen ))
            
            hsdatacls.spectra = data_out
            return ['PhaseErrorCorect','Type', 'ALS', 'p', p, 'lambda', lam, 'redux', redux, 'alg', als_type]
        else:
            return None