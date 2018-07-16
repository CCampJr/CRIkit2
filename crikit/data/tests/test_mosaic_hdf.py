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

# def test_2D_uniform_obj():
#     mos = Mosaic()
    
#     m_obj = 3
#     n_obj = 4
    
#     new_obj = np.ones((m_obj, n_obj))
#     m_side = 2
#     n_side = 2
    
#     n = m_side * n_side
    
#     for ct in range(n):
#         mos.append(new_obj)
    
#     assert mos.shape == tuple(n*[new_obj.shape])
#     assert mos.size == n
#     assert mos.issamedim
#     assert mos.dtype == np.float
#     assert mos.unitshape == (m_obj, n_obj)
#     assert mos.unitshape_orig == (m_obj, n_obj)
#     assert mos.mosaic2d((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj)
#     assert mos.mosaic2d((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj)

#     assert mos.mosaicfull((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj)
#     assert mos.mosaicfull((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj)

# def test_3D_uniform_obj():
#     mos = Mosaic()
    
#     m_obj = 3
#     n_obj = 4
#     p_obj = 2

#     new_obj = np.ones((m_obj, n_obj, p_obj))

#     m_side = 2
#     n_side = 2
    
#     n = m_side * n_side
    
#     for ct in range(n):
#         mos.append(new_obj)
    
#     assert mos.shape == tuple(n*[new_obj.shape])
#     assert mos.size == n
#     assert mos.issamedim
#     assert mos.dtype == np.float
#     with pytest.raises(ValueError):
#         mos.mosaic2d((m_side, n_side)).shape
#     assert mos.mosaic2d((m_side, n_side), idx=0, order='R').shape == (m_side * m_obj, n_side * n_obj)
#     assert mos.mosaic2d((m_side, n_side), idx=0, order='C').shape == (m_side * m_obj, n_side * n_obj)
#     assert mos.mosaicfull((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj, p_obj)
#     assert mos.mosaicfull((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj, p_obj)

# def test_err_wrong_dim():
#     mos = Mosaic()

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(5))

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(2,2,2,2))

# def test_err_wrong_dim_append():

#     # Start with 2D
#     mos = Mosaic()
#     mos.append(np.random.randn(3,4))

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(5))

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(3,4,5))

#     # Start with 3D
#     mos = Mosaic()
#     mos.append(np.random.randn(3,4,2))

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(5))

#     with pytest.raises(TypeError):
#         mos.append(np.random.randn(3,5))