"""
Widget for PlotEffect that adjusts the parameters appropriate for
calibration

Created on Thu Dec 22 14:27:46 2016

@author: chc
"""
import copy as _copy

import numpy as _np

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from scipy.interpolate import UnivariateSpline as _UnivariateSpline

from crikit.data.frequency import (calib_pix_wn as _calib_pix_wn)

#from crikit.utils.general import find_nearest as _find_nearest

from crikit.ui.qt_PlotEffect_Calibrate import Ui_Form as _Ui_Form


class widgetCalibrate(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    calibration
    
    Parameters
    ----------
    calib_dict : dict
        Calibration dictionary
        
    Methods
    -------
    fcn : Perform arPLS detrending
    
    Signals:
        changed : a value in the UI has changed
        
    """
    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'Calibrate', 
                  'long_name' : 'Spectral Calibration'}
    
    # Labeling options for original data plot
    labels_orig = {
                   'x_label' : 'Wavenumber (cm$^{-1}$)',
                   'y_label' : 'Input Int (au)',
                   'title' : 'Uncalibrated'
                   }
    
    # Labeling options for affected data plot                             
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : 'Output Int (au)',
                       'title' : 'Calibrated'
                      }

    def __init__(self, calib_dict, parent=None):
        super(widgetCalibrate, self).__init__(parent) ### EDIT ###
        
        self.ui = _Ui_Form() 
        self.ui.setupUi(self)    

        self.parameters['orig_calib_dict'] = calib_dict
        
        if isinstance(self.parameters['orig_calib_dict']['a_vec'], tuple):
            self.parameters['orig_calib_dict']['a_vec'] = \
                list(self.parameters['orig_calib_dict']['a_vec'])

        self.parameters['new_calib_dict'] = \
            _copy.deepcopy(self.parameters['orig_calib_dict'])

        self.setup_calib()
#        self.orig_wn = _calib_pix_wn(self.parameters['orig_calib_dict'])
#        self.new_wn = _calib_pix_wn(self.parameters['new_calib_dict'])

        self.ui.spinBoxMeas.setValue(1004.0)
        self.ui.spinBoxCorrect.setValue(1004.0)

        # SIGNALS & SLOTS    
        # New
        self.ui.spinBoxNPix_2.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxCenterWL_2.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxProbeWL_2.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxIntercept_2.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxSlope_2.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxCalibWL_2.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.spinBoxCorrect.editingFinished.connect(self.meas_vs_ideal)
        self.ui.spinBoxMeas.editingFinished.connect(self.meas_vs_ideal)

    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """
        
        sdr = self.sender()
        
        # Original
        if sdr == self.ui.spinBoxNPix_2:
            self.parameters['new_calib_dict']['n_pix'] = \
                self.ui.spinBoxNPix_2.value()
        
        elif sdr == self.ui.spinBoxCenterWL_2:
            self.parameters['new_calib_dict']['ctr_wl'] = \
                self.ui.spinBoxCenterWL_2.value()
            
        elif sdr == self.ui.spinBoxCalibWL_2:
            self.parameters['new_calib_dict']['ctr_wl0'] = \
                self.ui.spinBoxCalibWL_2.value()
                
        elif sdr == self.ui.spinBoxSlope_2:
            self.parameters['new_calib_dict']['a_vec'][0] = \
                self.ui.spinBoxSlope_2.value()
                
        elif sdr == self.ui.spinBoxIntercept_2:
            self.parameters['new_calib_dict']['a_vec'][1] = \
                self.ui.spinBoxIntercept_2.value()
                
        elif sdr == self.ui.spinBoxProbeWL_2:
            self.parameters['new_calib_dict']['probe'] = \
                self.ui.spinBoxProbeWL_2.value()
        
        self.changed.emit()
        
    def meas_vs_ideal(self):
        meas = self.ui.spinBoxMeas.value()
        ideal = self.ui.spinBoxCorrect.value()

        delta_lambda = (1 / ((ideal / 1e7) + 
                            (1 / self.parameters['orig_calib_dict']['probe']))
                        - 1 / ((meas/1e7) + 
                               (1 / self.parameters['orig_calib_dict']['probe'])))
    
        self.parameters['new_calib_dict']['a_vec'][1] = \
            self.parameters['orig_calib_dict']['a_vec'][1] + delta_lambda

        self.setup_calib()
        self.changed.emit()
        
    def fcn(self, data_in):
        """
        Returns a shifted version of the input spectrum to mimic the effect
        of calibration. (Real calibration doesn't shift the spectrum, but 
        rather the independent variable)

        """
        orig_wn = _calib_pix_wn(self.parameters['orig_calib_dict'])[0]
        new_wn = _calib_pix_wn(self.parameters['new_calib_dict'])[0]
        
        if data_in.ndim == 1:
            spl = _UnivariateSpline(new_wn, data_in, s=0, ext=0)
            output = spl(orig_wn)
        elif data_in.ndim == 2:
            output = _np.zeros(data_in.shape)
            for num, spect in enumerate(data_in):
                spl = _UnivariateSpline(new_wn, spect, s=0, ext=0)
                output[num,:] = spl(orig_wn)
        return output

    def setup_calib(self):
        
        # Original
        self.ui.spinBoxNPix.setValue(self.parameters['orig_calib_dict']['n_pix'])
        self.ui.spinBoxCenterWL.setValue(self.parameters['orig_calib_dict']['ctr_wl'])
        self.ui.spinBoxCalibWL.setValue(self.parameters['orig_calib_dict']['ctr_wl0'])
        self.ui.spinBoxSlope.setValue(self.parameters['orig_calib_dict']['a_vec'][0])
        self.ui.spinBoxIntercept.setValue(self.parameters['orig_calib_dict']['a_vec'][1])
        self.ui.spinBoxProbeWL.setValue(self.parameters['orig_calib_dict']['probe'])
        
        # New
        self.ui.spinBoxNPix_2.setValue(self.parameters['new_calib_dict']['n_pix'])
        self.ui.spinBoxCenterWL_2.setValue(self.parameters['new_calib_dict']['ctr_wl'])
        self.ui.spinBoxProbeWL_2.setValue(self.parameters['new_calib_dict']['probe'])
        self.ui.spinBoxIntercept_2.setValue(self.parameters['new_calib_dict']['a_vec'][1])
        self.ui.spinBoxSlope_2.setValue(self.parameters['new_calib_dict']['a_vec'][0])
        self.ui.spinBoxCalibWL_2.setValue(self.parameters['new_calib_dict']['ctr_wl0'])

    
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    
    
    calib_dict = {'n_pix' : 1600,
                  'ctr_wl' : 730,
                  'ctr_wl0' : 730,
                  'a_vec' : [-0.167740721307557, 863.8736708961577],
                  'probe': 771.461}
                  
    pix = _np.arange(calib_dict['n_pix'])
    wl = calib_dict['a_vec'][0]*pix + calib_dict['a_vec'][1]
    WN = .01/(wl*1e-9) - .01/(calib_dict['probe']*1e-9)
    
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
    CARS = _np.dot(_np.ones((5,1)),CARS[None,:])

        
    winCalib = widgetCalibrate(calib_dict)
    winCalib.show()

    
    app.exec_()
    _sys.exit()