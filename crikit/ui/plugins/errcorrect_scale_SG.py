# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 12:39:53 2016

@author: chc
"""

from crikit.ui.helper_plugin_categories import ErrorCorrect
from crikit.ui.subui_ploteffect import DialogPlotEffect
from crikit.ui.widget_ploteffect import widgetSG

from crikit.process.maths.als_methods import als_baseline_redux as _als
from crikit.process.maths.kk import hilbertfft as _hilbert

import numpy as _np
import numexpr as _ne
import timeit as _ti
#import scipy as _scipy
from scipy.signal import savgol_filter as _sg
#import copy as _copy

class ErrCorrectScaleSG(ErrorCorrect):
    name = 'Scaling: Savitky-Golay'
    
    def errorCorrectHSData(self, hsdatacls):
        temp_spectra = hsdatacls._get_rand_spectra_real(10, pt_sz=3, quads=True)
        
        plugin = widgetSG()
        
        result = DialogPlotEffect.dialogPlotEffect(temp_spectra, x=hsdatacls.freqvec,
                                                   plugin=plugin, xlabel='Wavenumber (cm$^{-1}$)',
                                                   ylabel='Real {$\chi_R$} (au)', show_difference=True)
        if result is not None:
            win_size = result.win_size
            order = result.order
            
                        
            detrend_ct = 0
            detrend_tot = hsdatacls.mlen * hsdatacls.nlen
            
            # Most efficient system
            if len(hsdatacls.pixrange) != 0:
                data_out = hsdatacls.spectrafull[:,:, hsdatacls.pixrange[0]:hsdatacls.pixrange[1]+1]
            else:
                data_out = hsdatacls.spectrafull
                
            start = _ti.default_timer()
            
            correction = (1/_sg(data_out.real, window_length=win_size, polyorder=order, axis=-1))
          
            data_out = data_out*correction
                
            stop = _ti.default_timer()
#                print('2: {}'.format(stop2-start2))
#                print('3: {}'.format(stop3-start3))
#                print('4: {}'.format(stop4-start4))
#                print('5: {}'.format(stop5-start5))
#                
            print('Scaled {} spectra ({:.5f} sec/spect)'.format(detrend_tot, (stop-start)/(hsdatacls.mlen*hsdatacls.nlen)))
            
            hsdatacls.spectra = data_out
            return ['Scaling','Type', 'SG', 'win_size', win_size, 'order', order]
        else:
            return None