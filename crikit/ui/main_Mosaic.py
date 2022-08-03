"""
MainWindow program that allows construction of stitched images from
multiple dataset
"""

import sys as _sys
import os as _os
import copy as _copy

from collections import OrderedDict

import h5py
import numpy as _np

from PyQt5 import QtWidgets as _QtWidgets
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QMainWindow as _QMainWindow,
                             QWidget as _QWidget,
                             QListWidget as _QListWidget,
                             QMessageBox as _QMessageBox)

import PyQt5.QtCore as _QtCore
from PyQt5.QtCore import (pyqtSignal as _pyqtSignal)

from crikit.ui.qt_Mosaic import Ui_MainWindow

from crikit.data.frequency import calib_pix_wl, calib_pix_wn
from crikit.data.mosaic import Mosaic
from crikit.ui.dialog_save import DialogSave

from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

import crikit.io.lazy5 as lazy5
from crikit.io.lazy5.utils import FidOrFile, fullpath
from crikit.io.lazy5.ui.QtHdfLoad import HdfLoad


class DnDReorderListWidget(_QListWidget):
    """ List widget with drag-n-drop reordering """

    reordered = _pyqtSignal()

    def __init__(self, parent):
        super(DnDReorderListWidget, self).__init__(parent)

        self.setAcceptDrops(True)
        self.setEditTriggers(_QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setDragEnabled(True)
        self.setDragDropMode(_QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(_QtCore.Qt.MoveAction)
        self.setAlternatingRowColors(False)
        self.setSelectionMode(_QtWidgets.QAbstractItemView.SingleSelection)
        self.setObjectName("listWidgetDatasets")

        item = _QtWidgets.QListWidgetItem()
        self.addItem(item)
        item = _QtWidgets.QListWidgetItem()
        self.addItem(item)

        self.setSortingEnabled(False)
        item = self.item(0)
        item.setText('A')
        item = self.item(1)
        item.setText('B')

    def dropEvent(self, e):
        super().dropEvent(e)
        self.reordered.emit()

class MainWindowMosaic(_QMainWindow):
    """

    """

    frequency_calib = {'Slope':-0.165955456, 'Intercept':832.5510120093941,
                       'Probe': 771.461, 'Calib_WL': 700.0, 'Center_WL': 700.0}

    config = {'allow_duplicates':False}

    def __init__(self, parent=None):
        super(MainWindowMosaic, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupListWidget()

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

        self.ui.actionSaveToHDF5.triggered.connect(self.save)

        self.ui.sliderFreq.valueChanged.connect(self.updateSlider)
        self.ui.sliderFreq.sliderReleased.connect(self.updateMosaicImage)

        self.ui.lineEditPix.editingFinished.connect(self.lineEditPixChange)

        self.ui.spinBoxMRows.editingFinished.connect(self.updateParams)
        self.ui.spinBoxNCols.editingFinished.connect(self.updateParams)
        self.ui.comboBoxRowCol.currentIndexChanged.connect(self.updateParams)
        self.ui.checkBoxFlipH.stateChanged.connect(self.updateParams)
        self.ui.checkBoxFlipV.stateChanged.connect(self.updateParams)
        self.ui.checkBoxTranspose.stateChanged.connect(self.updateParams)
        self.ui.spinBoxStartRow.editingFinished.connect(self.updateParams)
        self.ui.spinBoxStartCol.editingFinished.connect(self.updateParams)
        self.ui.spinBoxEndRow.editingFinished.connect(self.updateParams)
        self.ui.spinBoxEndCol.editingFinished.connect(self.updateParams)

        # ! Currently, cannot save compress in HDF5
        self.ui.checkBoxCompress.setEnabled(False)
        # self.ui.checkBoxCompress.stateChanged.connect(self.updateParams)

        self.ui.spinBoxSlope.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxIntercept.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxProbe.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxCalibWL.editingFinished.connect(self.updateFrequency)
        self.ui.spinBoxCenterWL.editingFinished.connect(self.updateFrequency)

        # self.ui.spinBoxXStepSize.editingFinished.connect(self.updateSpace)
        # self.ui.spinBoxYStepSize.editingFinished.connect(self.updateSpace)

        self.ui.pushButtonMoveUp.pressed.connect(self.promote_demote_list_item)
        self.ui.pushButtonMoveDown.pressed.connect(self.promote_demote_list_item)
        self.ui.pushButtonDeleteDataset.pressed.connect(self.deleteDataset)

        self.ui.listWidgetDatasets.reordered.connect(self.list_reordered)

        # Close event
        self.ui.closeEvent = self.closeEvent
        self.ui.actionExit.triggered.connect(self.closeEvent)

    def setupListWidget(self):

        self.ui.listWidgetDatasets = DnDReorderListWidget(parent=self.ui.frame)
        self.ui.verticalLayout_4.insertWidget(2, self.ui.listWidgetDatasets)

    def deleteDataset(self):
        if self.data._data:
            row = self.ui.listWidgetDatasets.currentRow()

            if row < 0:
                # print('No selection')
                pass
            else:
                # print('Current row: {}'.format(row))

                it = self.ui.listWidgetDatasets.takeItem(row)
                out = self.data_list.pop(row)
                out = self.data._data.pop(row)
                out = self.h5dlist.pop(row)
                out.file.close()

                if self.data.size > 0:
                    self.list_reordered()
                else:
                    self.init_internals()
                    self.mpl.ax.clear()
                    self.mpl.draw()

    def promote_demote_list_item(self):
        if self.data._data:
            sndr = self.sender()
            row = self.ui.listWidgetDatasets.currentRow()
            isup = None

            if sndr == self.ui.pushButtonMoveUp:
                isup = True
            elif sndr == self.ui.pushButtonMoveDown:
                isup = False

            if row < 0:
                # print('No selection')
                pass
            else:
                # print('Current row: {}'.format(row))
                pass
            if isup & (row == 0):
                # print('Can\'t promote first')
                pass
            elif (isup == False) & (row + 1 == self.ui.listWidgetDatasets.count()):
                # print('Can\'t demote last')
                pass
            elif row < 0:
                # print('Can\'t promote/demote no selection')
                pass
            elif isup:
                # print('Promoting')
                it = self.ui.listWidgetDatasets.takeItem(row)
                self.ui.listWidgetDatasets.insertItem(row - 1, it)
                self.list_reordered()
            elif not isup:
                # print('Demoting')
                it = self.ui.listWidgetDatasets.takeItem(row)
                self.ui.listWidgetDatasets.insertItem(row + 1, it)
                self.list_reordered()

    def list_reordered(self):
        if self.data._data:
            if self.data.size >= 1:
                dset_list = []
                for num in range(self.ui.listWidgetDatasets.count()):
                    dset_list.append(self.ui.listWidgetDatasets.item(num).text().split(' : '))

                new_order = []
                for q in self.data_list:
                    new_order.append(dset_list.index(q))

                assert len(new_order) == self.data.size
                assert len(new_order) == _np.unique(new_order).size

                self.data_list = [self.data_list[idx] for idx in new_order]
                self.data._data = [self.data._data[idx] for idx in new_order]
                self.h5dlist = [self.h5dlist[idx] for idx in new_order]
                self.updateMosaicImage()

        else:
            pass

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

        self.imported_calib_vec = None
        self.imported_spatial_vec = None

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
            temp_last_path, temp_last_fname, _ = to_open

            # Since to_open's dsets will be lists, this is an unraveled version
            to_import = [[temp_last_path, temp_last_fname, q] for q in to_open[-1]]
            to_import2 = []  # Duplicates removed if NOT allowing duplicates

            for q in to_import:
                if not self.config['allow_duplicates']:
                    if self.is_duplicate_import([q[0], q[1], q[2]]):
                        msg = _QMessageBox(self)
                        msg.setIcon(_QMessageBox.Critical)
                        str1 = 'Cannot import duplicate image:\n\n'
                        str2 = '{} : {} : {}\n\n'.format(*q)
                        str3 = '\n\nNot importing this dataset'
                        msg.setText(str1 + str2 + str3)
                        msg.setWindowTitle('Duplicate Image Found.')
                        msg.setStandardButtons(_QMessageBox.Ok)
                        msg.setDefaultButton(_QMessageBox.Ok)
                        out = msg.exec()
                    else:
                        to_import2.append(q)

                else:
                    to_import2.append(q)

            for q in to_import2:
                fof = FidOrFile(fullpath(pth=q[0], filename=q[1]))
                if fof.fid[q[-1]].ndim != 3:
                    msg = _QMessageBox(self)
                    msg.setIcon(_QMessageBox.Critical)
                    str1 = 'Dataset is not 3D:\n\n'
                    str2 = '{} : {} : {}'.format(*q)
                    str3 = '\n\nNot importing this dataset'
                    msg.setText(str1 + str2 + str3)
                    msg.setWindowTitle('Cannot Load Non-3D Datasets.')
                    msg.setStandardButtons(_QMessageBox.Ok)
                    msg.setDefaultButton(_QMessageBox.Ok)
                    out = msg.exec()
                    fof.fid.close()
                else:
                    self.h5dlist.append(fof.fid[q[-1]])
                    self.data.append(fof.fid[q[-1]])
                    self.last_path = q[0]
                    self.last_fname = q[1]
                    self.last_dsetname = q[2]
                    self.data_list.append(q)

                    if first_dset:
                        flen = self.data.unitshape_orig[-1]
                        self.ui.sliderFreq.setMinimum(0)
                        self.ui.sliderFreq.setMaximum(flen-1)
                        self.ui.sliderFreq.setValue(0)

                        self.pix = _np.arange(flen)
                        calib_vec = self.check_for_spectral_calib(fof.fid[q[-1]])
                        self.check_for_spatial_calib(fof.fid[q[-1]])

                        self.updateFrequency(calib_vec)
                        first_dset = False

            self.updateDatasets()

    def check_for_spatial_calib(self, dset):
        """ See if dataset has spatial calibration meta data """
        if not isinstance(dset, h5py.Dataset):
            return None
        if not hasattr(dset, 'attrs'):
            return None

        spatial_vec = []  # X, Y
        
        attrs_dict = lazy5.inspect.get_attrs_dset(dset.file, dset.name)
        list_of_keys = list(attrs_dict)

        ct = 0
        temp = []
        to_check = ['Raster.Fast.StepSize', 'Raster.Slow.StepSize']  # X, Y
        for num, tc in enumerate(to_check):
            if list_of_keys.count(tc) > 0:
                ct += 1
                temp.append(attrs_dict[tc])
        if ct == len(to_check):
            print('Has StepSize info (New)')
            spatial_vec = temp
        else:
            ct = 0
            temp = []
            to_check = ['RasterScanParams.FastAxisStepSize', 'RasterScanParams.SlowAxisStepSize']  # X, Y
            for num, tc in enumerate(to_check):
                if list_of_keys.count(tc) > 0:
                    ct += 1
                    temp.append(attrs_dict[tc])
            if ct == len(to_check):
                print('Has StepSize info (Old)')
                spatial_vec = temp
            else:
                ct = 0
                temp = []
                to_check = ['Raster.Fast.Start', 'Raster.Fast.Stop', 'Raster.Fast.Steps', 
                            'Raster.Slow.Start', 'Raster.Slow.Stop', 'Raster.Slow.Steps']
                for num, tc in enumerate(to_check):
                    if list_of_keys.count(tc) > 0:
                        ct += 1
                        temp.append(attrs_dict[tc])
                if ct == len(to_check):
                    print('Has Start-Stop-Steps info (New)')
                    x_stepsize = (temp[1] - temp[0])/(temp[2]-1)
                    y_stepsize = (temp[4] - temp[3])/(temp[5]-1)
                    spatial_vec = [x_stepsize, y_stepsize]
                else:
                    ct = 0
                    temp = []
                    to_check = ['RasterScanParams.FastAxisStart', 'RasterScanParams.FastAxisStop', 
                                'RasterScanParams.FastAxisSteps', 
                                'RasterScanParams.SlowAxisStart', 'RasterScanParams.SlowAxisStop', 
                                'RasterScanParams.SlowAxisSteps']
                    for num, tc in enumerate(to_check):
                        if list_of_keys.count(tc) > 0:
                            ct += 1
                            temp.append(attrs_dict[tc])
                    if ct == len(to_check):
                        print('Has Start-Stop-Steps info (Old)')
                        x_stepsize = (temp[1] - temp[0])/(temp[2]-1)
                        y_stepsize = (temp[4] - temp[3])/(temp[5]-1)
                        spatial_vec = [x_stepsize, y_stepsize]

        if spatial_vec:
            self.imported_spatial_vec = spatial_vec
            self.ui.checkBoxSpaceFromData.setChecked(True)
            self.ui.spinBoxXStepSize.setValue(spatial_vec[0])
            self.ui.spinBoxYStepSize.setValue(spatial_vec[1])

    def check_for_spectral_calib(self, dset):
        """ See if dataset has spectral calibration meta data """
        if not isinstance(dset, h5py.Dataset):
            return None
        if not hasattr(dset, 'attrs'):
            return None

        calib_vec = []
        
        attrs_dict = lazy5.inspect.get_attrs_dset(dset.file, dset.name)
        list_of_keys = list(attrs_dict)

        ct = 0
        temp = []
        to_check = ['Calib.a_vec', 'Calib.ctr_wl', 'Calib.ctr_wl0', 'Calib.n_pix',
                    'Calib.probe']
        for num, tc in enumerate(to_check):
            if list_of_keys.count(tc) > 0:
                ct += 1
                temp.append(attrs_dict[tc])
        if ct == len(to_check):
            print('Has Calib series')
            calib_vec = temp
        else: 
            ct = 0
            temp = []
            to_check = ['Spectro.Avec', 'Spectro.CurrentWavelength', 'Spectro.CalibWavelength',
                        'Spectro.SpectralPixels', 'Spectro.ProbeWavelength']
            for num, tc in enumerate(to_check):
                if list_of_keys.count(tc) > 0:
                    ct += 1
                    temp.append(attrs_dict[tc])
            if ct == len(to_check):
                print('Has Spectro series')
                calib_vec = temp
        if calib_vec:
            self.ui.checkBoxSpectFromData.setChecked(True)
            return calib_vec

    def is_duplicate_import(self, to_open):
        if self.data._data:
            return self.data_list.count(to_open) > 0
        else:
            return False

    def updateFrequency(self, calib_vec=None):
        if self.pix is not None:
            if calib_vec is None:
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
            else:
                a_vec = calib_vec[0]
                if len(a_vec) == 2:
                    slope = a_vec[0] * 1e-9
                    intercept = a_vec[1] * 1e-9
                else:  # Linearizes higher order polynomial
                    a_vec = _np.polyfit(self.pix, _np.polyval(a_vec, self.pix), 1)
                    slope = a_vec[0] * 1e-9
                    intercept = a_vec[1] * 1e-9

                ctr_wl = calib_vec[1] * 1e-9
                calib_wl = calib_vec[2] * 1e-9
                local_pix = calib_vec[3]
                probe = calib_vec[4] * 1e-9
                
                self.ui.spinBoxProbe.setValue(probe * 1e9)
                self.ui.spinBoxIntercept.setValue(intercept * 1e9)
                self.ui.spinBoxSlope.setValue(slope * 1e9)
                self.ui.spinBoxCenterWL.setValue(ctr_wl * 1e9)
                self.ui.spinBoxCalibWL.setValue(calib_wl * 1e9)
                
                self.wl = slope*self.pix + intercept + (ctr_wl - calib_wl)
                if probe != 0.0:
                    self.freq = 0.01 /  self.wl - 0.01 / probe
                else:
                    self.freq = 0.01 /  self.wl

                self.imported_calib_vec = _copy.deepcopy(calib_vec)

            self.updateSlider()

    @staticmethod
    def _create_list_names(item_list):
        temp = []
        for q in item_list:
            temp.append(q[0] + ' : ' + q[1] + ' : ' + q[-1])
        return temp

    def updateDatasets(self):
        """ Update the listWidget of datasets """
        self.ui.listWidgetDatasets.clear()

        temp = self._create_list_names(self.data_list)

        for q in temp:
            self.ui.listWidgetDatasets.addItem(q)

        self.updateParams()
        # self.updateMosaicImage()

    def updateMosaicImage(self):
        if self.data._data:

            idx = self.ui.sliderFreq.value()
            self.ui.lineEditPix.setText(str(idx))
            if self.freq is not None:
                self.ui.lineEditFreq.setText(str(self.freq[idx]))

            self.mpl.ax.clear()
            temp = self.data.mosaic2d(idx=idx)
            if _np.iscomplexobj(temp):
                self.mpl.ax.imshow(temp.imag)
            else:
                self.mpl.ax.imshow(temp)

            self.mpl.draw()

    def closeEvent(self, event):
        print('Closing')

        if self.h5dlist:
            for q in self.h5dlist:
                print('Closing: {}'.format(q))
                q.file.close()
            self.init_internals()
        self.close()
        # app = _QApplication.instance()
        # app.closeAllWindows()
        # app.quit()



    def updateParams(self):
        """ Update Mosaic object parameters """
        self.data.parameters['StartC'] = self.ui.spinBoxStartCol.value()
        self.data.parameters['StartR'] = self.ui.spinBoxStartRow.value()
        self.data.parameters['EndC'] = -1*self.ui.spinBoxEndCol.value()
        self.data.parameters['EndR'] = -1*self.ui.spinBoxEndRow.value()
        self.data.parameters['Transpose'] = self.ui.checkBoxTranspose.isChecked()
        self.data.parameters['FlipVertical'] = self.ui.checkBoxFlipV.isChecked()
        self.data.parameters['FlipHorizontally'] = self.ui.checkBoxFlipH.isChecked()
        self.data.parameters['Compress'] = self.ui.checkBoxCompress.isChecked()
        self.data.parameters['Shape'] = [self.ui.spinBoxMRows.value(), self.ui.spinBoxNCols.value()]

        idx = self.ui.comboBoxRowCol.currentIndex()
        if idx == 0:
            self.data.parameters['Order'] = 'R'
        else:
            self.data.parameters['Order'] = 'C'

        mrows = self.ui.spinBoxMRows.value()
        ncols = self.ui.spinBoxNCols.value()
        n_dsets = len(self.data_list)

        if (mrows * ncols) < n_dsets:
            mrows = int(_np.ceil(n_dsets / ncols))

            self.ui.spinBoxMRows.setValue(mrows)
            self.ui.spinBoxNCols.setValue(ncols)

        self.data.parameters['Shape'] = [mrows, ncols]

        if self.data._data:
            self.updateMosaicImage()

    def save(self):

        if self.data.parameters['Compress']:
            msg = _QMessageBox(self)
            msg.setIcon(_QMessageBox.Information)
            str1 = 'Currently, HDF5-saving with compression is not supported. Saving full data.'
            msg.setText(str1)
            msg.setWindowTitle('Compression not supported.')
            msg.setStandardButtons(_QMessageBox.Ok)
            msg.setDefaultButton(_QMessageBox.Ok)
            msg.exec()

        ret = DialogSave.dialogSave(parent=self,
                                    current_filename='MOSAIC_' + self.last_fname,
                                    current_path=self.last_path,
                                    current_dataset_name=self.last_dsetname,
                                    suffix='')
        if ret is None:
            pass # Save canceled
        else:
            save_filename = ret[0]
            save_path = ret[1]
            save_dataset_name = ret[2]

            save_grp = save_dataset_name.rpartition('/')[0]
            save_dataset_name_no_grp = save_dataset_name.rpartition('/')[-1]
            save_dataset_mask = save_grp + '/' + 'MASK_' + save_dataset_name_no_grp
            mask = self.data.mosaic_mask()

            new_attrs = OrderedDict()
            new_attrs.update(self.data.attr_dict())

            if self.imported_calib_vec:
                new_attrs.update({'Calib.a_vec':self.imported_calib_vec[0],
                                  'Calib.ctr_wl':self.imported_calib_vec[1],
                                  'Calib.ctr_wl0':self.imported_calib_vec[2],
                                  'Calib.n_pix':self.imported_calib_vec[3],
                                  'Calib.probe':self.imported_calib_vec[4],
                                  'Calib.units':'nm'})

            if self.imported_spatial_vec:
                temp = self.data.mosaic_shape()
                x_stepsize = self.imported_spatial_vec[0]
                y_stepsize = self.imported_spatial_vec[0]
                x_start = 0
                y_start = 0
                x_stop = (temp[1]-1)*x_stepsize
                y_stop = (temp[0]-1)*y_stepsize
                x_steps = temp[1]
                y_steps = temp[0]

                # ['Raster.Fast.Start', 'Raster.Fast.Stop', 'Raster.Fast.Steps', 
                #         'Raster.Slow.Start', 'Raster.Slow.Stop', 'Raster.Slow.Steps']
                new_attrs.update({'Raster.Fast.StepSize':x_stepsize, 'Raster.Fast.Steps':x_steps,
                                  'Raster.Fast.Start':x_start, 'Raster.Fast.Stop':x_stop,
                                  'Raster.Slow.StepSize':y_stepsize, 'Raster.Slow.Steps':y_steps,
                                  'Raster.Slow.Start':y_start, 'Raster.Slow.Stop':y_stop})

            for num, q in enumerate(self.data._data):
                curr_shape = [(mask == num).sum(axis=0).max(), (mask == num).sum(axis=1).max()]
                new_attrs.update({'Mosaic.shape.{}'.format(num):curr_shape})
                new_attrs.update({'Mosaic.path.{}'.format(num):self.data_list[num][0]})
                new_attrs.update({'Mosaic.filename.{}'.format(num):self.data_list[num][1]})
                new_attrs.update({'Mosaic.datasetname.{}'.format(num):self.data_list[num][2]})
                if hasattr(q, 'attrs'):
                    orig_attrs = lazy5.inspect.get_attrs_dset(q.file, q.name)
                    for k in orig_attrs:
                        new_attrs.update({'Mosaic.{}.{}'.format(num, k):orig_attrs[k]})

            # try:
            fid = h5py.File(_os.path.join(save_path, save_filename), 'a')
            fid.require_group(save_grp)
            fid.create_dataset(save_dataset_name, shape=self.data.mosaic_shape(),
                               dtype=self.data.dtype, chunks=True)
            self.data.mosaicfull(out=fid[save_dataset_name])
            lazy5.alter.write_attr_dict(fid[save_dataset_name], new_attrs)
            fid.close()

            lazy5.create.save(save_filename, save_dataset_mask, self.data.mosaic_mask(),
                              pth=save_path, attr_dict=new_attrs)

if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    app.setQuitOnLastWindowClosed(True)

    win = MainWindowMosaic(parent=None)
    win.show()
    app.exec_()



    print(win)

    _sys.exit()