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
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.spinBoxSubsample.editingFinished.connect(self.changeSize)
        self.ui.spinBoxStart.editingFinished.connect(self.changeSize)
        self.ui.spinBoxEnd.editingFinished.connect(self.changeSize)
        self.ui.spinBoxSpectrographStep.editingFinished.connect(self.changeSize)
        self.ui.spinBoxProbe.editingFinished.connect(self.changeSize)

    def changeSize(self):
        subsample = self.ui.spinBoxSubsample.value()
        start = self.ui.spinBoxStart.value()
        stop = self.ui.spinBoxEnd.value()
        slope = self.ui.spinBoxSpectrographStep.value()
        probe = self.ui.spinBoxProbe.value()


    @staticmethod
    def dialogModel(parent=None):
        """

        """
        dialog = DialogModel(parent=parent)
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

    win = DialogModel.dialogModel()
    print(win)
    
    _sys.exit()