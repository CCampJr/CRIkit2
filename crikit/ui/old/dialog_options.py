"""
CRIkit Options Dialogs (crikit.ui.dialog_options)
=======================================================

Classes that present dialog boxes that retrieve options

DialogDarkOptions : Dark subtraction options dialog

DialogKKOptions : Phase retrieval options dialog. Note: this class only\
                    considers the Kramers-Kronig currently

References
----------
.. [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget, QDialog as _QDialog,
                             QMainWindow as _QMainWindow,
                             QSizePolicy as _QSizePolicy)
import PyQt5.QtCore as _QtCore

# Other imports
import numpy as _np

# Import from Designer-based GUI
from crikit.ui.qt_DarkOptions import Ui_Dialog as Ui_DarkOptions ### EDIT ###
from crikit.ui.qt_KKOptions import Ui_Dialog as Ui_KKOptions
from crikit.ui.qt_AnscombeOptions import Ui_Dialog as Ui_AnscombeOptions

from crikit.ui.subui_ploteffect import DialogPlotEffect as _DialogPlotEffect
from crikit.ui.widget_ploteffect import widgetKK as _widgetKK

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10
#import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as _FigureCanvas, \
    NavigationToolbar2QT as _NavigationToolbar)

from matplotlib.figure import Figure as _Figure

class DialogDarkOptions(_QDialog):
    """
    DialogDarkOptions : Dark subtraction options dialog

    Static Method
    -------------
    dialogDarkOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    .. [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    """
    SUB_DARK = True
    SUB_DARK_IMG = True
    SUB_DARK_NRB = True

    RESIDUAL_FREQ = [-1500, -400]
    SUB_RESIDUAL = True

    def __init__(self, parent = None):
        super(DialogDarkOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_DarkOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.frameResidual.setEnabled(self.SUB_RESIDUAL)
        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[0])
        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[1])

        self.subdark = self.SUB_DARK
        self.subdarkimg = self.SUB_DARK_IMG
        self.subdarknrb = self.SUB_DARK_NRB

        self.subresidual = self.SUB_RESIDUAL
        self.freq0 = self.RESIDUAL_FREQ[0]
        self.freq1 = self.RESIDUAL_FREQ[1]

        self.ui.checkBoxResidualDarkSub.stateChanged.connect(self.checkBoxResidualSub)
        self.ui.checkBoxDarkSub.stateChanged.connect(self.checkBoxDarkSub)
        self.ui.checkBoxDarkSubImg.stateChanged.connect(self.checkBoxDarkSubImg)
        self.ui.checkBoxDarkSubNRB.stateChanged.connect(self.checkBoxDarkSubNRB)

        self.ui.spinBoxMin.editingFinished.connect(self.checkMinMax)
        self.ui.spinBoxMax.editingFinished.connect(self.checkMinMax)

    @staticmethod
    def dialogDarkOptions(parent = None, darkloaded = False, nrbloaded = False):
        """
        Static Method.

        Retrieve dark subtraction dialog results

        Inputs
        ----------
        nrbloaded : (bool)
            Is there an NRB loaded?

        darkloaded : (bool)
            Is there a Dark spectrum(a) loaded?

        Returns
        ----------
        out : (tuple)
            Subtract Dark : (bool)
            Subtract Dark from HSData: (bool)
            Subtract Dark from NRB: (bool)
            Subtract Residual over Frequency Range: (bool)
            Frequency Range : (list[str])
        """
        dialog = DialogDarkOptions(parent)
        dialog.ui.checkBoxDarkSubNRB.setChecked(nrbloaded)
        dialog.ui.checkBoxDarkSubNRB.setEnabled(nrbloaded)
        dialog.ui.checkBoxDarkSub.setChecked(darkloaded)
        dialog.ui.checkBoxDarkSubImg.setChecked(darkloaded)
        dialog.ui.checkBoxDarkSub.setEnabled(darkloaded)
        #dialog.ui.checkBoxDarkSubNRB.setEnabled(nrbloaded)

        result = dialog.exec_()

        subdark = dialog.subdark
        subresidual = dialog.subresidual

        if result == 1:
            if subdark == True:
                subdarkimg = dialog.subdarkimg
                subdarknrb = dialog.subdarknrb
            else:
                subdarkimg = None
                subdarknrb = None

            if subresidual == True:
                freq = [dialog.freq0, dialog.freq1]
                freq.sort()
            else:
                subresidual = False
                freq = None
            return (subdark, subdarkimg, subdarknrb, subresidual, freq)
        else:
            return (None, None, None, None, None)

    def checkBoxDarkSubImg(self):
        if self.ui.checkBoxDarkSubImg.isChecked() == True:
             self.subdarkimg = True
        else:
            self.subdarkimg = False


    def checkBoxDarkSubNRB(self):

        if self.ui.checkBoxDarkSubNRB.isChecked() == True:
             self.subdarknrb = True
        else:
            self.subdarknrb = False

    def checkBoxDarkSub(self):
        if self.ui.checkBoxDarkSub.isChecked() == True:
            self.ui.frameDark.setEnabled(True)
            self.subdark = True
        else:
            self.ui.frameDark.setEnabled(False)
            self.subdark = False
            self.ui.checkBoxDarkSubImg.setChecked(False)
            self.ui.checkBoxDarkSubNRB.setChecked(False)

    def checkBoxResidualSub(self):
        if self.ui.checkBoxResidualDarkSub.isChecked() == True:
            self.ui.frameResidual.setEnabled(True)
            self.subresidual = True
        else:
            self.ui.frameResidual.setEnabled(False)
            self.subresidual = False

    def checkMinMax(self):
        self.freq0 = self.ui.spinBoxMin.value()
        self.freq1 = self.ui.spinBoxMax.value()

class DialogKKOptions(_QDialog):
    """
    DialogKKOptions : Phase-Retrieval (only Kramers-Kronig currently \
        supported) options dialog

    Static Method
    -------------
    dialogKKOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    .. [1] Y. Liu, Y. J. Lee, and M. T. Cicerone, "Broadband CARS spectral \
    phase retrieval using a time-domain Kramers-Kronig transform," \
    Opt. Lett. 34, 1363-1365 (2009).

    .. [2] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    """
    NORM_TO_NRB = True
    NRB_AMP = 0.0
    CARS_AMP = 0.0
    PHASE_OFFSET = 0.0
    PAD_FACTOR = 1

    def __init__(self, parent=None, data=None):
        super(DialogKKOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_KKOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.doubleSpinBoxCARSAmp.setValue(self.CARS_AMP)
        self.ui.doubleSpinBoxNRBAmp.setValue(self.NRB_AMP)
        self.ui.doubleSpinBoxPhase.setValue(self.PHASE_OFFSET)
        self.ui.checkBoxNormToNRB.setChecked(self.NORM_TO_NRB)
        self.ui.spinBoxPadFactor.setValue(self.PAD_FACTOR)

        self.ui.checkBoxNormToNRB.stateChanged.connect(self.checkBoxNormToNRB)

        self.norm_to_nrb = self.NORM_TO_NRB

        self.data = data

        if data is None:
            self.ui.pushButtonInteractive.setEnabled(False)
        else:
            self.ui.pushButtonInteractive.pressed.connect(self.goInteractive)

    def checkBoxNormToNRB(self):
        if self.ui.checkBoxNormToNRB.isChecked() == True:
            self.norm_to_nrb = True
        else:
            self.norm_to_nrb = False

    def goInteractive(self):

        plugin = _widgetKK()

        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(self.data, x=self.data[0], plugin=plugin, xlabel='Wavenumber (cm$^{-1}$)', ylabel='Imag. {$\chi_R$} (au)')

        if winPlotEffect is not None:
            self.ui.doubleSpinBoxCARSAmp.setValue(winPlotEffect.cars_bias)
            self.ui.doubleSpinBoxNRBAmp.setValue(winPlotEffect.nrb_bias)
            self.ui.checkBoxNormToNRB.setChecked(winPlotEffect.nrb_norm)
            self.ui.doubleSpinBoxPhase.setValue(winPlotEffect.phaselin)
            self.ui.spinBoxPadFactor.setValue(winPlotEffect.pad_factor)

    @staticmethod
    def dialogKKOptions(parent=None, data=None):
        """
        Static Method.

        Retrieve dark subtraction dialog results

        Inputs
        ----------
        None : None

        Returns
        ----------
        out : (tuple)
            HSData amp offset : (float)
            NRB amp offset : (float)
            Phase offset : (float)
            Normalize by NRB : (bool)
            Pad factor : (int)
        """
        dialog = DialogKKOptions(parent=parent,data=data)

        result = dialog.exec_()

        if result == 1:

            return (dialog.ui.doubleSpinBoxCARSAmp.value(),
                    dialog.ui.doubleSpinBoxNRBAmp.value(),
                    dialog.ui.doubleSpinBoxPhase.value(),
                    dialog.norm_to_nrb,
                    dialog.ui.spinBoxPadFactor.value())
        else:
            return (None, None, None, None, None)
#
#class DialogAnscombeOptions(_QDialog):
#    """
#    DialogAnscombeOptions : Anscombe Transformation options dialog
#
#    Static Method
#    -------------
#    dialogAnscombeOptions : Used to call UI and retrieve results of dialog
#
#    References
#    ----------
#    .. [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
#    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
#    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
#
#    """
#    STDDEV = 12.44
#    GAIN = 1.4
#
#    def __init__(self, parent = None):
#        super(DialogAnscombeOptions, self).__init__(parent) ### EDIT ###
#        self.ui = Ui_AnscombeOptions() ### EDIT ###
#        self.ui.setupUi(self)     ### EDIT ###
#
#        self.ui.spinBoxGain.setValue(self.GAIN)
#        self.ui.spinBoxStdDev.setValue(self.STDDEV)
#
#        #self.stddev = self.STDDEV
#        #self.gain = self.GAIN
#
#    @staticmethod
#    def dialogAnscombeOptions(parent = None, nrbloaded = False):
#        """
#        Static Method.
#
#        Retrieve Anscombe Transform dialog results
#
#        Inputs
#        ----------
#        None : None
#
#        Returns
#        ----------
#        out : (tuple)
#            Standard deviation of Gaussian noise : (float)
#            Detector gain of Poisson noise : (float)
#        """
#        dialog = DialogAnscombeOptions(parent)
#
#        result = dialog.exec_()
#
#        stddev = dialog.ui.spinBoxStdDev.value()
#        gain = dialog.ui.spinBoxGain.value()
#
#        if result == 1:
#            return (stddev, gain)
#        else:
#            return (None, None)

if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')


    winDark = DialogDarkOptions.dialogDarkOptions(darkloaded=True)

    from crikit.data.hsi import Hsi as _Hsi

    temp = _Hsi()

    WN = _np.linspace(500,4000,1000)

    CARS = _np.zeros((20,20,WN.size))
    CARS[:,:,:] = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    temp.data = CARS
    temp.freq.data = WN


    NRB = 0*WN + .055


    winKK = DialogKKOptions.dialogKKOptions(data=[WN, NRB,
        temp.get_rand_spectra(10, pt_sz=3, quads=False)])
#
#    winAnscombe = DialogAnscombeOptions.dialogAnscombeOptions()

    print('Dark return: {}'.format(winDark))
#    print('KK return:{}'.format(winKK))
#    print('Anscombe return:{}'.format(winAnscombe))

    _sys.exit()