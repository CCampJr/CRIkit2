# -*- coding: utf-8 -*-
"""


References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
"""

import sys as _sys

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)

# Import from Designer-based GUI
from crikit.ui.qt_SubResidualOptions import Ui_Dialog as Ui_ResidualOptions ### EDIT ###

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10

class DialogSubResidualOptions(_QDialog):
    """
    
    """
    RESIDUAL_FREQ = [-1500, -400]
    SUB_RESIDUAL = True

    def __init__(self, parent = None):
        super(DialogSubResidualOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_ResidualOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[0])
        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[1])
        
        self.submain = False
        self.subnrb = False
        self.freq0 = self.RESIDUAL_FREQ[0]
        self.freq1 = self.RESIDUAL_FREQ[1]

        self.ui.checkBoxMain.stateChanged.connect(self.updateCheckBoxMain)
        self.ui.checkBoxBG.stateChanged.connect(self.updateCheckBoxBG)
        
        self.ui.spinBoxMin.editingFinished.connect(self.checkMinMax)
        self.ui.spinBoxMax.editingFinished.connect(self.checkMinMax)

    @staticmethod
    def dialogSubResidualOptions(parent = None,
                                 imgloaded = False,
                                 nrbloaded = False):
        """
        Static Method.

        Retrieve dark subtraction dialog results

        Parameters
        ----------
        imgloaded : (bool)
            Is there an HSI image loaded?
            
        nrbloaded : (bool)
            Is there an NRB loaded?

        Returns
        ----------
        out : dict{'submain' : bool, 'subnrb' : bool, 'subrange' : list}
            In order: subtract residual from image, subtract residual from NRB,
            range to subtract from.
        """
        dialog = DialogSubResidualOptions(parent)
        
        # If nrb loaded, check and enable checkbox
        dialog.ui.checkBoxBG.setChecked(nrbloaded)
        dialog.ui.checkBoxBG.setEnabled(nrbloaded)
        dialog.subnrb = nrbloaded
        
        # If img is loaded, check and enable checkbox
        dialog.ui.checkBoxMain.setChecked(imgloaded)
        dialog.ui.checkBoxMain.setEnabled(imgloaded)
        dialog.submain = imgloaded
        
        result = dialog.exec_()

        if result == 1:
            freq = [dialog.freq0, dialog.freq1]
            freq.sort()
            ret = {'submain' : dialog.submain, 'subnrb' : dialog.subnrb, 
                   'subrange' : freq}
            return ret
        else:
            return None


    def updateCheckBoxMain(self):
        if self.ui.checkBoxMain.isChecked() == True:
            self.submain = True
        else:
            self.submain = False
            
    def updateCheckBoxBG(self):
        if self.ui.checkBoxBG.isChecked() == True:
            self.subnrb = True
        else:
            self.subnrb = False

    def checkMinMax(self):
        self.freq0 = self.ui.spinBoxMin.value()
        self.freq1 = self.ui.spinBoxMax.value()


if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    out = DialogSubResidualOptions.dialogSubResidualOptions(imgloaded=True, nrbloaded=True)
    print(out)
    app.exec_()
    