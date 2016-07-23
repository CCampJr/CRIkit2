# -*- coding: utf-8 -*-
"""


References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
"""

# Append sys path
import sys as _sys
import os as _os

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)

# Import from Designer-based GUI
from crikit.ui.qt_DarkOptions import Ui_Dialog as Ui_DarkOptions ### EDIT ###

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10

class DialogDarkOptions(_QDialog):
    """
    DialogDarkOptions : Dark subtraction options dialog

    Static Method
    -------------
    dialogDarkOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.03.14")
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


if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')


    winDark = DialogDarkOptions.dialogDarkOptions(darkloaded=True)
    print(winDark)
    app.exec_()
    