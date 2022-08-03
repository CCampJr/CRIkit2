"""
CRIKit2: Hyperspectral imaging toolkit
======================================

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform (user interface, UI).

HSI Processing:
    * Dark subtraction
    * Detrending
    * Denoising

Coherent Raman-Specific Processing:
    * Kramers-Kronig phase retrieval
    * Phase- and scale-error correction

Analysis:
    * Coming soon

Usage
-----
From ./crikit2 directory
python3 main.py

Authors
-------
* Charles H. Camp Jr. <charles.camp@nist.gov>
"""

import copy as _copy
import os as _os
import sys as _sys
import traceback as _traceback
import webbrowser as _webbrowser


import matplotlib as _mpl
import matplotlib.pyplot as _plt
import numpy as _np
import h5py as _h5py

import PyQt5.QtCore as _QtCore

from PyQt5.QtGui import QCursor as _QCursor
from PyQt5.QtWidgets import QApplication as _QApplication
from PyQt5.QtWidgets import QFileDialog as _QFileDialog
from PyQt5.QtWidgets import QInputDialog as _QInputDialog
from PyQt5.QtWidgets import QMainWindow as _QMainWindow
from PyQt5.QtWidgets import QMessageBox as _QMessageBox
from PyQt5.QtWidgets import QWidget as _QWidget
from PyQt5.QtWidgets import QTableWidgetItem as _QTableWidgetItem

from scipy.signal import savgol_filter as _sg


from crikit.cri.error_correction import (PhaseErrCorrectALS as _PhaseErrCorrectALS)
from crikit.cri.error_correction import ScaleErrCorrectSG as _ScaleErrCorrectSG
from crikit.cri.kk import KramersKronig
from crikit.cri.merge_nrbs import MergeNRBs as _MergeNRBs

from crikit.data.frequency import (calib_pix_wn as _calib_pix_wn,
                                   calib_pix_wl as _calib_pix_wl)
from crikit.data.spectra import Hsi
from crikit.data.spectra import Spectra
from crikit.data.spectra import Spectrum

from crikit.datasets.model import Model as _Model

from crikit.io.macros import import_csv_nist_special1 as io_nist_dlm
from crikit.io.macros import (import_hdf_nist_special as io_nist, hdf_nist_special_macroraster as io_nist_macro)
from crikit.io.macros import import_hdf_nist_special_ooc as io_nist_ooc

# from crikit.io.meta_configs import special_nist_bcars2 as _snb2
# from crikit.io.meta_process import meta_process as _meta_process

import crikit.measurement.peakamps as _peakamps

from crikit.preprocess.crop import ZeroColumn as _ZeroColumn
from crikit.preprocess.crop import ZeroRow as _ZeroRow
from crikit.preprocess.crop import CutEveryNSpectra as _CutEveryNSpectra
from crikit.preprocess.denoise import SVDDecompose, SVDRecompose
from crikit.preprocess.standardize import Anscombe as _Anscombe
from crikit.preprocess.standardize import AnscombeInverse as _AnscombeInverse
from crikit.preprocess.subtract_baseline import \
    SubtractBaselineALS as _SubtractBaselineALS
from crikit.preprocess.subtract_dark import SubtractDark
from crikit.preprocess.subtract_mean import SubtractMeanOverRange

from crikit.ui.dialog_kkOptions import DialogKKOptions
from crikit.ui.dialog_model import DialogModel
from crikit.ui.dialog_ploteffect import \
    DialogPlotEffect as _DialogPlotEffect
from crikit.ui.dialog_save import DialogSave
from crikit.ui.dialog_varstabAnscombeOptions import DialogAnscombeOptions
from crikit.ui.dialog_AnscombeParams import DialogCalcAnscombeParams
from crikit.ui.qt_CRIkit import Ui_MainWindow
from crikit.ui.main_Mosaic import MainWindowMosaic

from crikit.ui.utils.roi import roimask as _roimask
from crikit.ui.widget_Calibrate import widgetCalibrate as _widgetCalibrate
from crikit.ui.widget_DeTrending import widgetALS as _widgetALS
from crikit.ui.widget_DeTrending import widgetArPLS as _widgetArPLS
from crikit.ui.widget_DeTrending import widgetDeTrending as _widgetDeTrending
from crikit.ui.widget_images import (widgetBWImg, widgetCompositeColor, widgetSglColor)

from crikit.ui.widget_mergeNRBs import widgetMergeNRBs as _widgetMergeNRBs
from crikit.ui.widget_SG import widgetSG as _widgetSG

from crikit.ui.widget_Cut_every_n_spectra import widgetCutEveryNSpectra as _widgetCutEveryNSpectra

from crikit.utils.breadcrumb import BCPre as _BCPre
from crikit.utils.general import find_nearest, mean_nd_to_1d, std_nd_to_1d

from sciplot.sciplotUI import SciPlotUI as _SciPlotUI

from crikit.io.lazy5.ui.QtHdfLoad import HdfLoad
import crikit.io.lazy5 as lazy5

force_not_sw = False

try:
    import crikit2_sw
except Exception:
    __sw_installed = False
    # print('SW package not installed, using standard')
    from crikit.ui.dialog_SVD import DialogSVD
else:
    __sw_installed = True

    if force_not_sw:
        print('SW package installed, but forced off -- using standard')
        from crikit.ui.dialog_SVD import DialogSVD
    else:
        print('SW package installed, let\'s rock!')
        from crikit2_sw.ui.dialog_SVD import DialogSVD


_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 9

jupyter_flag = 0
try:
    from crikit.ui.widget_Jupyter import QJupyterWidget
    jupyter_flag = 1
except Exception:
    print('No appropriate Jupyter/IPython installation found. Console will not be available')
    jupyter_flag = -1

str_doc = '../docs/build/html/index.html'
help_index = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), str_doc))

if _os.path.exists(help_index):
    pass
else:
    help_index = None

