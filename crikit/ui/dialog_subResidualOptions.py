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

    def __init__(self, parent = None):
        super(DialogSubResidualOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_ResidualOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[0])
        self.ui.spinBoxMax.setValue(self.RESIDUAL_FREQ[1])
        
        
    @staticmethod
    def dialogSubResidualOptions(parent = None,
                                 imgloaded = False,
                                 nrbloaded = False):
        """
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
            ret = {}
            freq = [dialog.ui.spinBoxMin.value(),
                    dialog.ui.spinBoxMax.value()]
            ret['subrange'] = freq
            ret['submain'] = dialog.ui.checkBoxMain.isChecked()
            ret['subnrb'] = dialog.ui.checkBoxBG.isChecked()
            
            return ret
        else:
            return None

if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    out = DialogSubResidualOptions.dialogSubResidualOptions(imgloaded=True, nrbloaded=True)
    print(out)
    app.exec_()
    