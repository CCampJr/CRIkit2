import numpy as np
import pytest

from crikit.data.mosaic import Mosaic

def test_blank():
    mos = Mosaic()
    assert mos.shape is None
    assert mos.size is None
    assert mos.issamedim is None
    assert mos.issamedim is None
    assert mos.dtype is None
    assert mos.mosaic2d((2,2)) is None
    assert mos.mosaicfull((2,2)) is None

def test_2D_uniform_obj():
    mos = Mosaic()
    
    m_obj = 3
    n_obj = 4
    
    new_obj = np.ones((m_obj, n_obj))
    m_side = 2
    n_side = 2
    
    n = m_side * n_side
    
    for ct in range(n):
        mos.append(new_obj)
    
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float
    assert mos.unitshape == (m_obj, n_obj)
    assert mos.unitshape_orig == (m_obj, n_obj)
    assert mos.mosaic2d((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj)

    assert mos.mosaicfull((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaicfull((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj)

def test_3D_uniform_obj():
    mos = Mosaic()
    
    m_obj = 3
    n_obj = 4
    p_obj = 2

    new_obj = np.ones((m_obj, n_obj, p_obj))

    m_side = 2
    n_side = 2
    
    n = m_side * n_side
    
    for ct in range(n):
        mos.append(new_obj)
    
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float
    with pytest.raises(ValueError):
        mos.mosaic2d((m_side, n_side)).shape
    assert mos.mosaic2d((m_side, n_side), idx=0, order='R').shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side), idx=0, order='C').shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaicfull((m_side, n_side), order='R').shape == (m_side * m_obj, n_side * n_obj, p_obj)
    assert mos.mosaicfull((m_side, n_side), order='C').shape == (m_side * m_obj, n_side * n_obj, p_obj)

def test_err_wrong_dim():
    mos = Mosaic()

    with pytest.raises(TypeError):
        mos.append(np.random.randn(5))

    with pytest.raises(TypeError):
        mos.append(np.random.randn(2,2,2,2))

def test_err_wrong_dim_append():

    # Start with 2D
    mos = Mosaic()
    mos.append(np.random.randn(3,4))

    with pytest.raises(TypeError):
        mos.append(np.random.randn(5))

    with pytest.raises(TypeError):
        mos.append(np.random.randn(3,4,5))

    # Start with 3D
    mos = Mosaic()
    mos.append(np.random.randn(3,4,2))

    with pytest.raises(TypeError):
        mos.append(np.random.randn(5))

    with pytest.raises(TypeError):
        mos.append(np.random.randn(3,5))

def test_big_to_small_2d():
    orig_data = np.random.randn(40,5)
    
    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ct in range(m_ct):
        mos.append(orig_data[ct*m_unit_size:(ct+1)*m_unit_size,:])

    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R'), orig_data)
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='C'), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='R'), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='C'), orig_data)

def test_big_to_small_2d_2():
    orig_data = np.random.randn(40,10)
    
    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ni in range(n_ct):
        for mi in range(m_ct):
            mos.append(orig_data[mi*m_unit_size:(mi+1)*m_unit_size,
                                 ni*n_unit_size:(ni+1)*n_unit_size])

    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R'), orig_data)
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='C'), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='R'), orig_data)
    assert not np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='C'), orig_data)

def test_big_to_small_3d():
    orig_data = np.random.randn(40,5,3)
    
    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ct in range(m_ct):
        mos.append(orig_data[ct*m_unit_size:(ct+1)*m_unit_size, ...])

    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R', idx=0), orig_data[...,0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='C', idx=0), orig_data[...,0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R', idx=1), orig_data[...,1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='C', idx=1), orig_data[...,1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R', idx=2), orig_data[...,2])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='C', idx=2), orig_data[...,2])
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='R'), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='C'), orig_data)

def test_big_to_small_3d_2():
    orig_data = np.random.randn(40,10, 3)
    
    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ni in range(n_ct):
        for mi in range(m_ct):
            mos.append(orig_data[mi*m_unit_size:(mi+1)*m_unit_size,
                                 ni*n_unit_size:(ni+1)*n_unit_size, :])

    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0, order='R'), orig_data[..., 0])
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0, order='C'), orig_data[..., 0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1, order='R'), orig_data[..., 1])
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1, order='C'), orig_data[..., 1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2, order='R'), orig_data[..., 2])
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2, order='C'), orig_data[..., 2])
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='R'), orig_data)
    assert not np.allclose(mos.mosaicfull(shape=(m_ct, n_ct), order='C'), orig_data)