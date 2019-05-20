"""
CRIkit Save Dialog (crikit.ui.dialog_save)
=======================================================

Classes that present dialog boxes that retrieve options

DialogSave : Save Dialog

"""

# Append sys path
import sys as _sys
import os as _os
import datetime as _datetime

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget, QDialog as _QDialog,
                             QMainWindow as _QMainWindow,
                             QSizePolicy as _QSizePolicy,
                             QFileDialog as _QFileDialog)
import PyQt5.QtCore as _QtCore

# Other imports
import numpy as _np

# Import from Designer-based GUI
from crikit.ui.qt_Save import Ui_Dialog

class DialogSave(_QDialog):
    """
    DialogDarkOptions : Dark subtraction options dialog
    
    Methods
    --------
    dialogSave : Used to call UI and retrieve results of dialog
    
    """

    def __init__(self, current_filename=None, current_path=None,
                 current_dataset_name=None, save_filename=None,
                 save_path=None, save_dataset_name=None, suffix=None,
                 parent=None):
        super(DialogSave, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###
        self.ui.lineEditFilename.setFocus()
        
#        print('Current filename: {}'.format(current_filename))
        if save_filename is not None and save_filename != '':
            self.filename = save_filename
        elif current_filename is not None and current_filename != '':
            self.filename = current_filename
        else:
            self.filename = None
            
        if save_path is not None and save_path != '':
            self.path = save_path
        elif current_path is not None and current_path != '':
            self.path = current_path
        else:
            self.path = None
            
        if save_dataset_name is not None and save_dataset_name != '':
            self.dataset_name = save_dataset_name
        elif current_dataset_name is not None and current_dataset_name != '':
            self.dataset_name = current_dataset_name
        else:
            self.dataset_name = None
        
        
        self.current_filename=current_filename
        self.current_path=current_path
        self.current_dataset_name=current_dataset_name
        self.save_filename=save_filename
        self.save_path=save_path
        self.save_dataset_name=save_dataset_name
        
        self.suffix = suffix
        
        self.ui.lineEditFilename.setText(self.filename)
        self.generateFilename()
        self.ui.lineEditPath.setText(self.path)
        self.ui.lineEditDataset.setText(self.dataset_name)
        self.ui.lineReadDataset.setText(self.dataset_name)
        self.generateDatasetName()
            
        self.ui.buttonCancel.pressed.connect(self.reject)
        self.ui.buttonOK.pressed.connect(self.accept)
        
        self.ui.lineEditFilename.editingFinished.connect(self.changeFilename)
        self.ui.lineEditPath.editingFinished.connect(self.changePath)
        self.ui.lineEditDataset.editingFinished.connect(self.changeDataset)
        self.ui.buttonGetFilename.pressed.connect(self.getFilename)
        self.ui.buttonGetPath.pressed.connect(self.getPath)
        self.ui.buttonGenerateFilename.pressed.connect(self.generateFilename)
        self.ui.buttonGenerateDatasetname.pressed.connect(self.generateDatasetName)
        
    def changeFilename(self):
        self.filename = self.ui.lineEditFilename.text()
        self.filename = self.filename.split('.h5')[0]
        self.filename = self.filename + '.h5'
        
        self.ui.lineEditFilename.setText(self.filename)
        
        if self.path is None or self.path == '':        
            self.ui.lineReadFileNamePath.setText('./' + self.filename)
        else:
            self.ui.lineReadFileNamePath.setText(self.path + self.filename)
                
    def changePath(self):
        self.path = self.ui.lineEditPath.text()
        self.changeFilename()
        
    def changeDataset(self):
        self.dataset_name = self.ui.lineEditDataset.text()
        self.ui.lineReadDataset.setText(self.dataset_name)
        
    def getFilename(self):
        filename,_ = _QFileDialog.getSaveFileName(self, "Open H5 File", "./",\
            "HDF5 Files (*.h5 *.hdf);;All Files (*.*)",options=_QFileDialog.Options(4))
        
        if filename != '':
            self.path = _os.path.dirname(filename) + '/'
            self.filename = filename.split(_os.path.dirname(filename))[1][1::]
            self.ui.lineEditFilename.setText(self.filename)
            self.ui.lineReadFileNamePath.setText(self.path + self.filename)
            self.ui.lineEditPath.setText(self.path)
        
    def getPath(self):
        path = _QFileDialog.getExistingDirectory(self)
        
        if path != '':
            self.path = path + '/'
            self.ui.lineEditPath.setText(self.path)
            self.changeFilename()
    
    def generateFilename(self):
        curr_time = _datetime.datetime.now()
        rnd_fname = 'PROCESS_' + str(curr_time.year) + str(curr_time.month) + \
        str(curr_time.day) + '_' + str(curr_time.hour) + '_' + \
        str(curr_time.minute) + '_' + str(curr_time.second) + '_' + \
        str(curr_time.microsecond) + '.h5'
        if self.filename is None or self.filename == '':
            self.filename = rnd_fname
            self.ui.lineEditFilename.setText(self.filename)
        else:
            self.filename = self.filename.split('.h5')[0] + '_' + rnd_fname
            self.ui.lineEditFilename.setText(self.filename)
                        
        if self.path is None or self.path == '':
            self.ui.lineReadFileNamePath.setText('./' + self.filename)
        else:
            self.ui.lineReadFileNamePath.setText(self.path + self.filename)
    def generateDatasetName(self):
        if self.save_dataset_name is not None:
            if self.suffix is not None:
                self.dataset_name = self.save_dataset_name + self.suffix
            else:
                curr_time = _datetime.datetime.now()
                self.dataset_name = self.save_dataset_name + '_' + str(curr_time.year) + str(curr_time.month) + \
                str(curr_time.day) + '_' + str(curr_time.hour) + '_' + \
                str(curr_time.minute) + '_' + str(curr_time.second) + '_' + \
                str(curr_time.microsecond)
        elif self.current_dataset_name is not None:
            if self.suffix is not None:
                self.dataset_name = self.current_dataset_name + self.suffix
            else:
                curr_time = _datetime.datetime.now()
                self.dataset_name = self.current_dataset_name + '_PROCESS_' + str(curr_time.year) + str(curr_time.month) + \
                str(curr_time.day) + '_' + str(curr_time.hour) + '_' + \
                str(curr_time.minute) + '_' + str(curr_time.second) + '_' + \
                str(curr_time.microsecond)
        else:
            if self.suffix is not None:
                self.dataset_name = 'PROCESS_' + self.suffix
            else:
                curr_time = _datetime.datetime.now()
                self.dataset_name = 'PROCESS_' + str(curr_time.year) + str(curr_time.month) + \
                str(curr_time.day) + '_' + str(curr_time.hour) + '_' + \
                str(curr_time.minute) + '_' + str(curr_time.second) + '_' + \
                str(curr_time.microsecond)
        
        self.ui.lineEditDataset.setText(self.dataset_name)
        self.ui.lineReadDataset.setText(self.dataset_name)
            
        
        
    @staticmethod
    def dialogSave(current_filename=None, current_path=None,
                 current_dataset_name=None, save_filename=None,
                 save_path=None, save_dataset_name=None, suffix=None,
                 parent=None):
        """
        Retrieve save dialog results

        Parameters
        ----------
        current_filename : str
            Filename of HDF5 file from where current data resided
        
        current_path : str
            Path to HDF5 file from where current data resided
            
        current_dataset_name : str
            Dataset path and name where current data resided
            
        save_filename : str
            Filename of HDF5 file where previously saved (if so)
            
        save_path : str
            Path of HDF5 file where previously saved (if so)
        
        save_dataset_name : str
            Dataset path and name where previously saved (if so)
        
        suffix : str
            Suffix to append to _dataset_name based on processing steps
            
        NOTE : save* parameters supercede current* parameters

        Returns
        ----------
        out : (tuple)
            Filename : str
            Path : str
            Dataset_name_path : str
        """
        dialog = DialogSave(current_filename=current_filename,
                            current_path=current_path,
                            current_dataset_name=current_dataset_name,
                            save_filename=save_filename,
                            save_path=save_path,
                            save_dataset_name=save_dataset_name,
                            suffix=suffix, parent=parent)
        
        result = dialog.exec_()
        if result == 1:
            if dialog.filename is not None and dialog.path is not None and dialog.dataset_name is not None:
                return (dialog.filename, dialog.path, dialog.dataset_name)
            else:
                return None
        else:
            return None

if __name__ == '__main__':

        
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = DialogSave.dialogSave()
    print(win)

    _sys.exit()