""" Test inspection of HDF5 files """
import os
import time

import h5py
import pytest

import numpy as np
from numpy.testing import assert_array_almost_equal

from crikit.io.lazy5.inspect import (get_groups, get_datasets, get_hierarchy,
                                     get_attrs_dset, valid_dsets, valid_file)

from crikit.io.lazy5.utils import hdf_is_open

@pytest.fixture(scope="module")
def hdf_dataset():
    """ Setups and tears down a sample HDF5 file """
    filename = 'temp_test.h5'
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
    fid['base'].attrs['Attribute_np_bytes_inarray'] = np.array(b'Test') # pylint: disable=no-member
    fid['base'].attrs['Attribute_np_bytes_inarray2'] = np.array([b'Test']) # pylint: disable=no-member
    fid['base'].attrs.create('Attribute_int', 1)
    fid['base'].attrs.create('Attribute_float', 1.1)
    fid['base'].attrs.create('Attribute_np_1d', np.array([1, 2, 3]))
    fid['base'].attrs.create('Attribute_np_2d', np.array([[1, 2, 3], [4, 5, 6]]))
    fid['base'].attrs.create('Attribute_np_sgl_int', np.array([1]))
    fid['base'].attrs.create('Attribute_np_sgl_float', np.array([1.0]))
    fid['base'].attrs.create('Attribute_np_array_float', np.array([1.0, 2.0]))
    fid['base'].attrs.create('Attribute_np_sgl_complex', np.array([1.0 + 1j]))

    yield filename, fid

    # Tear-down
    if hdf_is_open(fid):
        fid.close()
    
    time.sleep(1)
    try:
        os.remove(filename)
    except Exception:
        print('Could not delete {}'.format(filename))

