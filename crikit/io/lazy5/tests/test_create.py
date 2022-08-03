""" Test creation of HDF5 files """
import os
import time

import pytest

import numpy as np
import h5py

from crikit.io.lazy5.create import save
from crikit.io.lazy5.utils import FidOrFile


def test_save_no_attrs():
    data = np.random.randn(20,20)
    filename = 'temp_create.h5'
    dset_name = '/Group1/Dset'
    save(filename, dset_name, data, mode='w')

    fof = FidOrFile(filename)
    fid = fof.fid
    assert np.allclose(fid[dset_name], data)
    fof.close_if_file_not_fid()

    # Test re-write
    data = np.random.randn(20,20)
    save(filename, dset_name, data, mode='w')
    fof = FidOrFile(filename)
    fid = fof.fid
    assert np.allclose(fid[dset_name], data)
    fof.close_if_file_not_fid()

    # Test re-write when overwrite of dset set to False
    data = np.random.randn(20,20)
    with pytest.raises(IOError):
        save(filename, dset_name, data, dset_overwrite=False)

    # Test re-write with attributes
    data = np.random.randn(20,20)
    attr_dict = {'AT1':1, 'AT2':2}
    save(filename, dset_name, data, attr_dict=attr_dict, mode='w')

    fof = FidOrFile(filename)
    fid = fof.fid
    assert fid[dset_name].attrs['AT1'] == 1
    assert fid[dset_name].attrs['AT2'] == 2
    with pytest.raises(KeyError):
        fid[dset_name].attrs['DOESNOTEXIST'] == 2

    fof.close_if_file_not_fid()

    time.sleep(1)
    try:
        os.remove(filename)
    except Exception:
        print('Could not delete {}'.format(filename))


def test_save_diff_path():
    data = np.random.randn(20,20)
    filename = 'temp_create2.h5'
    dset_name = '/Group1/Dset'
    
    pth = './temp_test'
    os.mkdir(pth)

    save(filename, dset_name, data, pth=pth, mode='w')

    fp = os.path.join(pth, filename)

    assert os.path.isdir(pth)
    assert os.path.isfile(fp)
    assert os.path.getsize(fp) >= data.nbytes

    os.remove(fp)
    os.rmdir(pth)

def test_save_to_open_h5_file():
    """ Test saving to an H5 file where the H5 file id is passed """

    data = np.random.randn(20,20)
    filename = 'temp_create2.h5'
    dset_name = '/Group1/Dset'
    
    pth = './temp_test'
    os.mkdir(pth)
    assert os.path.isdir(pth)

    fp = os.path.join(pth, filename)
    with h5py.File(fp, 'w') as fid:
        save(fid, dset_name, data, pth=pth, mode='w')

    assert os.path.isfile(fp)
    assert os.path.getsize(fp) >= data.nbytes

    os.remove(fp)
    os.rmdir(pth)

def test_save_to_open_wrong_type():
    """ Test saving to an inappripriate input (not string or h5 file fid) """

    with pytest.raises(TypeError):
        save(123, 'Name', np.random.rand(10,10), pth=None, mode='w')
