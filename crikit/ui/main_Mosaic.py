"""
MainWindow program that allows construction of stitched images from
multiple dataset
"""

import sys as _sys
import os as _os

import numpy as _np

from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QMainWindow as _QMainWindow,
                             QWidget as _QWidget)
import PyQt5.QtCore as _QtCore

from crikit.ui.qt_Mosaic import Ui_MainWindow

from crikit.data.frequency import calib_pix_wl, calib_pix_wn
from crikit.data.mosaic import Mosaic

from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

import lazy5
from lazy5.utils import FidOrFile, fullpath
from lazy5.ui.QtHdfLoad import HdfLoad


class MainWindowMosaic(_QMainWindow):
    """

    """

    frequency_calib = {'Slope':-0.165955456, 'Intercept':832.5510120093941,
                       'Probe': 771.461, 'Calib_WL': 700.0, 'Center_WL': 700.0}

    def __init__(self, parent=None):
        super(MainWindowMosaic, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.spinBoxIntercept.setValue(self.frequency_calib['Intercept'])
        self.ui.spinBoxSlope.setValue(self.frequency_calib['Slope'])
        self.ui.spinBoxProbe.setValue(self.frequency_calib['Probe'])
        self.ui.spinBoxCalibWL.setValue(self.frequency_calib['Calib_WL'])
        self.ui.spinBoxCenterWL.setValue(self.frequency_calib['Center_WL'])

        # Internal data
        self.init_internals()

        self.mpl = _MplCanvas(parent=self)
        self.ui.verticalLayoutMPL.insertWidget(0, self.mpl, _QtCore.Qt.AlignCenter)
        self.ui.verticalLayoutMPL.insertWidget(0,self.mpl.toolbar, _QtCore.Qt.AlignHCenter)

        # SIGNALS AND SLOTS
        self.ui.actionAddFromHDF.triggered.connect(self.addDataset)
        self.ui.pushButtonAddDataset.pressed.connect(self.addDataset)
        self.ui.spinBoxMRows.editingFinished.connect(self.updateMosaicImage)
        self.ui.spinBoxNCols.editingFinished.connect(self.updateMosaicImage)

        self.ui.sliderFreq.valueChanged.connect(self.updateSlider)
        self.ui.sliderFreq.sliderReleased.connect(self.updateMosaicImage)

        self.ui.lineEditPix.editingFinished.connect(self.lineEditPixChange)

        self.ui.comboBoxRowCol.currentIndexChanged.connect(self.updateParams)
        self.ui.checkBoxFlipH.stateChanged.connect(self.updateParams)
        self.ui.checkBoxFlipV.stateChanged.connect(self.updateParams)
        self.ui.checkBoxTranspose.stateChanged.connect(self.updateParams)
        self.ui.spinBoxStartRow.editingFinished.connect(self.updateParams)
        self.ui.spinBoxStartCol.editingFinished.connect(self.updateParams)
        self.ui.spinBoxEndRow.editingFinished.connect(self.updateParams)
        self.ui.spinBoxEndCol.editingFinished.connect(self.updateParams)

        self.ui.spinBoxSlope.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxIntercept.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxProbe.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxCalibWL.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxCenterWL.editingFinished.connect(self.updateFrequency)

        # Close event
        self.ui.closeEvent = self.closeEvent

    def init_internals(self):
        """ Initialize internal variables """
        self.data = Mosaic()
        self.data_list = []  # List of list [pth, fname, dsetname]
        self.h5dlist = []  # List of dataset pointers

        self.pix = None
        self.wl = None
        self.freq = None

        self.last_path = None
        self.last_fname = None
        self.last_dsetname = None

    def lineEditPixChange(self):
        """
        Frequency manually entered in frequency-slider-display
        """

        freq_in = int(float(self.ui.lineEditPix.text()))

        max_freq = self.ui.sliderFreq.maximum()
        min_freq = self.ui.sliderFreq.minimum()

        if freq_in > max_freq:
            freq_in = max_freq
        elif freq_in < min_freq:
            freq_in = min_freq
        else:
            pass

        self.ui.sliderFreq.setValue(freq_in)

    def updateSlider(self):
        idx = self.ui.sliderFreq.value()
        self.ui.lineEditPix.setText(str(idx))

        if self.freq is not None:
            self.ui.lineEditFreq.setText(str(self.freq[idx]))

        # In case incremented by the arrow buttons
        if not self.ui.sliderFreq.isSliderDown():
            self.updateMosaicImage()

    def addDataset(self):
        if (self.last_path is None) | (self.last_fname is None) | (self.last_dsetname is None):
            first_dset = True
            to_open = HdfLoad.getFileDataSets(parent=self)
        else:
            first_dset = False
            to_open = HdfLoad.getFileDataSets(pth=_os.path.join(self.last_path, self.last_fname),
                                              parent=self)

        if to_open is not None:
            self.last_path, self.last_fname, self.last_dsetname = to_open
            self.last_dsetname = self.last_dsetname[-1]

            to_import = [[self.last_path, self.last_fname, q] for q in to_open[-1]]
            for ti in to_import:
                fof = FidOrFile(fullpath(pth=ti[0], filename=ti[1]))
                self.h5dlist.append(fof.fid[ti[-1]])
                self.data.append(fof.fid[ti[-1]])

            if first_dset:
                if self.data.is3d:
                    flen = self.data.unitshape_orig[-1]
                    self.ui.sliderFreq.setMinimum(0)
                    self.ui.sliderFreq.setMaximum(flen-1)
                    self.ui.sliderFreq.setValue(0)

                    self.pix = _np.arange(flen)

                    self.updateFrequency()

            self.data_list.extend(to_import)
            self.updateDatasets()

    def updateFrequency(self):

        if self.pix is not None:
            probe = self.ui.spinBoxProbe.value() * 1e-9
            intercept = self.ui.spinBoxIntercept.value() * 1e-9
            slope = self.ui.spinBoxSlope.value() * 1e-9
            ctr_wl = self.ui.spinBoxCenterWL.value() * 1e-9
            calib_wl = self.ui.spinBoxCalibWL.value() * 1e-9

            self.frequency_calib['Probe'] = probe
            self.frequency_calib['Intercept'] = intercept
            self.frequency_calib['Slope'] = slope
            self.frequency_calib['Center_WL'] = ctr_wl
            self.frequency_calib['Calib_WL'] = calib_wl

            self.wl = slope*self.pix + intercept + (ctr_wl - calib_wl)

            if probe != 0.0:
                self.freq = 0.01 /  self.wl - 0.01 / probe
            else:
                self.freq = 0.01 /  self.wl

            self.updateSlider()

    def updateDatasets(self):
        """ Update the listWidget of datasets """
        self.ui.listWidgetDatasets.clear()
        for q in self.data_list:
            print(q)
            self.ui.listWidgetDatasets.addItem(q[-1])

        self.updateRowsCols(optimize=False)
        self.updateMosaicImage()

    def updateMosaicImage(self):
        if self.data._data:
            self.updateRowsCols()
            mrows = self.ui.spinBoxMRows.value()
            ncols = self.ui.spinBoxNCols.value()

            idx = self.ui.sliderFreq.value()
            self.ui.lineEditPix.setText(str(idx))
            if self.freq is not None:
                self.ui.lineEditFreq.setText(str(self.freq[idx]))

            self.mpl.ax.clear()
            self.mpl.ax.imshow(self.data.mosaic2d(shape=(mrows, ncols), idx=idx))
            self.mpl.draw()

    def updateRowsCols(self, optimize=False):
        """ Update the values of MRows and NCols """
        mrows = self.ui.spinBoxMRows.value()
        ncols = self.ui.spinBoxNCols.value()
        n_dsets = len(self.data_list)

        if (mrows * ncols) < n_dsets:
            if optimize:
                pass
            else:
                mrows = int(_np.ceil(n_dsets / ncols))

            self.ui.spinBoxMRows.setValue(mrows)
            self.ui.spinBoxNCols.setValue(ncols)

    def closeEvent(self, event):
        print('Closing')
        self._data = None
        app = _QApplication.instance()
        app.closeAllWindows()
        app.quit()

        if self.h5dlist:
            for q in self.h5dlist:
                print('Closing: {}'.format(q))
                q.file.close()

    def updateParams(self):

        self.data.parameters['StartC'] = self.ui.spinBoxStartCol.value()
        self.data.parameters['StartR'] = self.ui.spinBoxStartRow.value()
        self.data.parameters['EndC'] = -1*self.ui.spinBoxEndCol.value()
        self.data.parameters['EndR'] = -1*self.ui.spinBoxEndRow.value()
        self.data.parameters['Transpose'] = self.ui.checkBoxTranspose.isChecked()
        self.data.parameters['FlipVertical'] = self.ui.checkBoxFlipV.isChecked()
        self.data.parameters['FlipHorizontally'] = self.ui.checkBoxFlipH.isChecked()

        idx = self.ui.comboBoxRowCol.currentIndex()
        if idx == 0:
            self.data.parameters['Order'] = 'R'
        else:
            self.data.parameters['Order'] = 'C'

        if self.data._data:
            self.updateMosaicImage()


if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    app.setQuitOnLastWindowClosed(True)

    win = MainWindowMosaic(parent=None)
    win.show()
    app.exec_()



    print(win)

    _sys.exit()