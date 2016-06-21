# -*- coding: utf-8 -*-
"""
Created on Sat Jun 18 16:46:45 2016

@author: chc
"""

# Append sys path
import sys as _sys
import os as _os

if __name__ == '__main__':
   _sys.path.append(_os.path.abspath('../'))

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication, \
QWidget as _QWidget, QMainWindow as _QMainWindow, QLayout as _QLayout,\
 QGridLayout as _QGridLayout, QInputDialog as _QInputDialog,
 QMessageBox as _QMessageBox)
import PyQt5.QtCore as _QtCore
from PyQt5.QtGui import (QCursor as _QCursor)

# Other imports
import numpy as _np
import timeit as _timeit
import copy as _copy

import h5py as _h5py
_h5py.get_config().complex_names = ('Re','Im')

# CRIkit import
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

from crikit.io.macros import import_hdf_nist_special as io_nist
from crikit.io.hdf5 import hdf_export_data as _io_export

from crikit.utils.breadcrumb import BCPre as _BCPre
from crikit.utils.general import find_nearest

from crikit.preprocess.subtract_dark import SubtractDark
from crikit.preprocess.subtract_mean import SubtractMeanOverRange
from crikit.preprocess.crop import (ZeroColumn as _ZeroColumn,
                                    ZeroRow as _ZeroRow)

from crikit.cri.kk import KramersKronig
#

#from crikit.ui.subui_plotter import SubUiPlotter as _Plotter
#from crikit.ui.subui_ploteffect import DialogPlotEffect as _DialogPlotEffect
#from crikit.ui.widget_ploteffect import (widgetCalibrate as _widgetCalibrate)
#from crikit.ui.helper_roiselect import ImageSelection as _ImageSelection
#from crikit.ui.utils.visgenutils import roimask as _roimask


#from crikit.data.retr import retr_freq_plane, retr_freq_plane_add, \
#    retr_freq_plane_div, retr_freq_plane_multi, retr_freq_plane_peak_bw_troughs, \
#    retr_freq_plane_sub, retr_freq_plane_sum_span


#from crikit.process.phase_retr import (alter_kk as _alter_kk,
#                                       test_alter_kk as _test_alter_kk)

# Import from Designer-based GUI
from crikit.ui.qt_CRIkit import Ui_MainWindow ### EDIT ###

#from crikit.ui.widget_images import widgetSglColor, widgetColorMath, widgetBWImg, widgetCompositeColor
#
from crikit.ui.subui_hdf_load import SubUiHDFLoad
from crikit.ui.dialog_options import DialogDarkOptions, DialogKKOptions
from crikit.ui.dialog_plugin import DialogDenoisePlugins, DialogErrCorrPlugins
from crikit.ui.subui_SVD import DialogSVD
#from crikit.ui.dialog_save import DialogSave

# Generic imports for MPL-incorporation
import matplotlib as _mpl
import matplotlib.pyplot as _plt

_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 12

#import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as _FigureCanvas, \
    NavigationToolbar2QT as _NavigationToolbar)
from matplotlib.figure import Figure as _Figure

jupyter_flag = 0
try:
    from crikit.ui.widget_Jupyter import QJupyterWidget
    jupyter_flag = 1
except:
    print('No appropriate Jupyter/IPython installation found. Console will not be available')
    jupyter_flag = -1

#from matplotlib.path import Path as _Path


class CRIkitUI_process(_QMainWindow):
    """
    CRIkitUI_process : CRIkitUI for image (pre-)processing

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

    version: ("16.2.12")
    """

    NUMCOLORS = 4  # Number of single-color windows to auto-generate

    def __init__(self, parent = None):

        # Generic load/init designer-based GUI
        super(CRIkitUI_process, self).__init__(parent) ### EDIT ###

        self.filename = None
        self.path = None
        self.dataset_name = None

        self.hsi = Hsi()
        self.bcpre = _BCPre()

        self.dark = Spectra()
        self.nrb = Spectra()

#        self.plotter = _Plotter()
#        self.selectiondata = _ImageSelection()

        self.ui = Ui_MainWindow() ### EDIT ###


        self.ui.setupUi(self)     ### EDIT ###

        # Initialize Intensity image (single frequency B&W)
#        self.ui.ui_BWImg = widgetBWImg()
#        if self.ui.ui_BWImg.ui.checkBoxFixed.checkState()==0:
#                self.ui.ui_BWImg.ui.lineEditMax.setText(str(round(self.ui.ui_BWImg.data.maxer,4)))
#                self.ui.ui_BWImg.ui.lineEditMin.setText(str(round(self.ui.ui_BWImg.data.minner,4)))
#
#
#
#        self.ui.sweeperVL.insertWidget(0, self.ui.ui_BWImg)
#        self.ui.ui_BWImg.mpl.fig.tight_layout(pad = 2)

        # Initialize Single-Color RGB widgets
#        self.ui.RGB = []
#
#        for count in range(self.NUMCOLORS):
#            self.ui.RGB.append(widgetSglColor())
#            self.ui.RGB[count].data.colormap =\
#                widgetSglColor.COLORMAPS[widgetSglColor.DEFAULT_COLORMAP_ORDER[count]]
#            ind = self.ui.RGB[count].ui.comboBox.findText(widgetSglColor.DEFAULT_COLORMAP_ORDER[count])
#            self.ui.RGB[count].ui.comboBox.setCurrentIndex(ind)
#            #self.ui.RGB[count].ui.pushButtonSpectrum.pressed.connect(lambda: self.spectrumColorImg(win=self.ui.RGB[count]))
#            self.ui.RGB[count].ui.pushButtonSpectrum.setEnabled(False)
#            self.ui.tabColors.addTab(self.ui.RGB[count], 'Color ' + str(count))
#
#            self.ui.RGB[count].math.ui.pushButtonDoMath.setEnabled(False)
#
#            self.ui.RGB[count].math.ui.pushButtonOpFreq1.pressed.connect(self.setOpFreq1)
#            self.ui.RGB[count].math.ui.pushButtonOpFreq2.pressed.connect(self.setOpFreq2)
#            self.ui.RGB[count].math.ui.pushButtonOpFreq3.pressed.connect(self.setOpFreq3)
#            self.ui.RGB[count].math.ui.comboBoxOperations.currentIndexChanged.connect(self.opChange)
#
#            self.ui.RGB[count].math.ui.pushButtonCondFreq1.pressed.connect(self.setCondFreq1)
#            self.ui.RGB[count].math.ui.pushButtonCondFreq2.pressed.connect(self.setCondFreq2)
#            self.ui.RGB[count].math.ui.pushButtonCondFreq3.pressed.connect(self.setCondFreq3)
#            self.ui.RGB[count].math.ui.comboBoxCondOps.currentIndexChanged.connect(self.condOpChange)
#            self.ui.RGB[count].math.ui.comboBoxCondInEquality.currentIndexChanged.connect(self.condInEqualityChange)
#            self.ui.RGB[count].math.ui.spinBoxInEquality.editingFinished.connect(self.spinBoxInEqualityChange)
#
#            self.ui.RGB[count].math.ui.pushButtonDoMath.pressed.connect(self.doMath)
#            self.ui.RGB[count].ui.gainSlider.valueChanged.connect(self.doComposite)
#
#
#        self.ui.CompositeColor = widgetCompositeColor(self.ui.RGB)
#        self.ui.CompositeColor2 = widgetCompositeColor(self.ui.RGB)

