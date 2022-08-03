""" Test inspection of HDF5 files """
import os
import sys
import h5py

import numpy as np
import pytest

try:
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtTest import QTest
    import PyQt5.QtCore
    from PyQt5.QtCore import Qt
except Exception:
    HAS_PYQT5 = False
else:
    HAS_PYQT5 = True
    import crikit.io.lazy5 as lazy5
    from crikit.io.lazy5.ui.QtHdfLoad import HdfLoad

from crikit.io.lazy5.utils import hdf_is_open

@pytest.mark.skipif(not HAS_PYQT5, reason='PyQt5 not installed, skipping.')
class TestUI:
    """ Test the HDF5 PyQt5 Viewer  """

    @pytest.fixture(scope="module")
    def hdf_dataset(self):
        """ Setups and tears down a sample HDF5 file """
        filename = 'temp_test_ui.h5'
        fid = h5py.File(filename, 'w')
        data_m, data_n, data_p = [20, 22, 24]
        data = np.random.randn(data_m, data_n, data_p)

        fid.create_dataset('base', data=data)

        grp1 = fid.create_group('Group1')
        grp3 = fid.create_group('Group2/Group3')
        grp6 = fid.create_group('Group4/Group5/Group6')

        grp1.create_dataset('ingroup1_1', data=data)
        grp1.create_dataset('ingroup1_2', data=data)
        fid.create_dataset('Group2/ingroup2', data=data)
        grp3.create_dataset('ingroup3', data=data)

        grp6.create_dataset('ingroup6', data=data)

        fid['base'].attrs['Attribute_str'] = 'Test'
        fid['base'].attrs['Attribute_bytes'] = b'Test'
        fid['base'].attrs['Attribute_np_bytes'] = np.bytes_('Test') # pylint: disable=no-member
        fid['base'].attrs.create('Attribute_int', 1)
        fid['base'].attrs.create('Attribute_float', 1.1)
        fid['base'].attrs.create('Attribute_np_1d', np.array([1, 2, 3]))
        fid['base'].attrs.create('Attribute_np_2d', np.array([[1, 2, 3], [4, 5, 6]]))

        app = QApplication(sys.argv)  # pylint: disable=C0103, W0612
        yield filename

        # Tear-down
        if hdf_is_open(fid):
            fid.close()
        os.remove(filename)
        # sys.exit()

    def test_ui_win_title_empty_load_dataset(self, hdf_dataset):
        """ Test whether load dataset dialog is titled properly with no title provided"""
        self.filename = hdf_dataset
        dialog = HdfLoad()
        _ = dialog.fileOpen(self.filename)

        assert dialog.windowTitle() == 'Select a dataset...'

    def test_ui_win_title_load_dataset(self, hdf_dataset):
        """ Test whether load dataset dialog is titled properly """
        self.filename = hdf_dataset
        dialog = HdfLoad(title='TEST')
        _ = dialog.fileOpen(self.filename)

        assert dialog.windowTitle() == 'TEST: Select a dataset...'

    def test_ui_load_file(self, hdf_dataset):
        """ Load test file and check groups """
        self.filename = hdf_dataset
        dialog = HdfLoad()
        _ = dialog.fileOpen(self.filename)

        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]

        list_grps = [dialog.ui.comboBoxGroupSelect.itemText(num) for num in
                     range(dialog.ui.comboBoxGroupSelect.count())]

        assert list_dsets == ['base']
        assert '/Group1' in list_grps
        assert '/Group2/Group3' in list_grps
        assert '/Group4/Group5/Group6' in list_grps
        assert '/Group5' not in list_grps

    def test_ui_change_grp_and_filter_include(self, hdf_dataset):
        """ Load test file, change to Group1, filter for _1 """
        self.filename = hdf_dataset
        dialog = HdfLoad()
        _ = dialog.fileOpen(self.filename)

        # Change group to Group1
        dialog.ui.comboBoxGroupSelect.setCurrentIndex(1)
        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]
        assert dialog.ui.comboBoxGroupSelect.currentText() == '/Group1'
        assert list_dsets == ['ingroup1_1', 'ingroup1_2']

        dialog.ui.filterIncludeString.setText('_1')
        QTest.mouseClick(dialog.ui.pushButtonFilter, Qt.LeftButton)
        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]
        assert list_dsets == ['ingroup1_1']

    def test_ui_change_grp_and_filter_exclude(self, hdf_dataset):
        """ Load test file, change to Group1, filter for _1 """
        self.filename = hdf_dataset
        dialog = HdfLoad()
        _ = dialog.fileOpen(self.filename)

        # Change group to Group1
        dialog.ui.comboBoxGroupSelect.setCurrentIndex(1)
        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]
        assert dialog.ui.comboBoxGroupSelect.currentText() == '/Group1'
        assert list_dsets == ['ingroup1_1', 'ingroup1_2']

        dialog.ui.filterExcludeString.setText('_1')
        QTest.mouseClick(dialog.ui.pushButtonFilter, Qt.LeftButton)
        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]
        assert list_dsets == ['ingroup1_2']

    def test_ui_attrs(self, hdf_dataset):
        """ Load test file, change to base group (/), check attributes """
        self.filename = hdf_dataset
        dialog = HdfLoad()
        _ = dialog.fileOpen(self.filename)

        # Change group to Group1
        dialog.ui.comboBoxGroupSelect.setCurrentIndex(0)
        list_dsets = [dialog.ui.listDataSet.item(num).text() for num in
                      range(dialog.ui.listDataSet.count())]
        assert dialog.ui.comboBoxGroupSelect.currentText() == '/'
        assert list_dsets == ['base']

        # Select dataset base
        dialog.ui.listDataSet.item(0).setSelected(True)
        QTest.mouseClick(dialog.ui.listDataSet.viewport(), Qt.LeftButton)

        assert (dialog.ui.tableAttributes.findItems('Attribute_str', Qt.MatchExactly)[0].text() ==
                'Attribute_str')
        assert not dialog.ui.tableAttributes.findItems('fake', Qt.MatchExactly)  # Empty

    def test_ui_wrongfile(self, hdf_dataset):
        """ Load test file, change to base group (/), check attributes """
        self.filename = hdf_dataset
        dialog = HdfLoad()
        with pytest.raises(FileNotFoundError):
            _ = dialog.fileOpen('does_not_exist.h5')
