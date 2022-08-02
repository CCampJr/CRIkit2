"""
Kramers-Kronig phase retrieval

References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

"""

import sys as _sys
import os as _os
import numpy as _np

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)


# Import from Designer-based GUI
from crikit.ui.qt_KKOptions import Ui_Dialog as Ui_KKOptions

from crikit.ui.dialog_ploteffect import (DialogPlotEffect as 
                                                _DialogPlotEffect)
from crikit.ui.widget_KK import (widgetKK as _widgetKK)

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10


class DialogKKOptions(_QDialog):
    """
    DialogKKOptions : Phase-Retrieval (only Kramers-Kronig currently \
        supported) options dialog

    Methods
    --------
    dialogKKOptions : Used to call UI and retrieve results of dialog

    References
    ----------
    [1] Y. Liu, Y. J. Lee, and M. T. Cicerone, "Broadband CARS spectral \
        phase retrieval using a time-domain Kramers-Kronig transform," \
        Opt. Lett. 34, 1363-1365 (2009).

    [2] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
        Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
        Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

    """
    NORM_TO_NRB = True
    NRB_AMP = 0.0
    CARS_AMP = 0.0
    PHASE_OFFSET = 0.0
    PAD_FACTOR = 1
    N_EDGE = 30

    def __init__(self, parent=None, data=None, conjugate=False):
        super(DialogKKOptions, self).__init__(parent) ### EDIT ###
        self.ui = Ui_KKOptions() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.doubleSpinBoxCARSAmp.setValue(self.CARS_AMP)
        self.ui.doubleSpinBoxNRBAmp.setValue(self.NRB_AMP)
        self.ui.doubleSpinBoxPhase.setValue(self.PHASE_OFFSET)
        self.ui.checkBoxNormToNRB.setChecked(self.NORM_TO_NRB)
        self.ui.spinBoxPadFactor.setValue(self.PAD_FACTOR)
        self.ui.spinBoxEdge.setValue(self.N_EDGE)
        self.ui.checkBoxConjugate.setChecked(conjugate)

        self.norm_to_nrb = self.NORM_TO_NRB

        self.data = data

        if data is None:
            self.ui.pushButtonInteractive.setEnabled(False)
        else:
            self.ui.pushButtonInteractive.pressed.connect(self.goInteractive)

    def goInteractive(self):

        plugin = _widgetKK()

        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(self.data[1:], 
                                                           x=self.data[0], 
                                                           plugin=plugin,
                                                           parent=self)

        if winPlotEffect is not None:
            self.ui.doubleSpinBoxCARSAmp.setValue(winPlotEffect.parameters['cars_amp_offset'])
            self.ui.doubleSpinBoxNRBAmp.setValue(winPlotEffect.parameters['nrb_amp_offset'])
            self.ui.checkBoxNormToNRB.setChecked(winPlotEffect.parameters['norm_to_nrb'])
            self.ui.doubleSpinBoxPhase.setValue(winPlotEffect.parameters['phase_offset'])
            self.ui.spinBoxPadFactor.setValue(winPlotEffect.parameters['pad_factor'])
            self.ui.spinBoxEdge.setValue(winPlotEffect.parameters['n_edge'])
            self.ui.checkBoxConjugate.setChecked(winPlotEffect.parameters['conjugate'])

    @staticmethod
    def dialogKKOptions(parent=None, data=None, conjugate=False):
        """
        Retrieve dark subtraction dialog results

        Parameters
        ----------
        None : None

        Returns
        ----------
        out : dict{'cars_amp' : float, 'nrb_amp' : float,
                   'phase_offset' : float, 'norm_to_nrb' : bool,
                   'pad_factor' : int}
            In order: CARS amp offset, NRB amp offset, phase offset, normalize
                by NRB, pad factor
        """
        dialog = DialogKKOptions(parent=parent,data=data, conjugate=conjugate)

        result = dialog.exec_()

        if result == 1:
            ret = {}
            ret['cars_amp'] = dialog.ui.doubleSpinBoxCARSAmp.value()
            ret['nrb_amp'] = dialog.ui.doubleSpinBoxNRBAmp.value()
            ret['phase_offset'] = dialog.ui.doubleSpinBoxPhase.value()
            ret['norm_to_nrb'] = dialog.ui.checkBoxNormToNRB.isChecked()
            ret['pad_factor'] = dialog.ui.spinBoxPadFactor.value()
            ret['n_edge'] = dialog.ui.spinBoxEdge.value()
            ret['conjugate'] = dialog.ui.checkBoxConjugate.isChecked()
            return ret
        else:
            return None

if __name__ == '__main__':


    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')


#    winDark = DialogDarkOptions.dialogDarkOptions(darkloaded=True)

    from crikit.data.spectra import Hsi as _Hsi

    temp = _Hsi()

    WN = _np.linspace(500,4000,1000)

    CARS = _np.zeros((20,20,WN.size))
    CARS[:,:,:] = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    temp.data = CARS
    temp.freq.data = WN


    NRB = 0*WN + .055


    winKK = DialogKKOptions.dialogKKOptions(data=[WN, NRB,
        temp.get_rand_spectra(10, pt_sz=3, quads=False)])

    print('KK return: {}'.format(winKK))

    _sys.exit()