# -*- coding: utf-8 -*-
"""
Plot-Effect Interface Version 2(crikit.ui.subui_ploteffect_v2)

Created on Tue Nov  1 16:22:23 2016

@author: chc
"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

import numpy as _np

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog, QWidget as _QWidget)

from PyQt5.QtCore import pyqtSignal as _pyqtSignal

# Import from Designer-based GUI
from crikit.ui.qt_PlotEffect import Ui_Dialog as Ui_DialogPlotEffect

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10
_mpl.rcParams['savefig.dpi'] = 300
_mpl.rcParams['figure.figsize'] = (4, 4)
_mpl.rcParams['legend.fontsize'] = 10


from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

from crikit.ui.widget_ploteffect import (widgetKK as _widgetKK)
from crikit.ui.qt_PlotEffect_MergeNRBs import Ui_Form as Ui_Merge_NRBs_Form
from crikit.utils.general import find_nearest as _find_nearest
from crikit.cri.merge_nrbs import MergeNRBs as _MergeNRBs
from crikit.cri.kk import KramersKronig as _KramersKronig

class widgetMergeNRBs(_QWidget):
    """

    Parameters
    ----------
    wn_vec : ndarray (1D)
        Wavenumber array
        
    """

    SCALE_IDX = 1
    WN = 2800.0
    
    changed = _pyqtSignal()

    def __init__(self, wn_vec, parent = None):
        super(widgetMergeNRBs, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Merge_NRBs_Form()
        self.ui.setupUi(self)
        self.kk_widget = _widgetKK(self)
        
        # Disable sigmoidal phase correction
        self.kk_widget.ui.tabWidget.setTabEnabled(1, False)
#        self.kk_widget.ui.tabWidget.removeTab(1)

        self.ui.horizontalLayoutKK.insertWidget(0, self.kk_widget)
        
        if self.SCALE_IDX == 0:
            self.scale = True
        elif self.SCALE_IDX == 1:
            self.scale = False
        else:
            self.scale = None
        
        self.wn_vec = wn_vec
        self.wn, self.pix = _find_nearest(self.wn_vec, self.WN)
        self.ui.spinBoxWN.setMinimum(self.wn_vec.min())
        self.ui.spinBoxWN.setMaximum(self.wn_vec.max())
        self.ui.spinBoxPix.setMinimum(0)
        self.ui.spinBoxPix.setMaximum(self.wn_vec.size-1)
        
        # Set Range
        self.ui.spinBoxLowRange.setValue(wn_vec.min())
        self.ui.spinBoxHighRange.setValue(wn_vec.max())
        self.rng = None
        self.rangeChanged()
        
        self.ui.comboBoxScaleLeftRight.setCurrentIndex(self.SCALE_IDX)
        self.ui.spinBoxWN.setValue(self.wn)
        self.ui.spinBoxPix.setValue(self.pix)
        
        # SIGNALS & SLOTS
        self.kk_widget.changed.connect(self.kkChanged)
        
        self.ui.comboBoxScaleLeftRight.currentIndexChanged.connect(self.scaleChanged)
        self.ui.spinBoxWN.editingFinished.connect(self.wnChanged)
        self.ui.spinBoxPix.editingFinished.connect(self.pixChanged)
        
        self.ui.spinBoxLowRange.editingFinished.connect(self.rangeChanged)
        self.ui.spinBoxHighRange.editingFinished.connect(self.rangeChanged)
    
    def rangeChanged(self):
        low = self.ui.spinBoxLowRange.value()
        high = self.ui.spinBoxHighRange.value()
        self.rng = [low, high]
        self.rng.sort()
        self.changed.emit()
        
    @property
    def fullRange(self):
        low = self.rng[0]
        high = self.rng[1]
        
        if (_np.isclose(self.wn_vec.min(), low, atol=.1) & 
            _np.isclose(self.wn_vec.max(), high, atol=.1)):
            return True
        else:
            return False
        
    def kkChanged(self):
        self.changed.emit()
    
    def scaleChanged(self):
        idx = self.ui.comboBoxScaleLeftRight.currentIndex()
        
        if idx == 0:
            self.scale = True
        elif idx == 1:
            self.scale = False
        else:
            self.scale = None
        self.changed.emit()

    def wnChanged(self):
#        print('WN Changed')
        self.wn, self.pix = _find_nearest(self.wn_vec, self.ui.spinBoxWN.value())
        self.ui.spinBoxWN.setValue(self.wn)
        self.ui.spinBoxPix.setValue(self.pix)
        self.changed.emit()
    
    def pixChanged(self):
        self.pix = self.ui.spinBoxPix.value()
        self.wn = self.wn_vec[self.pix]

        self.ui.spinBoxWN.setValue(self.wn)
        
        self.changed.emit()
    
        
class DialogPlotEffectMergeNRBs(_QDialog):
    """
    Dialog to Merge 2 NRBs
    
    Parameters
    ----------
    nrb_left : ndarray (1D)
        Left-side NRB
        
    nrb_right : ndarray (1D)
        Right-side NRB
        
    x : ndarray (1D)
        x-vector (wavenumber array)
        
    data : ndarray (1D, 2D)
        Array of CARS data to perform KK on with merged NRB 
        (M spectra x N wavenumbers)
        
    Attributes
    ----------
    pix : int
        Pixel to perform merge
        
    wn : double
        Wavenumber equivalent to pix to perform merge
        
    scale : bool or None
        TRUE scales the left-side NRB to match the right-side NRB; FALSE
        scales the right-side; None scales neither
        
    nrb_merge : ndarray (1D)
        Merged NRB
        
    Static Method
    -------------
    dialogPlotEffect : execute this dialog
    
    """
    XLABEL = 'X (au)'
    YLABEL = 'Y (au)'
    
    def __init__(self, nrb_left, nrb_right, x, data=None, parent=None):
        
        super(DialogPlotEffectMergeNRBs, self).__init__(parent)
        self.ui = Ui_DialogPlotEffect()
        self.ui.setupUi(self)

        self.x = x
        self.data = data
        self.nrb_left = nrb_left
        self.nrb_right = nrb_right
        self.nrb_merge = None
        
        self.mpl_orig = _MplCanvas()
        self.mpl_affected = _MplCanvas()

        self.ui.verticalLayout.insertWidget(1, self.mpl_orig)
        self.ui.verticalLayout.insertWidget(1, self.mpl_orig.toolbar)
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected)
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected.toolbar)
       
        self.merge_widget = widgetMergeNRBs(self.x)
        self.ui.verticalLayout.insertWidget(8, self.merge_widget)
        
        
        
        # Signal emited when something changes in the plugin widget
        self.merge_widget.changed.connect(self.widget_changed)
        
        
        self.widget_changed()

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
#    
    def widget_changed(self):
        """
        Plugin widget has changed. Re-submit data to plugin function.
        """
#        print('Here')
        self.scale = self.merge_widget.scale
        self.pix = self.merge_widget.pix
        self.wn = self.merge_widget.wn
        
        nrb_splice = _MergeNRBs(nrb_left=self.nrb_left, 
                                nrb_right=self.nrb_right,
                                pix=self.pix, left_side_scale=self.scale)
        self.nrb_merge = nrb_splice.calculate()
        
        self.cars_bias = self.merge_widget.kk_widget.cars_bias
        self.nrb_bias = self.merge_widget.kk_widget.nrb_bias
        self.nrb_norm = self.merge_widget.kk_widget.nrb_norm
        self.phase_bias = self.merge_widget.kk_widget.phaselin
        self.pad_factor = self.merge_widget.kk_widget.pad_factor
        
        if self.merge_widget.fullRange:
            x = self.x
            locs = _np.arange(x.size, dtype=_np.integer)
        else:
            list_rng_pix = _find_nearest(self.x, self.merge_widget.rng)[1]
            x = self.x[list_rng_pix[0]:list_rng_pix[1]+1]
            locs = _np.arange(list_rng_pix[0],list_rng_pix[1]+1, 
                              dtype=_np.integer)
            
        self.mpl_orig.ax.clear()
        self.mpl_orig.ax.plot(x, self.nrb_left[...,locs], label='Left')
        self.mpl_orig.ax.plot(x, self.nrb_right[...,locs], label='Right')
        self.mpl_orig.ax.set_xlabel('Wavenumber (cm$^{-1}$)')
        self.mpl_orig.ax.legend()
#        self.mpl_orig.fig.tight_layout()

        self.mpl_orig.draw()
        
        
        if self.data is None:
            self.mpl_affected.ax.clear()
            self.mpl_affected.ax.plot(x, self.nrb_merge[...,locs], 
                                      label='Merged')
            self.mpl_affected.ax.set_xlabel('Wavenumber (cm$^{-1}$)')
#            self.mpl_affected.fig.tight_layout()
            self.mpl_affected.ax.legend()
            
            self.mpl_affected.draw()
            
        else:
            self.mpl_orig.ax.plot(x, self.data[...,locs].T, label='Data')
            self.mpl_orig.ax.plot(x, self.nrb_merge[...,locs], 
                                      label='Merged') 
            self.mpl_orig.ax.legend(loc='best')
            self.mpl_orig.draw()

            kk = _KramersKronig(cars_amp_offset=self.cars_bias,
                                nrb_amp_offset=self.nrb_bias,
                                phase_offset=self.phase_bias,
                                norm_to_nrb=self.nrb_norm,
                                pad_factor=self.pad_factor)
            kkd = kk.calculate(self.data[...,locs], self.nrb_merge[...,locs])
#            print('KKd shape: {}'.format(kkd.shape))
            self.mpl_affected.ax.clear()
            self.mpl_affected.ax.plot(x, kkd.imag.T)
            self.mpl_affected.ax.set_xlabel('Wavenumber (cm$^{-1}$)')
            self.mpl_affected.ax.set_ylabel('KK Int.')
            self.mpl_affected.draw()

            
    @staticmethod
    def dialogPlotEffect(nrb_left, nrb_right, x, data=None, parent=None):
        """
        Parameters
        ----------
        nrb_left : ndarray (1D)
            Left-side NRB
            
        nrb_right : ndarray (1D)
            Right-side NRB
            
        x : ndarray (1D)
            x-vector (wavenumber array)
            
        data : ndarray (1D, 2D)
            Array of CARS data to perform KK on with merged NRB 
            (M spectra x N wavenumbers)
            
        Attributes
        ----------
        pix : int
            Pixel to perform merge
            
        wn : double
            Wavenumber equivalent to pix to perform merge
            
        scale : bool or None
            TRUE scales the left-side NRB to match the right-side NRB; FALSE
            scales the right-side; None scales neither
            
        nrb_merge : ndarray (1D)
            Merged NRB
        """        
        dialog = DialogPlotEffectMergeNRBs(nrb_left=nrb_left,
                                           nrb_right=nrb_right,
                                           x=x, data=data, parent=parent)
        
        result = dialog.exec_()  # 1 = Aceepted, 0 = Rejected/Canceled
        
        if result == 1:          
            return dialog
            
        else:
            return None
        
    
if __name__ == '__main__':

    
#    import matplotlib.pyplot as _plt
    
    app = _QApplication(_sys.argv)
    
    #################
    # KK Demo
#    plugin = _widgetMergeNRBs()
    
    WN = _np.linspace(-1500,3600,1600)
    
    NRB_LEFT = 20e3*_np.exp(-(WN)**2/(1000**2)) + 500
    NRB_RIGHT = 6e3*_np.exp(-(WN-2500)**2/(400**2)) + 500
    
    NRB_LEFT[WN<500] *= 0
    NRB_RIGHT[WN<500] *= 0
    
    
#    NRB = _np.exp(-(WN-2450)**2/(500**2))
    NRB = _MergeNRBs(nrb_left=NRB_LEFT, nrb_right=NRB_RIGHT, 
                     pix=_find_nearest(WN, 1885.0)[1],
                     left_side_scale=False).calculate()
    
    CARS = _np.abs(500*(1/(1000-WN-1j*20) + 1/(2700-WN-1j*20)) + NRB**0.5)**2
    CARS = _np.dot(_np.ones((10,1), dtype=_np.double),CARS[None,:])
#    _plt.plot(WN, NRB)
#    _plt.plot(WN, CARS/NRB)
#    _plt.plot(WN, NRB_LEFT)
#    _plt.plot(WN, NRB_RIGHT)
#    _plt.plot(WN, _KramersKronig().calculate(CARS,NRB).imag)
#    _plt.plot
#    _plt.show()
#    NRB_LEFT = 0*WN + .055
#    NRB_RIGHT = 0*WN + .065
    
    winPlotEffect = DialogPlotEffectMergeNRBs.dialogPlotEffect(nrb_left=NRB_LEFT, 
                                                               nrb_right=NRB_RIGHT,
                                                               x=WN, data=CARS)
    
    print(winPlotEffect)
    if winPlotEffect is not None:
        print('CARS Bias: {}'.format(winPlotEffect.cars_bias))
        print('NRB Bias: {}'.format(winPlotEffect.nrb_bias))
        print('Norm by NRB: {}'.format(winPlotEffect.nrb_norm))
        print('Phase correction constant: {}'.format(winPlotEffect.phase_bias))
        print('KK algorithm pad factor: {}'.format(winPlotEffect.pad_factor))
        
        print('NRB merge pixel: {}'.format(winPlotEffect.pix))
        print('NRB merge WN: {}'.format(winPlotEffect.wn))
        print('NRB merge scale left side: {}'.format(winPlotEffect.scale))
        print('NRB merged size: {}'.format(winPlotEffect.nrb_merge.size))
        
#        print('Phase correction constant type: {}'.format(winPlotEffect.kk_widget.phase_type))
    ##################
    
    _sys.exit()