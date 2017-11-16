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

    Methods
    -------
    dialogAnscombeOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    """
    
    def __init__(self, stddev=12.44, gain=1.4, parent = None):
        super(DialogAnscombeOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_AnscombeOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.spinBoxGain.setValue(gain)
        self.ui.spinBoxStdDev.setValue(stddev)


    @staticmethod
    def dialogAnscombeOptions(stddev=12.44, gain=1.4, parent=None):
        """
        Retrieve Anscombe Transform dialog results

        Parameters
        ----------
        None : None

        Returns
        ----------
        out : dict{'gain' : float, 'stddev' : float}
            Standard deviation of Gaussian noise : (float)
            Detector gain of Poisson noise : (float)
        """
        dialog = DialogAnscombeOptions(stddev=stddev, gain=gain, 
                                       parent=parent)

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