"""
HDF5 LOAD DATA QDialog (crikit.vis.subguis.h5loadgui)
=======================================================

    H5LoadGUI : A graphical user interface (GUI) to select HDF5 dataset(s)

    Method : H5LoadGUI.getFileDataSets()

    Return (tuple) : (path [str], filename [str], dataset(s) [list], selection_made [bool])

    Notes
    -----
    Methods that interact with Qt follow the Qt naming convention:
    firstSecondThird
"""


# Append sys path
import sys as _sys
import os as _os

try:
    # Generic imports for QT-based programs
    from PyQt5.QtWidgets import (QApplication as _QApplication, \
    QDialog as _QDialog, QFileDialog as _QFileDialog, \
    QTableWidgetItem as _QTableWidgetItem)
except Exception:
    HAS_PYQT5 = False
else:
    HAS_PYQT5 = True
from crikit.io.lazy5.ui.qt_HdfLoad import Ui_Dialog

from crikit.io.lazy5.inspect import get_hierarchy, get_attrs_dset
from crikit.io.lazy5.nonh5utils import filterlist

class HdfLoad(_QDialog): ### EDIT ###
    """ GUI Loader Class for H5 Files """

    # Default configuration
    config = {'only_show_grp_w_dset': True,  # Only show groups with datasets
              'attr_description': 'Memo',  # Description attribute key (optional)
              'excl_filtering' : True  # Filtering is exclusive (filters are AND'd)
             }

    def __init__(self, title=None, parent=None):

        # Generic load/init designer-based GUI
        super(HdfLoad, self).__init__(parent)
        self.ui = Ui_Dialog()  # pylint: disable=C0103
        self.ui.setupUi(self)

        self.path = None
        self.filename = None
        self.all_selected = None
        self.group_dset_dict = None

        if title:
            self.setWindowTitle('{}: Select a dataset...'.format(title))
        else:
            self.setWindowTitle('Select a dataset...')

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.comboBoxGroupSelect.currentTextChanged.connect(self.dataGroupChange)
        self.ui.listDataSet.itemClicked.connect(self.datasetSelected)
        self.ui.pushButtonFilter.clicked.connect(self.filterDatasets)
        self.ui.pushButtonResetFilter.clicked.connect(self.dataGroupChange)


    @staticmethod
    def getFileDataSets(pth='./', title=None, parent=None):  # pylint: disable=C0103; # pragma: no cover
        """
        Retrieve the filename and datasets selected by the user (via GUI)

        Parameters
        ----------
        pth : str
            Home directory to start in OR the relative pth to a file

        Returns
        ----------
        Tuple (str, str, list[str]) as (path, filename, [dataset(s)])

        """

        # pragma: no cover
        dialog = HdfLoad(title=title, parent=parent)

        ret_fileopen = True
        if pth is None:
            pth = './'
        else:
            pth = _os.path.abspath(pth)

        while True:
            ret_fileopen = dialog.fileOpen(pth, title=title)

            ret = None
            if ret_fileopen:
                ret_dset_select = dialog.exec_()
                if ret_dset_select == _QDialog.Rejected:
                    pth = dialog.path
                elif dialog.all_selected is None:
                    pass
                else:
                    ret = (dialog.path, dialog.filename, dialog.all_selected)
                    break
            else:
                break
        return ret

    def fileOpen(self, pth='./', title=None):  # Qt-related pylint: disable=C0103
        """ Select HDF5 File via QDialog built-in."""

        if pth is None:
            pth = './'

        if title is None:
            title_file='Select a file...'
        else:
            title_file='{}: Select a file...'.format(title)

        if _os.path.isdir(pth):  # No file provided, use QFileDialog; # pragma: no cover
            filetype_options = 'HDF5 Files (*.h5 *.hdf);;All Files (*.*)'
            full_pth_fname, _ = _QFileDialog.getOpenFileName(self, title_file, pth,
                                                             filetype_options)
        elif _os.path.isfile(pth):  # Is a valid file
            full_pth_fname = pth
        else:
            raise FileNotFoundError('Not a valid path. Not a valid file.')

        ret = None
        if full_pth_fname:
            full_pth_fname = _os.path.abspath(full_pth_fname)  # Ensure correct /'s for each OS
            self.filename = _os.path.basename(full_pth_fname)
            self.path = _os.path.dirname(full_pth_fname)
            self.populateGroups()
            ret = True
        return ret

    def populateGroups(self):  # Qt-related pylint: disable=C0103
        """ Populate dropdown box of group ui.comboBoxGroupSelect """
        self.group_dset_dict = get_hierarchy(_os.path.join(self.path, self.filename),
                                             grp_w_dset=HdfLoad.config['only_show_grp_w_dset'])
        # Load Group dropdown box
        self.ui.comboBoxGroupSelect.clear()
        for count in self.group_dset_dict:
            self.ui.comboBoxGroupSelect.addItem(count)
        return [self.path, self.filename]

    def dataGroupChange(self):  # Qt-related pylint: disable=C0103
        """ Action : ComboBox containing Groups with DataSets has changed"""

        #self.dsetlist = QListWidget(self.verticalLayoutWidget)
        self.ui.listDataSet.clear()

        if self.ui.comboBoxGroupSelect.currentText() != '':
            self.ui.listDataSet.addItems(self.group_dset_dict[self.ui.comboBoxGroupSelect.currentText()])
        #print('Changed')

    def populate_attrs(self, attr_dict=None):
        """ Populate attribute and memo boxes for currently selected dataset """

        self.ui.tableAttributes.setRowCount(0)
        self.ui.tableAttributes.setColumnCount(2)
        self.ui.tableAttributes.setSortingEnabled(False)
        self.ui.textDescription.setText('')

        if attr_dict:
            try:
                self.ui.textDescription.setText(attr_dict[HdfLoad.config['attr_description']])
            except (KeyError, AttributeError) as error_msg:
                print('{}\nNo memo at key {}'.format(error_msg, HdfLoad.config['attr_description']))

            for num, key in enumerate(attr_dict):
                self.ui.tableAttributes.insertRow(self.ui.tableAttributes.rowCount())
                self.ui.tableAttributes.setItem(num, 0, _QTableWidgetItem(key))
                self.ui.tableAttributes.setItem(num, 1, _QTableWidgetItem(str(attr_dict[key])))

    def datasetSelected(self):  # Qt-related pylint: disable=C0103
        """ Action : One or more DataSets were selected from the list """

        all_selected = self.ui.listDataSet.selectedItems()
        n_selected = len(all_selected)

        self.ui.textCurrentDataset.setText('')
        self.all_selected = []
        attrs = {}

        if n_selected > 0:
            current_selection = all_selected[-1].text()
            current_grp = self.ui.comboBoxGroupSelect.currentText()

            selection_str = '{} + ({} others)'.format(current_selection, n_selected - 1)
            self.ui.textCurrentDataset.setText(selection_str)
            if current_grp == '/':
                current_dset_fullpath = '{}{}'.format(current_grp, current_selection)
            else:
                current_dset_fullpath = '{}/{}'.format(current_grp, current_selection)
            # TODO: Figure out a better way to deal with base-group datasets
            # Bug when dsets are in base group '/'
            current_dset_fullpath = current_dset_fullpath.replace('//','/')
            attrs = get_attrs_dset(_os.path.join(self.path, self.filename),
                                   current_dset_fullpath, convert_to_str=True)
            self.all_selected = [('{}/{}'.format(current_grp, selection.text())).replace('//','/')
                                 for selection in all_selected]

        # Fill-in attribute table
        self.populate_attrs(attr_dict=attrs)

    def filterDatasets(self):  # Qt-related pylint: disable=C0103
        """ Filter list of datasets based on include and exclude strings """
        incl_str = self.ui.filterIncludeString.text()
        excl_str = self.ui.filterExcludeString.text()

        # From string with comma separation to list-of-strings
        incl_list = [q.strip() for q in incl_str.split(',') if q.strip()]
        excl_list = [q.strip() for q in excl_str.split(',') if q.strip()]

        dset_list = [self.ui.listDataSet.item(num).text() for num in
                     range(self.ui.listDataSet.count())]

        if incl_list:  # Include list is not empty
            dset_list = filterlist(dset_list, incl_list,
                                   keep_filtered_items=True,
                                   exclusive=HdfLoad.config['excl_filtering'])

        if excl_list:  # Exclude list is not empty
            dset_list = filterlist(dset_list, excl_list,
                                   keep_filtered_items=False,
                                   exclusive=HdfLoad.config['excl_filtering'])

        self.ui.listDataSet.clear()
        self.ui.listDataSet.addItems(dset_list)

if __name__ == '__main__':  # pragma: no cover
    app = _QApplication(_sys.argv)  # pylint: disable=C0103
    result = HdfLoad.getFileDataSets(pth='.', title='Test title')  # pylint: disable=C0103
    print('Result: {}'.format(result))

    _sys.exit()
    # pylint: error
