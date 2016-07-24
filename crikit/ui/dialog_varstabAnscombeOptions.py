# -*- coding: utf-8 -*-
"""
Created on Sat Jul 23 21:38:08 2016

@author: chc
"""
import sys as _sys
from PyQt5.QtWidgets import QApplication as _QApplication
from PyQt5.QtWidgets import QDialog as _QDialog
from crikit.ui.qt_AnscombeOptions import Ui_Dialog as Ui_AnscombeOptions

class DialogAnscombeOptions(_QDialog):
    """
    DialogAnscombeOptions : Anscombe Transformation options dialog

    Static Method
    -------------
    dialogAnscombeOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    """
    STDDEV = 12.44
    GAIN = 1.4

    def __init__(self, parent = None):
        super(DialogAnscombeOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_AnscombeOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.spinBoxGain.setValue(self.GAIN)
        self.ui.spinBoxStdDev.setValue(self.STDDEV)


    @staticmethod
    def dialogAnscombeOptions(parent = None):
        """
        Static Method.

        Retrieve Anscombe Transform dialog results

        Inputs
        ----------
        None : None

        Returns
        ----------
        out : dict{'gain' : float, 'stddev' : float}
            Standard deviation of Gaussian noise : (float)
            Detector gain of Poisson noise : (float)
        """
        dialog = DialogAnscombeOptions(parent)

        result = dialog.exec_()

        ret = {}

        ret['stddev'] = dialog.ui.spinBoxStdDev.value()
        ret['gain'] = dialog.ui.spinBoxGain.value()

        if result == 1:
            return ret
        else:
            return None
            
            
if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    out = DialogAnscombeOptions.dialogAnscombeOptions()
    print(out)
    app.exec_()