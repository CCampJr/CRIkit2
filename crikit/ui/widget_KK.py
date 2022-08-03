"""
Widget for PlotEffect that adjusts the parameters appropriate for
the Kramers-Kronig relation

Created on Thu Dec 22 11:43:42 2016

@author: chc
"""
import numpy as _np

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_KK import Ui_Form as _Ui_Form

from crikit.cri.kk import KramersKronig as _KramersKronig

class widgetKK(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    the Kramers-Kronig (KK) relation phase retrieval.

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
    parameters = {'name' : 'KK', 
                  'long_name' : 'Kramers-Kronig Relation'}
    
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
                      
    def __init__(self, cars_amp_offset=0.0, nrb_amp_offset=0.0,
                 conjugate=False, phase_offset=0.0, norm_to_nrb=True, pad_factor=1,
                 n_edge=30, parent=None):
        
        super(widgetKK, self).__init__(parent)
        
        self.ui = _Ui_Form()
        self.ui.setupUi(self)
        
        self.lock_cars_nrb_bias = True
        self.show_real = False

        # Update parameter dict
        self.parameters['cars_amp_offset'] = cars_amp_offset
        self.parameters['nrb_amp_offset'] = nrb_amp_offset
        self.parameters['phase_offset'] = phase_offset
        self.parameters['norm_to_nrb'] = norm_to_nrb
        self.parameters['pad_factor'] = pad_factor
        self.parameters['n_edge'] = n_edge
        self.parameters['conjugate'] = conjugate
                
        self.setupKK()
        
    def setupKK(self):

        self.ui.checkBoxNRBNorm.setChecked(self.parameters['norm_to_nrb'])
        self.ui.checkBoxConjugate.setChecked(self.parameters['conjugate'])
        self.ui.checkBoxLockBias.setChecked(self.lock_cars_nrb_bias)
        self.ui.checkBoxShowReal.setChecked(self.show_real)

        self.ui.spinBoxCARSBias.setValue(self.parameters['cars_amp_offset'])
        self.ui.spinBoxNRBBias.setValue(self.parameters['nrb_amp_offset'])
        self.ui.spinBoxPhaseLin.setValue(self.parameters['phase_offset'])
        self.ui.spinBoxPadFactor.setValue(self.parameters['pad_factor'])
        self.ui.spinBoxEdge.setValue(self.parameters['n_edge'])

        # SIGNALS & SLOTS
        self.ui.spinBoxCARSBias.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxNRBBias.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxPhaseLin.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxPadFactor.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxEdge.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.checkBoxNRBNorm.clicked.connect(self.changeCheckBoxNRBNorm)
        self.ui.checkBoxConjugate.clicked.connect(self.changeCheckBoxConjugate)
        self.ui.checkBoxShowReal.clicked.connect(self.changeShowReal)

        self.ui.checkBoxLockBias.clicked.connect(self.changeCheckBoxLockBias)

        self.ui.spinBoxNRBBias.setEnabled(not self.lock_cars_nrb_bias)
        

    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """
        
        assert isinstance(data_in, list), 'KK plot effect fcn requires the \
            data input be a list with length 2: NRB, CARS'

        assert len(data_in), 'KK plot effect fcn requires the \
            data input be a list with length 2: NRB, CARS'
            
        nrb = data_in[0]
        cars = data_in[1]
        
        data_out = _np.zeros(cars.shape, dtype=complex)
               
        cars_amp_offset = self.parameters['cars_amp_offset']
        nrb_amp_offset = self.parameters['nrb_amp_offset'] 
        conjugate = self.parameters['conjugate']
        phase_offset = self.parameters['phase_offset'] 
        norm_to_nrb = self.parameters['norm_to_nrb']
        pad_factor = self.parameters['pad_factor']
        n_edge = self.parameters['n_edge']
        
        _kk = _KramersKronig(cars_amp_offset=cars_amp_offset,
                             nrb_amp_offset=nrb_amp_offset,
                             conjugate=conjugate,
                             phase_offset=phase_offset,
                             norm_to_nrb=norm_to_nrb,
                             pad_factor=pad_factor,
                             n_edge=n_edge)

        data_out = _kk.calculate(cars, nrb)
        
        if self.show_real:
            return data_out.real
        else:
            return data_out.imag

    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """
        
        sdr = self.sender()
        
        if sdr == self.ui.spinBoxCARSBias:
            self.parameters['cars_amp_offset'] = self.ui.spinBoxCARSBias.value()
            if self.lock_cars_nrb_bias:
                self.parameters['nrb_amp_offset'] = \
                    self.ui.spinBoxCARSBias.value()
                self.ui.spinBoxNRBBias.setValue(self.parameters['nrb_amp_offset'])
                
        elif sdr == self.ui.spinBoxNRBBias:
            self.parameters['nrb_amp_offset'] = self.ui.spinBoxNRBBias.value()
            
        elif sdr == self.ui.spinBoxPhaseLin:
            self.parameters['phase_offset'] = self.ui.spinBoxPhaseLin.value()
            
        elif sdr == self.ui.spinBoxPadFactor:
            self.parameters['pad_factor'] = self.ui.spinBoxPadFactor.value()
        elif sdr == self.ui.spinBoxEdge:
            self.parameters['n_edge'] = self.ui.spinBoxEdge.value()
        self.changed.emit()

    def changeCheckBoxLockBias(self):
        if self.ui.checkBoxLockBias.isChecked():
            self.ui.spinBoxNRBBias.setEnabled(False)
            self.lock_cars_nrb_bias = True
        else:
            self.ui.spinBoxNRBBias.setEnabled(True)
            self.lock_cars_nrb_bias = False
        self.changed.emit()

    def changeCheckBoxNRBNorm(self):
        if self.ui.checkBoxNRBNorm.isChecked():
            self.parameters['norm_to_nrb'] = True
        else:
            self.parameters['norm_to_nrb'] = False
        self.changed.emit()

    def changeCheckBoxConjugate(self):
        if self.ui.checkBoxConjugate.isChecked():
            self.parameters['conjugate'] = True
        else:
            self.parameters['conjugate'] = False
        self.changed.emit()
        
    def changeShowReal(self):
        if self.show_real:
            self.show_real = False
        else:
            self.show_real = True
        self.changed.emit()
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = widgetKK()
    win.show()

    app.exec_()
    _sys.exit()