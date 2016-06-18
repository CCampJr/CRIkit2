# -*- coding: utf-8 -*-
"""
Widgets for Plot-Effect Interface (crikit.ui.subui_ploteffect)
=======================================================

widgetNothing : This demo widget does nothing

widgetKK : This applies the Kramers-Kronig relation phase retrieval operation

widgetALS : Controls alternating least square parameters

Operation
---------
PlotEffect subUI widgets are essentially 3 parts: a visual component that \
controls any necessary variables, a function (fcn) that performs the \
mathemtical operation on the input data, and a signal (changed) that conveys \
that some change has occurred to the variables within the widget UI.

data_in : (np.array, list)
    For function (fcn) with single-input, data_in should be a numpy array. For \
    fcn with multiple input variables, data_in of type list

changed : QtCore.pyqtSignal

Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("16.02.29")
"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget,
                             QSizePolicy as _QSizePolicy,
                             QColorDialog as _QColorDialog)

from PyQt5.QtCore import pyqtSignal as _pyqtSignal

# Other imports
import numpy as _np
from scipy.signal import savgol_filter as _sg
from scipy.interpolate import UnivariateSpline as _UnivariateSpline
import copy as _copy

# Import from Designer-based GUI

from crikit.ui.qt_PlotEffect_Nothing import Ui_Form as Ui_Nothing_Form
from crikit.ui.qt_PlotEffect_KK import Ui_Form as Ui_KK_Form
from crikit.ui.qt_PlotEffect_ALS import Ui_Form as Ui_ALS_Form
from crikit.ui.qt_PlotEffect_SG import Ui_Form as Ui_SG_Form
from crikit.ui.qt_PlotEffect_Calibrate import Ui_Form as Ui_Calibrate_Form

from crikit.cri.algorithms.kk import kkrelation as _kk
from crikit.preprocess.algorithms.als import als_baseline_redux as _als

from crikit.utils.general import (make_freq_vector as _make_freq_vector,
                                    find_nearest as _find_nearest)

class widgetNothing(_QWidget):
    """
    Plugin widget for PlotEffect subUI.

    This plugin does nothing (i.e., it is a template and for demonstration \
    purposes).

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.02.29")
    """

    changed = _pyqtSignal()

    def __init__(self, parent = None):
        super(widgetNothing, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Nothing_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

    def fcn(self, data_in):
        return data_in

class widgetCalibrate(_QWidget):
    """
    This plugin widget provides calibration functionality.


    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.03.15")
    """
    DEFAULT_NPIXELS = 1600
    DEFAULT_F0 = 730.0
    DEFAULT_F0_CALIB = 730.0
    DEFAULT_SLOPE = -0.167740721307557
    DEFAULT_INTERCEPT = 863.8736708961577
    DEFAULT_PROBE = 771.461

    DEFAULT_MEAS = 1004.0

    CALIB_DICT = {'npixels' : DEFAULT_NPIXELS, 'f0' : DEFAULT_F0,\
        'f0_calib' : DEFAULT_F0_CALIB, 'slope' : DEFAULT_SLOPE,\
        'intercept' : DEFAULT_INTERCEPT, 'probe' : DEFAULT_PROBE}


    changed = _pyqtSignal()

    def __init__(self, calib_dict=None, parent = None):
        super(widgetCalibrate, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Calibrate_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        if calib_dict is None:
            self.calib_dict = self.CALIB_DICT
        else:
            self.calib_dict = calib_dict

        self.new_calib_dict = _copy.deepcopy(self.calib_dict)

        self.updateUI()
        self.WN, self.WL, _ = _make_freq_vector(self.calib_dict)
        self.WN_2, self.WL_2, _ = _make_freq_vector(self.new_calib_dict)

        self.ui.spinBoxMeas.setValue(self.DEFAULT_MEAS)
        self.ui.spinBoxCorrect.setValue(self.DEFAULT_MEAS)

        self.meas = self.DEFAULT_MEAS
        self.correct = self.DEFAULT_MEAS

        self.ui.spinBoxCorrect.editingFinished.connect(self.calcCalibDict)
        self.ui.spinBoxMeas.editingFinished.connect(self.calcCalibDict)

    def fcn(self, data_in):
        """
        Performs the KK.

        Parameters
        ----------
            data : list
                data[0] : Wavenumber vector
                data[1] : NRB spectrum(a)
                data[2] : CARS spectrum(a)

        Returns
        -------
            out : np.array
                Imaginary component the of KK-retrieved spectrum(a)

        See also
        --------
        crikit.process.phase_retr, crikit.process.maths.kk

        """
        if data_in.ndim == 1:
            spl = _UnivariateSpline(self.WN_2, data_in, s=0, ext=0)
            output = spl(self.WN)
        elif data_in.ndim == 2:
            output = _np.zeros(data_in.shape)
            for num, spect in enumerate(data_in):
                spl = _UnivariateSpline(self.WN_2, spect, s=0, ext=0)
                output[num,:] = spl(self.WN)
        return output
        #return data_in

    def calcCalibDict(self):
        """
        (Re)-Calculate calibration dictionary components and recalculate \
        wavenumber/wavelength vector
        """
        self.meas = self.ui.spinBoxMeas.value()
        self.correct = self.ui.spinBoxCorrect.value()

        delta_lambda = 1/(((self.correct)/1e7) + 1/self.calib_dict['probe']) - \
                        1/(((self.meas)/1e7) + 1/self.calib_dict['probe'])

        self.new_calib_dict['intercept'] = self.calib_dict['intercept'] + delta_lambda

        self.WN_2 = _make_freq_vector(self.new_calib_dict)[0]

        self.updateUI()
        self.changed.emit()

    def updateUI(self):
        # Set calibration values

        self.ui.spinBoxNPix.setValue(self.calib_dict['npixels'])
        self.ui.spinBoxNPix_2.setValue(self.new_calib_dict['npixels'])

        self.ui.spinBoxCenterWL.setValue(self.calib_dict['f0'])
        self.ui.spinBoxCenterWL_2.setValue(self.new_calib_dict['f0'])

        self.ui.spinBoxCalibWL.setValue(self.calib_dict['f0_calib'])
        self.ui.spinBoxCalibWL_2.setValue(self.new_calib_dict['f0_calib'])

        self.ui.spinBoxSlope.setValue(self.calib_dict['slope'])
        self.ui.spinBoxSlope_2.setValue(self.new_calib_dict['slope'])

        self.ui.spinBoxIntercept.setValue(self.calib_dict['intercept'])
        self.ui.spinBoxIntercept_2.setValue(self.new_calib_dict['intercept'])

        self.ui.spinBoxProbeWL.setValue(self.calib_dict['probe'])
        self.ui.spinBoxProbeWL_2.setValue(self.new_calib_dict['probe'])



class widgetKK(_QWidget):
    """
    Plugin widget for PlotEffect subUI.

    This plugin performs the Kramers-Kronig (KK) relation phase retrieval.

    Attributes
    ----------
        nrb_norm : bool
            Normalize by the NRB flag

        cars_bias : (int, float)
            Constant added to the input CARS spectrum(a)

        nrb_bias : (int, float)
            Constant added to the input NRB spectrum(a)

        phaselin : (int, float)
            Constant phase correction to the retrieved phase

        phasesig1 : (int, float)
            For sigmoidal phase correction, the is the starting phase

        phasesig2 : (int, float)
            For sigmoidal phase correction, the is the ending phase

        sigrate : (int, float)
            For sigmoidal phase correction, this is the rate of change from \
            phasesig1 to phasesig2

        pad_factor : int
            Padding factor to use with the KK algorithm

        phase_type : str
            Global phase addition type: 'linear' or 'sigmoidal'


    Functions
    ---------
        fcn : Performs the KK

    Signals
    -------
        changed : a value in the UI has changed


    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.02.29")

    """

    changed = _pyqtSignal()

    NRB_NORM = True
    PHASE_TYPE = 'Linear'

    CARS_BIAS = 0
    NRB_BIAS = 0
    PHASELIN = 0

    PHASESIG1 = 0
    PHASESIG2 = 0
    SIGRATE = 1

    PADFACTOR = 1

    def __init__(self, parent = None):
        super(widgetKK, self).__init__(parent) ### EDIT ###
        self.ui = Ui_KK_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.checkBoxNRBNorm.setChecked(self.NRB_NORM)
        self.nrb_norm = self.NRB_NORM

        self.ui.spinBoxCARSBias.setValue(self.CARS_BIAS)
        self.ui.sliderCARSBias.setValue(self.CARS_BIAS)
        self.cars_bias = self.CARS_BIAS

        self.ui.spinBoxNRBBias.setValue(self.NRB_BIAS)
        self.ui.sliderNRBBias.setValue(self.NRB_BIAS)
        self.nrb_bias = self.NRB_BIAS

        self.ui.spinBoxPhaseLin.setValue(self.PHASELIN)
        self.ui.sliderPhaseLin.setValue(self.PHASELIN)
        self.phaselin = self.PHASELIN

        self.ui.spinBoxSigPhase1.setValue(self.PHASESIG1)
        self.ui.sliderSigPhase1.setValue(self.PHASESIG1)
        self.phasesig1 = self.PHASESIG1

        self.ui.spinBoxSigPhase2.setValue(self.PHASESIG2)
        self.ui.sliderSigPhase2.setValue(self.PHASESIG2)
        self.phasesig2 = self.PHASESIG2

        self.ui.spinBoxSigRate.setValue(self.SIGRATE)
        self.ui.sliderSigRate.setValue(self.SIGRATE)
        self.sigrate = self.SIGRATE

        self.ui.spinBoxPadFactor.setValue(self.PADFACTOR)
        self.pad_factor = self.PADFACTOR

        if self.PHASE_TYPE.lower() == 'linear':
            self.ui.tabWidget.setCurrentIndex(0)
            self.phase_type = 'linear'
        elif self.PHASE_TYPE.lower() == 'sigmoidal':
            self.ui.tabWidget.setCurrentIndex(1)
            self.phase_type = 'sigmoidal'
        else:
            self.ui.tabWidget.setCurrentIndex(0)
            self.phase_type = 'linear'

        # Signals-Slots
        self.ui.sliderCARSBias.valueChanged.connect(self.changeSliderCARSBiasPre)
        self.ui.sliderCARSBias.sliderReleased.connect(self.changeSliderCARSBiasFinal)
        self.ui.spinBoxCARSBias.valueChanged.connect(self.changeSpinBoxCARSBias)

        self.ui.sliderNRBBias.valueChanged.connect(self.changeSliderNRBBiasPre)
        self.ui.sliderNRBBias.sliderReleased.connect(self.changeSliderNRBBiasFinal)
        self.ui.spinBoxNRBBias.valueChanged.connect(self.changeSpinBoxNRBBias)

        self.ui.sliderPhaseLin.valueChanged.connect(self.changeSliderPhaseLinPre)
        self.ui.sliderPhaseLin.sliderReleased.connect(self.changeSliderPhaseLinFinal)
        self.ui.spinBoxPhaseLin.valueChanged.connect(self.changeSpinBoxPhaseLin)

        self.ui.sliderSigPhase1.valueChanged.connect(self.changeSliderSigPhase1Pre)
        self.ui.sliderSigPhase1.sliderReleased.connect(self.changeSliderSigPhase1Final)
        self.ui.spinBoxSigPhase1.valueChanged.connect(self.changeSpinBoxSigPhase1)

        self.ui.sliderSigPhase2.valueChanged.connect(self.changeSliderSigPhase2Pre)
        self.ui.sliderSigPhase2.sliderReleased.connect(self.changeSliderSigPhase2Final)
        self.ui.spinBoxSigPhase2.valueChanged.connect(self.changeSpinBoxSigPhase2)

        self.ui.sliderSigRate.valueChanged.connect(self.changeSliderSigRatePre)
        self.ui.sliderSigRate.sliderReleased.connect(self.changeSliderSigRateFinal)
        self.ui.spinBoxSigRate.valueChanged.connect(self.changeSpinBoxSigRate)

        self.ui.spinBoxPadFactor.valueChanged.connect(self.changeSpinBoxPadFactor)

        self.ui.checkBoxNRBNorm.clicked.connect(self.changeCheckBoxNRBNorm)
        self.ui.checkBoxLockBias.clicked.connect(self.changeCheckBoxLockBias)

        self.ui.radioButtonPhaseLin.clicked.connect(self.changeRadioPhaseLin)
        self.ui.radioButtonPhaseSig.clicked.connect(self.changeRadioPhaseSig)

        # Disabled sigmoidal phase correction for now
        self.ui.radioButtonPhaseSig.setEnabled(False)

        self.ui.sliderNRBBias.setEnabled(False)
        self.ui.spinBoxNRBBias.setEnabled(False)
        self.ui.sliderCARSBias.sliderReleased.connect(self.sliderBiasLock)
        self.ui.spinBoxCARSBias.valueChanged.connect(self.spinBoxBiasLock)



    def fcn(self, data_in):
        """
        Performs the KK.

        Parameters
        ----------
            data : list
                data[0] : Wavenumber vector
                data[1] : NRB spectrum(a)
                data[2] : CARS spectrum(a)

        Returns
        -------
            out : np.array
                Imaginary component the of KK-retrieved spectrum(a)

        See also
        --------
        crikit.process.phase_retr, crikit.process.maths.kk

        """
        assert isinstance(data_in, list), 'KK plot effect fcn requires the data input be a list with length 3: WN, NRB, CARS'

        out = _kk(data_in[1] + self.nrb_bias, data_in[2] +
                          self.cars_bias, phase_offset=self.phaselin*_np.pi/360,
                          norm_by_bg=self.nrb_norm, pad_factor=self.pad_factor)
        return out.imag



    def changeSliderCARSBiasPre(self):
        self.ui.spinBoxCARSBias.setValue(self.ui.sliderCARSBias.value())
        self.cars_bias = self.ui.sliderCARSBias.value()
        self.changed.emit()

    def changeSliderCARSBiasFinal(self):
        self.ui.spinBoxCARSBias.setValue(self.ui.sliderCARSBias.value())
        self.cars_bias = self.ui.sliderCARSBias.value()
        self.changed.emit()

    def changeSpinBoxCARSBias(self):
        self.ui.sliderCARSBias.setValue(self.ui.spinBoxCARSBias.value())
        self.cars_bias = self.ui.spinBoxCARSBias.value()
        self.changed.emit()

    def changeSliderNRBBiasPre(self):
        self.ui.spinBoxNRBBias.setValue(self.ui.sliderNRBBias.value())
        self.nrb_bias = self.ui.sliderNRBBias.value()
        self.changed.emit()

    def changeSliderNRBBiasFinal(self):
        self.ui.spinBoxNRBBias.setValue(self.ui.sliderNRBBias.value())
        self.nrb_bias = self.ui.sliderNRBBias.value()
        self.changed.emit()

    def changeSpinBoxNRBBias(self):
        self.ui.sliderNRBBias.setValue(self.ui.spinBoxNRBBias.value())
        self.nrb_bias = self.ui.spinBoxNRBBias.value()
        self.changed.emit()

    def changeSliderPhaseLinPre(self):
        self.ui.spinBoxPhaseLin.setValue(self.ui.sliderPhaseLin.value())
        self.phaselin = self.ui.sliderPhaseLin.value()
        self.changed.emit()

    def changeSliderPhaseLinFinal(self):
        self.ui.spinBoxPhaseLin.setValue(self.ui.sliderPhaseLin.value())
        self.phaselin = self.ui.sliderPhaseLin.value()
        self.changed.emit()

    def changeSpinBoxPhaseLin(self):
        self.ui.sliderPhaseLin.setValue(self.ui.spinBoxPhaseLin.value())
        self.phaselin = self.ui.spinBoxPhaseLin.value()
        self.changed.emit()

    def changeSliderSigPhase1Pre(self):
        self.ui.spinBoxSigPhase1.setValue(self.ui.sliderSigPhase1.value())
        self.phasesig1 = self.ui.sliderSigPhase1.value()
        self.changed.emit()

    def changeSliderSigPhase1Final(self):
        self.ui.spinBoxSigPhase1.setValue(self.ui.sliderSigPhase1.value())
        self.phasesig1 = self.ui.sliderSigPhase1.value()
        self.changed.emit()

    def changeSpinBoxSigPhase1(self):
        self.ui.sliderSigPhase1.setValue(self.ui.spinBoxSigPhase1.value())
        self.phasesig1 = self.ui.spinBoxSigPhase1.value()
        self.changed.emit()

    def changeSliderSigPhase2Pre(self):
        self.ui.spinBoxSigPhase2.setValue(self.ui.sliderSigPhase2.value())
        self.phasesig2 = self.ui.sliderSigPhase2.value()
        self.changed.emit()

    def changeSliderSigPhase2Final(self):
        self.ui.spinBoxSigPhase2.setValue(self.ui.sliderSigPhase2.value())
        self.phasesig2 = self.ui.sliderSigPhase2.value()
        self.changed.emit()

    def changeSpinBoxSigPhase2(self):
        self.ui.sliderSigPhase2.setValue(self.ui.spinBoxSigPhase2.value())
        self.phasesig2 = self.ui.spinBoxSigPhase2.value()
        self.changed.emit()

    def changeSliderSigRatePre(self):
        self.ui.spinBoxSigRate.setValue(self.ui.sliderSigRate.value())
        self.sigrate = self.ui.sliderSigRate.value()
        self.changed.emit()

    def changeSliderSigRateFinal(self):
        self.ui.spinBoxSigRate.setValue(self.ui.sliderSigRate.value())
        self.sigrate = self.ui.sliderSigRate.value()
        self.changed.emit()

    def changeSpinBoxSigRate(self):
        self.ui.sliderSigRate.setValue(self.ui.spinBoxSigRate.value())
        self.sigrate = self.ui.spinBoxSigRate.value()
        self.changed.emit()

    def changeCheckBoxLockBias(self):
        if self.ui.checkBoxLockBias.isChecked():
            self.ui.sliderNRBBias.setEnabled(False)
            self.ui.spinBoxNRBBias.setEnabled(False)
            self.ui.sliderCARSBias.sliderReleased.connect(self.sliderBiasLock)
            self.ui.spinBoxCARSBias.valueChanged.connect(self.spinBoxBiasLock)
            self.sliderBiasLock()
            self.spinBoxBiasLock()

        else:
            self.ui.sliderNRBBias.setEnabled(True)
            self.ui.spinBoxNRBBias.setEnabled(True)
            self.ui.sliderCARSBias.sliderReleased.disconnect(self.sliderBiasLock)
            self.ui.spinBoxCARSBias.valueChanged.disconnect(self.spinBoxBiasLock)
        self.changed.emit()

    def sliderBiasLock(self):
        self.ui.sliderNRBBias.setValue(self.ui.sliderCARSBias.value())
        self.nrb_bias = self.ui.sliderCARSBias.value()
        self.changed.emit()

    def spinBoxBiasLock(self):
        self.ui.spinBoxNRBBias.setValue(self.ui.spinBoxCARSBias.value())
        self.nrb_bias = self.ui.sliderCARSBias.value()
        self.changed.emit()

    def changeCheckBoxNRBNorm(self):
        if self.ui.checkBoxNRBNorm.isChecked():
            self.nrb_norm = True
        else:
            self.nrb_norm = False
        self.changed.emit()

    def changeRadioPhaseLin(self):
        self.phase_type = 'linear'
        self.ui.tabWidget.setCurrentIndex(0)

    def changeRadioPhaseSig(self):
        self.phase_type = 'sigmoidal'
        self.ui.tabWidget.setCurrentIndex(1)

    def changeSpinBoxPadFactor(self):
        self.pad_factor = self.ui.spinBoxPadFactor.value()
        self.changed.emit()

class widgetALS(_QWidget):
    """
    Plugin widget for PlotEffect subUI.

    This performs detrending with the asymmetric least squares algorithms

    Attributes
    ----------
        p : float
            ALS asymmetry parameter

        lam : float
            ALS smoothness parameter

        redux : int



    Functions
    ---------
        fcn : Performs the Asymmetric Least Squares

    Signals
    -------
        changed : a value in the UI has changed

    Citation Reference
    ------------------
    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    References
    ----------
    P. H. C. Eilers, "A perfect smoother," Anal. Chem. 75,
    3631-3636 (2003).

    P. H. C. Eilers and H. F. M. Boelens, "Baseline correction with
    asymmetric least squares smoothing," Report. October 21, 2005.

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.02.29")

    """

    changed = _pyqtSignal()

    P_VAL = 1e-3  # Asymmetry
    LAMBDA_VAL = 1  # Smothness
    REDUX = 10  # Interpolation step size (pixels)

    def __init__(self, parent = None):
        super(widgetALS, self).__init__(parent) ### EDIT ###
        self.ui = Ui_ALS_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.spinBoxP.setValue(self.P_VAL)
        self.ui.spinBoxLambda.setValue(self.LAMBDA_VAL)
        self.ui.spinBoxRedux.setValue(self.REDUX)

        self.p = self.P_VAL
        self.lam = self.LAMBDA_VAL
        self.redux = self.REDUX

        self.ui.spinBoxP.valueChanged.connect(self.changeP)
        self.ui.spinBoxLambda.valueChanged.connect(self.changeLambda)
        self.ui.spinBoxRedux.valueChanged.connect(self.changeRedux)


    def fcn(self, data_in):
        data_out = _np.zeros(data_in.shape)

        if data_in.ndim == 1:
            baseline = _als(data_in, redux_factor=self.redux,
                                      redux_full=False,
                                      smoothness_param=self.lam,
                                      asym_param=self.p)[0]
            data_out = data_in - baseline
        else:
            for num, spectrum in enumerate(data_in):
                baseline = _als(spectrum, redux_factor=self.redux,
                            redux_full=False, smoothness_param=self.lam,
                            asym_param=self.p, print_iteration=False)[0]
                data_out[num,:] = spectrum - baseline
        return data_out

    def changeP(self):
        self.p = self.ui.spinBoxP.value()
        self.changed.emit()

    def changeLambda(self):
        self.lam = self.ui.spinBoxLambda.value()
        self.changed.emit()

    def changeRedux(self):
        self.redux = self.ui.spinBoxRedux.value()
        self.changed.emit()

class widgetSG(_QWidget):
    """
    Plugin widget for PlotEffect subUI.

    This performs the Savitky-Golay filtering

    Attributes
    ----------
        win_size : int
            Window size

        order : int
            Order (polynomial)

    Functions
    ---------
        fcn : Performs the Savitky-Golay

    Signals
    -------
        changed : a value in the UI has changed

    Citation Reference
    ------------------
    C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative,
    Comparable Coherent Anti-Stokes Raman Scattering (CARS)
    Spectroscopy: Correcting Errors in Phase Retrieval"

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.03.02")

    """

    changed = _pyqtSignal()

    WIN_SIZE = 601  # Window size
    ORDER = 2  # Order

    def __init__(self, parent = None):
        super(widgetSG, self).__init__(parent) ### EDIT ###
        self.ui = Ui_SG_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        # Window size must be odd
        if self.WIN_SIZE%2 == 1:
            pass
        else:
            self.WIN_SIZE += 1

        self.ui.spinBoxWinSize.setValue(self.WIN_SIZE)
        self.ui.spinBoxOrder.setValue(self.ORDER)

        self.win_size = self.WIN_SIZE
        self.order = self.ORDER

        self.ui.spinBoxWinSize.valueChanged.connect(self.changeWinSize)
        self.ui.spinBoxOrder.valueChanged.connect(self.changeOrder)

    def fcn(self, data_in):

        baseline = _sg(data_in, window_length=self.win_size, polyorder=self.order, axis=-1)
        data_out = data_in - baseline

        return data_out

    def changeWinSize(self):
        temp_win_size = self.ui.spinBoxWinSize.value()
        if temp_win_size%2 == 1:
            self.win_size = temp_win_size
        else:
            self.ui.spinBoxWinSize.setValue(temp_win_size+1)
            self.win_size = temp_win_size+1
        self.changed.emit()

    def changeOrder(self):
        self.order = self.ui.spinBoxOrder.value()
        self.changed.emit()


if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    winNothing = widgetNothing()
    winNothing.show()

    winKK = widgetKK()
    winKK.show()

    winALS = widgetALS()
    winALS.show()

    winSG = widgetSG()
    winSG.show()

    winCalib = widgetCalibrate()
    winCalib.show()

    app.exec_()
    _sys.exit()