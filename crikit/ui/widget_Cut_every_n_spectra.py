"""
Widget for PlotEffect that sets the parameters to cut M spectra of every N spectra

"""
import numpy as _np

import PyQt5.QtCore as QtCore

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_CutEveryNSpectra import Ui_Form as _Ui_Form
from crikit.preprocess.crop import CutEveryNSpectra

class widgetCutEveryNSpectra(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    the Cutting Every N Spectra.

    Attributes
    ----------
    cars_amp_offset : float, optional (default=0.0)
        DC offset applied to CARS spectrum(a) prior to KK relation.

    nrb_amp_offset : float, optional (default=0.0)
        DC offset applied to NRB spectrum(a) prior to KK relation. 

    phase_offset : float or ndarray, optional (default=0.0)
        Phase constant or ndarray applied to retrieved phase prior to 
        separating the real and imaginary components.

    norm_to_nrb : bool, optional (default=True)
        Normalize the amplitude by sqrt(NRB). This effectively removes several \
        system reponse functions.
        
    pad_factor : int, optional (default=1)
        Multiple size of spectral-length to pad the ends of each spectra with. \
        Padded with a constant value corresponding to the value at that end of \
        the spectrum.

    Methods
    ---------
        fcn : Performs the KK

    Signals:
        changed : a value in the UI has changed

    """
    
    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'CutEveryNSpectra', 
                  'long_name' : 'Cut M Spectra Every N Spectra'}
    
    # Labeling options for original data plot
    labels_orig = {
                   'x_label' : 'Repetition Number',
                   'y_label' : 'Intensity (au)',
                   'title' : 'Original'
                   }
    
    # Labeling options for affected data plot              
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : labels_orig['y_label'],
                       'title' : 'Cropped Spectra'
                      }
                      
    def __init__(self, offset=0, cut_m=1, every_n=100, action='cut', parent=None):
        
        super(widgetCutEveryNSpectra, self).__init__(parent)
        
        self.ui = _Ui_Form()
        self.ui.setupUi(self)
                
        # Update parameter dict
        self.parameters['offset'] = offset
        self.parameters['cut_m'] = cut_m
        self.parameters['every_n'] = every_n
        self.parameters['action'] = action
                
        self.setupOptions()
        
    def setupOptions(self):
        
        self.ui.spinBoxSpectraToCut.setValue(self.parameters['cut_m'])
        self.ui.spinBoxEveryNSpectra.setValue(self.parameters['every_n'])
        self.ui.spinBoxOffset.setValue(self.parameters['offset'])
        cbox_idx = self.ui.comboBoxAction.findText(self.parameters['action'], QtCore.Qt.MatchFixedString)
        self.ui.comboBoxAction.setCurrentIndex(cbox_idx)

        self.ui.spinBoxSpectraToCut.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxEveryNSpectra.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxOffset.editingFinished.connect(self.spinBoxChanged)

        self.ui.comboBoxAction.currentIndexChanged.connect(self.comboBoxChanged)
        # SIGNALS & SLOTS
        # self.ui.spinBoxCARSBias.editingFinished.connect(self.spinBoxChanged)
        # self.ui.spinBoxNRBBias.editingFinished.connect(self.spinBoxChanged)
        # self.ui.spinBoxPhaseLin.editingFinished.connect(self.spinBoxChanged)
        # self.ui.spinBoxPadFactor.editingFinished.connect(self.spinBoxChanged)
        
        # self.ui.checkBoxNRBNorm.clicked.connect(self.changeCheckBoxNRBNorm)
        # self.ui.checkBoxLockBias.clicked.connect(self.changeCheckBoxLockBias)

        # self.ui.spinBoxNRBBias.setEnabled(not self.lock_cars_nrb_bias)
        
    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """
        sdr = self.sender()

        if sdr == self.ui.spinBoxSpectraToCut:
            self.parameters['cut_m'] = self.ui.spinBoxSpectraToCut.value()
        elif sdr == self.ui.spinBoxEveryNSpectra:
            self.parameters['every_n'] = self.ui.spinBoxEveryNSpectra.value()
        elif sdr == self.ui.spinBoxOffset:
            self.parameters['offset'] = self.ui.spinBoxOffset.value()

        self.changed.emit()

    def comboBoxChanged(self):
        """ Action comboBox box changed """
        new_action = self.ui.comboBoxAction.currentText().lower()
        self.parameters['action'] = new_action

        self.changed.emit()

    def fcn(self, data_in):
        """
        Return the plot with the appropriate cuts
        """
        
        assert isinstance(data_in, _np.ndarray), 'Required input is an ndarray'

        assert data_in.ndim == 1, 'Required input is a 1D ndarray'
            
        data_out = 0*data_in

        cutter = CutEveryNSpectra(self.parameters['offset'], cut_m=self.parameters['cut_m'],
                                  every_n=self.parameters['every_n'], action=self.parameters['action'])

        # Because of the limits of PlotEffect, the input and output data HAS TO BE the same size
        temp = cutter.calculate(_np.repeat(data_in[:,None], 11, axis=-1)).sum(axis=-1)
        data_out[:temp.size] = temp
        
        return data_out
       
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = widgetCutEveryNSpectra()
    win.show()
    
    app.exec_()
    _sys.exit()