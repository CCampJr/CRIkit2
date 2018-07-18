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
    def __init__(self, parent=None):
        super(MainWindowMosaic, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Internal data
        self.init_internals()

        self.mpl = _MplCanvas(parent=self)
        self.ui.verticalLayoutMPL.insertWidget(0, self.mpl, _QtCore.Qt.AlignCenter)
        self.ui.verticalLayoutMPL.insertWidget(0,self.mpl.toolbar, _QtCore.Qt.AlignHCenter)

        # SIGNALS AND SLOTS
        self.ui.actionAddFromHDF.triggered.connect(self.addDataset)
        self.ui.pushButtonAddDataset.pressed.connect(self.addDataset)
        self.ui.spinBoxMRows.valueChanged.connect(self.updateMosaicImage)
        self.ui.spinBoxNCols.valueChanged.connect(self.updateMosaicImage)

        self.ui.comboBoxRowCol.currentIndexChanged.connect(self.updateParams)
        self.ui.checkBoxFlipH.stateChanged.connect(self.updateParams)
        self.ui.checkBoxFlipV.stateChanged.connect(self.updateParams)
        self.ui.checkBoxTranspose.stateChanged.connect(self.updateParams)
        self.ui.spinBoxStartRow.valueChanged.connect(self.updateParams)
        self.ui.spinBoxStartCol.valueChanged.connect(self.updateParams)
        self.ui.spinBoxEndRow.valueChanged.connect(self.updateParams)
        self.ui.spinBoxEndCol.valueChanged.connect(self.updateParams)

        # Close event
        self.ui.closeEvent = self.closeEvent

    def init_internals(self):
        """ Initialize internal variables """
        self.data = Mosaic()
        self.data_list = []  # List of list [pth, fname, dsetname]
        self.h5dlist = []  # List of dataset pointers

        self.freq = None

        self.last_path = None
        self.last_fname = None
        self.last_dsetname = None

    def addDataset(self):
        if (self.last_path is None) | (self.last_fname is None) | (self.last_dsetname is None):
            to_open = HdfLoad.getFileDataSets(parent=self)
        else:
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

            self.data_list.extend(to_import)
            self.updateDatasets()

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

            # self.mpl.ax.clear()
            self.mpl.ax.imshow(self.data.mosaic2d(shape=(mrows, ncols), idx=100))
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