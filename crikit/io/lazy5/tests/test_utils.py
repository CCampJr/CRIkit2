""" Test HDF-related utilities """
import os

import pytest

import h5py
import numpy as np

import crikit.io.lazy5 as lazy5
from crikit.io.lazy5.utils import (FidOrFile, hdf_is_open, fullpath)

@pytest.fixture(scope="module")
def hdf_dataset():
    """ Setups and tears down a sample HDF5 file """
    filename = 'temp_test_utils.h5'
    fid = h5py.File(filename, 'w')
    data_m, data_n, data_p = [20, 22, 24]
    data = np.random.randn(data_m, data_n, data_p)
    fid.create_dataset('base', data=data)

    yield filename, fid

    # Tear-down
    if hdf_is_open(fid):
        fid.close()
    os.remove(filename)

def test_fid_or_file_filename_provided(hdf_dataset):
    """ Test FidOrFile Class with provided filename """
    filename, _ = hdf_dataset

    fof = FidOrFile(filename)
    
    # ! New h5py v 2.9.*: id instead of fid
    try:
        status = fof.fid.id.valid
    except AttributeError:
        status = fof.fid.fid.valid

    assert status == 1
    assert fof.fid is not None
    assert not fof.is_fid

    fof.fid.close()

def test_fid_or_file_fid_provided(hdf_dataset):
    """ Test FidOrFile Class with provided fid """
    _, fid = hdf_dataset

    fof = FidOrFile(fid)
    # ! New h5py v 2.9.*: id instead of fid
    try:
        status = fof.fid.id.valid
    except AttributeError:
        status = fof.fid.fid.valid

    assert status == 1
    assert fof.fid is not None
    assert fof.is_fid

def test_fid_or_file_close_if_not_fid(hdf_dataset):
    """ Test close if filename was provided """
    filename, fid = hdf_dataset

    fof = FidOrFile(fid)
    fof.close_if_file_not_fid()
    # ! New h5py v 2.9.*: id instead of fid
    try:
        status = fof.fid.id.valid
    except AttributeError:
        status = fof.fid.fid.valid

    assert status == 1

    fof = FidOrFile(filename)
    fof.close_if_file_not_fid()
    # ! New h5py v 2.9.*: id instead of fid
    try:
        status = fof.fid.id.valid
    except AttributeError:
        status = fof.fid.fid.valid

    assert status == 0

def test_hdf_is_open(hdf_dataset):
    """ Test hdf_is_open function """
    _, fid = hdf_dataset

    assert hdf_is_open(fid)
    fid.close()

    assert not hdf_is_open(fid)

def test_fullpath():
    """ Test full path """
    fp = fullpath(filename=None,pth=None)
    assert fp is None

    fn = 'test.XYZ'
    p = 'Dir1/Dir2'

    fp = fullpath(filename=fn,pth=None)
    assert fp == fn

    fp = fullpath(filename=fn, pth=p)
    assert fp == os.path.join(p, fn)