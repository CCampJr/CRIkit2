"""
Calculate Anscombe Parameters

"""

import sys as _sys
import os as _os
import numpy as _np

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)


# Import from Designer-based GUI
from crikit.ui.qt_CalcAnscombeParameters import Ui_Dialog

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10

from crikit.preprocess.standardize import calc_anscombe_parameters

class DialogCalcAnscombeParams(_QDialog):
    """
    

    Methods
    --------
    
    References
    ----------
    
    """
    

    def __init__(self, parent=None, dark_array=None, rep_array=None, axis=None, rng=None, dark_sub=None):
        super(DialogCalcAnscombeParams, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        if (dark_array is None) or (rep_array is None) or (axis is None):
            raise ValueError('dark_array, rep_array, and axis must have inputs')

        self.dark = dark_array
        self.rep = rep_array
        
        self.rng = rng
        

        self.axis = axis
        self.ui.spinBoxAxis.setValue(self.axis)

        self.all_rng = self.ui.checkBoxAllFreqRange.isChecked()

        self.n_dark = dark_array.shape[axis]
        self.use_n_dark = 1*self.n_dark

        self.ui.spinBoxNSpectraDark.setMaximum(self.n_dark)
        self.ui.spinBoxNSpectraDark.setValue(self.n_dark)
        self.ui.spinBoxSkipNDark.setValue(0)
        self.ui.spinBoxSkipNDark.setMaximum(self.n_dark-2)

        self.n_rep = rep_array.shape[axis]
        self.use_n_rep = 1*self.n_rep
        self.ui.spinBoxNSpectraRep.setMaximum(self.n_rep)
        self.ui.spinBoxNSpectraRep.setValue(self.n_rep)
        self.ui.spinBoxSkipNRep.setValue(0)
        self.ui.spinBoxSkipNRep.setMaximum(self.n_dark-2)

        if dark_sub is not None:
            self.dark_sub = dark_sub
        else:
            self.dark_sub = False

        self.ui.checkBoxDarkSub.setChecked(self.dark_sub)

        self.updateInputValues()
        self.updateOutputValues()

        self.ui.checkBoxAllFreqRange.stateChanged.connect(self.updateOutputValues)
        self.ui.checkBoxDarkSub.stateChanged.connect(self.updateOutputValues)
        self.ui.spinBoxNSpectraDark.editingFinished.connect(self.updateOutputValues)
        self.ui.spinBoxNSpectraRep.editingFinished.connect(self.updateOutputValues)
        self.ui.spinBoxAxis.editingFinished.connect(self.updateOutputValues)
        self.ui.spinBoxSkipNDark.editingFinished.connect(self.updateOutputValues)
        self.ui.spinBoxSkipNRep.editingFinished.connect(self.updateOutputValues)

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonOk.setFocus(False)

    def updateInputValues(self):
        self.axis = self.ui.spinBoxAxis.value()
        self.all_rng = self.ui.checkBoxAllFreqRange.isChecked()

        self.skip_dark = self.ui.spinBoxSkipNDark.value()
        self.ui.spinBoxNSpectraDark.setMaximum(self.n_dark-self.skip_dark)
        if self.ui.spinBoxNSpectraDark.value() > self.n_dark-self.skip_dark:
            self.ui.spinBoxNSpectraDark.setValue(self.n_dark-self.skip_dark)
        
        self.skip_rep = self.ui.spinBoxSkipNRep.value()
        self.ui.spinBoxNSpectraRep.setMaximum(self.n_rep-self.skip_rep)
        if self.ui.spinBoxNSpectraRep.value() > self.n_rep-self.skip_rep:
            self.ui.spinBoxNSpectraRep.setValue(self.n_rep-self.skip_rep)

        self.use_n_dark = self.ui.spinBoxNSpectraDark.value()
        self.use_n_rep = self.ui.spinBoxNSpectraRep.value()
        
        self.dark_sub = self.ui.checkBoxDarkSub.isChecked()

    def updateOutputValues(self):

        self.updateInputValues()

        # NOTE: rng is dealt with in calc_anscombe_parameters; thus, full
        # spectral range is passed
        if self.axis == 0:
            slicer_dark = (slice(self.skip_dark, self.use_n_dark + self.skip_dark), slice(None))
            slicer_rep = (slice(self.skip_rep, self.use_n_rep + self.skip_rep), slice(None))
        else:
            slicer_dark = (slice(None), slice(self.skip_dark, self.use_n_dark + self.skip_dark))
            slicer_rep = (slice(None), slice(self.skip_rep, self.use_n_rep + self.skip_rep))

        if self.all_rng:
            values = calc_anscombe_parameters(self.dark[slicer_dark], self.rep[slicer_rep], self.axis, None, self.dark_sub)
        else:
            values = calc_anscombe_parameters(self.dark[slicer_dark], self.rep[slicer_rep], self.axis, self.rng, self.dark_sub)

        self.ui.spinBoxGMean.setValue(values['g_mean'].mean())
        self.ui.spinBoxGStdDev.setValue(values['g_std'].mean())
        self.ui.spinBoxAlphaMean.setValue(values['alpha'].mean())
        self.ui.spinBoxAlphaWMean.setValue(values['weighted_mean_alpha'])
        self.values = values

    @staticmethod
    def dialogCalcAnscombeParams(parent=None, dark_array=None, rep_array=None, axis=None, rng=None, dark_sub=None):
        """
        Calculate Anscombe Parameters

        Parameters
        ----------
        None : None

        Returns
        ----------
        
        """
        dialog = DialogCalcAnscombeParams(parent=parent, dark_array=dark_array, rep_array=rep_array, axis=axis, rng=rng, dark_sub=dark_sub)

        result = dialog.exec_()

        if result == 1:
            ret = dialog.values
            return ret
        else:
            return None

if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    n_spectra = 1000  # number of indep. spectra
    n_lambda = 901  # number of wavelengths in each spectrum

    f = _np.linspace(0,4000,n_lambda)  # Frequency (au)
    y = 40e2*_np.exp(-f**2/(2*350**2)) + 50e1*_np.exp(-(f-2900)**2/(2*250**2))   # signal

    g_mean = 100
    g_std = 25
    p_alpha = 10

    y_array = _np.dot(_np.ones((n_spectra,1)),y[None,:])
    y_noisy = p_alpha*_np.random.poisson(y_array) + g_std*_np.random.randn(*y_array.shape) + g_mean
    dark = g_std*_np.random.randn(*y_array.shape) + g_mean

    out = DialogCalcAnscombeParams.dialogCalcAnscombeParams(dark_array=dark, rep_array=y_noisy, axis=0)

    print('Returns: {}'.format(out))

    _sys.exit()