#        self.ui.tabColors.addTab(self.ui.CompositeColor, 'Composite Image')

#        self.ui.sweeperVL_2.insertWidget(0,self.ui.CompositeColor2)

#        self.ui.tabColors.currentChanged.connect(self.checkCompositeUpdate)


        # SET SIGNALS-SLOTS

        # Load Data
        self.ui.actionOpenHDFNIST.triggered.connect(self.fileOpenHDFNIST)
        self.ui.actionLoadNRB.triggered.connect(self.loadNRB)
        self.ui.actionLoadDark.triggered.connect(self.loadDark)

        self.ui.actionNRB_from_ROI.triggered.connect(self.nrbFromROI)
        self.ui.actionAppend_NRB_from_ROI.triggered.connect(self.nrbFromROI)


        # Settings
        self.ui.actionSettings.triggered.connect(self.settings)

        # Undo
        self.ui.actionUndo.triggered.connect(self.doUndo)

        # Close event
        self.ui.closeEvent = self.closeEvent

        # Subtract DARK-Related
        self.ui.actionDarkSubtract.triggered.connect(self.subDark)


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

        # Perform KK
        self.ui.actionKramersKronig.triggered.connect(self.doKK)
        self.ui.actionKKSpeedTest.triggered.connect(self.testKK)

        # DeNoise
        self.ui.actionDeNoise.triggered.connect(self.deNoise)

        # Error Correction
        self.ui.actionErrorCorrection.triggered.connect(self.errorCorrect)
        self.ui.actionSubtractROI.triggered.connect(self.subtractROIStart)

        # SAVE
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave.triggered.connect(self.save)

        # Plotting spectra-related
#        self.ui.actionPointSpectrum.triggered.connect(self.pointSpectrum)
#        self.ui.actionROISpectrum.triggered.connect(self.roiSpectrum)
#        self.plotter.model.dataDeleted.connect(self.deleteSelection)
#        self.plotter.model.colorChanged.connect(self.colorChange)
#        self.ui.actionDarkSpectrum.triggered.connect(self.plotDarkSpectrum)
#        self.ui.actionNRBSpectrum.triggered.connect(self.plotNRBSpectrum)
#        self.ui.actionShowPlotter.triggered.connect(self.plotter.show)
#
#        # Frequency-slider related
#        self.ui.freqSlider.valueChanged.connect(self.changeSlider)
#        self.ui.freqSlider.sliderPressed.connect(self.sliderPressed)
#        self.ui.freqSlider.sliderReleased.connect(self.sliderReleased)
#        self.ui.freqSlider.setTracking(True)
#
#        # Frequency-slider display boxes
#        self.ui.lineEditFreq.editingFinished.connect(self.lineEditFreqChanged)
#        self.ui.lineEditPix.editingFinished.connect(self.lineEditPixChanged)
#        self.ui.lineEditPix.setVisible(False)
#        self.ui.labelFreqPixel.setVisible(False)


        # Jupyter console

        if jupyter_flag == 1:


            self.jupyterConsole = QJupyterWidget(customBanner="Welcome to the embedded ipython console\n")
            self.ui.tabMain.addTab(self.jupyterConsole, 'Jupyter/IPython Console')
#            self.jupyterConsole.pushVariables({'ui':self.ui,
#                                          'bcpre':self.bcpre, 'dark':self.dark,
#                                          'nrb':self.nrb, 'plotter':self.plotter,
#                                          'crikit_data':self})
            self.jupyterConsole.pushVariables({'ui':self.ui,
                                          'bcpre':self.bcpre, 'dark':self.dark,
                                          'nrb':self.nrb,
                                          'crikit_data':self})
            self.ui.tabMain.currentChanged.connect(self.tabMainChange)


    def save(self):
        suffix = self.bcpre.dset_name_suffix
#        print('Suffix: {}'.format(suffix))
        try:
            ret = DialogSave.dialogSave(current_filename=self.filename,
                                                                current_path=self.path,
                                                                current_dataset_name=self.dataset_name[0],
                                                                suffix=suffix)
            if ret is None:
                pass # Save canceled
            else:
                self.save_filename = ret[0]
                self.save_path = ret[1]
                self.save_dataset_name = ret[2]
#                print('Filename: {}'.format(self.save_filename))
#                print('Dataset name: {}'.format(self.save_dataset_name))
#                print('Path: {}'.format(self.save_path))

                self.save_grp = self.save_dataset_name.rpartition('/')[0]
                self.save_dataset_name_no_grp = self.save_dataset_name.rpartition('/')[-1]

#                print('Group location: {}'.format(self.save_grp))

                try:
                    f_out = _h5py.File(self.save_path + self.save_filename, 'a')
                    loc = f_out.require_group(self.save_grp)
                    dset = loc.create_dataset(self.save_dataset_name_no_grp, data=self.hsi.spectrafull)

                    for attr_key in self.hsi.attr:
                        try:
                            dset.attrs.create(attr_key,self.hsi.attr[attr_key])
                        except:
                            print('Error in HSI attributes')

                    bc_attr_dict = self.bcpre.attr_dict
#                    print('BC Attr Dict: {}'.format(bc_attr_dict))
                    for attr_key in bc_attr_dict:
                        #print('Key: {}, Val: {}'.format(attr_key, bc_attr_dict[attr_key]))
                        val = bc_attr_dict[attr_key]
                        if isinstance(val, str):
                            dset.attrs[attr_key] = val
                        else:
                            try:
                                dset.attrs.create(attr_key,bc_attr_dict[attr_key])
                            except:
                                print('Could not create attribute')

                except:
                    print('Something went wrong while saving')
                else:
                    print('Saved without issues')
                finally:
                    f_out.close()




        except:
            pass

    def tabMainChange(self):
        if self.ui.tabMain.currentIndex() == 4:  # Jupyter console
            self.jupyterConsole._control.setFocus()

    def closeEvent(self, event):
        self.bcpre.pop_to_last(all=True)

        del_flag = 0

        for count in self.bcpre.cut_list:
            try:
                _os.remove(count + '.pickle')
            except:
                print('Error in deleting old pickle files')
            else:
                del_flag += 1
        if del_flag == len(self.bcpre.cut_list):
            del self.bcpre.cut_list
        else:
            print('Did not delete pickle file cut list... Something went wrong')

    def fileOpenHDFNIST(self):
        """
        Open and load HDF5 File
        """

        # Get data and load into CRI_HSI class
        # This will need to change to accomodate multiple-file selection

        try:
            to_open = SubUiHDFLoad.getFileDataSets()
            print('to_open: {}'.format(to_open))
            if to_open is not None:
                self.path, self.filename, self.dataset_name = to_open
        except:
            pass
        else:
            if to_open is not None:
                self.hsi = Hsi()
                success = io_nist(self.path, self.filename, self.dataset_name,
                                   self.hsi)
                if success:
                    self.ui.actionLoadDark.setEnabled(True)
                    self.ui.actionLoadNRB.setEnabled(True)
                    self.ui.actionZeroFirstColumn.setEnabled(True)
                    self.ui.actionZeroFirstRow.setEnabled(True)
                    self.ui.actionZeroLastColumn.setEnabled(True)
                    self.ui.actionZeroLastRow.setEnabled(True)

