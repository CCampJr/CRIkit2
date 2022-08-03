import os
import time

import numpy as np
import pytest
import h5py

import crikit.io.lazy5 as lazy5

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
    except Exception:
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

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((5, 2)).shape == (5*3, 2*4)

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((5, 2)).shape == (5*3, 2*4)

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

    mos.parameters['Order'] = 'R'
    mos.mosaicfull((m_ct, n_ct), out=fid_out[dset_out_name])

    assert np.allclose(fid_out[dset_out_name], orig_data_np)

    fid_in.close()
    fid_out.close()

    time.sleep(1)
    try:
        os.remove(filename_in)
    except Exception:
        print('Could not delete {}'.format(filename_in))

    time.sleep(1)
    try:
        os.remove(filename_out)
    except Exception:
        print('Could not delete {}'.format(filename_out))

def test_big_to_small_3d_output_given_crop():
    """ 3D big dataset, divied up into small chunks -- WITH CROPPING """
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
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1

    ct = 0
    for ni in range(n_ct):
        for mi in range(m_ct):
            mos.append(fid_in[dset_in_prefix+'{}'.format(ct)])
            ct += 1

    filename_out = 'test_h5mosaic_out.h5'
    dset_out_name = 'dset'

    fid_out = h5py.File(filename_out, 'w')
    fid_out.create_dataset(dset_out_name, shape=mos.mosaic_shape((m_ct, n_ct)),
                           dtype=orig_data_np.dtype)

    mos.parameters['Order'] = 'R'
    mos.mosaicfull((m_ct, n_ct), out=fid_out[dset_out_name])

    assert np.allclose(fid_out[dset_out_name][0:3,0:3,:],
                       orig_data_np[1:4, 1:4, :])
    assert np.allclose(fid_out[dset_out_name][8:11, 0:3, :],
                       orig_data_np[11:14, 1:4, :])

    assert np.allclose(fid_out[dset_out_name][0:3, 8:11, :],
                       orig_data_np[1:4, 11:14, :])

    fid_in.close()
    fid_out.close()

    time.sleep(1)
    try:
        os.remove(filename_in)
    except Exception:
        print('Could not delete {}'.format(filename_in))

    time.sleep(1)
    try:
        os.remove(filename_out)
    except Exception:
        print('Could not delete {}'.format(filename_out))

def test_big_to_small_3d_output_given_crop_transpose_flips():
    """
    3D big dataset, divied up into small chunks -- WITH CROPPING, TRANSPOSING
    AND FLIPPING H & V

    Note: This test does not assert anything, but rather just ensures the methods
    can run without raising errors
    """
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
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1
    mos.parameters['Transpose'] = True
    mos.parameters['FlipVertical'] = True
    mos.parameters['FlipHorizontally'] = True

    ct = 0
    for ni in range(n_ct):
        for mi in range(m_ct):
            mos.append(fid_in[dset_in_prefix+'{}'.format(ct)])
            ct += 1

    filename_out = 'test_h5mosaic_out.h5'
    dset_out_name = 'dset'

    fid_out = h5py.File(filename_out, 'w')
    fid_out.create_dataset(dset_out_name, shape=mos.mosaic_shape((m_ct, n_ct)),
                           dtype=orig_data_np.dtype)

    mos.parameters['Order'] = 'R'
    mos.mosaicfull((m_ct, n_ct), out=fid_out[dset_out_name])

    fid_in.close()
    fid_out.close()

    time.sleep(1)
    try:
        os.remove(filename_in)
    except Exception:
        print('Could not delete {}'.format(filename_in))

    time.sleep(1)
    try:
        os.remove(filename_out)
    except Exception:
        print('Could not delete {}'.format(filename_out))
