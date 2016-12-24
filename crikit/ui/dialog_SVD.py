# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:57:24 2016

@author: chc
"""
import numpy as _np
import sys as _sys
#import copy as _copy

from PyQt5.QtWidgets import (QApplication as _QApplication)
from crikit.ui.dialog_AbstractFactorization import DialogAbstractFactorization

from scipy.linalg import diagsvd as _diagsvd

class DialogSVD(DialogAbstractFactorization):
    """
    SVD Class
    """
    def __init__(self, data, img_shape, mask=None, use_imag=True, 
                 parent=None):
        super(DialogSVD, self).__init__(data, img_shape, mask, use_imag, 
                                        parent=parent) ### EDIT ###

        self.U = data[0]
        self.s = data[1]
        self.Vh = data[2]
        self._n_factors = self.s.size

        self.mask = mask
        
        self._use_imag = use_imag # By default, use imag portion of complex data
        
        self.updatePlots(0)
        self.updateCurrentRemainder()
        
        
    
    def max_factors(self):
        """
        Return maximum number of factors. Since DialogAbstractFactorization
        (parent) is initialized first (before self.s), need to return None
        at first.
        """
        try:
            return self.s.size
        except:
            return None
            
    def combiner(self, selections=None):
        S = self.s_from_selected(selections=selections)
        
        # U*S*Vh
        ret = _np.dot(self.U, _np.dot(S, self.Vh))
        return ret
        
    def mean_spatial(self, cube):
        ret = cube.mean(axis=-1)
        ret = ret.reshape((self._n_y, self._n_x))
        if _np.iscomplexobj(ret):
            if self._use_imag:
                return _np.imag(ret)
            else:
                return _np.real(ret)
        else:
            return ret
        
    def mean_spectral(self, cube):
        ret = cube.mean(axis=0)
        
        if _np.iscomplexobj(ret):
            if self._use_imag:
                return _np.imag(ret)
            else:
                return _np.real(ret)
        else:
            return ret
        
    def s_from_selected(self, selections=None):
        """
        Return SVD S-matrix of SELECTED singular values
        """
        M = self.U.shape[-1]
        N = self.Vh.shape[0]
            
        if selections is None:
            S = _diagsvd(self.s, M, N)
            return S
        else:
            if isinstance(selections, set):
                selections = list(selections)
            s_select = _np.zeros(self.s.size)
            s_select[selections] = self.s[selections]

            S = _diagsvd(s_select, M, N)
            return S
        
    def get_spatial_slice(self, num):
        img = self.U[...,num].reshape((self._n_y, self._n_x))
        
        if _np.iscomplexobj(img):
            if self._use_imag:
                return _np.imag(img)
            else:
                return _np.real(img)
        else:
            return img
            
      
        
    def get_spectral_slice(self, num):
        spect = self.Vh[num,:]
        
        if _np.iscomplexobj(spect):
            if self._use_imag:
                return _np.imag(spect)
            else:
                return _np.real(spect)
        else:
            return spect

if __name__ == '__main__':
    from scipy.linalg import svd as _svd
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    x = _np.linspace(100,200,20)
    y = _np.linspace(200,300,20)
    
    
    f = _np.linspace(500,3000,900)
    Ex = 30*_np.exp((-(f-1750)**2/(200**2)))
    Spectrum = _np.convolve(_np.flipud(Ex),Ex,mode='same')
#
    hsi = _np.zeros((y.size,x.size,f.size))
#
    for count in range(y.size):
        hsi[count,:,:] = y[count]*_np.random.poisson(_np.dot(x[:,None],Spectrum[None,:]))
    hsi = hsi + 1j*_np.random.rand(hsi.shape[0], hsi.shape[1], hsi.shape[2])
    
    data = _svd(hsi.reshape((-1,f.size)), full_matrices=False)
    
    # Class method route
    #ret = DialogSVD.main(data, hsi.shape)
    #print(ret)
    
    # Full route
    dialog = DialogSVD(data, hsi.shape)
    result = dialog.exec_()
    if result == 1:
            factors = list(dialog.selected_factors)
            if len(factors) == 0:
                factors = None
            else:
                factors.sort()
                factors = _np.array(factors)
    else:
        factors = None
    
    print('Factors selected: {}'.format(factors))

    app.exec_()