class CRIkitUI_process(_QMainWindow):
    """
    CRIkitUI_process : CRIkitUI for image (pre-)processing

    References
    ----------
    [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
    """

    NUMCOLORS = 4  # Number of single-color windows to auto-generate

    def __init__(self, **kwargs):

        # Generic load/init designer-based GUI
        parent = kwargs.get('parent')

        super(CRIkitUI_process, self).__init__(parent) ### EDIT ###
        
        self.parent = parent
        self.bcpre = _BCPre()
        self.fid = None
        
        self.filename = kwargs.get('filename')
        self.path = kwargs.get('path')
        self.dataset_name = kwargs.get('dataset_name')

        self.hsi = kwargs.get('hsi')
        if not isinstance(self.hsi, Hsi):
            self.hsi = Hsi()

        self.dark = Spectra()
        self.nrb = Spectra()

        # Overlays
        self.overlays = []
        self.show_overlays = True

        # ROI's to plot instead of random spectra
        # Primarily affects dialogPlotEffect activities
        # Also affected by setting actionUseSet
        self.preview_rois = None

        # Piecewise NRB's (not always used)
        self.nrb_left = Spectra()
        self.nrb_right = Spectra()

        # Internal Parameters
        self._anscombe_params = None


        self.plotter = _SciPlotUI(show=False, parent=self.parent)
        self._mpl_v1 = self.plotter._mpl_v1

        self.ui = Ui_MainWindow() ### EDIT ###


        self.ui.setupUi(self)     ### EDIT ###

        # Match UI Show overlays to attribute of this class
        self.ui.actionShowOverlays.setChecked(self.show_overlays)


        # Initialize Intensity image (single frequency B&W)
        self.img_BW = widgetBWImg(parent=self, figfacecolor=[1, 1, 1])
        if self.img_BW.ui.checkBoxFixed.checkState() == 0:
            self.img_BW.ui.spinBoxMax.setValue(self.img_BW.data.maxer)
            self.img_BW.ui.spinBoxMin.setValue(self.img_BW.data.minner)

        self.ui.sweeperVL.insertWidget(0, self.img_BW, stretch=1, alignment=_QtCore.Qt.AlignHCenter)
        try:
            self.img_BW.mpl.fig.tight_layout(pad=2)
        except Exception:
            print('tight_layout failed (CrikitUI: 1')

        # ID used for matplotlib to connect to a figure
        self.cid = None

        # Initialize Single-Color RGB widgets
        self.img_RGB_list = []

        for count in range(self.NUMCOLORS):
            self.img_RGB_list.append(widgetSglColor(figfacecolor=[1, 1, 1],
                                                    parent=self))

        # Split from previous for-loop for compactness of code
        for count, rgb_img in enumerate(self.img_RGB_list):
            color_str = rgb_img.colormode.ui.comboBoxFGColor.itemText(count)

            # Note: colors.to_rgb exists in MPL 2*, but is under colorConverter
            # in MPL < 2.
            rgb_img.data.colormap = _mpl.colors.colorConverter.to_rgb(_mpl.colors.cnames[color_str])
            rgb_img.colormode.ui.comboBoxFGColor.setCurrentIndex(count)

            rgb_img.popimage.ui.pushButtonSpectrum.setEnabled(False)
            self.ui.tabColors.addTab(rgb_img, 'Color ' + str(count))


            rgb_img.math.ui.pushButtonBasicMath.setEnabled(False)
            rgb_img.math.ui.pushButtonScripting.setEnabled(False)

            rgb_img.math.ui.pushButtonOpFreq1.pressed.connect(self.setOpFreq1)
            rgb_img.math.ui.pushButtonOpFreq2.pressed.connect(self.setOpFreq2)
            rgb_img.math.ui.pushButtonOpFreq3.pressed.connect(self.setOpFreq3)
            rgb_img.math.ui.comboBoxOperations.currentIndexChanged.connect(self.opChange)
            rgb_img.math.ui.pushButtonCondFreq1.pressed.connect(self.setCondFreq1)
            rgb_img.math.ui.pushButtonCondFreq2.pressed.connect(self.setCondFreq2)
            rgb_img.math.ui.pushButtonCondFreq3.pressed.connect(self.setCondFreq3)
            rgb_img.math.ui.comboBoxCondOps.currentIndexChanged.connect(self.condOpChange)
            rgb_img.math.ui.comboBoxCondInEquality.currentIndexChanged.connect(self.condInEqualityChange)
            rgb_img.math.ui.spinBoxInEquality.editingFinished.connect(self.spinBoxInEqualityChange)
            rgb_img.math.ui.pushButtonBasicMath.pressed.connect(self.doMath)
            rgb_img.ui.spinBoxMax.editingFinished.connect(self.doComposite)
            rgb_img.ui.spinBoxMin.editingFinished.connect(self.doComposite)
            rgb_img.math.ui.spinBoxGain.editingFinished.connect(self.doComposite)


        self.img_Composite = widgetCompositeColor(self.img_RGB_list,
                                                  figfacecolor=[1, 1, 1])
        self.img_Composite2 = widgetCompositeColor(self.img_RGB_list,
                                                   figfacecolor=[1, 1, 1])

        self.ui.tabColors.addTab(self.img_Composite, 'Composite Image')

        self.ui.sweeperVL_2.insertWidget(0, self.img_Composite2, stretch=1, alignment=_QtCore.Qt.AlignHCenter)

        self.ui.tabColors.currentChanged.connect(self.checkCompositeUpdate)


        # SIGNALS & SLOTS

        # Load Data
        self.ui.actionOpenHDFNIST.triggered.connect(self.fileOpenHDFNIST)
        self.ui.actionOpenHDFNISTOOC.triggered.connect(self.fileOpenHDFNISTOOC)
        self.ui.actionOpen_HDF_Macro_Raster_NIST.triggered.connect(self.fileOpenHDFMacroRasterNIST)

        self.ui.actionLoadNRB.triggered.connect(self.loadNRB)
        self.ui.actionLoadDark.triggered.connect(self.loadDark)

        self.ui.actionOpenDLMNIST.triggered.connect(self.fileOpenDLMNIST)
        self.ui.actionLoadNRBDLM.triggered.connect(self.loadNRBDLM)
        self.ui.actionLoadDarkDLM.triggered.connect(self.loadDarkDLM)

        self.ui.actionNRB_from_ROI.triggered.connect(self.nrbFromROI)
        self.ui.actionAppend_NRB_from_ROI.triggered.connect(self.nrbFromROI)

        self.ui.actionLoad_NRB_Left_Side.triggered.connect(self.loadNRB)
        self.ui.actionNRB_from_ROI_Left_Side.triggered.connect(self.nrbFromROI)

        self.ui.actionLoad_NRB_Right_Side.triggered.connect(self.loadNRB)
        self.ui.actionNRB_from_ROI_Right_Side.triggered.connect(self.nrbFromROI)

        self.ui.actionMergeNRBs.triggered.connect(self.mergeNRBs)
        self.ui.actionCropDarkSpectra.triggered.connect(self.cutEveryNSpectra)
        self.ui.actionCropNRBSpectra.triggered.connect(self.cutEveryNSpectra)

        self.ui.actionCreateMosaic.triggered.connect(self.mosaicTool)

        # Settings
        self.ui.actionSettings.triggered.connect(self.settings)

        # Undo
        self.ui.actionUndo.triggered.connect(self.doUndo)

        # Close event
        self.ui.closeEvent = self.closeEvent

        # Subtract DARK-Related
        self.ui.actionDarkSubtract.triggered.connect(self.subDark)
        self.ui.actionResidualSubtract.triggered.connect(self.subResidual)


        # ZERO first column or row
        self.ui.actionZeroFirstColumn.triggered.connect(self.zeroFirstColumn)
        self.ui.actionZeroFirstRow.triggered.connect(self.zeroFirstRow)
        self.ui.actionZeroLastColumn.triggered.connect(self.zeroLastColumn)
        self.ui.actionZeroLastRow.triggered.connect(self.zeroLastRow)

        # Set frequency WINDOW
        self.ui.actionFreqWindow.triggered.connect(self.freqWindow)

        # Calibrate Wavenumber
        self.ui.actionCalibrate.triggered.connect(self.calibrate)
        self.ui.actionResetCalibration.triggered.connect(self.calibrationReset)
        self.ui.actionEstCalibration.triggered.connect(self.specialEstCalibration1)

        # NIST Special
        self.ui.actionDeMosaicRGBImages.triggered.connect(self.specialDemosaicRGB)

        # Perform KK
        self.ui.actionKramersKronig.triggered.connect(self.doKK)

        self.ui.actionKKSpeedTest.setEnabled(False)

        # Variance Stabilize
        self.ui.actionAnscombe.triggered.connect(self.anscombe)
        self.ui.actionInverseAnscombe.triggered.connect(self.inverseAnscombe)
        self.ui.actionCalcAnscParams.triggered.connect(self.calcAnscombeParams)

        # DeNoise
        self.ui.actionDeNoise.triggered.connect(self.deNoise)
        self.ui.actionDeNoiseNRB.triggered.connect(self.deNoiseNRB)
        self.ui.actionDeNoiseDark.triggered.connect(self.deNoiseDark)

        # Error Correction
        self.ui.actionPhaseErrorCorrection.triggered.connect(self.errorCorrectPhase)
        self.ui.actionScaleErrorCorrection.triggered.connect(self.errorCorrectScale)
        self.ui.actionAmpErrorCorrection.triggered.connect(self.errorCorrectAmp)
        self.ui.actionSubtractROI.triggered.connect(self.subtractROIStart)

        # Preview ROIs
        self.ui.actionSetPreviewROI.triggered.connect(self.set_preview_rois)
        self.ui.actionDeletePreviewROI.triggered.connect(self.delete_preview_rois)
        self.ui.actionShowPreviewROI.triggered.connect(self.changeSlider)
        self.ui.actionShowPreviewROILegend.triggered.connect(self.changeSlider)

        # SAVE

        self.ui.actionSave.triggered.connect(self.save)

        # Plotting spectra-related
        self.ui.actionPointSpectrum.triggered.connect(self.pointSpectrum)
        self.ui.actionROISpectrum.triggered.connect(self.roiSpectrum)

        self.ui.actionDarkSpectrum.triggered.connect(self.plotDarkSpectrum)
        self.ui.actionNRBSpectrum.triggered.connect(self.plotNRBSpectrum)
        self.ui.actionLeftSideNRBSpect.triggered.connect(self.plotLeftNRBSpectrum)
        self.ui.actionRightSideNRBSpect.triggered.connect(self.plotRightNRBSpectrum)
        self.ui.actionShowPlotter.triggered.connect(self.plotter_show)

        # Overlays
        self.plotter.modelLine.dataDeleted.connect(self.updateOverlays)
        self.plotter.modelLine.dataChanged.connect(self.updateOverlays)
        self.plotter.all_cleared.connect(self.deleteOverlays)
        self.ui.actionShowOverlays.triggered.connect(self.checkShowOverlays)
        self.ui.actionShowOverlayLegend.triggered.connect(self.changeSlider)

       # Frequency-slider related
        self.ui.freqSlider.valueChanged.connect(self.changeSlider)
        self.ui.freqSlider.sliderPressed.connect(self.sliderPressed)
        self.ui.freqSlider.sliderReleased.connect(self.sliderReleased)
        self.ui.freqSlider.setTracking(True)

       # Frequency-slider display boxes
        self.ui.lineEditFreq.editingFinished.connect(self.lineEditFreqChanged)
        self.ui.lineEditPix.editingFinished.connect(self.lineEditPixChanged)
        self.ui.lineEditPix.setVisible(False)
        self.ui.labelFreqPixel.setVisible(False)

        # Settings
        self.ui.actionUseImagData.triggered.connect(self.changeSlider)

        # Help
        if help_index is not None:
            self.ui.actionHelpManual.triggered.connect(lambda: _webbrowser.open('file:///' + help_index, new=1))
        else:
            self.ui.actionHelpManual.setEnabled(False)

        self.ui.actionRamanPhantom.triggered.connect(self.makeRamanPhantom)
        self.ui.actionBCARSPhantom.triggered.connect(self.makeBCARSPhantom)

        # Jupyter console

        if jupyter_flag == 1:
            try:
                str_banner = 'Welcome to the embedded ipython console\n\n'
                self.jupyterConsole = QJupyterWidget(customBanner=str_banner)
            except Exception:
                print('Error loading embedded IPython Notebook')
            else:
                self.ui.tabMain.addTab(self.jupyterConsole, 'Jupyter/IPython Console')

                self.jupyterConsole.pushVariables({'ui':self.ui,
                                                'bcpre':self.bcpre,
                                                'dark':self.dark,
                                                'nrb':self.nrb,
                                                'crikit_data':self})
                self.ui.tabMain.currentChanged.connect(self.tabMainChange)


        # Temporary toolbar setup
        self.ui.toolBar.setVisible(True)
        self.ui.toolBar.setToolButtonStyle(_QtCore.Qt.ToolButtonTextUnderIcon)

        # Default toolbar is NIST Workflow
        self.toolbarSetup()

        # COMMAND LINE INTERPRETATION

        # file and dset info provided
        if (self.filename is not None) & (self.dataset_name is not None):
            if lazy5.inspect.valid_dsets(filename=self.filename,
                                        dset_list=self.dataset_name, pth=self.path):
                self.fileOpenHDFNIST(dialog=False)

        # Hsi provided
        temp = kwargs.get('hsi')
        if temp is not None:
            try:
                self.fileOpenSuccess(True)
            except Exception:
                print('Error in input hsi')
                self.hsi = Hsi()

        # x-array provided
        temp = kwargs.get('x')
        if temp is not None:
            try:
                self.hsi.x = temp
                self.hsi._x_rep.units = kwargs.get('x_units')
                self.hsi._x_rep.label = kwargs.get('x_label')
            except Exception:
                print('Error in input x-array')
                self.hsi.x = None

        # y-array provided
        temp = kwargs.get('y')
        if temp is not None:
            try:
                self.hsi.y = temp
                self.hsi._y_rep.units = kwargs.get('y_units')
                self.hsi._y_rep.label = kwargs.get('y_label')
            except Exception:
                print('Error in input y-array')
                self.hsi.y = None

        # freq-array provided
        temp = kwargs.get('f')
        if temp is not None:
            try:
                self.hsi.freq._data = temp
                self.hsi.freq._units = kwargs.get('f_units')
                self.hsi.freq._label = kwargs.get('f_label')
            except Exception:
                print('Error in input freq-array (f)')
                self.hsi.freq._data = None

        # data provided
        if isinstance(kwargs.get('data'), _np.ndarray):
            try:
                self.hsi.data = kwargs.get('data')
                self.hsi.check()
                self.fileOpenSuccess(True)
            except Exception:
                print('Error in input data')
                self.hsi = Hsi()

    def mosaicTool(self):
        win = MainWindowMosaic(parent=self)
        win.show()

    def updateHistory(self):
        self.ui.tableWidgetHistory.clearContents()
        self.ui.tableWidgetHistory.setRowCount(len(self.bcpre.attr_dict))
        for num, q in enumerate(self.bcpre.attr_dict):
            self.ui.tableWidgetHistory.setItem(num, 0, _QTableWidgetItem(q))
            self.ui.tableWidgetHistory.setItem(num, 1,
                                               _QTableWidgetItem(str(self.bcpre.attr_dict[q])))

    def plotter_show(self):
        self.plotter.show()
        self.plotter.raise_()

    def toolbarSetup(self):
        """
        Setup the tool ribbon icons
        """
        self.ui.toolbar_view_actions = {}
        self.ui.toolbar_view_configs = {'default' : [self.ui.actionOpenHDFNIST,self.ui.actionSave,'separator',
                                                     self.ui.actionPointSpectrum,self.ui.actionROISpectrum,
                                                     'separator', self.ui.actionUndo, 'separator', self.ui.actionLoadDark,
                                                     self.ui.actionLoadNRB, 'separator', self.ui.actionDarkSubtract,
                                                     self.ui.actionFreqWindow, self.ui.actionAnscombe,
                                                     self.ui.actionDeNoise, self.ui.actionInverseAnscombe,
                                                     self.ui.actionKramersKronig,
                                                     self.ui.actionPhaseErrorCorrection,
                                                     self.ui.actionScaleErrorCorrection,
                                                     self.ui.actionCalibrate],
                                        'NIST BCARS2' : [self.ui.actionOpenHDFNIST,self.ui.actionSave,'separator',
                                                         self.ui.actionPointSpectrum,self.ui.actionROISpectrum,
                                                         'separator', self.ui.actionUndo, 'separator', 
                                                         self.ui.actionLoadDark, self.ui.actionLoad_NRB_Right_Side,
                                                         'separator', self.ui.actionDarkSubtract, self.ui.actionEstCalibration,
                                                         self.ui.actionFreqWindow, self.ui.actionAnscombe,
                                                         self.ui.actionDeNoise, self.ui.actionInverseAnscombe,
                                                         self.ui.actionNRB_from_ROI_Left_Side,
                                                         self.ui.actionMergeNRBs, self.ui.actionKramersKronig,
                                                         self.ui.actionPhaseErrorCorrection,
                                                         self.ui.actionScaleErrorCorrection,
                                                         self.ui.actionCalibrate],
                                        'NIST BCARS1' : [self.ui.actionOpenDLMNIST,self.ui.actionSave,'separator',
                                                         self.ui.actionPointSpectrum,self.ui.actionROISpectrum,
                                                         'separator', self.ui.actionUndo, 'separator', 
                                                         self.ui.actionLoadDarkDLM, self.ui.actionLoadNRBDLM,
                                                         'separator', self.ui.actionDarkSubtract,
                                                         self.ui.actionFreqWindow, self.ui.actionAnscombe,
                                                         self.ui.actionDeNoise, self.ui.actionInverseAnscombe,
                                                         self.ui.actionKramersKronig, 
                                                         self.ui.actionPhaseErrorCorrection,
                                                         self.ui.actionScaleErrorCorrection,
                                                         self.ui.actionCalibrate],
                                        'None' : []}

        for k in self.ui.toolbar_view_configs:
            ret = self.ui.menuToolbar.addAction(k)
            ret.triggered.connect(self.toolbarSetting)
            ret.setCheckable(True)
            self.ui.toolbar_view_actions.update({k:ret})

        self.ui.toolbar_view_actions['default'].trigger()

    def toolbarSetting(self):
        """ Set the toolbar ribbon view """

        sndr = self.sender()
        action_key = None
        action = None

        for k in self.ui.toolbar_view_actions:
            acn = self.ui.toolbar_view_actions[k]
            if sndr == acn:
                self.ui.toolBar.clear()
                action_key = _copy.deepcopy(k)
                acn.setChecked(True)
            else:
                acn.setChecked(False)

        for to_add in self.ui.toolbar_view_configs[action_key]:
            if to_add == 'separator':
                self.ui.toolBar.addSeparator()
            else:
                self.ui.toolBar.addAction(to_add)
        

    def save(self):
        suffix = self.bcpre.dset_name_suffix

        ret = DialogSave.dialogSave(parent=self,
                                    current_filename=self.filename,
                                    current_path=self.path,
                                    current_dataset_name=self.dataset_name[0],
                                    suffix=suffix)
        if ret is None:
            pass # Save canceled
        else:
            self.save_filename = ret[0]
            self.save_path = ret[1]
            self.save_dataset_name = ret[2]

            self.save_grp = self.save_dataset_name.rpartition('/')[0]
            self.save_dataset_name_no_grp = self.save_dataset_name.rpartition('/')[-1]

            if isinstance(self.hsi.meta, dict):
                attr_dict = _copy.deepcopy(self.hsi.meta)
            else:
                print('Meta data (hsi.meta) is not a dictionary')
                attr_dict = {}

            attr_dict.update(self.bcpre.attr_dict)

            try:
                ret_save = lazy5.create.save(self.save_filename, self.save_dataset_name,
                                            self.hsi._data, pth=self.save_path,
                                            attr_dict= attr_dict, sort_attrs=True,
                                            chunks=True, verbose=True)
            except Exception as e:
                _traceback.print_exc(limit=1)
                print('Error in KK: {}'.format(e))
            else:
                if ret_save:
                    print('Save succeeded with no errors.')
                    self.setWindowTitle('{} -> {}'.format(self.windowTitle(), self.save_filename))

    def tabMainChange(self):
        if self.ui.tabMain.currentIndex() == 4:  # Jupyter console
            self.jupyterConsole._control.setFocus()

    def closeEvent(self, event):
        print('Closing')
        app = _QApplication.instance()
        app.closeAllWindows()
        app.quit()
        
        self.bcpre.pop_to_last(all=True)

        del_flag = 0

        for count in self.bcpre.cut_list:
            try:
                _os.remove(count + '.pickle')
            except Exception:
                print('Error in deleting old pickle files')
            else:
                del_flag += 1
        if del_flag == len(self.bcpre.cut_list):
            del self.bcpre.cut_list
        else:
            print('Did not delete pickle file cut list... Something went wrong')

        if self.fid:
            print('Closing HDF File')
            try:
                self.fid.close()
            except Exception:
                print('Something failed in closing the file')
            else:
                print('Successfully closed HDF File')

    def fileOpenHDFMacroRasterNIST(self, *args, dialog=True):
        """
        Open and load multiple datasets from HDF file that describe a single image. 
        Used for a macrostage rastering mode at NIST.

        dialog : bool
            Present a gui for file and dataset selection
        """

        # Get data and load into CRI_HSI class
        # This will need to change to accomodate multiple-file selection

        if dialog:
            try:
                if (self.filename is not None) & (self.path is not None):
                    to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='Hyperspectral Image')
                else:
                    to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='Hyperspectral Image')

                print('to_open: {}'.format(to_open))
                if to_open is not None:
                    self.path, self.filename, self.dataset_name = to_open
            except Exception as e:
                _traceback.print_exc(limit=1)
                print('Could not open file. Corrupt or not appropriate file format: {}'.format(e))
            else:
                if to_open is not None:
                    self.hsi = Hsi()
                    print('Path: {}'.format(self.path))
                    print('filename: {}'.format(self.filename))
                    print('dset name: {}'.format(self.dataset_name))
                    success = io_nist_macro(self.path, self.filename, self.dataset_name,
                                            self.hsi)
                    print('Was successful: {}'.format(success))
                    print('HSI shape: {}'.format(self.hsi.shape))
                    print('Succes: {}'.format(success))
                    self.fileOpenSuccess(success)
        else:
            self.hsi = Hsi()
            success = io_nist_macro(self.path, self.filename, self.dataset_name,
                                    self.hsi)
            self.fileOpenSuccess(success)

    def fileOpenHDFNIST(self, *args, dialog=True):
        """
        Open and load HDF5 File

        dialog : bool
            Present a gui for file and dataset selection
        """

        # Get data and load into CRI_HSI class
        # This will need to change to accomodate multiple-file selection

        if dialog:
            try:
                if (self.filename is not None) & (self.path is not None):
                    to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='Hyperspectral Image')
                else:
                    to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='Hyperspectral Image')

                print('to_open: {}'.format(to_open))
                if to_open is not None:
                    self.path, self.filename, self.dataset_name = to_open
            except Exception as e:
                _traceback.print_exc(limit=1)
                print('Could not open file. Corrupt or not appropriate file format: {}'.format(e))
            else:
                if to_open is not None:
                    self.hsi = Hsi()
                    print('Path: {}'.format(self.path))
                    print('filename: {}'.format(self.filename))
                    print('dset name: {}'.format(self.dataset_name))
                    success = io_nist(self.path, self.filename, self.dataset_name,
                                      self.hsi)
                    print('Was successful: {}'.format(success))
                    print('HSI shape: {}'.format(self.hsi.shape))
                    self.fileOpenSuccess(success)
        else:
            self.hsi = Hsi()
            success = io_nist(self.path, self.filename, self.dataset_name,
                              self.hsi)
            self.fileOpenSuccess(success)

    def fileOpenHDFNISTOOC(self, *args):
        """
        Open and load HDF5 File OUT-OF-CORE

        dialog : bool
            Present a gui for file and dataset selection
        """

        # Get data and load into CRI_HSI class
        # This will need to change to accomodate multiple-file selection

        try:
            if (self.filename is not None) & (self.path is not None):
                to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='Hyperspectral Image')
            else:
                to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='Hyperspectral Image')

            print('to_open: {}'.format(to_open))
            if to_open is not None:
                self.path, self.filename, self.dataset_name = to_open
                self.dataset_name = self.dataset_name[0]
        except Exception:
            print('Could not open file. Corrupt or not appropriate file format.')
        else:
            if to_open is not None:
                self.hsi = Hsi()
                success_fid = io_nist_ooc(self.path, self.filename, self.dataset_name,
                                   self.hsi)
                if success_fid:
                    self.fid = success_fid
                    print('HSI shape: {}'.format(self.hsi.shape))
                    self.ui.actionUndo_Backup_Enabled.setChecked(False)
                    self.ui.actionUndo_Backup_Enabled.setEnabled(False)

                    self.fileOpenSuccess(True)

    def fileOpenDLMNIST(self):
        """
        Open and load DLM File
        """

        # Get data and load into CRI_HSI class
        # This will need to change to accomodate multiple-file selection
        filename_header,_ = _QFileDialog.getOpenFileName(self, 'Open Header File',
                                                         './', 'All Files (*.*)')


        if filename_header != '':
            self.path = _os.path.dirname(filename_header) + '/'
            filename_data,_ = _QFileDialog.getOpenFileName(self, 'Open Data File',
                                                           self.path,
                                                           'All Files (*.*)')

            if filename_data != '':
                self.path = _os.path.dirname(filename_data) + '/'
                self.filename = filename_data.split(_os.path.dirname(filename_data))[1][1::]
                self.filename_header = filename_header

                success = io_nist_dlm(self.path, self.filename_header,
                                      self.filename,
                                      self.hsi)
                self.fileOpenSuccess(success)

    def fileOpenSuccess(self, success):
        """
        Executed after a file is loaded. Checks success and appropriately
        activates or deactivates action (buttons)
        """
        if success:
            # * If HSI is integer dtype, convert to float
            if (self.hsi.data.dtype.kind in ['i','u']) & isinstance(self.hsi.data, _np.ndarray):
                print('Converting HSI from int to float')
                self.hsi.data = 1.0 * self.hsi.data

            self.setWindowTitle('{}: {}'.format(self.windowTitle(), self.filename))
            # FILE
            self.ui.actionSave.setEnabled(True)

            # EDIT
            self.ui.actionZeroFirstColumn.setEnabled(True)
            self.ui.actionZeroFirstRow.setEnabled(True)
            self.ui.actionZeroLastColumn.setEnabled(True)
            self.ui.actionZeroLastRow.setEnabled(True)
            self.ui.actionFreqWindow.setEnabled(True)
            self.ui.actionCalibrate.setEnabled(True)
            self.ui.actionResetCalibration.setEnabled(True)

            # VIEW
            self.ui.actionPointSpectrum.setEnabled(True)
            self.ui.actionROISpectrum.setEnabled(True)
            self.ui.actionSetPreviewROI.setEnabled(True)
            self.ui.actionDeletePreviewROI.setEnabled(True)

            # IMPORT/LOAD
            self.ui.actionLoadDark.setEnabled(True)
            self.ui.actionLoadNRB.setEnabled(True)
            self.ui.actionLoadDarkDLM.setEnabled(True)
            self.ui.actionLoadNRBDLM.setEnabled(True)
            self.ui.actionNRB_from_ROI.setEnabled(True)
            # self.ui.actionAppend_NRB_from_ROI.setEnabled(True)
            self.ui.actionLoad_NRB_Left_Side.setEnabled(True)
            self.ui.actionLoad_NRB_Right_Side.setEnabled(True)
            self.ui.actionNRB_from_ROI_Left_Side.setEnabled(True)
            self.ui.actionNRB_from_ROI_Right_Side.setEnabled(True)

            # PREPROCESS
            self.ui.actionResidualSubtract.setEnabled(True)
            self.ui.actionAnscombe.setEnabled(True)
            self.ui.actionInverseAnscombe.setEnabled(True)

            self.ui.actionDeNoise.setEnabled(True)
            self.ui.actionAmpErrorCorrection.setEnabled(True)
            self.ui.actionSubtractROI.setEnabled(True)
            self.ui.actionNRB_from_ROI.setEnabled(True)
            self.ui.menuVariance_Stabilize.setEnabled(True)

            # NIST SPECIAL
            self.ui.actionEstCalibration.setEnabled(True)
            self.ui.actionDeMosaicRGBImages.setEnabled(True)

            is_complex = _np.iscomplexobj(self.hsi.data)
            if is_complex:
                self.ui.actionPhaseErrorCorrection.setEnabled(True)
                self.ui.actionScaleErrorCorrection.setEnabled(True)
        else:
            self.ui.actionLoadDark.setEnabled(False)
            self.ui.actionLoadNRB.setEnabled(False)
            self.ui.actionZeroFirstColumn.setEnabled(False)
            self.ui.actionZeroFirstRow.setEnabled(False)
            self.ui.actionZeroLastColumn.setEnabled(False)
            self.ui.actionZeroLastRow.setEnabled(False)

        # Backup for Undo
        offset = self.hsi.meta.get(self.bcpre.PREFIX)
        if offset:
            self.bcpre.offset = offset
            self.bcpre.add_step(['Continue'])
        else:
            self.bcpre.add_step(['Raw'])
        del offset
        self.updateHistory()

        if self.ui.actionUndo_Backup_Enabled.isChecked():
            try:
                _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
            except Exception as e:
                _traceback.print_exc(limit=1)
                print(e)
                print('Error in pickle backup (Undo functionality)')
            else:
                self.bcpre.backed_up()


        # Set frequency slider and associated displays
        self.ui.freqSlider.setMinimum(self.hsi.freq.op_range_pix[0])
        self.ui.freqSlider.setMaximum(self.hsi.freq.op_range_pix[-1])
        self.ui.freqSlider.setSliderPosition(self.hsi.freq.op_range_pix[0])
        pos = self.ui.freqSlider.sliderPosition()
        self.ui.lineEditPix.setText(str(self.ui.freqSlider.sliderPosition()))
        self.ui.lineEditFreq.setText(str(round(self.hsi.f[0], 2)))
        # Set BW Class Data
        self.img_BW.initData()

        if _np.iscomplexobj(self.hsi.data):
            if self.ui.actionUseImagData.isChecked():
                self.img_BW.data.grayscaleimage = _np.imag(self.hsi.data[:, :, pos])
                val_extrema = _np.max(_np.abs(self.img_BW.data.grayscaleimage))
            else:
                self.img_BW.data.grayscaleimage = _np.real(self.hsi.data[:, :, pos])
                val_extrema = _np.max(_np.abs(self.img_BW.data.grayscaleimage))
        else:
            self.img_BW.data.grayscaleimage = self.hsi.data[:, :, pos]
            val_extrema = _np.max(_np.abs(self.img_BW.data.grayscaleimage))
        
        self.img_BW.ui.spinBoxMin.setMinimum(-1.1*val_extrema)
        self.img_BW.ui.spinBoxMin.setMaximum(1.1*val_extrema)
        self.img_BW.ui.spinBoxMax.setMinimum(-1.1*val_extrema)
        self.img_BW.ui.spinBoxMax.setMaximum(1.1*val_extrema)

        xlabel = ''
        if isinstance(self.hsi.x_rep.label, str):
            xlabel += self.hsi.x_rep.label.strip()
        if isinstance(self.hsi.x_rep.units, str):
            xlabel += ' ('
            xlabel += self.hsi.x_rep.units.strip()
            xlabel += ')'

        # print('Xlabel: {}'.format(xlabel))
        ylabel = ''
        if isinstance(self.hsi.y_rep.label, str):
            ylabel += self.hsi.y_rep.label.strip()
        if isinstance(self.hsi.y_rep.units, str):
            ylabel += ' ('
            ylabel += self.hsi.y_rep.units.strip()
            ylabel += ')'
        # xlabel = r'{} ({})'.format(self.hsi.x_rep.label.strip(), self.hsi.x_rep.units.strip())
        # ylabel = r'{} ({})'.format(self.hsi.y_rep.label.strip(), self.hsi.y_rep.units.strip())

        # print('Ylabel: {}'.format(ylabel))
        self.img_BW.data.set_x(self.hsi.x, xlabel)
        self.img_BW.data.set_y(self.hsi.y, ylabel)
        # Set min/max, fixed, compress, etc buttons to defaults
        self.img_BW.ui.checkBoxFixed.setChecked(False)
        # self.img_BW.ui.checkBoxCompress.setChecked(False)
        self.img_BW.ui.comboBoxAboveMax.setCurrentIndex(0)
        self.img_BW.ui.checkBoxRemOutliers.setChecked(False)
        self.createImgBW(self.img_BW.data.image)
        self.img_BW.mpl.draw()
        # RGB images
        temp = 0*self.img_BW.data.grayscaleimage

        # Re-initialize RGB images

        for num, rgb_img in enumerate(self.img_RGB_list):
            rgb_img.initData()
            rgb_img.math.clear()
            rgb_img.data.grayscaleimage = temp
            rgb_img.data.set_x(self.hsi.x, xlabel)
            rgb_img.data.set_y(self.hsi.y, ylabel)

            color_str = rgb_img.colormode.ui.comboBoxFGColor.itemText(num)
            rgb_img.data.colormap = _mpl.colors.colorConverter.to_rgb(_mpl.colors.cnames[color_str])
            rgb_img.colormode.ui.comboBoxFGColor.setCurrentIndex(num)

            # Cute way of setting the colormap to last setting and replotting
            rgb_img.changeColor()

            # Enable Math
            # rgb_img.math.ui.pushButtonDoMath.setEnabled(True)
            rgb_img.math.ui.pushButtonBasicMath.setEnabled(True)

            # Enable mean spectrum from RGB images
            # Note: if load new file after one has already loaded, need to disconnect
            # signal then reconnect (or could have ignored, but this is easier)
            try:
                rgb_img.popimage.ui.pushButtonSpectrum.pressed.disconnect()
            except Exception:
                pass

            rgb_img.popimage.ui.pushButtonSpectrum.pressed.connect(self.spectrumColorImg)

            rgb_img.popimage.ui.pushButtonSpectrum.setEnabled(True)

            rgb_img.gsinfo.ui.spinBoxMin.setMinimum(-1.1*val_extrema)
            rgb_img.gsinfo.ui.spinBoxMin.setMaximum(1.1*val_extrema)
            rgb_img.gsinfo.ui.spinBoxMax.setMinimum(-1.1*val_extrema)
            rgb_img.gsinfo.ui.spinBoxMax.setMaximum(1.1*val_extrema)

        # Set X- and Y- scales, labels, etc for composite color images
        self.img_Composite.data.set_x(self.hsi.x, xlabel)
        self.img_Composite.data.set_y(self.hsi.y, ylabel)
        self.img_Composite2.data.set_x(self.hsi.x, xlabel)
        self.img_Composite2.data.set_y(self.hsi.y, ylabel)

    def loadDark(self):
        """
        Open HDF file and load dark spectrum(a)
        """

        if (self.filename is not None) & (self.path is not None):
            to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='Dark')
        else:
            to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='Dark')
        print('To_open: {}'.format(to_open))

        if to_open is not None:
            pth, filename, datasets = to_open
            success = io_nist(pth, filename, datasets, self.dark)

            if success:
                # If Dark is integer dtype, convert to float
                if self.dark.data.dtype.kind in ['u', 'i']:
                    print('Converting Dark from int to float')
                    self.dark.data = 1.0*self.dark.data

                if self.dark.shape[-1] == self.hsi.freq.size:
                    self.ui.actionDarkSubtract.setEnabled(True)
                    self.ui.actionDarkSpectrum.setEnabled(True)
                    self.ui.actionDeNoiseDark.setEnabled(True)
                    if self.nrb.data is not None:
                        self.ui.actionCalcAnscParams.setEnabled(True)
                else:
                    self.dark = Spectra()
                    print('Dark was the wrong shape')
            else:
                self.dark = Spectra()
                self.ui.actionDarkSubtract.setEnabled(False)
                self.ui.actionDarkSpectrum.setEnabled(False)
                self.ui.actionDeNoiseDark.setEnabled(False)


    def loadDarkDLM(self):
        """
        Open DLM file and load dark spectrum(a)
        """


        filename,_ = _QFileDialog.getOpenFileName(self, 'Open Dark File',
                                                  self.path,
                                                  'All Files (*.*)')
        if filename != '':
            filename = filename.split(_os.path.dirname(filename))[1][1::]


            # Spectra first
            self.dark = Spectra()
            success = io_nist_dlm(self.path, self.filename_header, filename,
                                  self.dark)
            if not success: # Maybe Spectrum
                self.dark = Spectrum()
                success = io_nist_dlm(self.path, self.filename_header, filename,
                                      self.dark)


            if success:
                # If Dark is integer dtype, convert to float
                if self.dark.data.dtype.kind in ['u', 'i']:
                    print('Converting Dark from int to float')
                    self.dark.data = 1.0*self.dark.data

                if self.dark.shape[-1] == self.hsi.freq.size:
                    self.ui.actionDarkSubtract.setEnabled(True)
                    self.ui.actionDarkSpectrum.setEnabled(True)
                    if self.nrb.data is not None:
                        self.ui.actionCalcAnscParams.setEnabled(True)
                else:
                    self.dark = Spectra()
                    print('Dark was the wrong shape')
            else:
                self.dark = Spectra()
                self.ui.actionDarkSubtract.setEnabled(False)
                self.ui.actionDarkSpectrum.setEnabled(False)


    def loadNRB(self):
        """
        Open HDF file and load NRB spectrum(a)
        """

        sender = self.sender()

        if sender == self.ui.actionLoadNRB:
            nrb = self.nrb
        elif sender == self.ui.actionLoad_NRB_Left_Side:
            nrb = self.nrb_left
        elif sender == self.ui.actionLoad_NRB_Right_Side:
            nrb = self.nrb_right


        if (self.filename is not None) & (self.path is not None):
            to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='NRB')
        else:
            to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='NRB')

        if to_open is not None:
            pth, filename, datasets = to_open

            success = io_nist(pth, filename, datasets, nrb)
            if success:
                # If NRB is integer dtype, convert to float
                if nrb.data.dtype.kind in ['u', 'i']:
                    print('Converting NRB from int to float')
                    nrb.data = 1.0*nrb.data

                if nrb.shape[-1] == self.hsi.freq.size:
                    if sender == self.ui.actionLoadNRB:
                        self.ui.menuCoherent_Raman_Imaging.setEnabled(True)
                        self.ui.actionKramersKronig.setEnabled(True)
                        self.ui.actionKKSpeedTest.setEnabled(True)
                        self.ui.actionNRBSpectrum.setEnabled(True)
                        self.ui.actionDeNoiseNRB.setEnabled(True)
                        if self.dark.data is not None:
                            self.ui.actionCalcAnscParams.setEnabled(True)
                    elif sender == self.ui.actionLoad_NRB_Left_Side:
                        self.ui.actionLeftSideNRBSpect.setEnabled(True)
                        if ((self.nrb_left.data is not None) and
                                (self.nrb_right.data is not None)):
                            if self.nrb_right.mean().size == self.nrb_left.mean().size:
                                self.ui.actionMergeNRBs.setEnabled(True)
                    elif sender == self.ui.actionLoad_NRB_Right_Side:
                        self.ui.actionRightSideNRBSpect.setEnabled(True)
                        if ((self.nrb_left.data is not None) and
                                (self.nrb_right.data is not None)):
                            if self.nrb_right.mean().size == self.nrb_left.mean().size:
                                self.ui.actionMergeNRBs.setEnabled(True)
                else:
                    nrb = Spectra()
                    print('NRB was the wrong shape')
            else:
                nrb = Spectra()
                if sender == self.ui.actionLoadNRB:
                    self.ui.actionKramersKronig.setEnabled(False)
                    self.ui.actionKKSpeedTest.setEnabled(False)
                    self.ui.actionNRBSpectrum.setEnabled(False)

    def loadNRBDLM(self):
        """
        Open DLM file and load NRB spectrum(a)
        """


        filename, _ = _QFileDialog.getOpenFileName(self, 'Open NRB File',
                                                   self.path,
                                                   'All Files (*.*)')
        if filename != '':
            filename = filename.split(_os.path.dirname(filename))[1][1::]


            # Spectra first
            self.nrb = Spectra()
            success = io_nist_dlm(self.path, self.filename_header, filename,
                                  self.nrb)
            if not success: # Maybe Spectrum
                self.nrb = Spectrum()
                success = io_nist_dlm(self.path, self.filename_header, filename,
                                      self.nrb)
            print('Success: {}'.format(success))

            if success:
                if self.dark.shape[-1] == self.hsi.freq.size:
                    self.ui.actionKramersKronig.setEnabled(True)
                    self.ui.actionKKSpeedTest.setEnabled(True)
                    self.ui.actionNRBSpectrum.setEnabled(True)
                    self.ui.actionDeNoiseNRB.setEnabled(True)
                    if self.dark.data is not None:
                        self.ui.actionCalcAnscParams.setEnabled(True)
                else:
                    self.nrb = Spectra()
                    print('NRB was the wrong shape')
            else:
                self.nrb = Spectra()
                self.ui.actionKramersKronig.setEnabled(False)
                self.ui.actionKKSpeedTest.setEnabled(False)
                self.ui.actionNRBSpectrum.setEnabled(False)
                self.ui.actionDeNoiseNRB.setEnabled(False)

    def get_preview_spectra(self, full=False):
        """ If self.preview_rois is set, output the mean spectra from thos regions """
        if full:
            rng = self.hsi.freq.pix_vec
        else:
            rng = self.hsi.freq.op_range_pix

        if self.preview_rois:
            prev_spectra = []

            for prx, pry in self.preview_rois:

                mask, path = _roimask(self.hsi.x, self.hsi.y, prx, pry)

                mask_hits = _np.sum(mask)
                if mask_hits > 0:  # Len(mask) > 0
                    temp = self.hsi.data[mask == 1][..., rng]
                    
                    if mask_hits > 1:
                        prev_spectra.append(_np.mean(temp, axis=0))
                    else:
                        prev_spectra.append(temp[self.hsi.freq.op_range_pix])
            return _np.array(prev_spectra)

        else:
            return self.hsi.get_rand_spectra(2, pt_sz=3, quads=True)

    def set_preview_rois(self):
        """ Set the preview ROIs. NOTE: this function just sets the signal for the MPL window """
        if self.cid is None:
            # Updated by _roiClick
            self.preview_rois = []
            self.x_loc_list = []
            self.y_loc_list = []

            self.cid = self.img_BW.mpl.mpl_connect('button_press_event',
                                                   lambda event: self._roiPreviewClick(event))

            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
            self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
        pass

    def showPreviewRois(self):
        lines = []
        if self.preview_rois:
            for num, (prx, pry) in enumerate(self.preview_rois):
                temp, = self.img_BW.mpl.ax.plot(prx, pry, label='Preview ROI {}'.format(num),
                                            linestyle=':', color='C{}'.format(num % 10))
                lines.append(temp)
            
            if self.ui.actionShowPreviewROILegend.isChecked():
                # lg = self.img_BW.mpl.ax.legend(handles=lines, loc='lower left', mode='expand', 
                #                                bbox_to_anchor=(0.01, 1.02, 1., 0.2),
                #                                ncol=2, fontsize=9)
                lg = self.img_BW.mpl.ax.legend(handles=lines, loc='best', 
                                            ncol=2, fontsize=9)
                self.img_BW.mpl.ax.add_artist(lg)
            try:
                self.img_BW.mpl.fig.tight_layout(pad=1)
            except Exception:
                print('tight_layout failed (CrikitUI: 2')
            self.img_BW.mpl.draw()

    def _roiPreviewClick(self, event, *args):
        """
        Capture region-of-interest mouse click locations in MPL window.
        """

        getx = self.img_BW.mpl.ax.get_xlim()
        gety = self.img_BW.mpl.ax.get_ylim()

        if event.button == 1:
            if event.inaxes == self.img_BW.mpl.ax:

                self.x_loc_list.append(event.xdata)
                self.y_loc_list.append(event.ydata)

                if len(self.x_loc_list) == 1:
                    self.img_BW.mpl.ax.plot(self.x_loc_list, self.y_loc_list,
                                            markerfacecolor=[.9, .9, 0],
                                            markeredgecolor=[.9, .9, 0],
                                            marker='+',
                                            markersize=10,
                                            linestyle='None')
                    self.img_BW.mpl.ax.set_xlim(getx)
                    self.img_BW.mpl.ax.set_ylim(gety)
                    self.img_BW.mpl.draw()
                else:
                    self.img_BW.mpl.ax.plot(self.x_loc_list[-2:],
                                            self.y_loc_list[-2:],
                                            linewidth=2,
                                            marker='+',
                                            markersize=10,
                                            color=[.9, .9, 0],
                                            markerfacecolor=[.9, .9, 0],
                                            markeredgecolor=[.9, .9, 0])
                    self.img_BW.mpl.ax.set_xlim(getx)
                    self.img_BW.mpl.ax.set_ylim(gety)

                    self.img_BW.mpl.draw()
        else:
            if len(self.x_loc_list) > 0: # Insure at least 1 vertex
                self.x_loc_list.append(self.x_loc_list[0])
                self.y_loc_list.append(self.y_loc_list[0])

                self.img_BW.mpl.ax.plot(self.x_loc_list[-2:],
                                        self.y_loc_list[-2:],
                                        linewidth=2,
                                        marker='+',
                                        markersize=10,
                                        color=[.9, .9, 0],
                                        markerfacecolor=[.9, .9, 0],
                                        markeredgecolor=[.9, .9, 0])
                self.img_BW.mpl.ax.set_xlim(getx)
                self.img_BW.mpl.ax.set_ylim(gety)
                self.img_BW.mpl.draw()

                self.preview_rois.append([self.x_loc_list, self.y_loc_list])

                self.x_loc_list = []
                self.y_loc_list = []
            else:
                del self.x_loc_list
                del self.y_loc_list
            
                self.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
                self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
                self.img_BW.mpl.mpl_disconnect(self.cid)
                self.cid = None
                self.changeSlider()

    def delete_preview_rois(self):
        self.preview_rois = None
        self.changeSlider()

    def mergeNRBs(self):
        """
        Interactive merge of the left- and right-side NRB
        """
        if self.nrb_left is not None and self.nrb_right is not None:
            rng = self.hsi.freq.op_range_pix

            if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
                preview_spectra = self.hsi.get_rand_spectra(2, pt_sz=3, quads=True)
            else:
                preview_spectra = self.get_preview_spectra(full=False)

            if _np.iscomplexobj(preview_spectra):
                preview_spectra = preview_spectra.imag

            plugin = _widgetMergeNRBs(wn_vec=self.hsi.f,
                                      nrb_left=self.nrb_left.mean()[rng],
                                      nrb_right=self.nrb_right.mean()[rng])
            winPlotEffect = _DialogPlotEffect.dialogPlotEffect(data=preview_spectra,
                                                               x=self.hsi.f,
                                                               plugin=plugin)

            if winPlotEffect is not None:
                print('NRB merge pixel: {}'.format(winPlotEffect.parameters['pix_switchpt']))
                print('NRB merge WN: {}'.format(winPlotEffect.parameters['wn_switchpt']))
                print('NRB merge scale left side: {}'.format(winPlotEffect.parameters['scale_left']))

                self.nrb.data = _np.squeeze(0*self.nrb_left.mean())
                print('nrb shape: {}'.format(self.nrb.shape))

                inst_nrb_merge = _MergeNRBs(nrb_left=self.nrb_left.mean()[rng],
                                            nrb_right=self.nrb_right.mean()[rng],
                                            pix=winPlotEffect.parameters['pix_switchpt'],
                                            left_side_scale=winPlotEffect.parameters['scale_left'])
                nrb_merge = inst_nrb_merge.calculate()

                # Need 2D because of class Spectra NOT Spectrum
                self.nrb.data[:, self.hsi.freq.op_range_pix] = nrb_merge

                self.ui.actionNRBSpectrum.setEnabled(True)
                self.ui.actionKramersKronig.setEnabled(True)
                self.ui.actionKKSpeedTest.setEnabled(True)
                self.ui.menuCoherent_Raman_Imaging.setEnabled(True)
                self.ui.actionDeNoiseNRB.setEnabled(True)
                if self.dark.data is not None:
                    self.ui.actionCalcAnscParams.setEnabled(True)

                wn, pix = find_nearest(self.hsi.f_full, \
                   self.hsi.f[winPlotEffect.parameters['pix_switchpt']])

                # Backup for Undo
                self.bcpre.add_step(['MergeNRBs',
                                     'pix_switchpt', pix,
                                     'wn_switchpt',
                                     winPlotEffect.parameters['wn_switchpt'],
                                     'scale_left',
                                     winPlotEffect.parameters['scale_left']])
                self.updateHistory()

        else:
            pass

    def cutEveryNSpectra(self):
        """
        Cut m spectra every n spectra
        """
        sdr = self.sender()
        if sdr == self.ui.actionCropDarkSpectra:
            preview_spectra = self.dark.data.sum(axis=-1)
        elif sdr == self.ui.actionCropNRBSpectra:
            preview_spectra = self.nrb.data.sum(axis=-1)
        plugin = _widgetCutEveryNSpectra()
        
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(data=preview_spectra,
                                                            x=_np.arange(preview_spectra.size),
                                                            plugin=plugin)

        if winPlotEffect is not None:
            # Do stuff here
            params = _copy.deepcopy(winPlotEffect.parameters)
            params.pop('name')
            params.pop('long_name')

            cutter = _CutEveryNSpectra(**params)
            if sdr == self.ui.actionCropDarkSpectra:
                self.dark.data = cutter.calculate(self.dark.data)
                # Backup for Undo
                h_list = ['CutDark']
                for k in params:
                    h_list.extend([k, params[k]])
                self.bcpre.add_step(h_list)
                self.updateHistory()
            elif sdr == self.ui.actionCropNRBSpectra:
                self.nrb.data = cutter.calculate(self.nrb.data)
                h_list = ['CutNRB']
                for k in params:
                    h_list.extend([k, params[k]])
                self.bcpre.add_step(h_list)
                self.updateHistory()
        else:
            pass
        del winPlotEffect

    def settings(self):
        """
        Go to settings tab
        """
        index = self.ui.tabMain.indexOf(self.ui.tabSettings)
        self.ui.tabMain.setCurrentIndex(index)

    def calibrate(self):
        """
        Calibrate spectra
        """

        if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
            preview_spectra = self.hsi.get_rand_spectra(5, pt_sz=3, quads=True, full=True)
        else:
            preview_spectra = self.get_preview_spectra(full=True)

        if _np.iscomplexobj(preview_spectra):
                preview_spectra = preview_spectra.imag

        plugin = _widgetCalibrate(calib_dict=self.hsi.freq.calib)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(preview_spectra,
                                                           x=self.hsi.f_full,
                                                           plugin=plugin,
                                                           parent=self)

        if winPlotEffect is not None:
            #print('New Calibration Dictionary: {}'.format(winPlotEffect.new_calib_dict))
            self.hsi.freq.calib = winPlotEffect.parameters['new_calib_dict']
            self.hsi.freq.update()
        self.changeSlider()


    def calibrationReset(self):
        """
        Set self.hsi.freqcalib back to self.hsi.freqcaliborig
        """
        self.hsi.freq.calib = None
        self.hsi.freq.update()
        self.changeSlider()

    def specialEstCalibration1(self):
        """
        For NIST BCARS 2, maximum raw spectrum occurs at approximately
        745.8 nm (18/07/11)
        """
        msg = _QMessageBox(self)
        msg.setIcon(_QMessageBox.Warning)
        msg.setText('Estimate calibration for NIST BCARS2?')
        msg.setWindowTitle('Confirm estimation of calibration')
        msg.setInformativeText('This should only be applied to RAW BCARS2 data from NIST.')
        msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
        msg.setDefaultButton(_QMessageBox.Ok)
        out = msg.exec()

        if out == _QMessageBox.Ok:
            nm_diff = 745.8 - _calib_pix_wl(self.hsi.freq.calib)[0][self.hsi.mean().argmax()]
            self.hsi.freq.calib['a_vec'][-1] = self.hsi.freq.calib['a_vec'][-1] + nm_diff
            self.hsi.freq.update()
            self.changeSlider()

    def plotDarkSpectrum(self):
        """
        Plot dark spectrum
        """
        if self.dark.data is None:
            pass
        else:
            meaner = mean_nd_to_1d(self.dark.data)
            self.plotter.plot(self.hsi.f_full, meaner, 
                              label='Mean Dark Spectrum ({})'.format(self.dark.n_pix))
            
            if self.dark.n_pix > 1:
                stder = std_nd_to_1d(self.dark.data)
                color = self.plotter.list_all[-1].style_dict['color']
                std_label = r'Dark Spectrum $\pm$1 Std. Dev. ({})'.format(self.dark.n_pix)
                self.plotter.fill_between(self.hsi.f_full, meaner - stder,
                                          meaner + stder, color=color,
                                          alpha=0.25,
                                          label=std_label)

            self.plotter.show()
            self.plotter.raise_()

    def plotNRBSpectrum(self):
        """
        Plot NRB spectrum
        """
        if self.nrb.data is None:
            pass
        else:
            meaner = mean_nd_to_1d(self.nrb.data)
            self.plotter.plot(self.hsi.f_full, meaner, 
                              label='Mean NRB Spectrum ({})'.format(self.nrb.n_pix))
            
            if self.nrb.n_pix > 1:
                stder = std_nd_to_1d(self.nrb.data)
                color = self.plotter.list_all[-1].style_dict['color']
                std_label = r'NRB Spectrum $\pm$1 Std. Dev. ({})'.format(self.nrb.n_pix)
                self.plotter.fill_between(self.hsi.f_full, meaner - stder,
                                          meaner + stder, color=color,
                                          alpha=0.25,
                                          label=std_label)

            # self.plotter.plot(self.hsi.f_full, mean_nd_to_1d(self.nrb.data),
            #                   label='Mean NRB Spectrum')

            self.plotter.show()
            self.plotter.raise_()

    def plotLeftNRBSpectrum(self):
        """
        Plot Left-Side NRB spectrum
        """
        if self.nrb_left.data is None:
            pass
        else:
            meaner = mean_nd_to_1d(self.nrb_left.data)
            self.plotter.plot(self.hsi.f_full, meaner, 
                              label='Mean Left-Side NRB Spectrum ({})'.format(self.nrb_left.n_pix))
            
            if self.nrb_left.n_pix > 1:
                stder = std_nd_to_1d(self.nrb_left.data)
                color = self.plotter.list_all[-1].style_dict['color']
                std_label = r'Left-Side NRB Spectrum $\pm$1 Std. Dev. ({})'.format(self.nrb_left.n_pix)
                self.plotter.fill_between(self.hsi.f_full, meaner - stder,
                                          meaner + stder, color=color,
                                          alpha=0.25,
                                          label=std_label)

            # self.plotter.plot(self.hsi.f_full, mean_nd_to_1d(self.nrb_left.data),
            #                   label='Mean Left-Side NRB Spectrum')

            self.plotter.show()
            self.plotter.raise_()

    def plotRightNRBSpectrum(self):
        """
        Plot NRB spectrum
        """
        if self.nrb_right.data is None:
            pass
        else:
            meaner = mean_nd_to_1d(self.nrb_right.data)
            self.plotter.plot(self.hsi.f_full, meaner,
                              label='Mean Right-Side NRB Spectrum ({})'.format(self.nrb_right.n_pix))
            
            if self.nrb_right.n_pix > 1:
                stder = std_nd_to_1d(self.nrb_right.data)
                color = self.plotter.list_all[-1].style_dict['color']
                std_label = r'Right-Side NRB Spectrum $\pm$1 Std. Dev. ({})'.format(self.nrb_right.n_pix)
                self.plotter.fill_between(self.hsi.f_full, meaner - stder,
                                          meaner + stder, color=color,
                                          alpha=0.25,
                                          label=std_label)

            self.plotter.show()
            self.plotter.raise_()

    def pointSpectrum(self):
        """
        Get spectrum of selected point.

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        Action:
            Left mouse-click : Select vertex point
        """
        if self.cid is None:
            self.cid = self.img_BW.mpl.mpl_connect('button_press_event',
                                                   lambda event: self._pointClick(event, self._pointSpectrumPlot))

            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
            self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def subtractROIStart(self):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        """

        if self.cid is None:
            # Updated by _roiClick
            self.x_loc_list = []
            self.y_loc_list = []


            self.cid = self.img_BW.mpl.mpl_connect('button_press_event',
                                                   lambda event: self._roiClick(event, self._roiSubtract))

            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
            self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def _roiSubtract(self, locs):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        """
        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.x, x_loc_list)[1]
        y_pix = find_nearest(self.hsi.y, y_loc_list)[1]

        mask, path = _roimask(self.hsi.x, self.hsi.y,
                              x_loc_list, y_loc_list)


        mask_hits = _np.sum(mask)


        if mask_hits > 0:  # Len(mask) > 0

            spectra = self.hsi.data[mask == 1]

            if mask_hits > 1:
                spectrum = _np.mean(spectra, axis=0)
            else:
                spectrum = _np.squeeze(spectra)
            spectrum = spectrum.astype(self.hsi.data.dtype)
            self.hsi.data -= spectrum[..., :]
            self.changeSlider()


            # Backup for Undo
            self.bcpre.add_step(['SubtractROI', 'Spectrum', spectrum])
            self.updateHistory()
            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()


            del spectrum

        del x_pix
        del y_pix

    def nrbFromROI(self):
        """
        Acquire an average spectrum from a user-selected ROI and apply to the \
        NRB-- either as the new NRB or averaged with the existing (sender- \
        dependent)

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        """

        # I found that the objectName is a better way than a reference to the
        # actual action (e.g., self.ui.action_*) as the reference may change
        # depending on the call location or how this method is called
        sender = self.sender().objectName()

        if ((sender == 'actionNRB_from_ROI') or
                (sender == 'actionAppend_NRB_from_ROI') or
                (sender == 'actionNRB_from_ROI_Left_Side') or
                (sender == 'actionNRB_from_ROI_Right_Side')):
            # Updated by _roiClick
            self.x_loc_list = []
            self.y_loc_list = []

            # Need to send sender as the text name as the actual object
            # will change
            if self.cid is None:
                self.cid = self.img_BW.mpl.mpl_connect('button_press_event',
                                                       lambda event: self._roiClick(event, self._roiNRB, sender))

                self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
                self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

        else:
            print('Unknown action send to nrbFromROI')

    def _roiNRB(self, locs, sender):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        """
        # Sender was sent as a text reference to the actual sender
        # the pass of sender put it in a tuple; thus the [0]
        sender = sender[0]

        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.x, x_loc_list)[1]
        y_pix = find_nearest(self.hsi.y, y_loc_list)[1]

        mask, path = _roimask(self.hsi.x, self.hsi.y,
                              x_loc_list, y_loc_list)


        mask_hits = _np.sum(mask)
        if mask_hits > 0:  # Len(mask) > 0
            if isinstance(self.hsi.data, _h5py.Dataset):
                spectra = self.hsi.data[_np.repeat(mask[...,None], 
                                                   self.hsi.data.shape[-1], axis=-1) == 1]
            else:
                spectra = self.hsi.data[mask == 1]

            if _np.iscomplexobj(spectra) & self.ui.actionUseImagData.isChecked():
                spectra = spectra.imag
            else:
                spectra = spectra.real

            if mask_hits > 1:
                spectrum = _np.mean(spectra, axis=0)
            else:
                spectrum = _np.squeeze(spectra)

            spectrum = spectrum.astype(self.hsi.data.dtype)
            if sender == 'actionNRB_from_ROI':
                self.nrb.data = spectra
                self.ui.actionKramersKronig.setEnabled(True)
                self.ui.actionKKSpeedTest.setEnabled(True)
                self.ui.actionNRBSpectrum.setEnabled(True)
                self.ui.menuCoherent_Raman_Imaging.setEnabled(True)
                self.ui.actionDeNoiseNRB.setEnabled(True)
                if self.dark.data is not None:
                    self.ui.actionCalcAnscParams.setEnabled(True)

            elif sender == 'actionAppend_NRB_from_ROI':
                if self.nrb.size == 0:
                    self.nrb.data = spectra
                else:
                    self.nrb.data = (self.nrb.data + spectrum)/2
                self.ui.actionKramersKronig.setEnabled(True)
                self.ui.actionNRBSpectrum.setEnabled(True)
            elif sender == 'actionNRB_from_ROI_Left_Side':
                self.nrb_left.data = spectra
                self.ui.actionLeftSideNRBSpect.setEnabled(True)
                if ((self.nrb_left.data is not None) and
                        (self.nrb_right.data is not None)):
                    if self.nrb_right.mean().size == self.nrb_left.mean().size:
                        self.ui.actionMergeNRBs.setEnabled(True)

            elif sender == 'actionNRB_from_ROI_Right_Side':
                self.nrb_right.data = spectra
                self.ui.actionRightSideNRBSpect.setEnabled(True)
                if ((self.nrb_left.data is not None) and
                        (self.nrb_right.data is not None)):
                    if self.nrb_right.mean().size == self.nrb_left.mean().size:
                        self.ui.actionMergeNRBs.setEnabled(True)
            else:
                print('Unknown action sent to _roiNRB')

            del spectrum

        del x_pix
        del y_pix

    def roiSpectrum(self):
        """
        Plot spectrum over selected region-of-interest (ROI).

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        Action:
            Left mouse-click : Select vertex point
            Right mouse-click : Close polygon
        """
        if self.cid is None:
            # Updated by _roiClick
            self.x_loc_list = []
            self.y_loc_list = []


            self.cid = self.img_BW.mpl.mpl_connect('button_press_event',
                                                   lambda event: self._roiClick(event, self._roiSpectrumPlot))

            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
            self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def _pointClick(self, event, pass_fcn):
        """
        Capture single mouse click location in MPL window.

        After this function completes, it sends the data (x_pt, y_pt) on to \
        the pass_fcn function.
        """
        if event.button == 1:
            if event.inaxes == self.img_BW.mpl.ax:
                    #self.tempverts += [[event.xdata, event.ydata]]
                x_loc = event.xdata
                y_loc = event.ydata

                # Send on to a function that will use the collected data
                pass_fcn((x_loc, y_loc))

                self.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
                self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
                self.img_BW.mpl.mpl_disconnect(self.cid)
                self.cid = None
            else:  # Clicked out-of-bounds
                pass

        else: # Right-or-middle clicked; thus, cancel
            self.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.img_BW.mpl.mpl_disconnect(self.cid)
            self.cid = None

    def _pointSpectrumPlot(self, locs):
        """
        Add a plot (in plotter) of a point spectrum
        """

        x_loc, y_loc = locs
        x_pix = find_nearest(self.hsi.x, x_loc)[1]
        y_pix = find_nearest(self.hsi.y, y_loc)[1]

        self.changeSlider()

        plot_num = self.plotter.n_lines
        label = 'Point ' + str(plot_num)

        rng = self.hsi.freq.op_range_pix

        meta = {'x': x_loc, 'y': y_loc, 'x_pix': x_pix, 'y_pix': y_pix,
                'overlay': True}

        if _np.iscomplexobj(self.hsi.data) & self.ui.actionUseImagData.isChecked():
            self.plotter.plot(self.hsi.f,
                              self.hsi.data[y_pix, x_pix, rng].imag,
                              label=label, meta=meta)
        else:
            self.plotter.plot(self.hsi.f,
                              self.hsi.data[y_pix, x_pix, rng].real,
                              label=label, meta=meta)


        self.plotter.show()
        self.plotter.raise_()
        self.updateOverlays()

    def _roiSpectrumPlot(self, locs):
        """
        Add a plot (in plotter) of the mean spectrum over a region
        """
        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.x, x_loc_list)[1]
        y_pix = find_nearest(self.hsi.y, y_loc_list)[1]


        mask, path = _roimask(self.hsi.x, self.hsi.y,
                              x_loc_list, y_loc_list)


        mask_hits = _np.sum(mask)
        if mask_hits > 0:  # Len(mask) > 0
            rng = self.hsi.freq.op_range_pix

            if isinstance(self.hsi.data, _h5py.Dataset):

                # * Can't do fancy boolean indexing with HDF
                # * Make a square bounding box
                m,n = _np.where(mask == 1)
                rmin = m.min()
                rmax = m.max()+1
                cmin = n.min()
                cmax = n.max()+1

                spectra = self.hsi.data[rmin:rmax, cmin:cmax,:][mask[rmin:rmax, cmin:cmax]==1]

            else:
                spectra = self.hsi.data[mask == 1]

            if _np.iscomplexobj(spectra) & self.ui.actionUseImagData.isChecked():
                spectra = spectra.imag
            else:
                spectra = spectra.real

            if mask_hits > 1:
                spectrum = _np.mean(spectra[..., rng], axis=0)
                stddev = _np.std(spectra[..., rng], axis=0)
            else:
                spectrum = _np.squeeze(spectra[..., rng])

            plot_num = self.plotter.n_lines

            label_plot = 'ROI {} ({})'.format(plot_num, mask_hits)
            label_std = r'$\pm$1 Std. Dev. ROI {} ({})'.format(plot_num, mask_hits)

            # Plot line
            meta = {'x': x_loc_list, 'y': y_loc_list, 'x_pix': x_pix,
                    'y_pix': y_pix, 'overlay': True}
            self.plotter.plot(self.hsi.f, spectrum, label=label_plot, meta=meta)

            # Check color of line b/c uses color cycler-- for fill_b/w
            color = self.plotter.list_all[-1].style_dict['color']


            # Alternative
            #color = self.plotter.modelLine._model_data[-1]['color']

            # Plot +-1 std. dev.
            if mask_hits > 1:
                self.plotter.fill_between(self.hsi.f, spectrum-stddev,
                                          spectrum+stddev, color=color,
                                          alpha=0.25,
                                          label=label_std,
                                          meta=meta)

            del spectrum
            self.plotter.show()
            self.plotter.raise_()
            self.updateOverlays()


        del x_pix
        del y_pix

    def _roiClick(self, event, pass_fcn, *args):
        """
        Capture region-of-interest mouse click locations in MPL window.
        """


        if event.button == 1:
            if event.inaxes == self.img_BW.mpl.ax:

                self.x_loc_list.append(event.xdata)
                self.y_loc_list.append(event.ydata)

                getx = self.img_BW.mpl.ax.get_xlim()
                gety = self.img_BW.mpl.ax.get_ylim()

                if len(self.x_loc_list) == 1:
                    self.img_BW.mpl.ax.plot(self.x_loc_list, self.y_loc_list,
                                            markerfacecolor=[.9, .9, 0],
                                            markeredgecolor=[.9, .9, 0],
                                            marker='+',
                                            markersize=10,
                                            linestyle='None')
                    self.img_BW.mpl.ax.set_xlim(getx)
                    self.img_BW.mpl.ax.set_ylim(gety)
                    self.img_BW.mpl.draw()
                else:
                    self.img_BW.mpl.ax.plot(self.x_loc_list[-2:],
                                            self.y_loc_list[-2:],
                                            linewidth=2,
                                            marker='+',
                                            markersize=10,
                                            color=[.9, .9, 0],
                                            markerfacecolor=[.9, .9, 0],
                                            markeredgecolor=[.9, .9, 0])
                    self.img_BW.mpl.ax.set_xlim(getx)
                    self.img_BW.mpl.ax.set_ylim(gety)

                    self.img_BW.mpl.draw()
        else:
            if len(self.x_loc_list) > 0: # Insure at least 1 vertex
                self.x_loc_list.append(self.x_loc_list[0])
                self.y_loc_list.append(self.y_loc_list[0])

                # Pass on roi data
                if not args:
                    pass_fcn((self.x_loc_list, self.y_loc_list))
                else:
                    pass_fcn((self.x_loc_list, self.y_loc_list), args)

            del self.x_loc_list
            del self.y_loc_list

            self.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.img_BW.mpl.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.img_BW.mpl.mpl_disconnect(self.cid)
            self.cid = None
            self.changeSlider()


    def freqWindow(self):
        """
        Limit the frequency window displayed and analyzed
        """
        text, ok = _QInputDialog.getText(None, 'Frequency Window',
                                         'Range Tuple (cm-1): ',
                                         text='(500, 3800)')
        if ok:
            text_str_list = text.strip('(').strip(')').strip().split(',')
            freqwin = [float(q) for q in text_str_list]
            freqwin.sort()
            self.hsi.freq.op_list_freq = freqwin
            self.ui.freqSlider.setMinimum(0)
            self.ui.freqSlider.setMaximum(self.hsi.freq.op_size-1)
            self.changeSlider()


    def lineEditFreqChanged(self):
        """
        Frequency manually entered in frequency-slider-display
        """

        try:
            freq_in = float(self.ui.lineEditFreq.text())
            pos = self.hsi.freq.get_index_of_closest_freq(freq_in)
            if self.hsi.freq.op_list_pix is not None:
                pos -= self.hsi.freq.op_list_pix[0]

            self.ui.freqSlider.setSliderPosition(pos)
            self.changeSlider()
        except Exception:
            pass

    def lineEditPixChanged(self):
        """
        Frequency in pixel units manually entered in frequency-slider-display
        """
        pos = int(self.ui.lineEditPix.text())

        self.ui.freqSlider.setSliderPosition(pos)
        self.changeSlider()

    def zeroFirstColumn(self):
        """
        Zero first non-all-zero column. (Rather than crop)

        """
        self.zc = _ZeroColumn(first_or_last=0)
        self.zc.transform(self.hsi.data)

        # Adjust mask
        # self.hsi._mask[:, self.zc.zero_col] *= 0

        self.changeSlider()

    def zeroFirstRow(self):
        """
        Zero first non-all-zero row. (Rather than crop)

        """
        self.zr = _ZeroRow(first_or_last=0)
        self.zr.transform(self.hsi.data)

        # Adjust mask
        # self.hsi._mask[self.zr.zero_row, :] *= 0

        self.changeSlider()

    def zeroLastColumn(self):
        """
        Zero first non-all-zero column. (Rather than crop)

        """
        self.zc = _ZeroColumn(first_or_last=-1)
        self.zc.transform(self.hsi.data)

        # Adjust mask
        # self.hsi._mask[:, self.zc.zero_col] *= 0

        self.changeSlider()

    def zeroLastRow(self):
        """
        Zero first non-all-zero row. (Rather than crop)

        """
        self.zr = _ZeroRow(first_or_last=-1)
        self.zr.transform(self.hsi.data)

        # Adjust mask
        # self.hsi._mask[self.zr.zero_row, :] *= 0

        self.changeSlider()

    def opChange(self):
        """
        Math operation performed on single-color images changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.img_RGB_list[rgbnum].math.ui.comboBoxOperations.currentText()
            self.img_RGB_list[rgbnum].data.operation = currentop
        except Exception:
            pass

    def condOpChange(self):
        """
        Conditional math operation performed on single-color images changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.img_RGB_list[rgbnum].math.ui.comboBoxCondOps.currentText()
            self.img_RGB_list[rgbnum].data.condoperation = currentop
        except Exception:
            pass

    def condInEqualityChange(self):
        """
        Conditional inequality changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.img_RGB_list[rgbnum].math.ui.comboBoxCondInEquality.currentText()
            self.img_RGB_list[rgbnum].data.inequality = currentop
        except Exception:
            pass

    def spinBoxInEqualityChange(self):
        """
        Conditional inequality value changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            self.img_RGB_list[rgbnum].data.inequalityval = \
                self.img_RGB_list[rgbnum].math.ui.spinBoxInEquality.value()
        except Exception:
            pass

    def doKK(self):
        """
        Pop-up Kramers-Kronig parameter entry dialog and perform
        the Kramers-Kronig phase retrieval algorithm.
        """

        if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
            preview_spectra = self.hsi.get_rand_spectra(5, pt_sz=3, quads=True,
                                                    full=False)

        else:
            preview_spectra = self.get_preview_spectra(full=False)

        nrb = self.nrb.mean()

        # Range of pixels to perform-over
        rng = self.hsi.freq.op_range_pix

        try:
            if (self.hsi.f[1] - self.hsi.f[0]) < 0:
                conj = True
            else:
                conj = False
        except Exception:
            conj = False

        out = DialogKKOptions.dialogKKOptions(data=[self.hsi.f,
                                              nrb[..., rng],
                                              preview_spectra], parent=self,
                                              conjugate=conj)

        if out is not None:
            cars_amp_offset = out['cars_amp']
            nrb_amp_offset = out['nrb_amp']
            phase_offset = out['phase_offset']
            conjugate = out['conjugate']
            norm_to_nrb = out['norm_to_nrb']
            pad_factor = out['pad_factor']
            n_edge = out['n_edge']

            kk = KramersKronig(cars_amp_offset=cars_amp_offset,
                               nrb_amp_offset=nrb_amp_offset,
                               conjugate=conjugate,
                               phase_offset=phase_offset, norm_to_nrb=norm_to_nrb,
                               pad_factor=pad_factor, n_edge=n_edge,
                               rng=rng)

            try:
                self.hsi.data = kk.calculate(self.hsi.data, self.nrb.data)
            except Exception as e:
                _traceback.print_exc(limit=1)
                print('Error in KK: {}'.format(e))

            self.changeSlider()

            self.ui.actionPhaseErrorCorrection.setEnabled(True)
            self.ui.actionScaleErrorCorrection.setEnabled(True)

            # Backup for Undo
            self.bcpre.add_step(['KK', 'CARSAmp', cars_amp_offset, 'NRBAmp',
                                 nrb_amp_offset, 'Phase', phase_offset,
                                 'Norm', norm_to_nrb, 'Pad Factor', pad_factor,
                                 'N Edge', n_edge])
            self.updateHistory()
            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()

    def deNoiseNRB(self):
        """
        Denoise NRB with Savitky-Golay
        """
        # Range of pixels to perform-over
        rng = self.hsi.freq.op_range_pix

        plugin = _widgetSG(window_length=11, polyorder=3)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(self.nrb.mean()[rng],
                                                           x=self.hsi.f,
                                                           plugin=plugin,
                                                           parent=self)
        if winPlotEffect is not None:
            win_size = winPlotEffect.parameters['window_length']
            order = winPlotEffect.parameters['polyorder']

            nrb_denoise = _copy.deepcopy(_np.squeeze(self.nrb.data))
            nrb_denoise[..., rng] = _sg(nrb_denoise[..., rng], win_size, order)

            self.nrb.data = nrb_denoise

            # Backup for Undo
            self.bcpre.add_step(['DenoiseNrbSG',
                                 'Win_size', win_size,
                                 'Order', order])
            self.updateHistory()

        self.changeSlider()

    def deNoiseDark(self):
        """
        Denoise Dark with Savitky-Golay
        """
        # Range of pixels to perform-over
        rng = self.hsi.freq.op_range_pix

        plugin = _widgetSG(window_length=201, polyorder=3)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(self.dark.mean()[rng],
                                                           x=self.hsi.f,
                                                           plugin=plugin,
                                                           parent=self)
        if winPlotEffect is not None:
            win_size = winPlotEffect.parameters['window_length']
            order = winPlotEffect.parameters['polyorder']

            dark_denoise = _copy.deepcopy(_np.squeeze(self.dark.data))
            dark_denoise[..., rng] = _sg(dark_denoise[..., rng], win_size, order)

            self.dark.data = dark_denoise

            # Backup for Undo
            self.bcpre.add_step(['DenoiseDarkSG',
                                 'Win_size', win_size,
                                 'Order', order])
            self.updateHistory()

        self.changeSlider()

    def deNoise(self):
        """
        SVD
        """
        # Range of pixels to perform-over
        rng = self.hsi.freq.op_range_pix
        # SVD Decompose
        svd_decompose = SVDDecompose(rng=rng)
        UsVh = svd_decompose.calculate(self.hsi.data)

        # Class method route
        if rng is None:
            # Note: .main in dialog_AbstractFactorization
            svs = DialogSVD.dialogSVD(UsVh, self.hsi.data.shape, mask=self.hsi.mask,
                                      img_all=self.hsi.data.mean(axis=-1),
                                      spect_all=self.hsi.data.mean(axis=(0,1)),
                                      parent=self)
        else:
            svs = DialogSVD.dialogSVD(UsVh, self.hsi.data[..., rng].shape,
                                      mask=self.hsi.mask,
                                      img_all=self.hsi.data[..., rng].mean(axis=-1),
                                      spect_all=self.hsi.data[..., rng].mean(axis=(0,1)),
                                      parent=self)

        print('SV\'s:{}'.format(svs))

        if svs is not None:
            svd_recompose = SVDRecompose(rng=rng)
            svd_recompose.transform(self.hsi.data, UsVh[0], UsVh[1], UsVh[2],
                                    svs=svs)

            # Backup for Undo
            self.bcpre.add_step(['SVD', 'SVs', svs])
            self.updateHistory()

            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()
            self.changeSlider()

    def errorCorrectPhase(self):
        """
        Error Correction: Phase
        """

        if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
            preview_spectra = self.hsi.get_rand_spectra(5, pt_sz=3, quads=True,
                                                    full=True)
        else:
            preview_spectra = self.get_preview_spectra(full=True)

        if _np.iscomplexobj(preview_spectra):
            preview_spectra = _np.angle(preview_spectra)

        rng = self.hsi.freq.op_range_pix

        wn_increase = (self.hsi.f[1] - self.hsi.f[1]) > 0
        plugin = _widgetALS(x=self.hsi.f_full, rng=rng, 
                            wavenumber_increasing=wn_increase)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(preview_spectra,
                                                           x=self.hsi.f_full,
                                                           plugin=plugin,
                                                           parent=self)
        if winPlotEffect is not None:
            # asym_param = winPlotEffect.parameters['asym_param']
            # smoothness_param = winPlotEffect.parameters['smoothness_param']
            # redux_factor = winPlotEffect.parameters['redux']
            # fix_end_points = winPlotEffect.parameters['fix_end_points']
            # max_iter = winPlotEffect.parameters['max_iter']
            # min_diff = winPlotEffect.parameters['min_diff']

            phase_err_correct_als = _PhaseErrCorrectALS(**winPlotEffect.parameters)

            phase_err_correct_als.transform(self.hsi.data)

            temp = ['PhaseErrorCorrectALS']
            [temp.extend(q) for q in winPlotEffect.parameters.items()]
            self.bcpre.add_step(temp)
            # Backup for Undo
            # if _np.size(asym_param) == 1:
            #     self.bcpre.add_step(['PhaseErrorCorrectALS',
            #                          'smoothness_param', smoothness_param,
            #                          'asym_param', asym_param,
            #                          'redux', redux_factor,
            #                          'order', 2,
            #                          'fix_end_points', fix_end_points,
            #                          'max_iter', max_iter,
            #                          'min_diff', min_diff])

            # else:
            #     self.bcpre.add_step(['PhaseErrorCorrectALS',
            #                          'smoothness_param', smoothness_param,
            #                          'asym_param_start',
            #                          winPlotEffect.parameters['asym_param_start'],
            #                          'asym_param_end',
            #                          winPlotEffect.parameters['asym_param_end'],
            #                          'redux', redux_factor,
            #                          'order', 2,
            #                          'fix_end_points', fix_end_points,
            #                          'max_iter', max_iter,
            #                          'min_diff', min_diff])
            self.updateHistory()
            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()

        self.changeSlider()

    def errorCorrectScale(self):
        """
        Error Correction: Scale
        """

        if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
            preview_spectra = self.hsi.get_rand_spectra(5, pt_sz=3, quads=True,
                                                    full=False)
        else:
            preview_spectra = self.get_preview_spectra(full=False)

        if _np.iscomplexobj(preview_spectra):
                preview_spectra = preview_spectra.real

        rng = self.hsi.freq.op_range_pix

        plugin = _widgetSG(window_length=601, polyorder=2)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(preview_spectra,
                                                           x=self.hsi.f,
                                                           plugin=plugin,
                                                           parent=self)
        if winPlotEffect is not None:
            win_size = winPlotEffect.parameters['window_length']
            order = winPlotEffect.parameters['polyorder']

            scale_err_correct_sg = _ScaleErrCorrectSG(win_size=win_size,
                                                      order=order,
                                                      rng=rng)
            scale_err_correct_sg.transform(self.hsi.data)

            # Backup for Undo
            self.bcpre.add_step(['ScaleErrorCorrectSG',
                                 'win_size', win_size,
                                 'order', order])
            self.updateHistory()

            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()
        self.changeSlider()

    def errorCorrectAmp(self):
        """
        Error Correction: Amp aka Baseline Detrending

        Notes
        -----
        If data is complex, amplitude detrending occurs on and only on the \
        imaginary portion
        """

        if (self.preview_rois is None) | (not self.ui.actionUsePreviewROI.isChecked()):
            preview_spectra = self.hsi.get_rand_spectra(5, pt_sz=3, quads=True,
                                                    full=True)
        else:
            preview_spectra = self.get_preview_spectra(full=True)

        if _np.iscomplexobj(preview_spectra):
                preview_spectra = preview_spectra.imag

        rng = self.hsi.freq.op_range_pix

        plugin = _widgetALS(x=self.hsi.f_full, rng=rng)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(preview_spectra,
                                                           x=self.hsi.f_full,
                                                           plugin=plugin,
                                                           parent=self)
        if winPlotEffect is not None:
            # asym_param = winPlotEffect.parameters['asym_param']
            # smoothness_param = winPlotEffect.parameters['smoothness_param']
            # redux_factor = winPlotEffect.parameters['redux']
            # fix_end_points = winPlotEffect.parameters['fix_end_points']
            # max_iter = winPlotEffect.parameters['max_iter']
            # min_diff = winPlotEffect.parameters['min_diff']

            temp = ['AmpErrorCorrectALS']
            [temp.extend(q) for q in winPlotEffect.parameters.items()]
            self.bcpre.add_step(temp)

            baseline_detrend = _SubtractBaselineALS(**winPlotEffect.parameters)

            baseline_detrend.transform(self.hsi.data)

            # Backup for Undo
            # if _np.size(asym_param) == 1:
            #     self.bcpre.add_step(['AmpErrorCorrectALS',
            #                          'smoothness_param', smoothness_param,
            #                          'asym_param', asym_param,
            #                          'redux', redux_factor,
            #                          'order', 2,
            #                          'fix_end_points', fix_end_points,
            #                          'max_iter', max_iter,
            #                          'min_diff', min_diff])
            # else:
            #     self.bcpre.add_step(['AmpErrorCorrectALS',
            #                          'smoothness_param', smoothness_param,
            #                          'asym_param_start',
            #                          winPlotEffect.parameters['asym_param_start'],
            #                          'asym_param_end',
            #                          winPlotEffect.parameters['asym_param_end'],
            #                          'redux', redux_factor,
            #                          'order', 2,
            #                          'fix_end_points', fix_end_points,
            #                          'max_iter', max_iter,
            #                          'min_diff', min_diff])
            self.updateHistory()

            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()

        self.changeSlider()

    def doUndo(self):
        """
        Undo last operation back to last backup point
        """
        self.bcpre.pop_to_last()
        self.hsi = _BCPre.load_pickle(self.bcpre.id_list[-1])
        self.updateHistory()

        del_flag = 0

        for count in self.bcpre.cut_list:
            try:
                _os.remove(count + '.pickle')
            except Exception:
                print('Error in deleting old pickle files')
            else:
                del_flag += 1
        if del_flag == len(self.bcpre.cut_list):
            del self.bcpre.cut_list
        else:
            print('Did not delete pickle file cut list... Something went wrong')

        self.ui.freqSlider.setMinimum(0)
        self.ui.freqSlider.setMaximum(self.hsi.freq.op_size-1)

        self.changeSlider()

    def subDark(self):
        """
        Subtract loaded dark spectrum from HSI data.
        """

        nrbloaded = self.nrb.data is not None
        nrbloaded_left = self.nrb_left.data is not None
        nrbloaded_right = self.nrb_right.data is not None
        darkloaded = self.dark.data is not None

        if self.hsi.data is not None:
            if darkloaded:
                # Instantiate SubtractDark
                sub_dark = SubtractDark(self.dark.data)

                msg = _QMessageBox(self)
                msg.setIcon(_QMessageBox.Question)
                msg.setText('Subtract Dark Spectrum from Image?')
                msg.setWindowTitle('Confirm dark subtract from image')
                msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                msg.setDefaultButton(_QMessageBox.Ok)
                out = msg.exec()

                if out == _QMessageBox.Ok:
                    sub_dark.transform(self.hsi.data)

                    # Backup for Undo
                    self.bcpre.add_step(['SubDark'])
                    self.updateHistory()
                    if self.ui.actionUndo_Backup_Enabled.isChecked():
                        try:
                            _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                        except Exception:
                            print('Error in pickle backup (Undo functionality)')
                        else:
                            self.bcpre.backed_up()

                if nrbloaded:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Dark Spectrum from NRB Spectrum(a)?')
                    msg.setWindowTitle('Confirm dark subtract from NRB spectrum(a)')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_dark.transform(self.nrb.data)

                if nrbloaded_left:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Dark Spectrum from Left-Side NRB Spectrum(a)?')
                    msg.setWindowTitle('Confirm dark subtract from Left-Side NRB spectrum(a)')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_dark.transform(self.nrb_left.data)

                if nrbloaded_right:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Dark Spectrum from Right-Side NRB Spectrum(a)?')
                    msg.setWindowTitle('Confirm dark subtract from Right-Side NRB spectrum(a)')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_dark.transform(self.nrb_right.data)

                self.changeSlider()
            else:
                msg = _QMessageBox(self)
                msg.setIcon(_QMessageBox.Information)
                msg.setText('Dark spectrum not loaded.')
                msg.setStandardButtons(_QMessageBox.Ok)
                msg.setDefaultButton(_QMessageBox.Ok)
                msg.exec()
        else:
            msg = _QMessageBox(self)
            msg.setIcon(_QMessageBox.Information)
            msg.setText('Image data not loaded. Cannot subtract dark spectrum.')
            msg.setStandardButtons(_QMessageBox.Ok)
            msg.setDefaultButton(_QMessageBox.Ok)
            msg.exec()

    def subResidual(self):
        """
        Subtract a linear residual over range
        """
        nrbloaded = self.nrb.data is not None
        nrbloaded_left = self.nrb_left.data is not None
        nrbloaded_right = self.nrb_right.data is not None
        imgloaded = self.hsi.data is not None

        if nrbloaded or imgloaded:
            text, ok = _QInputDialog.getText(None, 'Frequency Window',
                                             'Range Tuple (cm-1): ',
                                             text='(-1500, -500)')
            if ok:
                text_str_list = text.strip('(').strip(')').strip().split(',')
                freqwin = [float(q) for q in text_str_list]
                freqwin.sort()

                rng = self.hsi.freq.get_index_of_closest_freq(freqwin)
                sub_residual = SubtractMeanOverRange(rng)

                if imgloaded:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Residual Dark Spectrum from Image?')
                    msg.setWindowTitle('Confirm residual subtraction from Image')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out_img = msg.exec()

                    if out_img == _QMessageBox.Ok:
                        sub_residual.transform(self.hsi.data)

                if nrbloaded:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Residual Dark Spectrum from NRB?')
                    msg.setWindowTitle('Confirm residual subtraction from NRB')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_residual.transform(self.nrb.data)

                if nrbloaded_left:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Residual Dark Spectrum from Left-Side NRB?')
                    msg.setWindowTitle('Confirm residual subtraction from Left-Side NRB')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_residual.transform(self.nrb_left.data)

                if nrbloaded_right:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Question)
                    msg.setText('Subtract Residual Dark Spectrum from Right-Side NRB?')
                    msg.setWindowTitle('Confirm residual subtraction from Right-Side NRB')
                    msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()

                    if out == _QMessageBox.Ok:
                        sub_residual.transform(self.nrb_right.data)

                # Backup for Undo
                if out_img == _QMessageBox.Ok:
                    self.bcpre.add_step(['SubResidual','RangeStart',
                                         freqwin[0], 'RangeEnd',
                                         freqwin[1]])
                    self.updateHistory()
                    if self.ui.actionUndo_Backup_Enabled.isChecked():
                        try:
                            _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                        except Exception:
                            print('Error in pickle backup (Undo functionality)')
                        else:
                            self.bcpre.backed_up()
                self.changeSlider()
        else:
            msg = _QMessageBox(self)
            msg.setIcon(_QMessageBox.Information)
            msg.setText('Image or NRB data need be loaded.')
            msg.setStandardButtons(_QMessageBox.Ok)
            msg.setDefaultButton(_QMessageBox.Ok)
            msg.exec()

    def anscombe(self):
        """
        Performance Anscombe transformation
        """
        if self._anscombe_params is None:
            out = DialogAnscombeOptions.dialogAnscombeOptions(parent=self)
        else:
            out = DialogAnscombeOptions.dialogAnscombeOptions(stddev=self._anscombe_params['stddev'],
                                                              gain=self._anscombe_params['gain'],
                                                              parent=self)

        if out is not None:
            self._anscombe_params = _copy.deepcopy(out)

            rng = self.hsi.freq.op_range_pix

            ansc = _Anscombe(gauss_std=out['stddev'], gauss_mean=0.0,
                             poisson_multi=out['gain'], rng=rng)
            ansc.transform(self.hsi.data)

            # Backup for Undo
            self.bcpre.add_step(['Anscombe','Gauss_mean', 0.0,
                                 'Gauss_std', out['stddev'],
                                 'Poisson_multi', out['gain']])
            self.updateHistory()
            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()
            self.changeSlider()

    def inverseAnscombe(self):
        """
        Performance an Inverse Anscombe transformation
        """
        if self._anscombe_params is None:
            out = DialogAnscombeOptions.dialogAnscombeOptions(parent=self)
        else:
            out = DialogAnscombeOptions.dialogAnscombeOptions(stddev=self._anscombe_params['stddev'],
                                                              gain=self._anscombe_params['gain'],
                                                              parent=self)

        if out is not None:
            rng = self.hsi.freq.op_range_pix

            iansc = _AnscombeInverse(gauss_std=out['stddev'], gauss_mean=0.0,
                                     poisson_multi=out['gain'], rng=rng)
            iansc.transform(self.hsi.data)

            # Backup for Undo
            self.bcpre.add_step(['InvAnscombe','Gauss_mean', 0.0,
                                 'Gauss_std', out['stddev'],
                                 'Poisson_multi', out['gain']])
            self.updateHistory()
            if self.ui.actionUndo_Backup_Enabled.isChecked():
                try:
                    _BCPre.backup_pickle(self.hsi, self.bcpre.id_list[-1])
                except Exception:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()
            self.changeSlider()

    def calcAnscombeParams(self):
        """
        Calculate Anscombe Parameters
        """
        dark_sub = _np.any(['SubDark' in k for k in self.bcpre.attr_dict])

        out = DialogCalcAnscombeParams.dialogCalcAnscombeParams(parent=self, dark_array=self.dark.data,
                                                                rep_array=self.nrb.data, 
                                                                axis=0, rng=self.hsi.freq.op_range_pix,
                                                                dark_sub=dark_sub)

        if out is not None:
            self._anscombe_params = {'stddev':out['g_std'].mean(), 'gain':out['weighted_mean_alpha'], 'mean':out['g_mean'].mean()}

    def doMath(self):
        """
        Perform selected math operation on single-color imagery.
        """

        # Which RGB image is it
        rgbnum = self.ui.tabColors.currentIndex()

        # Which operation is selected
        operation_index = self.img_RGB_list[rgbnum].math.ui.comboBoxCondOps.currentIndex()
        operation_text = self.img_RGB_list[rgbnum].math.ui.comboBoxCondOps.currentText()


        if operation_index == 0:
            num_freq_needed = 0
        else:
            # num_freq_needed = widgetColorMath.OPERATION_FREQ_COUNT[operation_index-1]
            num_freq_needed = self.img_RGB_list[rgbnum].math.OPERATION_FREQ_COUNT[operation_index-1]
        # Check conditional frequencies are set
        cond_set = False

        if (num_freq_needed == 1 and
                self.img_RGB_list[rgbnum].data.condfreq1 is not None):

            # Conditional frequency LOCATION 1
            condloc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq1)

            # All frequencies set
            cond_set = True
        elif (num_freq_needed == 2 and
              self.img_RGB_list[rgbnum].data.condfreq1 is not None and
              self.img_RGB_list[rgbnum].data.condfreq2 is not None):

            # Conditional frequency LOCATIONS
            condloc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq1)
            condloc2 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq2)

            # All frequencies set
            cond_set = True
        elif (num_freq_needed == 3 and
              self.img_RGB_list[rgbnum].data.condfreq1 is not None and
              self.img_RGB_list[rgbnum].data.condfreq2 is not None and
              self.img_RGB_list[rgbnum].data.condfreq3 is not None):

            # Conditional frequency LOCATIONS
            condloc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq1)
            condloc2 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq2)
            condloc3 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.condfreq3)

            # All frequencies set
            cond_set = True
        else:
            cond_set = False

        if cond_set is False:
            self.img_RGB_list[rgbnum].math.ui.comboBoxCondOps.setCurrentIndex(0)
            Mask = 1
        else:
            if (operation_text == '') or (operation_text == ' '):  # Return just a plane
                Mask = _peakamps.MeasurePeak.measure(self.hsi.data,
                                                     condloc1)


            elif operation_text == '+':  # Addition
                Mask = _peakamps.MeasurePeakAdd.measure(self.hsi.data,
                                                        condloc1, condloc2)

            elif operation_text == '-':  # Subtraction
                Mask = _peakamps.MeasurePeakMinus.measure(self.hsi.data,
                                                          condloc1, condloc2)

            elif operation_text == '*':  # Multiplication
                Mask = _peakamps.MeasurePeakMultiply.measure(self.hsi.data,
                                                             condloc1, condloc2)

            elif operation_text == '/':  # Division
                Mask = _peakamps.MeasurePeakDivide.measure(self.hsi.data,
                                                           condloc1, condloc2)

            elif operation_text == 'SUM':  # Summation over range
                Mask = _peakamps.MeasurePeakSum.measure(self.hsi.data,
                                                              condloc1, condloc2)

            elif operation_text == 'SUM(ABS(Re) + 1j*ABS(Im))':  # Abs of Re and Im
                Mask = _peakamps.MeasurePeakSumAbsReImag.measure(self.hsi.data,
                                                                       condloc1, condloc2)

            elif operation_text == 'Peak b/w troughs':  # Peak between troughs
                Mask = _peakamps.MeasurePeakBWTroughs.measure(self.hsi.data,
                                                              condloc1, condloc2, condloc3)
            elif operation_text == 'Max':  # Max over range
                Mask = _peakamps.MeasurePeakMax.measure(self.hsi.data,
                                                        condloc1, condloc2)
            elif operation_text == 'Min':  # Min over range
                Mask = _peakamps.MeasurePeakMin.measure(self.hsi.data,
                                                        condloc1, condloc2)
            elif operation_text == 'MaxAbs':  # Max of Abs value over range
                Mask = _peakamps.MeasurePeakMaxAbs.measure(self.hsi.data,
                                                           condloc1, condloc2)
            elif operation_text == 'MinAbs':  # Min of Abs value over range
                Mask = _peakamps.MeasurePeakMinAbs.measure(self.hsi.data,
                                                           condloc1, condloc2)  
            else:
                pass

            if Mask is not None:
                if _np.iscomplexobj(self.hsi.data) & self.ui.actionUseImagData.isChecked():
                    Mask = Mask.imag
                else:
                    Mask = Mask.real


        if cond_set is True:
            inequality_text = self.img_RGB_list[rgbnum].math.ui.comboBoxCondInEquality.currentText()
            inequality_val = self.img_RGB_list[rgbnum].math.ui.spinBoxInEquality.value()
            if inequality_text == '<':
                Mask = Mask < inequality_val
            elif inequality_text == '>':
                Mask = Mask > inequality_val
            elif inequality_text == '=':
                Mask = Mask == inequality_val
            elif inequality_text == '>=':
                Mask = Mask >= inequality_val
            elif inequality_text == '<=':
                Mask = Mask <= inequality_val
            else:
                print('Inequality type error... setting to 1')
                Mask = 1
        # Check frequencies are set
        operation_index = self.img_RGB_list[rgbnum].math.ui.comboBoxOperations.currentIndex()
        operation_text = self.img_RGB_list[rgbnum].math.ui.comboBoxOperations.currentText()

        # num_freq_needed = widgetColorMath.OPERATION_FREQ_COUNT[operation_index]
        num_freq_needed = self.img_RGB_list[rgbnum].math.OPERATION_FREQ_COUNT[operation_index]

        freq_set = False

        if (num_freq_needed == 1 and
                self.img_RGB_list[rgbnum].data.opfreq1 is not None):

            # Operating frequency LOCATION 1
            oploc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq1)

            # All frequencies set
            freq_set = True
        elif (num_freq_needed == 2 and
              self.img_RGB_list[rgbnum].data.opfreq1 is not None and
              self.img_RGB_list[rgbnum].data.opfreq2 is not None):

            # Operating frequency LOCATIONS
            oploc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq1)
            oploc2 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq2)

            # All frequencies set
            freq_set = True

        elif (num_freq_needed == 3 and
              self.img_RGB_list[rgbnum].data.opfreq1 is not None and
              self.img_RGB_list[rgbnum].data.opfreq2 is not None and
              self.img_RGB_list[rgbnum].data.opfreq3 is not None):

            # Operating frequency LOCATIONS
            oploc1 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq1)
            oploc2 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq2)
            oploc3 = self.hsi.freq.get_index_of_closest_freq(self.img_RGB_list[rgbnum].data.opfreq3)

            # All frequencies set
            freq_set = True

        else:
            freq_set = False

        if freq_set == True:
            if (operation_text == '') or (operation_text == ' '):  # Return just a plane
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeak.measure(self.hsi.data,
                                                  oploc1)
            elif operation_text == '+':  # Addition
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakAdd.measure(self.hsi.data,
                                                     oploc1, oploc2)

            elif operation_text == '-':  # Subtraction
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakMinus.measure(self.hsi.data,
                                                       oploc1, oploc2)
            elif operation_text == '*':  # Multiplication
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakMultiply.measure(self.hsi.data,
                                                          oploc1, oploc2)
            elif operation_text == '/':  # Division
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakDivide.measure(self.hsi.data,
                                                        oploc1, oploc2)
            elif operation_text == 'SUM':  # Division
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakSum.measure(self.hsi.data,
                                                           oploc1, oploc2)
            elif operation_text == 'SUM(ABS(Re) + 1j*ABS(Im))':  # Division
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakSumAbsReImag.measure(self.hsi.data,
                                                              oploc1, oploc2)                                               
            elif operation_text == 'Peak b/w troughs':  # Division
                self.img_RGB_list[rgbnum].data.grayscaleimage = Mask * \
                    _peakamps.MeasurePeakBWTroughs.measure(self.hsi.data,
                                                           oploc1, oploc2,
                                                           oploc3)                
            else:
                pass

            if (_np.iscomplexobj(self.img_RGB_list[rgbnum].data.grayscaleimage) & 
                self.ui.actionUseImagData.isChecked()):

                self.img_RGB_list[rgbnum].data.grayscaleimage = self.img_RGB_list[rgbnum].data.grayscaleimage.imag
            else:
                self.img_RGB_list[rgbnum].data.grayscaleimage = self.img_RGB_list[rgbnum].data.grayscaleimage.real
            
            
            minner = self.img_RGB_list[rgbnum].data.grayscaleimage.min()
            minner = _np.sign(minner)*(1.1*_np.abs(minner))

            maxer = self.img_RGB_list[rgbnum].data.grayscaleimage.max()
            maxer = _np.sign(maxer)*(1.1*_np.abs(maxer))

            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMin.setMinimum(minner)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMin.setMaximum(maxer)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMax.setMinimum(minner)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMax.setMaximum(maxer)

            self.img_RGB_list[rgbnum].changeColor()

        else:
            pass
        self.doComposite()

    def setOpFreq1(self):
        """
        Set color math frequency #1 (the primary frequency)
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.opfreq1 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonOpFreq1.setText(str(round(currentfreq, 1)))
            self.img_RGB_list[rgbnum].data.grayscaleimage = self.img_BW.data.grayscaleimage

            minner = self.img_RGB_list[rgbnum].data.grayscaleimage.min()
            minner = _np.sign(minner)*(1.1*_np.abs(minner))

            maxer = self.img_RGB_list[rgbnum].data.grayscaleimage.max()
            maxer = _np.sign(maxer)*(1.1*_np.abs(maxer))

            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMin.setMinimum(minner)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMin.setMaximum(maxer)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMax.setMinimum(minner)
            self.img_RGB_list[rgbnum].gsinfo.ui.spinBoxMax.setMaximum(maxer)
            
            self.img_RGB_list[rgbnum].changeColor()

            self.img_RGB_list[rgbnum].mpl.draw()

        except Exception:
            print('Error')
        self.doComposite()

    def setOpFreq2(self):
        """
        Set color math frequency #2 (e.g., freq #1 + freq #2)
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.opfreq2 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonOpFreq2.setText(str(round(currentfreq, 1)))
        except Exception:
            pass

    def setOpFreq3(self):
        """
        Set color math frequency #3 (e.g., Amplitude at freq #1 - interpolation [freq #2, freq #3])
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.opfreq3 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonOpFreq3.setText(str(round(currentfreq, 1)))

        except Exception:
            pass

    def setCondFreq1(self):
        """
        Set color math conditional frequency #1
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.condfreq1 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonCondFreq1.setText(str(round(currentfreq, 1)))

        except Exception:
            print('Error')

    def setCondFreq2(self):
        """
        Set color math conditional frequency #2
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.condfreq2 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonCondFreq2.setText(str(round(currentfreq, 1)))

        except Exception:
            print('Error')

    def setCondFreq3(self):
        """
        Set color math conditional frequency #1
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.img_RGB_list[rgbnum].data.condfreq3 = currentfreq
            self.img_RGB_list[rgbnum].math.ui.pushButtonCondFreq3.setText(str(round(currentfreq, 1)))

        except Exception:
            print('Error')

    def spectrumColorImg(self):
        """
        Generate plot of mean
        """
        # Which RGB image is it
        rgbnum = self.ui.tabColors.currentIndex()

        Mask = _copy.deepcopy(self.img_RGB_list[rgbnum].data.grayscaleimage)

        if self.img_RGB_list[rgbnum].data.setmin is not None:
            Mask *= Mask >= self.img_RGB_list[rgbnum].data.setmin

        if self.img_RGB_list[rgbnum].data.setmax is not None:
            Mask *= Mask <= self.img_RGB_list[rgbnum].data.setmax

        if Mask.max() <= 0:
            pass
        else:

            Mask = Mask > 0
            Mask = Mask.astype(_np.int32)

            mask_hits = Mask.sum()


            mloc, nloc = _np.where(Mask)


            if mask_hits > 0:
                rng = self.hsi.freq.op_range_pix

                if isinstance(self.hsi.data, _h5py.Dataset):

                    # * Can't do fancy boolean indexing with HDF
                    # * Make a square bounding box

                    rmin = mloc.min()
                    rmax = mloc.max()+1
                    cmin = nloc.min()
                    cmax = nloc.max()+1

                    spectra = self.hsi.data[rmin:rmax, cmin:cmax,:][Mask[rmin:rmax, cmin:cmax]==1]
                    
                else:
                    spectra = self.hsi.data[Mask == 1]
                
                if _np.iscomplexobj(spectra) & self.ui.actionUseImagData.isChecked():
                    spectra = spectra.imag
                else:
                    spectra = spectra.real

                if mask_hits > 1:
                    spectrum = _np.mean(spectra[..., rng], axis=0)
                    stddev = _np.std(spectra[..., rng], axis=0)
                else:
                    spectrum = _np.squeeze(spectra[..., rng])
                    stddev = 0
                    
                self.plotter.plot(self.hsi.f, spectrum, label='Mean spectrum ({})'.format(mask_hits))
                
                # Check color of line b/c uses color cycler-- for fill_b/w
                color = self.plotter.list_all[-1].style_dict['color']

                # Alternative
                #color = self.plotter.modelLine._model_data[-1]['color']

                # Plot +-1 std. dev.
                if mask_hits > 1:
                    self.plotter.fill_between(self.hsi.f, spectrum - stddev,
                                              spectrum + stddev,
                                              color=color,
                                              alpha=0.25,
                                              label=r'$\pm$1 Std. Dev. ({})'.format(mask_hits))


            self.plotter.show()
            self.plotter.raise_()

    def createImgBW(self, img):
        """
        Generate the single-frequency grayscale image
        """
        xunits = self.img_BW.data.xunits
        yunits = self.img_BW.data.yunits
        extent = self.img_BW.data.winextent

        self.img_BW.createImg(img=img, xunits=xunits,
                              yunits=yunits,
                              extent=extent,
                              cmap=self.img_BW.colormode.ui.comboBoxColormap.currentText())

        if self.img_BW.ui.checkBoxFixed.checkState()==0:
            self.img_BW.ui.spinBoxMax.setValue(self.img_BW.data.maxer)
            self.img_BW.ui.spinBoxMin.setValue(self.img_BW.data.minner)

    def changeSlider(self):
        """
        Respond to change in frequency slider
        """

        # Get current axis limits to reset to these
        # after refresh is performed
        orig_axis_lims = self.img_BW.mpl.ax.axis()

        pos = self.ui.freqSlider.sliderPosition()
        assert isinstance(pos, int), 'Slider position need be an integer'

        if self.hsi.freq.op_list_pix is not None:
            offset = self.hsi.freq.op_list_pix[0]
        else:
            offset = 0

        self.ui.lineEditPix.setText(str(pos))

        try:
            self.ui.lineEditFreq.setText(str(round(self.hsi.f[pos],2)))
            # Set BW Class Data

            self.img_BW.data.grayscaleimage = self.hsi.data[:, :, pos+offset]
            if _np.iscomplexobj(self.img_BW.data.grayscaleimage) & self.ui.actionUseImagData.isChecked():
                self.img_BW.data.grayscaleimage = self.img_BW.data.grayscaleimage.imag
            else:
                self.img_BW.data.grayscaleimage = self.img_BW.data.grayscaleimage.real

            val_extrema = _np.max(_np.abs(self.img_BW.data.grayscaleimage))
        
            self.img_BW.ui.spinBoxMin.setMinimum(-1.1*val_extrema)
            self.img_BW.ui.spinBoxMin.setMaximum(1.1*val_extrema)
            self.img_BW.ui.spinBoxMax.setMinimum(-1.1*val_extrema)
            self.img_BW.ui.spinBoxMax.setMaximum(1.1*val_extrema)

            xlabel = ''
            if isinstance(self.hsi.x_rep.label, str):
                xlabel += self.hsi.x_rep.label.strip()
            if isinstance(self.hsi.x_rep.units, str):
                xlabel += ' ('
                xlabel += self.hsi.x_rep.units.strip()
                xlabel += ')'

            # print('Xlabel: {}'.format(xlabel))
            ylabel = ''
            if isinstance(self.hsi.y_rep.label, str):
                ylabel += self.hsi.y_rep.label.strip()
            if isinstance(self.hsi.y_rep.units, str):
                ylabel += ' ('
                ylabel += self.hsi.y_rep.units.strip()
                ylabel += ')'

            self.img_BW.data.set_x(self.hsi.x, xlabel)
            self.img_BW.data.set_y(self.hsi.y, ylabel)

            self.img_BW.checkBoxRemOutliers()
            # if self.img_BW.ui.checkBoxFixed.checkState() == 0:
            #     self.img_BW.data.setmax = None
            #     self.img_BW.data.setmin = None

            # Set axis to original limits
            self.img_BW.mpl.ax.axis(orig_axis_lims)

            if self._mpl_v1:
                self.img_BW.mpl.ax.hold(True)

        except Exception:
            print('Error in changeSlider: display img_BW')

        try:
            if self.show_overlays:
                for ol in self.overlays:
                    x = ol['meta']['x']
                    y = ol['meta']['y']

                    color = ol['color']
                    mfc = color  # Marker face color
                    mec = color  # Marker edge color
                    lw = ol['linewidth']  # Linewidth
                    label = ol['label']
                    ls = ol['linestyle']  # Linestyle
                    ms = ol['markersize']  # Markersize
                    a = ol['alpha']
                    marker = ol['marker']

                    # Need some sort of marker if just a point
                    if _np.size(x) == 1:
                        if isinstance(marker, str):
                            if marker.lower() == 'none':
                                marker = 'x'

                    self.img_BW.mpl.ax.plot(x, y, marker=marker,
                                            mfc=mfc, mec=mec,
                                            color=color, lw=lw,
                                            ls=ls, ms=ms, alpha=a,
                                            label=label)

                if self.ui.actionShowOverlayLegend.isChecked():
                    if self.overlays:
                        try:
                            # self.img_BW.mpl.ax.legend(loc='best')
                            lg = self.img_BW.mpl.ax.legend(loc='lower left', 
                                                            mode='expand', 
                                                            bbox_to_anchor=(0.01, 1.02, 1., 0.2),
                                                            ncol=2, fontsize=9)
                            self.img_BW.mpl.ax.add_artist(lg)
                            try:
                                self.img_BW.mpl.fig.tight_layout(pad=1)
                            except Exception:
                                print('tight_layout failed (CrikitUI: 3')
                        except Exception:
                            print('Error in showing overlay legend')
        except Exception:
            print('Error in changeSlider: display overlays')

        self.img_BW.mpl.draw()

        if self.ui.actionShowPreviewROI.isChecked():
            self.showPreviewRois()

        if self.bcpre.backed_flag.count(True) > 1:
            self.ui.actionUndo.setEnabled(True)
        else:
            self.ui.actionUndo.setEnabled(False)

    def sliderPressed(self):
        """
        Respond to press of frequency slider (set tracking of location)
        """
        self.ui.freqSlider.setTracking(False)

    def sliderReleased(self):
        """
        Respond to release of frequency slider (end tracking of location)
        """
        self.ui.freqSlider.setTracking(True)

    def checkCompositeUpdate(self,num):
        """
        Update color composite only if appropriate tab is selected.
        """
        if num == self.ui.tabColors.count()-1:
            self.doComposite()

    def doComposite(self):
        """
        Update color composite image.
        """
        try:
            self.img_Composite.initData(self.img_RGB_list)
            self.img_Composite.changeMode()  # This checks what mode is set

            xlabel = ''
            if isinstance(self.hsi.x_rep.label, str):
                xlabel += self.hsi.x_rep.label.strip()
            if isinstance(self.hsi.x_rep.units, str):
                xlabel += ' ('
                xlabel += self.hsi.x_rep.units.strip()
                xlabel += ')'

            # print('Xlabel: {}'.format(xlabel))
            ylabel = ''
            if isinstance(self.hsi.y_rep.label, str):
                ylabel += self.hsi.y_rep.label.strip()
            if isinstance(self.hsi.y_rep.units, str):
                ylabel += ' ('
                ylabel += self.hsi.y_rep.units.strip()
                ylabel += ')'

            self.img_Composite.data.set_x(self.hsi.x, xlabel)
            self.img_Composite.data.set_y(self.hsi.y, ylabel)

            self.img_Composite.createImg(img=self.img_Composite.data.image,
                                         xunits=self.img_Composite.data.xunits,
                                         yunits=self.img_Composite.data.yunits,
                                         extent=self.img_BW.data.winextent)
            self.img_Composite.mpl.draw()

            self.img_Composite2.initData(self.img_RGB_list)
            self.img_Composite2.changeMode()

            self.img_Composite2.data.set_x(self.hsi.x, xlabel)
            self.img_Composite2.data.set_y(self.hsi.y, ylabel)
            self.img_Composite2.createImg(img=self.img_Composite2.data.image,
                                          xunits=self.img_Composite2.data.xunits,
                                          yunits=self.img_Composite2.data.yunits,
                                          extent=self.img_BW.data.winextent)
            self.img_Composite2.mpl.draw()
        except Exception:
            print('Error in doComposite')

    def updateOverlays(self):
        self.overlays=[]
        for ln in self.plotter.list_line_objs:
            ms = ln.model_style

            # Make sure there is the appropriate meta data
            if ms.get('meta').get('overlay') is not None:
                if ms['meta']['overlay'] == True:
                    self.overlays.append(ms)
        self.changeSlider()

    def deleteOverlays(self):
        self.updateOverlays()

    def checkShowOverlays(self):
        self.show_overlays = self.ui.actionShowOverlays.isChecked()
        self.changeSlider()

    def makeRamanPhantom(self):
        """
        Generate a numerical phantom for Raman
        """
        cplx = False  # Is model complex-valued -- False for Raman

        dialog = DialogModel.dialogModel(cplx=cplx, parent=self)
        if dialog is not None:
            model = _Model(subsample=dialog['subsample'])

            wn_start = dialog['wn_start']
            wn_end = dialog['wn_end']

            lam_start = 0.01 / (wn_start + 0.01/(dialog['probe']*1e-9))  # meters
            lam_start *= 1e9  # nm

            lam_end = 0.01 / (wn_end + 0.01/(dialog['probe']*1e-9))  # meters
            lam_end *= 1e9  # nm

            lam_ctr = (lam_start + lam_end) / 2  # nm

            n_pix = _np.ceil((lam_end-lam_start) / dialog['wl_slope'])

            # Make a properly linear frequency-vector and polyfit
            f = dialog['wl_slope'] * _np.arange(n_pix)  # Temporary frequency vec
            f -= f.mean()
            f += lam_ctr

            a_vec = _np.polyfit(_np.arange(n_pix), f, 1)

            calib = {'a_vec': a_vec,
                     'ctr_wl': lam_ctr,
                     'ctr_wl0': lam_ctr,
                     'n_pix': n_pix,
                     'probe': dialog['probe'],
                     'units': 'nm'}

            f = _calib_pix_wn(calib)[0]
            model.make_hsi(f=f)

            if cplx:
                model.hsi = model.hsi.astype(_np.complex64)
                self.hsi = Hsi(data=model.hsi, x=model.x, y=model.y)
            else:
                model.hsi = 1*model.hsi.imag
                model.hsi = model.hsi.astype(_np.float32)
                self.hsi = Hsi(data=model.hsi, x=model.x, y=model.y)

            # For Raman -- make the Hsi more intense
            # This is ARBITRARY
            self.hsi._data *= 50e3

            self.hsi.freq.calib_fcn = _calib_pix_wn
            self.hsi.freq.calib = calib
            self.hsi.freq.update()

            add_gnoise = dialog['gnoise_bool']  # AWGN (Gaussian)
            add_pnoise = dialog['pnoise_bool']  # Poisson noise
            add_dark = dialog['dark_bool']  # Dark background -- just a constant

            # These values correspond to the defaults of the
            # Anscombe UI
            g_noise = dialog['gnoise_stddev']  # Std Dev of Gaussian noise
            p_amp = dialog['pnoise_gain']  # Multiplier of Poisson noise
            dark_amp = dialog['dark_level']

            if add_pnoise:  # Add Poisson noise
                # NOTE: CORRECT is p_amp*poisson(signal)
                # DEFINITELY NOT p_amp*(poisson(signal)-signal) + signal
                self.hsi._data += p_amp*(_np.random.poisson(self.hsi._data)) - self.hsi._data
            if add_gnoise:  # Add AGWN
                self.hsi._data += _np.random.randn(*self.hsi._data.shape)
            if add_dark:  # Add a constant dark background
                self.hsi._data += dark_amp
                self.dark._data = dark_amp + 0*f
                self.dark.freq = self.hsi.freq

            self.filename = 'Phantom.h5'
            self.path = _os.path.abspath('./')
            self.dataset_name = ['/RamanImage/Phantom_v0/Phantom_v0']

            meta = {'Calib.a_vec': a_vec,
                    'Calib.ctr_wl': lam_ctr,
                    'Calib.ctr_wl0': lam_ctr,
                    'Calib.n_pix': n_pix,
                    'Calib.probe': calib['probe'],
                    'Calib.units': 'nm',
                    'Memo': 'Numerical phantom from murine pancreas artery. See Camp et al, JRS (2016).',
                    'RasterScanParams.FastAxis': 'X',
                    'RasterScanParams.FastAxisStart': model.x[0],
                    'RasterScanParams.FastAxisStepSize': _np.diff(model.x).mean(),
                    'RasterScanParams.FastAxisSteps': model.x.size,
                    'RasterScanParams.FastAxisStop': model.x[-1],
                    'RasterScanParams.FixedAxis': 'Z',
                    'RasterScanParams.FixedAxisPosition': 0,
                    'RasterScanParams.SlowAxis': 'Y',
                    'RasterScanParams.SlowAxisStart': model.y[0],
                    'RasterScanParams.SlowAxisStepSize': _np.diff(model.y).mean(),
                    'RasterScanParams.SlowAxisSteps': model.y.size,
                    'RasterScanParams.SlowAxisStop': model.y[-1],
                    'Spectro.CenterWavelength': lam_ctr,
                    }
            self.hsi._meta = meta
            self.fileOpenSuccess(True)
            self.changeSlider()
        else:
            pass


    def makeBCARSPhantom(self):
        """
        Generate a numerical phantom for BCARS
        """
        cplx = True  # Is model complex-valued -- True for BCARS

        dialog = DialogModel.dialogModel(cplx=cplx, parent=self)
        if dialog is not None:
            model = _Model(subsample=dialog['subsample'])

            wn_start = dialog['wn_start']
            wn_end = dialog['wn_end']

            lam_start = 0.01 / (wn_start + 0.01/(dialog['probe']*1e-9))  # meters
            lam_start *= 1e9  # nm

            lam_end = 0.01 / (wn_end + 0.01/(dialog['probe']*1e-9))  # meters
            lam_end *= 1e9  # nm

            lam_ctr = (lam_start + lam_end) / 2  # nm

            n_pix = _np.ceil((lam_end-lam_start) / dialog['wl_slope'])

            # Make a properly linear frequency-vector and polyfit
            f = dialog['wl_slope'] * _np.arange(n_pix)  # Temporary frequency vec
            f -= f.mean()
            f += lam_ctr

            a_vec = _np.polyfit(_np.arange(n_pix), f, 1)

            calib = {'a_vec': a_vec,
                     'ctr_wl': lam_ctr,
                     'ctr_wl0': lam_ctr,
                     'n_pix': n_pix,
                     'probe': dialog['probe'],
                     'units': 'nm'}

            f = _calib_pix_wn(calib)[0]
            model.make_hsi(f=f)

            if cplx:
                model.hsi = model.hsi.astype(_np.complex64)
                self.hsi = Hsi(data=model.hsi, x=model.x, y=model.y)
            else:
                model.hsi = 1*model.hsi.imag
                model.hsi = model.hsi.astype(_np.float32)
                self.hsi = Hsi(data=model.hsi, x=model.x, y=model.y)

            # Simple Gaussian 0-centered source profile
            source = 1e2*_np.exp(-f**2/(2*1500**2))
            nrb = 10*_np.exp(-(f-20e3)**2/(2*10e3**2))

            self.hsi.data = _np.abs((self.hsi.data+nrb)*source)**2
            self.hsi.freq.calib_fcn = _calib_pix_wn
            self.hsi.freq.calib = calib
            self.hsi.freq.update()

            self.nrb.data = _np.abs(source*nrb)**2
            self.nrb.freq = self.hsi.freq

            add_gnoise = dialog['gnoise_bool']  # AWGN (Gaussian)
            add_pnoise = dialog['pnoise_bool']  # Poisson noise
            add_dark = dialog['dark_bool']  # Dark background -- just a constant

            # These values correspond to the defaults of the
            # Anscombe UI
            g_noise = dialog['gnoise_stddev']  # Std Dev of Gaussian noise
            p_amp = dialog['pnoise_gain']  # Multiplier of Poisson noise
            dark_amp = dialog['dark_level']

            # Only dark added to NRB
            # Others only to Hsi data
            if add_pnoise:  # Add Poisson noise
                # NOTE: CORRECT is p_amp*poisson(signal)
                # DEFINITELY NOT p_amp*(poisson(signal)-signal) + signal
                self.hsi._data += p_amp*(_np.random.poisson(self.hsi._data)) - self.hsi._data
            if add_gnoise:  # Add AGWN
                self.hsi._data += _np.random.randn(*self.hsi._data.shape)
            if add_dark:  # Add a constant dark background
                self.hsi._data += dark_amp
                self.nrb._data += dark_amp
                self.dark._data = dark_amp + 0*f
                self.dark.freq = self.hsi.freq

            self.filename = 'Phantom.h5'
            self.path = _os.path.abspath('./')
            self.dataset_name = ['/BCARSImage/Phantom_v0/Phantom_v0']

            meta = {'Calib.a_vec': a_vec,
                    'Calib.ctr_wl': lam_ctr,
                    'Calib.ctr_wl0': lam_ctr,
                    'Calib.n_pix': n_pix,
                    'Calib.probe': calib['probe'],
                    'Calib.units': 'nm',
                    'Memo': 'Numerical phantom from murine pancreas artery. See Camp et al, JRS (2016).',
                    'RasterScanParams.FastAxis': 'X',
                    'RasterScanParams.FastAxisStart': model.x[0],
                    'RasterScanParams.FastAxisStepSize': _np.diff(model.x).mean(),
                    'RasterScanParams.FastAxisSteps': model.x.size,
                    'RasterScanParams.FastAxisStop': model.x[-1],
                    'RasterScanParams.FixedAxis': 'Z',
                    'RasterScanParams.FixedAxisPosition': 0,
                    'RasterScanParams.SlowAxis': 'Y',
                    'RasterScanParams.SlowAxisStart': model.y[0],
                    'RasterScanParams.SlowAxisStepSize': _np.diff(model.y).mean(),
                    'RasterScanParams.SlowAxisSteps': model.y.size,
                    'RasterScanParams.SlowAxisStop': model.y[-1],
                    'Spectro.CenterWavelength': lam_ctr,
                    }
            self.hsi._meta = meta

            self.ui.actionDarkSpectrum.setEnabled(True)
            self.ui.actionNRBSpectrum.setEnabled(True)
            self.ui.actionDarkSubtract.setEnabled(True)
            self.ui.actionKramersKronig.setEnabled(True)
            self.ui.actionPhaseErrorCorrection.setEnabled(True)
            self.ui.actionScaleErrorCorrection.setEnabled(True)
            self.ui.menuCoherent_Raman_Imaging.setEnabled(True)

            self.fileOpenSuccess(True)
            self.changeSlider()
        else:
            pass

    def specialDemosaicRGB(self):
        msg = _QMessageBox(self)
        msg.setIcon(_QMessageBox.Question)
        msg.setText('You will need to select the MASK dataset associated with your mosaic image')
        msg.setWindowTitle('Select Mask file')
        # msg.setInformativeText('This should only be applied to RAW BCARS2 data from NIST.')
        msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
        msg.setDefaultButton(_QMessageBox.Ok)
        out = msg.exec()
        
        if out != _QMessageBox.Ok:
            return None

        try:
            if (self.filename is not None) & (self.path is not None):
                to_open = HdfLoad.getFileDataSets(_os.path.join(self.path, self.filename), parent=self, title='Mask Image')
            else:
                to_open = HdfLoad.getFileDataSets(self.path, parent=self, title='Mask Image')
        except Exception as e:
            _traceback.print_exc(limit=1)
            print('Could not open file. Corrupt or not appropriate file format: {}'.format(e))
        else:
            if to_open is not None:
                path, filename, dataset_name = to_open
                if isinstance(dataset_name, list):
                    dataset_name = dataset_name[0]
                print('Opening {}/{}/{}'.format(path, filename, dataset_name))
                with _h5py.File(lazy5.utils.fullpath(filename, pth=path), 'r') as fid:
                    img_shape = fid[dataset_name].shape
                    self._mosaic_mask = _np.zeros(img_shape)
                    fid[dataset_name].read_direct(self._mosaic_mask)
                    n_imgs = self._mosaic_mask.max().astype(int)
                    fid.close()
            
            msg = _QMessageBox(self)
            msg.setIcon(_QMessageBox.Question)
            msg.setText('You will need to select/create a directory to save the new images in')
            msg.setWindowTitle('Select directory')
            msg.setStandardButtons(_QMessageBox.Ok | _QMessageBox.Cancel)
            msg.setDefaultButton(_QMessageBox.Ok)
            out = msg.exec()
            if out != _QMessageBox.Ok:
                return None
            save_path = _QFileDialog.getExistingDirectory(self, 'Select Folder to Save Images',
                                                          path)

            
            for num_rgb, rgb_win in enumerate(self.img_RGB_list):
                if rgb_win.data.image.sum() == 0:
                    continue
                for num_z in range(n_imgs):
                    save_name = 'Color_{}_z{}.tiff'.format(num_rgb, num_z)
                    w = _np.where(self._mosaic_mask == num_z)
                    temp = rgb_win.data.image[slice(w[0].min(), w[0].max()+1), slice(w[1].min(), w[1].max()+1), :]
                    _plt.figure(dpi=300)
                    _plt.imshow(temp)
                    _plt.axis('off')
                    _plt.tight_layout(pad=0)
                    _plt.savefig(lazy5.utils.fullpath(save_name, pth=save_path), dpi=300)
                    _plt.close()
            for num_z in range(n_imgs):
                save_name = 'Composite_z{}.tiff'.format(num_z)
                w = _np.where(self._mosaic_mask == num_z)
                temp = self.img_Composite.data.image[slice(w[0].min(), w[0].max()+1), slice(w[1].min(), w[1].max()+1), :]
                _plt.figure(dpi=300)
                _plt.imshow(temp)
                _plt.axis('off')
                _plt.tight_layout(pad=0)
                _plt.savefig(lazy5.utils.fullpath(save_name, pth=save_path), dpi=300)
                _plt.close()


def crikit_launch(**kwargs):
    """
    Command line launching of CRIkitUI.

    Input kwargs (Optional)
    ------------------------
    hsi : crikit.data.spectra.Hsi
        Hsi instance

    data : ndarray (3D)
        Numpy array (Y,X,Freq) hsi

    x : ndarray (1D)
        x-array

    x_units : str
        Units of x (e.g. r'$\mu$m')

    x_label : str
        Label of x (e.g. 'X')

    y : ndarray (1D)
        y-array

    y_units : str
        Units of y (e.g. r'$\mu$m')

    y_label : str
        Label of y (e.g. 'Y')

    f : ndarray (1D)
        frequency-array

    f_units : str
        Units of frequency (e.g. r'cm$^{-1}$')

    f_label : str
        Label of frequency (e.g. 'Wavenumber')

    filename : str
        Filename of HDF data to auto-load (requires path and dataset_name as well)

    path : str
        Path of HDF data to auto-load (requires filename and dataset_name as well)

    dataset_name : str
        Dataset name(s) of HDF data to auto-load (requires path and filename as well)

    """

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    app.setQuitOnLastWindowClosed(False)

    parent = kwargs.get('parent')

    if parent is None:
        obj = _QWidget()
    else:
        obj = parent

    kwargs['parent'] = obj
    # print('Kwargs: {}'.format(kwargs))
    win = CRIkitUI_process(**kwargs) ### EDIT ###

    # Insert other stuff to do

    # Final stuff
    win.showMaximized()
    #win.plotter.lower()
    #win.raise_()
    app.exec_()
    return None

if __name__ == '__main__':

    from crikit.ui.utils.check_requirements import check_requirements
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    app.setQuitOnLastWindowClosed(False)
    
    obj = _QWidget()

    has_requirements = check_requirements()
    if has_requirements:
        win = CRIkitUI_process(parent=obj) ### EDIT ###
        win.showMaximized()
        _sys.exit(app.exec_())
    else:
        app.quit()
    #app.closeAllWindows()
