import os
import time

import numpy as np
import pytest
import h5py

import lazy5

from crikit.data.mosaic import Mosaic

@pytest.fixture(scope="module")
def hdf_dataset2():
    """ Setups and tears down a sample HDF5 file """
    filename = 'temp_test.h5'
    fid = h5py.File(filename, 'w')
    # data_m, data_n, data_p = [3, 4, 24]
    data_m, data_n = [3, 4]
    data = np.random.randn(data_m, data_n)

    N = 10
    for n in range(N):
        fid.create_dataset('img_z{}'.format(n), data=data)

    yield filename, fid

    # Tear-down
    if lazy5.utils.hdf_is_open(fid):
        fid.close()

    time.sleep(1)
    try:
        os.remove(filename)
    except:
        print('Could not delete {}'.format(filename))

def test_hdf2(hdf_dataset2):
    filename, fid = hdf_dataset2

    dset_list = lazy5.inspect.get_datasets(fid)
    mos = Mosaic()
    for n in range(10):
        mos.append(fid[dset_list[n]])

    # assert mos.shape is None
    assert mos.size == 10
    assert mos.issamedim
    assert mos.mosaic2d((5, 2), order='R').shape == (5*3, 2*4)
    assert mos.mosaic2d((5, 2), order='C').shape == (5*3, 2*4)

def test_big_to_small_3d_output_given():
    orig_data_np = np.random.randn(40, 10, 3)

    filename_in = 'test_h5mosaic_in.h5'
    dset_in_prefix = 'dset_'
    fid_in = h5py.File(filename_in, 'w')

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data_np.shape[0]//m_unit_size
    n_ct = orig_data_np.shape[1]//n_unit_size

    ct = 0
    for ni in range(n_ct):
        for mi in range(m_ct):
            temp = orig_data_np[mi*m_unit_size:(mi+1)*m_unit_size,
                                ni*n_unit_size:(ni+1)*n_unit_size, :]
            fid_in.create_dataset(dset_in_prefix+'{}'.format(ct), shape=temp.shape, data=temp)
            ct += 1

    fid_in.close()

    fid_in = h5py.File(filename_in, 'r')
    mos = Mosaic()

    ct = 0
    for ni in range(n_ct):
        for mi in range(m_ct):
            mos.append(fid_in[dset_in_prefix+'{}'.format(ct)])
            ct += 1

    filename_out = 'test_h5mosaic_out.h5'
    dset_out_name = 'dset'

    fid_out = h5py.File(filename_out, 'w')
    fid_out.create_dataset(dset_out_name, shape=orig_data_np.shape, data=np.zeros(orig_data_np.shape))

    mos.mosaicfull((m_ct, n_ct), out=fid_out[dset_out_name], order='R')

    assert np.allclose(fid_out[dset_out_name], orig_data_np)

    fid_in.close()
    fid_out.close()

    time.sleep(1)
    try:
        os.remove(filename_in)
    except:
        print('Could not delete {}'.format(filename_in))

    time.sleep(1)
    try:
        os.remove(filename_out)
    except:
        print('Could not delete {}'.format(filename_out))
