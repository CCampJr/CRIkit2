"""
Dialog for creating BCARS or Raman numerical phantom
"""
import sys as _sys

import numpy as _np

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget, QDialog as _QDialog,
                             QMainWindow as _QMainWindow,
                             QSizePolicy as _QSizePolicy,
                             QFileDialog as _QFileDialog)
import PyQt5.QtCore as _QtCore

from crikit.ui.qt_Model import Ui_Dialog
from crikit.datasets.model import Model

class DialogModel(_QDialog):
    """
    Dialog for creating BCARS or Raman numerical phantom
    """
    def __init__(self, cplx=True, parent=None):
        super().__init__(parent)
        self.cplx = cplx  # Is dataset complex-valued

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.pushButtonCancel.setDefault(False)
        self.ui.pushButtonCancel.setAutoDefault(False)
        self.ui.pushButtonOk.setDefault(False)
        self.ui.pushButtonOk.setAutoDefault(False)
        self.ui.spinBoxSubsample.setFocus()

        self.ui.pushButtonOk.pressed.connect(self.accept)
        self.ui.pushButtonCancel.pressed.connect(self.reject)

        self.ui.spinBoxSubsample.valueChanged.connect(self.changeSize)
        self.ui.spinBoxStart.valueChanged.connect(self.changeSize)
        self.ui.spinBoxEnd.valueChanged.connect(self.changeSize)
        self.ui.spinBoxSpectrographStep.valueChanged.connect(self.changeSize)
        self.ui.spinBoxProbe.valueChanged.connect(self.changeSize)

        self.changeSize()

    def changeSize(self):
        subsample = self.ui.spinBoxSubsample.value()
        start = self.ui.spinBoxStart.value()
        stop = self.ui.spinBoxEnd.value()
        slope = self.ui.spinBoxSpectrographStep.value()
        probe = self.ui.spinBoxProbe.value()

        m = Model._M
        n = Model._N

        x = _np.arange(n)
        y = _np.arange(m)

        rows = y[::subsample].size
        cols = x[::subsample].size
        
        lam_start = 0.01 / (start + 0.01/(probe*1e-9))  # meters
        lam_start *= 1e9  # nm

        lam_end = 0.01 / (stop + 0.01/(probe*1e-9))  # meters
        lam_end *= 1e9  # nm

        lam_ctr = (lam_start + lam_end) / 2  # nm
        
        n_pix = _np.abs(_np.ceil((lam_end-lam_start) / slope)).astype(int)

        datasize = rows * cols * n_pix
        if self.cplx:
            datasize *= (128/8)  # Assume complex128, for now
        else:
            datasize *= (64/8)  # Assume float64, for now
        datasize *= 1e-9  # Gigbytes (Gb)

        self.ui.spinBoxOutputColors.setValue(n_pix)
        self.ui.spinBoxOutputRows.setValue(rows)
        self.ui.spinBoxOutputCols.setValue(cols)
        self.ui.spinBoxMemory.setValue(datasize)
    @staticmethod
    def dialogModel(cplx=True, parent=None):
        """

        """
        dialog = DialogModel(cplx=cplx, parent=parent)
        result = dialog.exec_()
        if result == 1:
            settings = {}
            settings['subsample'] = dialog.ui.spinBoxSubsample.value()
            settings['wn_start'] = dialog.ui.spinBoxStart.value()
            settings['wn_end'] = dialog.ui.spinBoxEnd.value()
            settings['wl_slope'] = dialog.ui.spinBoxSpectrographStep.value()
            settings['probe'] = dialog.ui.spinBoxProbe.value()

            settings['gnoise_bool'] = dialog.ui.checkBoxGNoise.isChecked()
            settings['pnoise_bool'] = dialog.ui.checkBoxPNoise.isChecked()
            settings['dark_bool'] = dialog.ui.checkBoxDark.isChecked()

            settings['gnoise_stddev'] = dialog.ui.spinBoxGStdDev.value()
            settings['pnoise_gain'] = dialog.ui.spinBoxPMulti.value()
            settings['dark_level'] = dialog.ui.spinBoxDark.value()
            return settings
        else:
            return None

if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = DialogModel.dialogModel(cplx=False, parent=None)
    print(win)
    
    _sys.exit()