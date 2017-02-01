"""
Widget for PlotEffect that adjusts the parameters appropriate for
merging 2 NRBs

Created on Thu Dec 22 22:20:06 2016

@author: chc
"""

import numpy as _np

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                     as
                                                     _AbstractPlotEffectPlugin)


from crikit.ui.widget_KK import (widgetKK as _widgetKK)
from crikit.ui.qt_PlotEffect_MergeNRBs import Ui_Form as _Ui_Form
from crikit.utils.general import find_nearest as _find_nearest
from crikit.cri.merge_nrbs import MergeNRBs as _MergeNRBs

class widgetMergeNRBs(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    merging 2 NRBs
    """
    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'mergeNRBs', 
                  'long_name' : 'Merge 2 NRBs'}
    
    # Labeling options for original data plot
    labels_orig = {
                   'x_label' : 'Wavenumber (cm$^{-1}$)',
                   'y_label' : 'Input Int (au)',
                   'title' : 'Original'
                   }
    
    # Labeling options for affected data plot              
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : 'Raman-Like Int (au)',
                       'title' : 'KK-Raman'
                      }
  
    def __init__(self, wn_vec, nrb_left, nrb_right, scale_left=False, 
                 wn_switchpt=2800.0, parent = None):
                      
        super(widgetMergeNRBs, self).__init__(parent)
        
        self.ui = _Ui_Form()
        self.ui.setupUi(self)
        
        self.wn = wn_vec
        self.nrb_left = nrb_left
        self.nrb_right = nrb_right
        
        # Update parameter dict
        self.parameters['scale_left'] = scale_left
        self.parameters['wn_switchpt'] = wn_switchpt
        self.parameters['pix_switchpt'] = \
            _find_nearest(self.wn, self.parameters['wn_switchpt'])[1]
        
        self.kk_widget = _widgetKK()
        
        self.ui.horizontalLayoutKK.insertWidget(0, self.kk_widget)
        
        self.ui.spinBoxWN.setMinimum(self.wn.min())
        self.ui.spinBoxWN.setMaximum(self.wn.max())
        self.ui.spinBoxPix.setMinimum(0)
        self.ui.spinBoxPix.setMaximum(self.wn.size-1)
        
        # Set range
        self.ui.spinBoxLowRange.setValue(self.wn.min())
        self.ui.spinBoxHighRange.setValue(self.wn.max())
        self.rng = None
        self.rangeChanged()
        
        if self.parameters['scale_left']:
            self.ui.comboBoxScaleLeftRight.setCurrentIndex(0)
        elif self.parameters['scale_left'] == False:
            self.ui.comboBoxScaleLeftRight.setCurrentIndex(1)
        elif self.parameters['scale_left'] is None:
            self.ui.comboBoxScaleLeftRight.setCurrentIndex(2)
            
        self.ui.spinBoxWN.setValue(self.parameters['wn_switchpt'])
        self.ui.spinBoxPix.setValue(self.parameters['pix_switchpt'])
        
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
        
        if (_np.isclose(self.wn.min(), low, atol=.1) & 
            _np.isclose(self.wn.max(), high, atol=.1)):
            return True
        else:
            return False
        
    def kkChanged(self):
        self.changed.emit()
    
    def scaleChanged(self):
        idx = self.ui.comboBoxScaleLeftRight.currentIndex()
        
        if idx == 0:
            self.parameters['scale_left'] = True
        elif idx == 1:
            self.parameters['scale_left'] = False
        else:
            self.parameters['scale_left'] = None
        self.changed.emit()

    def wnChanged(self):
#        print('WN Changed')
        self.parameters['wn_switchpt'], self.parameters['pix_switchpt'] = \
            _find_nearest(self.wn, self.ui.spinBoxWN.value())
            
        self.ui.spinBoxWN.setValue(self.parameters['wn_switchpt'])
        self.ui.spinBoxPix.setValue(self.parameters['pix_switchpt'])
        self.changed.emit()
    
    def pixChanged(self):
        self.parameters['pix_switchpt'] = self.ui.spinBoxPix.value()
        self.parameters['wn_switchpt'] = self.wn[self.parameters['pix_switchpt']]

        self.ui.spinBoxWN.setValue(self.parameters['wn_switchpt'])
        
        self.changed.emit()

    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """
        inst_nrb_merge = _MergeNRBs(nrb_left=self.nrb_left, 
                                        nrb_right=self.nrb_right,
                                        pix=self.parameters['pix_switchpt'],
                                        left_side_scale=self.parameters['scale_left'])
        
        if self.fullRange:
            pix = _np.arange(self.wn.size, dtype=_np.integer)
            
        else:
            list_rng_pix = _find_nearest(self.wn, self.rng)[1]
            pix = _np.arange(list_rng_pix[0],list_rng_pix[1]+1,
                             dtype=_np.integer)
            
        nrb_merged = inst_nrb_merge.calculate()
        kkd = _np.zeros(data_in.shape)

        # Note: kk_widget.fcn return imag part
        kkd[..., pix] = self.kk_widget.fcn([nrb_merged[pix], data_in[..., pix]])
        
        return [_np.vstack((self.nrb_left, self.nrb_right, nrb_merged)),
                kkd]
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import QApplication as _QApplication
    app = _QApplication(_sys.argv)
    
    WN = _np.linspace(-1500,3600,1600)
    
    NRB_LEFT = 20e3*_np.exp(-(WN)**2/(1000**2)) + 500
    NRB_RIGHT = 6e3*_np.exp(-(WN-2500)**2/(400**2)) + 500
    
    NRB_LEFT[WN<500] *= 0
    NRB_LEFT[WN<500] += 1e-6
    NRB_RIGHT[WN<500] *= 0
    NRB_RIGHT[WN<500] += 1e-6
    
    win = widgetMergeNRBs(WN, NRB_LEFT, NRB_RIGHT)
    win.show()
    
    app.exec_()
    _sys.exit()
    
