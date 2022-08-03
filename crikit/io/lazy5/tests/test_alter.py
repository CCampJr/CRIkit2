""" Test inspection of HDF5 files """
import os
import time

from collections import OrderedDict as _OrderedDict

import h5py
import pytest

import numpy as np

from crikit.io.lazy5.utils import hdf_is_open
from crikit.io.lazy5.alter import alter_attr_same, alter_attr, write_attr_dict

@pytest.fixture(scope="function")
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
    fid['base'].attrs.create('Attribute_int', 1)
    fid['base'].attrs.create('Attribute_float', 1.1)
    fid['base'].attrs.create('Attribute_np_1d', np.array([1, 2, 3]))
    fid['base'].attrs.create('Attribute_np_2d', np.array([[1, 2, 3], [4, 5, 6]]))

    yield filename, fid

    # Tear-down
    if hdf_is_open(fid):
        fid.close()

    time.sleep(1)
    try:
        os.remove(filename)
    except Exception:
        print('Could not delete {}'.format(filename))


def test_attr_alter_same(hdf_dataset):
    """ Try altering an attribute with the same type of value type """

    _, fid = hdf_dataset
    dset_obj = fid['base']
    attr_obj = dset_obj.attrs

    # Try new attrbute
    orig_key = 'Attribute_new'
    new_val = 'Test2'
    alter_attr_same(dset_obj, orig_key, new_val)
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_new2'
    new_val = 'Test2'
    with pytest.raises(KeyError):
        alter_attr_same(dset_obj, orig_key, new_val, must_exist=True)

    # Try same-type writes first
    orig_key = 'Attribute_str'
    orig_val = attr_obj[orig_key]
    new_val = 'Test2'
    alter_attr_same(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    # NOTE: looks like hdf5 has changed how byte strings are delt with, maybe
    # orig_key = 'Attribute_bytes'
    # orig_val = attr_obj[orig_key]
    # new_val = b'Test2'
    # alter_attr_same(dset_obj, orig_key, new_val)
    # assert orig_val != attr_obj[orig_key]
    # assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_bytes'
    orig_val = attr_obj[orig_key]
    new_val = np.bytes_('Test2')  # pylint: disable=E1101
    alter_attr_same(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_int'
    orig_val = attr_obj[orig_key]
    new_val = 2
    alter_attr_same(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_float'
    orig_val = attr_obj[orig_key]
    new_val = 2.2
    alter_attr_same(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_1d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([4, 5, 6])
    alter_attr_same(dset_obj, orig_key, new_val)
    assert np.allclose(attr_obj[orig_key], new_val)

    orig_key = 'Attribute_np_2d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([[7, 8, 9], [10, 11, 12]])
    alter_attr_same(dset_obj, orig_key, new_val)
    assert np.allclose(attr_obj[orig_key], new_val)

    # Try DIFFERENT-type writes first
    orig_key = 'Attribute_str'
    orig_val = attr_obj[orig_key]
    new_val = 1
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)

    # NOTE: looks like hdf5 has changed how byte strings are delt with, maybe
    # orig_key = 'Attribute_bytes'
    # orig_val = attr_obj[orig_key]
    # new_val = 'Test2'
    # with pytest.raises(TypeError):
    #     alter_attr_same(dset_obj, orig_key, new_val)

    orig_key = 'Attribute_np_bytes'
    orig_val = attr_obj[orig_key]
    new_val = 'Test2'
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)

    orig_key = 'Attribute_int'
    orig_val = attr_obj[orig_key]
    new_val = True
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)

    orig_key = 'Attribute_float'
    orig_val = attr_obj[orig_key]
    new_val = 2
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)

    orig_key = 'Attribute_np_1d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([4.1, 5.1, 6.1])
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)

    orig_key = 'Attribute_np_2d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([[7, 8.1, 9], [10, 11, 12.1]])
    with pytest.raises(TypeError):
        alter_attr_same(dset_obj, orig_key, new_val)