#                self.ui.actionSave.setEnabled(True)
#                self.ui.actionDeNoise.setEnabled(True)
#                self.ui.actionErrorCorrection.setEnabled(True)
#                self.ui.actionAnalysisToolkit.setEnabled(True)
#                self.ui.actionPointSpectrum.setEnabled(True)
#                self.ui.actionROISpectrum.setEnabled(True)
#                self.ui.actionDarkSubtract.setEnabled(True)
#                self.ui.actionCalibrate.setEnabled(True)
#                self.ui.actionResetCalibration.setEnabled(True)
#                self.ui.actionNRB_from_ROI.setEnabled(True)
#                self.ui.actionAppend_NRB_from_ROI.setEnabled(True)
#                self.ui.actionSubtractROI.setEnabled(True)
                else:
                    self.ui.actionLoadDark.setEnabled(False)
                    self.ui.actionLoadNRB.setEnabled(False)
                    self.ui.actionZeroFirstColumn.setEnabled(False)
                    self.ui.actionZeroFirstRow.setEnabled(False)
                    self.ui.actionZeroLastColumn.setEnabled(False)
                    self.ui.actionZeroLastRow.setEnabled(False)

                #self.bcpre.add_step(['Raw'])
#                try:
#                    self.hsi.backup_pickle(self.bcpre.id_list[-1])
#                except:
#                    print('Error in pickle backup (Undo functionality)')
#                else:
#                    self.bcpre.backed_up()
#                # Set frequency slider and associated displays
#                self.ui.freqSlider.setMinimum(self.hsi.pixrange[0])
#                self.ui.freqSlider.setMaximum(self.hsi.pixrange[1])
#                self.ui.freqSlider.setSliderPosition(self.hsi.pixrange[0])
#                pos = self.ui.freqSlider.sliderPosition()
#                self.ui.lineEditPix.setText(str(self.ui.freqSlider.sliderPosition()))
#                self.ui.lineEditFreq.setText(str(round(self.hsi.freqvec[0],2)))
#
#
#                # Set BW Class Data
#                self.ui.ui_BWImg.initData()
#                self.ui.ui_BWImg.data.grayscaleimage = retr_freq_plane(self.hsi, pos)
#                self.ui.ui_BWImg.data.set_x(self.hsi.nvec, 'X ($\mu m$)')
#                self.ui.ui_BWImg.data.set_y(self.hsi.mvec, 'Y ($\mu m$)')
#
#                # Set min/max, fixed, compress, etc buttons to defaults
#                self.ui.ui_BWImg.ui.checkBoxFixed.setChecked(False)
#                self.ui.ui_BWImg.ui.checkBoxCompress.setChecked(False)
#                self.ui.ui_BWImg.ui.checkBoxRemOutliers.setChecked(False)
#
#                # Plot Grayscale image
#                self.createImgBW(self.ui.ui_BWImg.data.image)
#                self.ui.ui_BWImg.mpl.canvas.draw()
#
#
#                # RGB images
#                temp = 0*self.ui.ui_BWImg.data.grayscaleimage
#
#                # Re-initialize RGB images
#                for count in enumerate(self.ui.RGB):
#                    self.ui.RGB[count[0]].initData()
#                    self.ui.RGB[count[0]].data.grayscaleimage = temp
#                    self.ui.RGB[count[0]].data.set_x(self.hsi.nvec, 'X ($\mu m$)')
#                    self.ui.RGB[count[0]].data.set_y(self.hsi.mvec, 'Y ($\mu m$)')
#
#                    # Cute way of setting the colormap to last setting and replotting
#                    self.ui.RGB[count[0]].changeColor()
#
#                    # Enable Math
#                    self.ui.RGB[count[0]].math.ui.pushButtonDoMath.setEnabled(True)
#
#                    # Enable Spectrum
#                    self.ui.RGB[count[0]].ui.pushButtonSpectrum.pressed.connect(self.spectrumColorImg)
#                    self.ui.RGB[count[0]].ui.pushButtonSpectrum.setEnabled(True)

                self.ui.actionFreqWindow.setEnabled(True)
                self.ui.actionZeroFirstColumn.setEnabled(True)
                self.ui.actionZeroFirstRow.setEnabled(True)
                self.ui.actionZeroLastColumn.setEnabled(True)
                self.ui.actionZeroLastRow.setEnabled(True)
#                self.ui.actionSave.setEnabled(True)
                self.ui.actionDeNoise.setEnabled(True)