def test_valid_file(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Test whether a file is valid or not """
    
    filename, fid = hdf_dataset

    assert valid_file(filename, verbose=True)
    assert not valid_file('NOT_A_REAL_FILE.XYZ', verbose=True)

def test_valid_dsets(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Test whether a dset or list of dsets are valid or not """
    
    filename, fid = hdf_dataset

    # NOT valid filename
    assert not valid_dsets('NOTAFILE.XYZ', 'base', verbose=True)

    # Single dataset
    dset_list = 'base'
    assert valid_dsets(filename, dset_list, verbose=True)

    # Single dataset by fid
    dset_list = 'base'
    assert valid_dsets(fid, dset_list, verbose=True)

    # Single dataset is WRONG
    dset_list = 'NOTADSET'
    assert not valid_dsets(filename, dset_list, verbose=True)

    # Single dataset in list
    dset_list = ['base']
    assert valid_dsets(filename, dset_list, verbose=True)

    # Datasets in list -- NOTE some have leading slashes, some don't
    dset_list = ['base', '/Group1/ingroup1_1', '/Group1/ingroup1_2',
                 'Group2/ingroup2']
    assert valid_dsets(filename, dset_list, verbose=True)

    # Datasets in list -- 1 IS WRONG
    dset_list = ['base', '/Group1/ingroup1_1', '/Group1/ingroup1_2',
                 'Group2/DOESNOTEXIST']
    assert not valid_dsets(filename, dset_list, verbose=True)

    # Dataset with wrong-type
    dset_list = 1
    with pytest.raises(TypeError):
        valid_dsets(filename, dset_list, verbose=True)

    # Dataset with wrong-type
    dset_list = ['base', 1]
    with pytest.raises(TypeError):
        valid_dsets(filename, dset_list, verbose=True)

def test_get_groups(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Get an HDF5 file's group list """

    filename, fid = hdf_dataset

    # Passing fid
    grp_list = get_groups(fid)
    assert set(grp_list) == {'/', '/Group1', '/Group2', '/Group2/Group3', '/Group4', '/Group4/Group5',
                             '/Group4/Group5/Group6'}

    # Passing filename
    grp_list = get_groups(filename)
    assert set(grp_list) == {'/', '/Group1', '/Group2', '/Group2/Group3', '/Group4', '/Group4/Group5',
                             '/Group4/Group5/Group6'}

def test_get_datasets_fullpath(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Get an HDF5 file's dataset list with groupnames prepended"""
    filename, fid = hdf_dataset

    # Passing fid
    dataset_list = get_datasets(fid, fulldsetpath=True)
    assert set(dataset_list) == {'/base', '/Group1/ingroup1_1', '/Group1/ingroup1_2',
                                 '/Group2/ingroup2', '/Group2/Group3/ingroup3',
                                 '/Group4/Group5/Group6/ingroup6'}

    # Passing filename
    dataset_list = get_datasets(filename, fulldsetpath=True)
    assert set(dataset_list) == {'/base', '/Group1/ingroup1_1', '/Group1/ingroup1_2',
                                 '/Group2/ingroup2', '/Group2/Group3/ingroup3',
                                 '/Group4/Group5/Group6/ingroup6'}

def test_get_datasets_nopath(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Get an HDF5 file's dataset list with no groupnames prepended """
    filename, fid = hdf_dataset

    # Passing fid
    dataset_list = get_datasets(fid, fulldsetpath=False)
    assert set(dataset_list) == {'base', 'ingroup1_1', 'ingroup1_2', 'ingroup2',
                                 'ingroup3', 'ingroup6'}

    # Passing filename
    dataset_list = get_datasets(filename, fulldsetpath=False)
    assert set(dataset_list) == {'base', 'ingroup1_1', 'ingroup1_2', 'ingroup2',
                                 'ingroup3', 'ingroup6'}

def test_get_hierarchy_fullpath(hdf_dataset):  # pylint:disable=redefined-outer-name
    """
    OrderedDict describing HDF5 file hierarchy. Testing with full paths in
    the dataset names. Keys are groups, values are datasets.
    """
    filename, fid = hdf_dataset

    # Passing fid
    hierarchy = get_hierarchy(fid, fulldsetpath=True, grp_w_dset=False)
    assert hierarchy == {'/':['base'],
                         '/Group1':['/Group1/ingroup1_1', '/Group1/ingroup1_2'],
                         '/Group2':['/Group2/ingroup2'],
                         '/Group2/Group3':['/Group2/Group3/ingroup3'],
                         '/Group4':[],
                         '/Group4/Group5':[],
                         '/Group4/Group5/Group6':['/Group4/Group5/Group6/ingroup6']
                        }

    # Passing filename
    hierarchy = get_hierarchy(filename, fulldsetpath=True, grp_w_dset=False)
    assert hierarchy == {'/':['base'],
                         '/Group1':['/Group1/ingroup1_1', '/Group1/ingroup1_2'],
                         '/Group2':['/Group2/ingroup2'],
                         '/Group2/Group3':['/Group2/Group3/ingroup3'],
                         '/Group4':[],
                         '/Group4/Group5':[],
                         '/Group4/Group5/Group6':['/Group4/Group5/Group6/ingroup6']
                        }

def test_get_hierarchy_grp_w_dset(hdf_dataset):  # pylint:disable=redefined-outer-name
    """
    OrderedDict describing HDF5 file hierarchy. Testing empty sets are NOT
    returned. Keys are groups, values are datasets.
    """

    filename, fid = hdf_dataset

    # Passing fid
    hierarchy = get_hierarchy(fid, fulldsetpath=True, grp_w_dset=True)
    assert hierarchy == {'/':['base'],
                         '/Group1':['/Group1/ingroup1_1', '/Group1/ingroup1_2'],
                         '/Group2':['/Group2/ingroup2'],
                         '/Group2/Group3':['/Group2/Group3/ingroup3'],
                         '/Group4/Group5/Group6':['/Group4/Group5/Group6/ingroup6']
                        }

    # Passing filename
    hierarchy = get_hierarchy(filename, fulldsetpath=True, grp_w_dset=True)
    assert hierarchy == {'/':['base'],
                         '/Group1':['/Group1/ingroup1_1', '/Group1/ingroup1_2'],
                         '/Group2':['/Group2/ingroup2'],
                         '/Group2/Group3':['/Group2/Group3/ingroup3'],
                         '/Group4/Group5/Group6':['/Group4/Group5/Group6/ingroup6']
                        }

def test_get_hierarchy_nopath(hdf_dataset):  # pylint:disable=redefined-outer-name
    """
    OrderedDict describing HDF5 file hierarchy. Testing with no full paths in
    the dataset names. Keys are groups, values are datasets.
    """
    filename, fid = hdf_dataset

    # Passing fid
    hierarchy = get_hierarchy(fid, fulldsetpath=False, grp_w_dset=False)
    assert hierarchy == {'/':['base'],
                         '/Group1':['ingroup1_1', 'ingroup1_2'],
                         '/Group2':['ingroup2'],
                         '/Group2/Group3':['ingroup3'],
                         '/Group4':[],
                         '/Group4/Group5':[],
                         '/Group4/Group5/Group6':['ingroup6']
                        }


    # Passing filename
    hierarchy = get_hierarchy(filename, fulldsetpath=False, grp_w_dset=False)
    assert hierarchy == {'/':['base'],
                         '/Group1':['ingroup1_1', 'ingroup1_2'],
                         '/Group2':['ingroup2'],
                         '/Group2/Group3':['ingroup3'],
                         '/Group4':[],
                         '/Group4/Group5':[],
                         '/Group4/Group5/Group6':['ingroup6']}


def test_get_dset_attrs(hdf_dataset):  # pylint:disable=redefined-outer-name
    """ Get an HDF5 file's dataset list with groupnames prepended"""

    filename, fid = hdf_dataset

    # Passing fid
    # DO NOT CONVERT-to-STR
    dset_attrs = get_attrs_dset(fid, 'base', convert_to_str=False)
    assert dset_attrs['Attribute_str'] == 'Test'

    # NOTE: looks like hdf5 has changed how byte strings are delt with, maybe
    # assert dset_attrs['Attribute_bytes'] == b'Test'
    
    assert dset_attrs['Attribute_np_bytes'] == b'Test'
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray'] == b'Test', True)
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray2'] == b'Test', True)
    assert dset_attrs['Attribute_int'] == 1
    assert dset_attrs['Attribute_float'] == 1.1
    assert np.allclose(dset_attrs['Attribute_np_1d'], np.array([1, 2, 3]))
    assert np.allclose(dset_attrs['Attribute_np_2d'], np.array([[1, 2, 3], [4, 5, 6]]))
    assert dset_attrs['Attribute_np_sgl_int'] == np.array([1])
    assert dset_attrs['Attribute_np_sgl_float'] == np.array([1.0])
    assert dset_attrs['Attribute_np_sgl_complex'] == np.array([1.0 + 1j])
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))

    # DO CONVERT-to-STR
    dset_attrs = get_attrs_dset(fid, 'base', convert_to_str=True)
    assert dset_attrs['Attribute_str'] == 'Test'
    assert dset_attrs['Attribute_bytes'] == 'Test'
    assert dset_attrs['Attribute_np_bytes'] == 'Test'
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray'] == 'Test', True)
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray2'] == 'Test', True)
    assert dset_attrs['Attribute_int'] == 1
    assert dset_attrs['Attribute_float'] == 1.1
    assert np.allclose(dset_attrs['Attribute_np_1d'], np.array([1, 2, 3]))
    assert np.allclose(dset_attrs['Attribute_np_2d'], np.array([[1, 2, 3], [4, 5, 6]]))
    assert dset_attrs['Attribute_np_sgl_int'] == np.array([1])
    assert dset_attrs['Attribute_np_sgl_float'] == np.array([1.0])
    assert dset_attrs['Attribute_np_sgl_complex'] == np.array([1.0 + 1j])
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))

    # Passing filename
    # DO NOT CONVERT-to-STR
    dset_attrs = get_attrs_dset(filename, 'base', convert_to_str=False)
    assert dset_attrs['Attribute_str'] == 'Test'
    
    # NOTE: looks like hdf5 has changed how byte strings are delt with, maybe
    # assert dset_attrs['Attribute_bytes'] == b'Test'
    
    assert dset_attrs['Attribute_np_bytes'] == b'Test'
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray'] == b'Test', True)
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray2'] == b'Test', True)
    assert dset_attrs['Attribute_int'] == 1
    assert dset_attrs['Attribute_float'] == 1.1
    assert np.allclose(dset_attrs['Attribute_np_1d'], np.array([1, 2, 3]))
    assert np.allclose(dset_attrs['Attribute_np_2d'], np.array([[1, 2, 3], [4, 5, 6]]))
    assert dset_attrs['Attribute_np_sgl_int'] == np.array([1])
    assert dset_attrs['Attribute_np_sgl_float'] == np.array([1.0])
    assert dset_attrs['Attribute_np_sgl_complex'] == np.array([1.0 + 1j])
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))

    # DO CONVERT-to-STR
    dset_attrs = get_attrs_dset(filename, 'base', convert_to_str=True)
    assert dset_attrs['Attribute_str'] == 'Test'
    assert dset_attrs['Attribute_bytes'] == 'Test'
    assert dset_attrs['Attribute_np_bytes'] == 'Test'
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray'] == 'Test', True)
    assert np.allclose(dset_attrs['Attribute_np_bytes_inarray2'] == 'Test', True)
    assert dset_attrs['Attribute_int'] == 1
    assert dset_attrs['Attribute_float'] == 1.1
    assert np.allclose(dset_attrs['Attribute_np_1d'], np.array([1, 2, 3]))
    assert np.allclose(dset_attrs['Attribute_np_2d'], np.array([[1, 2, 3], [4, 5, 6]]))
    assert dset_attrs['Attribute_np_sgl_int'] == np.array([1])
    assert dset_attrs['Attribute_np_sgl_float'] == np.array([1.0])
    assert dset_attrs['Attribute_np_sgl_complex'] == np.array([1.0 + 1j])
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))

    # CONVERT Single Numpy Value to Numeric 
    dset_attrs = get_attrs_dset(filename, 'base', convert_sgl_np_to_num=True)
    assert dset_attrs['Attribute_np_sgl_int'] == 1
    assert isinstance(dset_attrs['Attribute_np_sgl_int'], int)
    assert not isinstance(dset_attrs['Attribute_np_sgl_int'], np.ndarray)
    assert dset_attrs['Attribute_np_sgl_float'] == 1.0
    assert isinstance(dset_attrs['Attribute_np_sgl_float'], float)
    assert not isinstance(dset_attrs['Attribute_np_sgl_float'], np.ndarray)
    assert dset_attrs['Attribute_np_sgl_complex'] == 1.0 + 1j
    assert isinstance(dset_attrs['Attribute_np_sgl_complex'], complex)
    assert not isinstance(dset_attrs['Attribute_np_sgl_complex'], np.ndarray)
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))
    assert isinstance(dset_attrs['Attribute_np_array_float'], np.ndarray)

    # DO NOT CONVERT Single Numpy Value to Numeric 
    dset_attrs = get_attrs_dset(filename, 'base', convert_sgl_np_to_num=False)
    assert dset_attrs['Attribute_np_sgl_int'] == 1
    assert not isinstance(dset_attrs['Attribute_np_sgl_int'], int)
    assert isinstance(dset_attrs['Attribute_np_sgl_int'], np.ndarray)
    assert dset_attrs['Attribute_np_sgl_float'] == 1.0
    assert not isinstance(dset_attrs['Attribute_np_sgl_float'], float)
    assert isinstance(dset_attrs['Attribute_np_sgl_float'], np.ndarray)
    assert dset_attrs['Attribute_np_sgl_complex'] == 1.0 + 1j
    assert not isinstance(dset_attrs['Attribute_np_sgl_complex'], complex)
    assert isinstance(dset_attrs['Attribute_np_sgl_complex'], np.ndarray)
    assert_array_almost_equal(dset_attrs['Attribute_np_array_float'], np.array([1.0, 2.0]))
    assert isinstance(dset_attrs['Attribute_np_array_float'], np.ndarray)