def test_attr_alter(hdf_dataset):
    """ Try altering an attribute with the same or different type of value"""

    filename, fid = hdf_dataset
    dset_obj = fid['base']
    attr_obj = dset_obj.attrs

    # Try new attrbute (dset_obj)
    orig_key = 'Attribute_new'
    new_val = 'Test2'
    assert attr_obj.get(orig_key) is None
    alter_attr(dset_obj, orig_key, new_val)
    assert attr_obj[orig_key] == new_val

    # Try new attrbute (dset_obj)
    orig_key = 'Attribute_new2'
    new_val = 'Test2'
    assert attr_obj.get(orig_key) is None
    with pytest.raises(TypeError):
        alter_attr([], orig_key, new_val, file=fid)
    alter_attr(dset_obj, orig_key, new_val, file=fid)
    assert attr_obj[orig_key] == new_val

    # Try new attrbute (given filename)
    orig_key = 'Attribute_new3'
    new_val = 'Test3'
    with pytest.raises(TypeError):
        alter_attr(dset_obj, orig_key, new_val, file=filename)
    alter_attr('base', orig_key, new_val, file=filename)
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_new4'
    new_val = 'Test2'
    with pytest.raises(KeyError):
        alter_attr(dset_obj, orig_key, new_val, must_exist=True)

    # Try same-type writes
    orig_key = 'Attribute_str'
    orig_val = attr_obj[orig_key]
    new_val = 'Test2'
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    # NOTE: looks like hdf5 has changed how byte strings are delt with, maybe
    # orig_key = 'Attribute_bytes'
    # orig_val = attr_obj[orig_key]
    # new_val = b'Test2'
    # alter_attr(dset_obj, orig_key, new_val)
    # assert orig_val != attr_obj[orig_key]
    # assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_bytes'
    orig_val = attr_obj[orig_key]
    new_val = np.bytes_('Test2')  # pylint: disable=E1101
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_int'
    orig_val = attr_obj[orig_key]
    new_val = 2
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_float'
    orig_val = attr_obj[orig_key]
    new_val = 2.2
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_1d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([4, 5, 6])
    alter_attr(dset_obj, orig_key, new_val)
    assert np.allclose(attr_obj[orig_key], new_val)

    orig_key = 'Attribute_np_2d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([[7, 8, 9], [10, 11, 12]])
    alter_attr(dset_obj, orig_key, new_val)
    assert np.allclose(attr_obj[orig_key], new_val)

    # Try DIFFERENT-type writes first
    orig_key = 'Attribute_str'
    orig_val = attr_obj[orig_key]
    new_val = 1
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_bytes'
    orig_val = attr_obj[orig_key]
    new_val = 'Test2'
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_bytes'
    orig_val = attr_obj[orig_key]
    new_val = 'Test2'
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_int'
    orig_val = attr_obj[orig_key]
    new_val = True
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_float'
    orig_val = attr_obj[orig_key]
    new_val = 2
    alter_attr(dset_obj, orig_key, new_val)
    assert orig_val != attr_obj[orig_key]
    assert attr_obj[orig_key] == new_val

    orig_key = 'Attribute_np_1d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([4.1, 5.1, 6.1])
    alter_attr(dset_obj, orig_key, new_val)
    assert not np.allclose(orig_val, attr_obj[orig_key])
    assert np.allclose(attr_obj[orig_key], new_val)

    orig_key = 'Attribute_np_2d'
    orig_val = attr_obj[orig_key]
    new_val = np.array([[7, 8.1, 9], [10, 11, 12.1]])
    alter_attr(dset_obj, orig_key, new_val)
    assert not np.allclose(orig_val, attr_obj[orig_key])
    assert np.allclose(attr_obj[orig_key], new_val)

    # Try providing dset as str but no file
    orig_key = 'Attribute_int'
    new_val = 3
    with pytest.raises(TypeError):
        alter_attr('base', orig_key, new_val)

def test_write_attr_dict(hdf_dataset):
    """ Try writing dictionary of attributes """

    filename, fid = hdf_dataset
    dset_obj = fid['base']
    
    attr_dict = _OrderedDict([['WDA2', 2], ['WDA1', 1]])
    
    # Write via dset obj
    assert write_attr_dict(dset_obj, attr_dict, fid=None, sort_attrs=False, verbose=False)
    assert dset_obj.attrs['WDA2'] == 2
    assert dset_obj.attrs['WDA1'] == 1
    assert dset_obj.attrs['Attribute_str'] == 'Test'
    l_attr = list(dset_obj.attrs.keys())

    # Order should be that written
    l_attr[-2] == 'WDA2'
    l_attr[-1] == 'WDA1'

    # Write via dset str MISSING fid
    with pytest.raises(TypeError):
        write_attr_dict('base', attr_dict, fid=None, sort_attrs=False, verbose=False)

    # Write via dset str
    assert write_attr_dict('base', attr_dict, fid=fid, sort_attrs=False, verbose=False)
    assert dset_obj.attrs['WDA2'] == 2
    assert dset_obj.attrs['WDA1'] == 1
    assert dset_obj.attrs['Attribute_str'] == 'Test'

    # Write via dset str and SORT attr
    assert write_attr_dict('base', attr_dict, fid=fid, sort_attrs=True, verbose=False)
    assert dset_obj.attrs['WDA2'] == 2
    assert dset_obj.attrs['WDA1'] == 1

    # Order should be sorted. WDA* are the last alphanumerically in this test file
    l_attr = list(dset_obj.attrs.keys())
    l_attr[-1] == 'WDA2'
    l_attr[-2] == 'WDA1'