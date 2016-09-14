# -*- coding: utf-8 -*-
"""
HDF5 LOAD DATA QDialog (crikit.vis.subguis.h5loadgui)
=======================================================

    H5LoadGUI : A graphical user interface (GUI) to select HDF5 dataset(s)

    Method : H5LoadGUI.getFileDataSets()

    Return (tuple) : (path [str], filename [str], dataset(s) [list], selection_made [bool])

Software Info
--------------

Original Python branch: Feb 16 2015\n
\n
@author: ("Charles H Camp Jr")\n
@email: ("charles.camp@nist.gov")\n
@date: ("Jun 28 2015")\n
@version: ("1.1")\n
"""


# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication, \
QDialog as _QDialog, QFileDialog as _QFileDialog, \
QTableWidgetItem as _QTableWidgetItem)

# Other imports
import numpy as _np
import crikit.utils.h5 as _h5utils

# Import from Designer-based GUI
from crikit.ui.qt_HDFLoad import Ui_Dialog ### EDIT ###

class SubUiHDFLoad(_QDialog): ### EDIT ###
    """ GUI Loader Class for H5 Files """

    def __init__(self, parent = None):

        # Generic load/init designer-based GUI
        super(SubUiHDFLoad, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        # Set static GUI  parameters

        # Set signal(s)-slot(s) connection/actions

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.dataGroupSelect.currentTextChanged.connect(self.datagroupchange)
        self.ui.dataSetList.itemClicked.connect(self.datasetselected)
        self.ui.filterButton.clicked.connect(self.filterlist)
        self.ui.resetFilter.clicked.connect(self.datagroupchange)
        # Setup GUI variables
        self.path = None
        self.filename = None
        self.allselect=None
        # Initial Actions

    @staticmethod
    def getFileDataSets(start_path='./', parent = None):
        """
        Retrieve the filename and datasets selected by the user (via GUI)

        Inputs
        ----------
        start_path : str
            Home directory to start in

        Returns
        ----------
        out : (tuple)
            path : str
            filename : (str)
            dataset(s) : (list[str])
        """
        if start_path is None:
            start_path = './'
            
        dialog = SubUiHDFLoad(parent)

        ret_fileopen = dialog.fileopen(start_path)

        if ret_fileopen is None:
            return None

        # Execute dialog, which defined by QDialog class returns
        # QDialog.Accepted or QDialog.Rejected
        ret_dset_select = dialog.exec_()
        if ret_dset_select == _QDialog.Rejected:
            return None
        elif dialog.allselect is None:
            return None
        else:
            return (dialog.path, dialog.filename, dialog.allselect)

    def fileopen(self, start_path='./'):
        """ Select HDF5 File """

        if start_path is None:
            start_path = './'
            
        filename = _QFileDialog.getOpenFileName(self, "Open H5 File", 
                                                start_path,\
            "HDF5 Files (*.h5 *.hdf);;All Files (*.*)")

        if filename[0]:
            self.filename = filename[0]
            self.path = _os.path.dirname(self.filename) + '/'
            self.filename = self.filename.split(_os.path.dirname(self.filename))[1][1::]

            self.group_dset_dict = _h5utils.retrieve_group_dataset_dict(self.path + self.filename)
            self.ui.dataGroupSelect.clear()
            for count in self.group_dset_dict:
                self.ui.dataGroupSelect.addItem(count)
            return [self.path, self.filename]
        else:
            return None
    def datagroupchange(self):
        """ Action : ComboBox containing Groups with DataSets has changed"""

        #self.dsetlist = QListWidget(self.verticalLayoutWidget)
        self.ui.dataSetList.clear()
        self.ui.dataSetList.addItems(self.group_dset_dict[self.ui.dataGroupSelect.currentText()])
        #print('Changed')

    def datasetselected(self):
        """ Action : One or more DataSets were selected from the list """

        #print('Selection changed')
        self.currentdset = self.ui.dataGroupSelect.currentText() + '/' + \
            self.ui.dataSetList.currentItem().text()

#        print('Current Selection : {}'.format(self.currentdset))
        self.allselect = ['/' + str(self.ui.dataGroupSelect.currentText() +\
            '/' + i.text()) for i in self.ui.dataSetList.selectedItems()]


        if len(self.allselect) == 0:
            self.allselect = None
            self.ui.currentDatasetText.setText('')
            attrs = {}
            self.ui.dataSetAttribs.setRowCount(0)
            self.ui.dataSetMemo.setText('')
        else:
            if len(self.allselect) == 1:
                self.ui.currentDatasetText.setText(self.currentdset)
            else:
                self.ui.currentDatasetText.setText(self.currentdset + ' ( + ' +\
                    str(len(self.allselect)-1) + ' others)' )

            self.ui.dataSetAttribs.setSortingEnabled(False)
            self.ui.dataSetAttribs.setRowCount(0)
            self.ui.dataSetAttribs.setColumnCount(2)

            attrs = _h5utils.retrieve_dataset_attribute_dict(self.path + self.filename,self.currentdset)

            for count, key in enumerate(attrs.keys()):
                self.ui.dataSetAttribs.insertRow(self.ui.dataSetAttribs.rowCount())
                self.ui.dataSetAttribs.setItem(count,0,_QTableWidgetItem(str(key)))
                temp = attrs[key]
                if isinstance(temp,_np.bytes_):
                    self.ui.dataSetAttribs.setItem(count,1,_QTableWidgetItem(temp.decode()))
                else:
                    self.ui.dataSetAttribs.setItem(count,1,_QTableWidgetItem(str(temp)))

            self.ui.dataSetAttribs.setSortingEnabled(True)
            self.ui.dataSetAttribs.sortItems(0)

            try:
                self.ui.dataSetMemo.setText(attrs['Memo'].decode())
            except:
                pass

    def filterlist(self):
        """ Action : Filter available dataset list (*.ui.dataSetList) based on
        include or exclude strings (or comma-separated strings)
        """

        temp_list = []

        for count in range(self.ui.dataSetList.count()):
            temp_list.append(self.ui.dataSetList.item(count).text())

        temp_list_filt = temp_list

        # Has strings to Exclude
        if self.ui.filterExcludeString.text() != '':
            # Convert comma-separated string to list-of-strings
            strexclude = str.split(self.ui.filterExcludeString.text(),',')

            # Strip white-space
            strexclude = [str.strip(strexclude) for strexclude in strexclude]

            # Exclude Filter
            for count in strexclude[0::]:
                temp_list_filt = ([i for i in temp_list_filt if str.find(i,count) == -1])
                #print(count)
        else:
            pass

        # Has strings to Include
        if self.ui.filterIncludeString.text() != '':
            # Convert comma-separated string to list-of-strings
            strinclude = str.split(self.ui.filterIncludeString.text(),',')

            # Strip white-space
            strinclude = [str.strip(strinclude) for strinclude in strinclude]

            # Include Filter
            for count in strinclude:
                temp_list_filt = ([i for i in temp_list_filt if str.find(i,count) != -1])
        else:
            pass

        # Update GUI
        self.ui.dataSetList.clear()
        self.ui.dataSetList.addItems(temp_list_filt)

if __name__ == '__main__':

    app = _QApplication(_sys.argv)
    #win = H5LoadGUI() ### EDIT ###
    result = SubUiHDFLoad.getFileDataSets()
    print('Result: {}'.format(result))

    _sys.exit()