#                self.ui.actionErrorCorrection.setEnabled(True)
#                self.ui.actionAnalysisToolkit.setEnabled(True)
#                self.ui.actionPointSpectrum.setEnabled(True)
#                self.ui.actionROISpectrum.setEnabled(True)
#                self.ui.actionDarkSubtract.setEnabled(True)
#                self.ui.actionCalibrate.setEnabled(True)
#                self.ui.actionResetCalibration.setEnabled(True)
#                self.ui.actionNRB_from_ROI.setEnabled(True)
#                self.ui.actionAppend_NRB_from_ROI.setEnabled(True)
#                self.ui.actionSubtractROI.setEnabled(True)

    def loadDark(self):
        """
        Open HDF file and load dark spectrum(a)
        """

        to_open = SubUiHDFLoad.getFileDataSets()
        print('To_open: {}'.format(to_open))

        if to_open is not None:
            pth, filename, datasets = to_open
            success = io_nist(pth, filename, datasets, self.dark)

            if success:
                if self.dark.shape[-1] == self.hsi.freq.size:
                    self.ui.actionDarkSubtract.setEnabled(True)
                    self.ui.actionDarkSpectrum.setEnabled(True)
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

        to_open = SubUiHDFLoad.getFileDataSets()
        if to_open is not None:
            pth, filename, datasets = to_open

            success = io_nist(pth, filename, datasets, self.nrb)
            if success:
                if self.nrb.shape[-1] == self.hsi.freq.size:
                    self.ui.actionKramersKronig.setEnabled(True)
                    self.ui.actionKKSpeedTest.setEnabled(True)
                    self.ui.actionNRBSpectrum.setEnabled(True)
                else:
                    self.nrb = Spectra()
                    print('NRB was the wrong shape')
            else:
                self.nrb = Spectra()
                self.ui.actionKramersKronig.setEnabled(False)
                self.ui.actionKKSpeedTest.setEnabled(False)
                self.ui.actionNRBSpectrum.setEnabled(False)

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
        rand_spectra = self.hsi._get_rand_spectra(5,pt_sz=3,quads=True, full=True)
        plugin = _widgetCalibrate(calib_dict=self.hsi.freqcalib)
        winPlotEffect = _DialogPlotEffect.dialogPlotEffect(rand_spectra, x=self.hsi.freqvecfull, plugin=plugin,
                                                      xlabel='Wavenumber (cm$^{-1}$)',
                                                      ylabel='Imag. {$\chi_R$} (au)',
                                                      show_difference=False)

        if winPlotEffect is not None:
            #print('New Calibration Dictionary: {}'.format(winPlotEffect.new_calib_dict))
            self.hsi.freqcalib = winPlotEffect.new_calib_dict
            self.hsi.freqcalib_update()
        self.changeSlider()


    def calibrationReset(self):
        """
        Set self.hsi.freqcalib back to self.hsi.freqcaliborig
        """
        del self.hsi.freqcalib
        self.changeSlider()

    def plotDarkSpectrum(self):
        """
        Plot dark spectrum
        """
        if (self.dark.dark_spectrum == _np.array(None)).any():
            pass
        else:
            self.selectiondata.append_selection([None],[None],[None],[None])
            self.plotter.append_spectrum(freq=self.hsi.freqvecfull,
                                         spectrum=self.dark.dark_spectrum,
                                         label='Dark',
                                         frequnits=self.hsi.frequnits,
                                         spectrumunits=self.hsi.intensityunits)
            self.plotter.show()

    def plotNRBSpectrum(self):
        """
        Plot NRB spectrum
        """
        if (self.nrb.nrb_spectrum == _np.array(None)).any():
            pass
        else:
            self.selectiondata.append_selection([None],[None],[None],[None])
            self.plotter.append_spectrum(freq=self.hsi.freqvecfull,
                                 spectrum=self.nrb.nrb_spectrum,
                                 label='NRB',
                                 frequnits=self.hsi.frequnits,
                                 spectrumunits=self.hsi.intensityunits)

            self.plotter.show()

    def pointSpectrum(self):
        """
        Get spectrum of selected point.

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        Action
        ------
            Left mouse-click : Select vertex point
        """
        self.cid = self.ui.ui_BWImg.mpl.canvas.mpl_connect('button_press_event', lambda event: self._pointClick(event, self._pointSpectrumPlot))

        self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
        self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def subtractROIStart(self):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        Note: This function just sets up the signal-slot connection for the \
        MPL window. It executes all the way through

        """
        # Updated by _roiClick
        self.x_loc_list = []
        self.y_loc_list = []


        self.cid = self.ui.ui_BWImg.mpl.canvas.mpl_connect('button_press_event', lambda event: self._roiClick(event, self._roiSubtract))

        self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
        self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def _roiSubtract(self, locs):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        """
        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.nvec,x_loc_list)[1]
        y_pix = find_nearest(self.hsi.mvec,y_loc_list)[1]

        mask, path = _roimask(self.hsi.nvec, self.hsi.mvec,
                              x_loc_list, y_loc_list)


        mask_hits = _np.sum(mask)
        if mask_hits > 0:  # Len(mask) > 0
            spectra = _np.squeeze(self.hsi.spectrafull[mask == 1])

            if mask_hits > 1:
                spectrum = _np.mean(spectra, axis=0)
            else:
                spectrum = spectra

            spectrum = spectrum.astype(self.hsi.spectrafull.dtype)
            self.hsi.spectrafull -= spectrum[None,None,:]
            self.bcpre.add_step(['SubtractROI','Spectrum',spectrum])
            try:
                self.hsi.backup_pickle(self.bcpre.id_list[-1])
            except:
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

        sender = self.sender().objectName()
        if sender == 'actionNRB_from_ROI' or sender == 'actionAppend_NRB_from_ROI':
            # Updated by _roiClick
            self.x_loc_list = []
            self.y_loc_list = []


            self.cid = self.ui.ui_BWImg.mpl.canvas.mpl_connect('button_press_event', lambda event: self._roiClick(event, self._roiNRB, sender))

            self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
            self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
        else:
            print('Unknown action send to nrbFromROI')

    def _roiNRB(self, locs, sender):
        """
        Acquire an average spectrum from a user-selected ROI and subtract.

        """
        sender = sender[0]

        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.nvec,x_loc_list)[1]
        y_pix = find_nearest(self.hsi.mvec,y_loc_list)[1]

        mask, path = _roimask(self.hsi.nvec, self.hsi.mvec,
                              x_loc_list, y_loc_list)


        mask_hits = _np.sum(mask)
        if mask_hits > 0:  # Len(mask) > 0
            spectra = _np.squeeze(self.hsi.spectrafull[mask == 1])

            if mask_hits > 1:
                spectrum = _np.mean(spectra, axis=0)
            else:
                spectrum = spectra

            spectrum = spectrum.astype(self.hsi.spectrafull.dtype)
            if sender == 'actionNRB_from_ROI':
                self.nrb.nrb_spectrum = spectrum
                self.ui.actionKramersKronig.setEnabled(True)
                self.ui.actionKKSpeedTest.setEnabled(True)
                self.ui.actionNRBSpectrum.setEnabled(True)
            elif sender == 'actionAppend_NRB_from_ROI':
                if self.nrb.nrb_spectrum.size == 0:
                    self.nrb.nrb_spectrum = spectrum
                else:
                    self.nrb.nrb_spectrum = (self.nrb.nrb_spectrum + spectrum)/2
                self.ui.actionKramersKronig.setEnabled(True)
                self.ui.actionNRBSpectrum.setEnabled(True)
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

        Action
        ------
            Left mouse-click : Select vertex point
            Right mouse-click : Close polygon
        """
        # Updated by _roiClick
        self.x_loc_list = []
        self.y_loc_list = []


        self.cid = self.ui.ui_BWImg.mpl.canvas.mpl_connect('button_press_event', lambda event: self._roiClick(event, self._roiSpectrumPlot))

        self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.CrossCursor))
        self.setCursor(_QCursor(_QtCore.Qt.CrossCursor))

    def _pointClick(self, event, pass_fcn):
        """
        Capture single mouse click location in MPL window.

        After this function completes, it sends the data (x_pt, y_pt) on to \
        the pass_fcn function.
        """
        if event.inaxes == self.ui.ui_BWImg.mpl.ax:
                #self.tempverts += [[event.xdata, event.ydata]]
            x_loc = event.xdata
            y_loc = event.ydata

            # Send on to a function that will use the collected data
            pass_fcn((x_loc, y_loc))

            self.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.ui.ui_BWImg.mpl.canvas.mpl_disconnect(self.cid)
        else:
            print('Clicked out-of-bounds')

    def _pointSpectrumPlot(self, locs):
        """
        Add a plot (in plotter) of a point spectrum
        """
        try:
            x_loc, y_loc = locs
            x_pix = find_nearest(self.hsi.nvec, x_loc)[1]
            y_pix = find_nearest(self.hsi.mvec, y_loc)[1]
            self.selectiondata.append_selection([x_pix],[y_pix],[x_loc],[y_loc])
            self.changeSlider()

            spectrum = _np.squeeze(self.hsi.spectra[y_pix,x_pix,:])
            plot_num = self.plotter._data.num_plots
            label = 'Point ' + str(plot_num)

            self.plotter.append_spectrum(freq=self.hsi.freqvec,
                             spectrum=spectrum,
                             label=label,
                             frequnits=self.hsi.frequnits,
                             spectrumunits=self.hsi.intensityunits)

            self.plotter.show()
            self.plotter.raise_()
        except:
            print('Error in _pointSpectrumPlot')

    def _roiSpectrumPlot(self, locs):
        """
        Add a plot (in plotter) of the mean spectrum over a region
        """
        x_loc_list, y_loc_list = locs

        x_pix = find_nearest(self.hsi.nvec,x_loc_list)[1]
        y_pix = find_nearest(self.hsi.mvec,y_loc_list)[1]

        self.selectiondata.append_selection(x_pix, y_pix, x_loc_list, y_loc_list)
        #self.ui.ui_BWImg.mpl.canvas.mpl_disconnect(self.cid)

        mask, path = _roimask(self.hsi.nvec, self.hsi.mvec,
                              x_loc_list, y_loc_list)

        #_plt.figure()
        #_plt.imshow(mask,origin='lower')
        #_plt.show()
        #print('Mask size: {}; nvec size: {}; mvec size: {}'.format(mask.shape,
        #      self.hsi.nvec.size, self.hsi.mvec.size))

        mask_hits = _np.sum(mask)
        if mask_hits > 0:  # Len(mask) > 0
            spectra = _np.squeeze(self.hsi.spectra[mask == 1])

            if mask_hits > 1:
                spectrum = _np.mean(spectra, axis=0)
            else:
                spectrum = spectra
            plot_num = self.plotter._data.num_plots
            label = 'ROI ' + str(plot_num)
            self.plotter.append_spectrum(freq=self.hsi.freqvec,
                                         spectrum=spectrum,
                                         label=label,
                                         frequnits=self.hsi.frequnits,
                                         spectrumunits=self.hsi.intensityunits)

            del spectrum
            self.plotter.show()


        del x_pix
        del y_pix

    def _roiClick(self, event, pass_fcn, *args):
        """
        Capture region-of-interest mouse click locations in MPL window.
        """


        if event.button == 1:
            if event.inaxes == self.ui.ui_BWImg.mpl.ax:

                self.x_loc_list.append(event.xdata)
                self.y_loc_list.append(event.ydata)

                getx = self.ui.ui_BWImg.mpl.ax.get_xlim()
                gety = self.ui.ui_BWImg.mpl.ax.get_ylim()

                if len(self.x_loc_list) == 1:
                    self.ui.ui_BWImg.mpl.ax.plot(self.x_loc_list, self.y_loc_list,
                                          markerfacecolor=[.9,.9,0],
                                          markeredgecolor=[.9,.9,0],
                                          marker='+',
                                          markersize=10,
                                          linestyle='None')
                    self.ui.ui_BWImg.mpl.ax.set_xlim(getx)
                    self.ui.ui_BWImg.mpl.ax.set_ylim(gety)
                    self.ui.ui_BWImg.mpl.canvas.draw()
                else:
                    self.ui.ui_BWImg.mpl.ax.plot(self.x_loc_list[-2:], self.y_loc_list[-2:],
                                          linewidth=2,
                                          marker='+',
                                          markersize=10,
                                          color=[.9,.9,0],
                                          markerfacecolor=[.9,.9,0],
                                          markeredgecolor=[.9,.9,0])
                    self.ui.ui_BWImg.mpl.ax.set_xlim(getx)
                    self.ui.ui_BWImg.mpl.ax.set_ylim(gety)

                    self.ui.ui_BWImg.mpl.canvas.draw()
        else:
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
            self.ui.ui_BWImg.mpl.canvas.setCursor(_QCursor(_QtCore.Qt.ArrowCursor))
            self.ui.ui_BWImg.mpl.canvas.mpl_disconnect(self.cid)
            self.changeSlider()


    def colorChange(self, num):
        """
        Changes color of point or ROI overlay. May be triggered by alterations \
        made in plotter subui
        """
        self.selectiondata.pointdata_list[num].style.color = \
            self.plotter._data.spectra_list[num].style.color
        self.changeSlider()


    def deleteSelection(self, num):
        """
        Removes point or ROI overlay. May be triggered by deletion of \
        selection from plotter subui
        """
        self.selectiondata.pointdata_list.pop(num)
        self.changeSlider()


    def freqWindow(self):
        """
        Limit the frequency window displayed and analyzed
        """
        text, ok = _QInputDialog.getText(None, 'Frequency Window', 'Range Tuple (cm-1): ', text='(500, 4000)')
        if ok:
            text_str_list = text.strip('(').strip(')').strip().split(',')
            freqwin = [float(q) for q in text_str_list]
            freqwin.sort()
            self.hsi.freqrange = freqwin
            self.ui.freqSlider.setMinimum(0)
            self.ui.freqSlider.setMaximum(self.hsi.freqlen-1)
            self.changeSlider()


    def lineEditFreqChanged(self):
        """
        Frequency manually entered in frequency-slider-display
        """

        try:
            freq_in = float(self.ui.lineEditFreq.text())
            pos = self.hsi._get_index_of_freq(freq_in, use_full=False)

            self.ui.freqSlider.setSliderPosition(pos)
            self.changeSlider()
        except:
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
        zc = _ZeroColumn(first_or_last=0)
        zc.transform(self.hsi.data)

    def zeroFirstRow(self):
        """
        Zero first non-all-zero row. (Rather than crop)

        """
        zr = _ZeroRow(first_or_last=0)
        zr.transform(self.hsi.data)

    def zeroLastColumn(self):
        """
        Zero first non-all-zero column. (Rather than crop)

        """
        zc = _ZeroColumn(first_or_last=-1)
        zc.transform(self.hsi.data)

    def zeroLastRow(self):
        """
        Zero first non-all-zero row. (Rather than crop)

        """
        zr = _ZeroRow(first_or_last=-1)
        zr.transform(self.hsi.data)

    def opChange(self):
        """
        Math operation performed on single-color images changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.ui.RGB[rgbnum].math.ui.comboBoxOperations.currentText()
            self.ui.RGB[rgbnum].data.operation = currentop
        except:
            pass

    def condOpChange(self):
        """
        Conditional math operation performed on single-color images changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.ui.RGB[rgbnum].math.ui.comboBoxCondOps.currentText()
            self.ui.RGB[rgbnum].data.condoperation = currentop
        except:
            pass

    def condInEqualityChange(self):
        """
        Conditional inequality changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentop = self.ui.RGB[rgbnum].math.ui.comboBoxCondInEquality.currentText()
            self.ui.RGB[rgbnum].data.inequality = currentop
        except:
            pass

    def spinBoxInEqualityChange(self):
        """
        Conditional inequality value changed.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            self.ui.RGB[rgbnum].data.inequalityval = \
                self.ui.RGB[rgbnum].math.ui.spinBoxInEquality.value()
        except:
            pass

    def testKK(self):
        """
        KK Speed test
        """

        if len(self.hsi.pixrange) == 0:
            nrb = self.nrb.nrb_spectrum
        else:
            ndim_nrb = _np.squeeze(self.nrb.nrb_spectrum).ndim
            if  ndim_nrb == 1:
                nrb = self.nrb.nrb_spectrum[self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]
            elif ndim_nrb == 2:
                nrb = self.nrb.nrb_spectrum[:,self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]
            else:
                nrb = self.nrb.nrb_spectrum[:,:,self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]

        rand_spectra = self.hsi._get_rand_spectra(5,pt_sz=3,quads=True)

        cars_amp_offset, nrb_amp_offset, phase_offset, norm_to_nrb, pad_factor= \
            DialogKKOptions.dialogKKOptions(data=[self.hsi.freqvec, nrb, rand_spectra])

        if cars_amp_offset is not None:
            try:
                est_rate, est_tot = _test_alter_kk(self.hsi, self.nrb,
                                                   cars_amp_offset=cars_amp_offset,
                                                   nrb_amp_offset=nrb_amp_offset,
                                                   phase_offset=phase_offset,
                                                   norm_to_nrb=norm_to_nrb,
                                                   pad_factor=pad_factor,
                                                   num_rows = 10)
                time_str = 'Est. Total time: {:.3f} s ({:.6f} s/spectrum)'.format(est_tot, est_rate)
                msg = _QMessageBox(parent=None)
                msg.setText(time_str)
                msg.setWindowTitle('Estimated Speed of Kramers-Kronig')
                msg.exec()
            except:
                print('Something went wrong. Try again')

    def doKK(self):
        """
        Pop-up Kramers-Kronig parameter entry dialog and perform
        the Kramers-Kronig phase retrieval algorithm.
        """

        rand_spectra = self.hsi.get_rand_spectra(5,pt_sz=3,quads=True)
        nrb = self.nrb.mean()

#        if len(self.hsi.pixrange) == 0:
#            nrb = self.nrb.nrb_spectrum
#        else:
#            ndim_nrb = _np.squeeze(self.nrb.nrb_spectrum).ndim
#            if  ndim_nrb == 1:
#                nrb = self.nrb.nrb_spectrum[self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]
#            elif ndim_nrb == 2:
#                nrb = self.nrb.nrb_spectrum[:,self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]
#            else:
#                nrb = self.nrb.nrb_spectrum[:,:,self.hsi.pixrange[0]:self.hsi.pixrange[1]+1]

        cars_amp_offset, nrb_amp_offset, phase_offset, norm_to_nrb, pad_factor= \
            DialogKKOptions.dialogKKOptions(data=[self.hsi.freq.data, nrb, rand_spectra])

        if cars_amp_offset is not None:
            kk = KramersKronig(cars_amp_offset=cars_amp_offset,
                      nrb_amp_offset=nrb_amp_offset,
                      phase_offset=phase_offset, norm_to_nrb=norm_to_nrb,
                      pad_factor=pad_factor,
                      rng=self.hsi.freq.op_range_pix)

            start = _timeit.default_timer()
            self.hsi.data = kk.calculate(self.hsi.data, self.nrb.data)
            stop = _timeit.default_timer()

            num_spectra = int(self.hsi.size/self.hsi.freq.size)
            print('KK Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start, (stop-start)/num_spectra))

            start = _timeit.default_timer()

            self.bcpre.add_step(['KK','CARSAmp',cars_amp_offset,'NRBAmp',nrb_amp_offset,'Phase',phase_offset,'Norm',norm_to_nrb])
            try:
                self.hsi.backup_pickle(self.bcpre.id_list[-1])
            except:
                print('Error in pickle backup (Undo functionality)')
            else:
                self.bcpre.backed_up()
            stop = _timeit.default_timer()
            print('Save time: {:.6f} sec'.format(stop-start))


#        self.changeSlider()

    def deNoise(self):
        """
        DeNoise Plugin Caller
        """

        selected_denoise_cls = DialogDenoisePlugins.dialogDenoisePlugins()
        if selected_denoise_cls is not None:
            bcpre_descript = selected_denoise_cls.denoiseHSData(self.hsi)
            if bcpre_descript is not None:
                self.bcpre.add_step(bcpre_descript)
                try:
                    self.hsi.backup_pickle(self.bcpre.id_list[-1])
                except:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()
        self.changeSlider()

    def errorCorrect(self):
        """
        Error Correction plugin caller
        """
        selected_err_correct_cls = DialogErrCorrPlugins.dialogErrCorrPlugins()
#        print(selected_err_correct_cls)
        if selected_err_correct_cls is not None:
             bcpre_descript = selected_err_correct_cls.errorCorrectHSData(self.hsi)
             if bcpre_descript is not None:
                 self.bcpre.add_step(bcpre_descript)
                 try:
                     self.hsi.backup_pickle(self.bcpre.id_list[-1])
                 except:
                    print('Error in pickle backup (Undo functionality)')
                 else:
                    self.bcpre.backed_up()
        self.changeSlider()

    def doUndo(self):
        """
        Undo last operation back to last backup point
        """
        self.bcpre.pop_to_last()
        self.hsi = self.hsi.load_pickle(self.bcpre.id_list[-1])
        del_flag = 0

        for count in self.bcpre.cut_list:
            try:
                _os.remove(count + '.pickle')
            except:
                print('Error in deleting old pickle files')
            else:
                del_flag += 1
        if del_flag == len(self.bcpre.cut_list):
            del self.bcpre.cut_list
        else:
            print('Did not delete pickle file cut list... Something went wrong')

        self.ui.freqSlider.setMinimum(0)
        self.ui.freqSlider.setMaximum(self.hsi.freqlen-1)

        self.changeSlider()


    def subDark(self):
        """
        Subtract loaded dark spectrum from HSI data.
        """

        nrbloaded = self.nrb.data is not None
        darkloaded = self.dark.data is not None

        subdark, subdarkimg, subdarknrb, subresidual, freq = \
            DialogDarkOptions.dialogDarkOptions(darkloaded=darkloaded,
                                                nrbloaded=nrbloaded)

        if (subdark is None and subresidual is None):
            pass
        else:
            if subdark:
#                print('Sub Dark')
                if subdarkimg:
                    sub_dark = SubtractDark(self.dark.data)
                    sub_dark.transform(self.hsi.data)
#                    self.dark.alter_dark_sub(self.hsi)
                    self.bcpre.add_step(['SubDark'])
                    try:
                        self.hsi.backup_pickle(self.bcpre.id_list[-1])
                    except:
                        print('Error in pickle backup (Undo functionality)')
                    else:
                        self.bcpre.backed_up()

                if subdarknrb:
                    sub_dark.transform(self.nrb.data)
#                    self.dark.nrb_dark_sub(self.nrb)

            if subresidual:
                rng = self.hsi.freq.get_index_of_closest_freq(freq)
                sub_residual = SubtractMeanOverRange(rng)
                sub_residual.transform(self.hsi.data)

                self.bcpre.add_step(['SubResidual', 'RangeStart', freq[0],
                                     'RangeEnd', freq[1]])
                try:
                    self.hsi.backup_pickle(self.bcpre.id_list[-1])
                except:
                    print('Error in pickle backup (Undo functionality)')
                else:
                    self.bcpre.backed_up()

                if nrbloaded:
                    sub_residual.transform(self.nrb.data)

#            # Refresh BW image
#            self.changeSlider()

    def doMath(self):
        """
        Perform selected math operation on single-color imagery.
        """
        rgbnum = self.ui.tabColors.currentIndex()

        # Check conditional frequencies are set
        operation_index = self.ui.RGB[rgbnum].math.ui.comboBoxCondOps.currentIndex()
        operation_text = self.ui.RGB[rgbnum].math.ui.comboBoxCondOps.currentText()

        if operation_index == 0:
            num_freq_needed = 0
        else:
            num_freq_needed = widgetColorMath.OPERATION_FREQ_COUNT[operation_index-1]

        cond_set = False

        if (num_freq_needed == 1 and
            self.ui.RGB[rgbnum].data.condfreq1 is not None):
            cond_set = True
        elif (num_freq_needed == 2 and
            self.ui.RGB[rgbnum].data.condfreq1 is not None and
            self.ui.RGB[rgbnum].data.condfreq2 is not None):
            cond_set = True
        elif (num_freq_needed == 3 and
            self.ui.RGB[rgbnum].data.condfreq1 is not None and
            self.ui.RGB[rgbnum].data.condfreq2 is not None and
            self.ui.RGB[rgbnum].data.condfreq3 is not None):
            cond_set = True
        else:
            cond_set = False

        if cond_set is False:
            self.ui.RGB[rgbnum].math.ui.comboBoxCondOps.setCurrentIndex(0)
            Mask = 1
        else:
            if (operation_text == '' or operation_text == ' '):  # Return just a plane
                Mask = retr_freq_plane(self.hsi, self.ui.RGB[rgbnum].data.condfreq1)

            elif (operation_text == '+'):  # Addition
                Mask = retr_freq_plane_add(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                           self.ui.RGB[rgbnum].data.condfreq2)

            elif (operation_text == '-'):  # Subtraction
                Mask = retr_freq_plane_sub(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                           self.ui.RGB[rgbnum].data.condfreq2)

            elif (operation_text == '*'):  # Multiplication
                Mask = retr_freq_plane_multi(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                                     self.ui.RGB[rgbnum].data.condfreq2)

            elif (operation_text == '/'):  # Division
                Mask = retr_freq_plane_div(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                                     self.ui.RGB[rgbnum].data.condfreq2)

            elif (operation_text == 'SUM'):  # Summation over range
                Mask = retr_freq_plane_sum_span(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                                     self.ui.RGB[rgbnum].data.condfreq2)

            elif (operation_text == 'Peak b/w troughs'):  # Peak between troughs
                Mask = retr_freq_plane_peak_bw_troughs(self.hsi, self.ui.RGB[rgbnum].data.condfreq1,
                                                     self.ui.RGB[rgbnum].data.condfreq2,
                                                     self.ui.RGB[rgbnum].data.condfreq3)
            else:
                pass

        if cond_set is True:
            inequality_text = self.ui.RGB[rgbnum].math.ui.comboBoxCondInEquality.currentText()
            inequality_val = self.ui.RGB[rgbnum].math.ui.spinBoxInEquality.value()
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
        operation_index = self.ui.RGB[rgbnum].math.ui.comboBoxOperations.currentIndex()
        operation_text = self.ui.RGB[rgbnum].math.ui.comboBoxOperations.currentText()

        num_freq_needed = widgetColorMath.OPERATION_FREQ_COUNT[operation_index]

        freq_set = False

        if (num_freq_needed == 1 and
            self.ui.RGB[rgbnum].data.opfreq1 is not None):
            freq_set = True
        elif (num_freq_needed == 2 and
            self.ui.RGB[rgbnum].data.opfreq1 is not None and
            self.ui.RGB[rgbnum].data.opfreq2 is not None):
            freq_set = True
        elif (num_freq_needed == 3 and
            self.ui.RGB[rgbnum].data.opfreq1 is not None and
            self.ui.RGB[rgbnum].data.opfreq2 is not None and
            self.ui.RGB[rgbnum].data.opfreq3 is not None):
            freq_set = True
        else:
            freq_set = False

        if freq_set == True:
            if (operation_text == '' or operation_text == ' '):  # Return just a plane
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane(self.hsi, self.ui.RGB[rgbnum].data.opfreq1)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == '+'):  # Addition
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_add(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == '-'):  # Subtraction
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_sub(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == '*'):  # Multiplication
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_multi(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == '/'):  # Division
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_div(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == 'SUM'):  # Division
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_sum_span(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            elif (operation_text == 'Peak b/w troughs'):  # Division
                self.ui.RGB[rgbnum].data.grayscaleimage =\
                    Mask*retr_freq_plane_peak_bw_troughs(self.hsi, self.ui.RGB[rgbnum].data.opfreq1,
                                                     self.ui.RGB[rgbnum].data.opfreq2,
                                                     self.ui.RGB[rgbnum].data.opfreq3)
                self.ui.RGB[rgbnum].changeColor()
                #self.updateImgColorMinMax()
            else:
                pass
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

            self.ui.RGB[rgbnum].data.opfreq1 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonOpFreq1.setText(str(round(currentfreq,1)))
            self.ui.RGB[rgbnum].data.grayscaleimage = self.ui.ui_BWImg.data.grayscaleimage
            self.ui.RGB[rgbnum].changeColor()

            self.ui.RGB[rgbnum].mpl.canvas.draw()

        except:
            print('Error')
        self.doComposite()


    def setOpFreq2(self):
        """
        Set color math frequency #2 (e.g., freq #1 + freq #2)
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.ui.RGB[rgbnum].data.opfreq2 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonOpFreq2.setText(str(round(currentfreq,1)))
        except:
            pass

    def setOpFreq3(self):
        """
        Set color math frequency #3 (e.g., Amplitude at freq #1 - interpolation [freq #2, freq #3])
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.ui.RGB[rgbnum].data.opfreq3 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonOpFreq3.setText(str(round(currentfreq,1)))

        except:
            pass

    def setCondFreq1(self):
        """
        Set color math conditional frequency #1
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.ui.RGB[rgbnum].data.condfreq1 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonCondFreq1.setText(str(round(currentfreq,1)))

        except:
            print('Error')

    def setCondFreq2(self):
        """
        Set color math conditional frequency #2
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.ui.RGB[rgbnum].data.condfreq2 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonCondFreq2.setText(str(round(currentfreq,1)))

        except:
            print('Error')

    def setCondFreq3(self):
        """
        Set color math conditional frequency #1
        """
        rgbnum = self.ui.tabColors.currentIndex()

        try:
            currentfreq = float(self.ui.lineEditFreq.text())

            self.ui.RGB[rgbnum].data.condfreq3 = currentfreq
            self.ui.RGB[rgbnum].math.ui.pushButtonCondFreq3.setText(str(round(currentfreq,1)))

        except:
            print('Error')

    def spectrumColorImg(self):
        """
        Generate plot of mean or weighted-mean spectrum from color-image
        """
        fig = _plt.figure(figsize=(10,6))
#        plot_font = {'fontname':'Arial', 'size':'14'}
        ax = fig.add_subplot(111)

        win_num = self.ui.tabColors.currentIndex()
        win_title = self.ui.tabColors.tabText(win_num)
        label = 'Weighted Spect.: ' + win_title
        mask = self.ui.RGB[self.ui.tabColors.currentIndex()].data.image
        mask = mask.sum(axis=-1)
        mask -= mask.min()
        mask /= mask.max()
        y_loc, x_loc = _np.where(mask > 0)
#        print('Mask shape: {}'.format(mask.shape))
#        print('Mask[y_loc, x_loc] shape: {}'.format(mask[y_loc, x_loc].shape))
        # Weighted mean
        spectrum = mask[y_loc, x_loc, None]*self.hsi.spectra[y_loc,x_loc,:]
#        print(spectrum.shape)
        spectrum = spectrum.sum(axis=0)
#        print(spectrum.shape)
        #spectrum /= mask[y_loc, x_loc].sum()

        # Unweighted mean
#        spectrum = self.hsi.spectra[y_loc,x_loc,:].sum(axis=1).sum(axis=0)

        spectrum /= y_loc.size

        self.selectiondata.append_selection([None],[None],[None],[None])
        self.plotter.append_spectrum(freq=self.hsi.freqvec,
                                         spectrum=spectrum,
                                         label=label,
                                         frequnits=self.hsi.frequnits,
                                         spectrumunits=self.hsi.intensityunits)
        self.plotter.show()

        #_plt.plot(spectrum)
        #fig.show()

#        fig2 = _plt.figure()
#        _plt.imshow(mask)
#        _plt.colorbar()
#        fig2.show()

    def createImgBW(self, img):
        """
        Generate the single-frequency grayscale image
        """
        xunits = self.ui.ui_BWImg.data.xunits
        yunits = self.ui.ui_BWImg.data.yunits
        extent = self.ui.ui_BWImg.data.winextent

        self.ui.ui_BWImg.createImg(img = img, xunits = xunits,
                              yunits = yunits,
                              extent = extent, showcbar = True,
                              axison = True, cmap = _mpl.cm.gray)

        if self.ui.ui_BWImg.ui.checkBoxFixed.checkState()==0:
            self.ui.ui_BWImg.ui.lineEditMax.setText(str(round(self.ui.ui_BWImg.data.maxer,4)))
            self.ui.ui_BWImg.ui.lineEditMin.setText(str(round(self.ui.ui_BWImg.data.minner,4)))

    def changeSlider(self):
        """
        Respond to change in frequency slider
        """
        pos = self.ui.freqSlider.sliderPosition()
        assert isinstance(pos, int), 'Slider position need be an integer'

        self.ui.lineEditPix.setText(str(pos))

        try:

            self.ui.lineEditFreq.setText(str(round(self.hsi.freqvec[pos],2)))
            # Set BW Class Data
            self.ui.ui_BWImg.data.grayscaleimage = retr_freq_plane(self.hsi, pos)
            self.ui.ui_BWImg.data.set_x(self.hsi.nvec, 'X ($\mu m$)')
            self.ui.ui_BWImg.data.set_y(self.hsi.mvec, 'Y ($\mu m$)')

            if self.ui.ui_BWImg.ui.checkBoxFixed.checkState() == 0:
                self.ui.ui_BWImg.data.setmax = None
                self.ui.ui_BWImg.data.setmin = None

            self.createImgBW(self.ui.ui_BWImg.data.image)

            getx = self.ui.ui_BWImg.mpl.ax.get_xlim()
            gety = self.ui.ui_BWImg.mpl.ax.get_ylim()

            self.ui.ui_BWImg.mpl.ax.hold(True)
            for pts in self.selectiondata.pointdata_list:
                #print('Pts.X:{}'.format(pts.x))
                if len(pts.x) == 1:
                    #print('X2: {}, X2-Pix: {}, Y2: {}, Y2-Pix:{}'.format(pts.x, pts.xpix, pts.y, pts.ypix))
                    self.ui.ui_BWImg.mpl.ax.plot(pts.x, pts.y,
                                          marker='+',
                                          markersize=10,
                                          markerfacecolor=pts.style.color,
                                          markeredgecolor=pts.style.color,
                                          linestyle='None')
                else:
                    self.ui.ui_BWImg.mpl.ax.plot(pts.x, pts.y,
                                          marker='None',
                                          markersize=10,
                                          color=pts.style.color,
                                          markerfacecolor=pts.style.color,
                                          markeredgecolor=pts.style.color,
                                          linestyle=pts.style.linestyle,
                                          linewidth=2)

                self.ui.ui_BWImg.mpl.ax.set_xlim(getx)
                self.ui.ui_BWImg.mpl.ax.set_ylim(gety)

            self.ui.ui_BWImg.mpl.canvas.draw()

            if self.bcpre.backed_flag.count(True) > 1:
                self.ui.actionUndo.setEnabled(True)
            else:
                self.ui.actionUndo.setEnabled(False)

        except:
            print('Error in changeSlider')

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
        self.ui.CompositeColor.initData(self.ui.RGB)
        self.ui.CompositeColor.data.set_x(self.hsi.nvec, 'X ($\mu m$)')
        self.ui.CompositeColor.data.set_y(self.hsi.mvec, 'Y ($\mu m$)')


        self.ui.CompositeColor.createImg(img = self.ui.CompositeColor.data.image,
                                         xunits = self.ui.CompositeColor.data.xunits,
                                         yunits = self.ui.CompositeColor.data.yunits,
                                         showcbar = False, axison = True)
        self.ui.CompositeColor.mpl.canvas.draw()

        self.ui.CompositeColor2.initData(self.ui.RGB)
        self.ui.CompositeColor2.data.set_x(self.hsi.nvec, 'X ($\mu m$)')
        self.ui.CompositeColor2.data.set_y(self.hsi.mvec, 'Y ($\mu m$)')
        self.ui.CompositeColor2.createImg(img = self.ui.CompositeColor2.data.image,
                                         xunits = self.ui.CompositeColor2.data.xunits,
                                         yunits = self.ui.CompositeColor2.data.yunits,
                                         showcbar = False, axison = True)
        self.ui.CompositeColor2.mpl.canvas.draw()
        #self.ui.CompositeColor.mpl.canvas.draw()

if __name__ == '__main__':

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    win = CRIkitUI_process() ### EDIT ###

    # Insert other stuff to do


    # Final stuff
    win.showMaximized()
    _sys.exit(app.exec_())