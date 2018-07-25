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
    assert mos.mosaic_shape((2,2)) is None
    assert mos.mosaic2d((2,2)) is None
    assert mos.mosaicfull((2,2)) is None

def test_crop_2D():
    """ Test a 2D dataset with cropped rows and columns """
    mos = Mosaic()
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1

    m_obj = 3
    n_obj = 4

    # MANUALLY SET BASED ON PARAMS ABOVE
    m_obj_crop = m_obj - 2
    n_obj_crop = n_obj - 2

    new_obj = np.ones((m_obj, n_obj))
    m_side = 2
    n_side = 2

    n = m_side * n_side

    for ct in range(n):
        mos.append(new_obj)

    # NOT AFFECTED BY START* END*
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float

    # AFFECTED BY START* END*
    assert mos.unitshape == (m_obj_crop, n_obj_crop)
    assert mos.unitshape_orig == (m_obj, n_obj)

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

def test_crop_3D():
    """ Test a 2D dataset with cropped rows and columns """
    mos = Mosaic()
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1

    m_obj = 3
    n_obj = 4
    p_obj = 5

    # MANUALLY SET BASED ON PARAMS ABOVE
    m_obj_crop = m_obj - 2
    n_obj_crop = n_obj - 2
    p_obj_crop = p_obj

    new_obj = np.ones((m_obj, n_obj, p_obj))
    m_side = 2
    n_side = 2

    n = m_side * n_side

    for ct in range(n):
        mos.append(new_obj)

    # NOT AFFECTED BY START* END*
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float

    # AFFECTED BY START* END*
    assert mos.unitshape == (m_obj_crop, n_obj_crop, p_obj_crop)
    assert mos.unitshape_orig == (m_obj, n_obj, p_obj)

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop,
                                                      p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == (m_side * m_obj_crop, n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj_crop, n_side * n_obj_crop,
                                                      p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

def test_3D_crop_transpose_flips():
    """ Test a 2D dataset with cropped rows and columns """
    mos = Mosaic()
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1
    mos.parameters['Transpose'] = True
    mos.parameters['FlipVertical'] = True
    mos.parameters['FlipHorizontally'] = True

    m_obj = 3
    n_obj = 4
    p_obj = 5

    # MANUALLY SET BASED ON PARAMS ABOVE
    m_obj_crop = m_obj - 2
    n_obj_crop = n_obj - 2
    p_obj_crop = p_obj

    new_obj = np.ones((m_obj, n_obj, p_obj))
    m_side = 2
    n_side = 2

    n = m_side * n_side

    for ct in range(n):
        mos.append(new_obj)

    # NOT AFFECTED BY START* END*
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float

    # AFFECTED BY START* END*
    assert mos.unitshape == (m_obj_crop, n_obj_crop, p_obj_crop)
    assert mos.unitshape_orig == (m_obj, n_obj, p_obj)

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                             n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                       n_side * n_obj_crop,
                                                                       p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                             n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                       n_side * n_obj_crop,
                                                                       p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

def test_3D_crop_transpose_flips_2():
    """ Test a 2D dataset with cropped rows and columns (asymmetrically) """
    mos = Mosaic()
    mos.parameters['StartR'] = 2
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1
    mos.parameters['Transpose'] = True
    mos.parameters['FlipVertical'] = True
    mos.parameters['FlipHorizontally'] = True

    m_obj = 5
    n_obj = 6
    p_obj = 7

    # MANUALLY SET BASED ON PARAMS ABOVE
    m_obj_crop = m_obj - 3
    n_obj_crop = n_obj - 2
    p_obj_crop = p_obj

    new_obj = np.ones((m_obj, n_obj, p_obj))
    m_side = 2
    n_side = 2

    n = m_side * n_side

    for ct in range(n):
        mos.append(new_obj)

    # NOT AFFECTED BY START* END*
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == np.float

    # AFFECTED BY START* END*
    assert mos.unitshape == (m_obj_crop, n_obj_crop, p_obj_crop)
    assert mos.unitshape_orig == (m_obj, n_obj, p_obj)

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                             n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                       n_side * n_obj_crop,
                                                                       p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                             n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                       n_side * n_obj_crop,
                                                                       p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

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

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

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

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side), idx=0)
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj, p_obj)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == (m_side * m_obj, n_side * n_obj)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side), idx=0)
    assert mos.mosaicfull((m_side, n_side)).shape == (m_side * m_obj, n_side * n_obj, p_obj)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

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

    mos.parameters['Order'] = 'R'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct)), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

    mos.parameters['Order'] = 'C'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct)), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

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

    mos.parameters['Order'] = 'R'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct)), orig_data)
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

    mos.parameters['Order'] = 'C'
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct)), orig_data)
    assert not np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

def test_big_to_small_3d():
    orig_data = np.random.randn(40,5,3)

    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ct in range(m_ct):
        mos.append(orig_data[ct*m_unit_size:(ct+1)*m_unit_size, ...])

    mos.parameters['Order'] = 'R'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0), orig_data[...,0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1), orig_data[...,1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2), orig_data[...,2])
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

    mos.parameters['Order'] = 'C'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0), orig_data[...,0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1), orig_data[...,1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2), orig_data[...,2])
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

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

    mos.parameters['Order'] = 'R'
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0), orig_data[..., 0])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1), orig_data[..., 1])
    assert np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2), orig_data[..., 2])
    assert np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)

    mos.parameters['Order'] = 'C'
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=0), orig_data[..., 0])
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=1), orig_data[..., 1])
    assert not np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), idx=2), orig_data[..., 2])
    assert not np.allclose(mos.mosaicfull(shape=(m_ct, n_ct)), orig_data)


def test_big_to_small_3d_output_given():
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

    output_data = np.zeros(orig_data.shape[:-1], dtype=orig_data.dtype)
    id_in = id(output_data)

    mos.parameters['Order'] = 'R'
    mos.mosaic2d(shape=(m_ct, n_ct), idx=0, out=output_data)
    id_out = id(output_data)
    assert np.allclose(output_data, orig_data[..., 0])
    assert id_in == id_out

    output_data = np.zeros(orig_data.shape[:-1], dtype=orig_data.dtype)
    mos.mosaic2d(shape=(m_ct, n_ct), idx=1, out=output_data)
    assert np.allclose(output_data, orig_data[..., 1])

    output_data = np.zeros(orig_data.shape[:-1], dtype=orig_data.dtype)
    mos.mosaic2d(shape=(m_ct, n_ct), idx=2, out=output_data)
    assert np.allclose(output_data, orig_data[..., 2])

    output_data = np.zeros(orig_data.shape, dtype=orig_data.dtype)
    mos.mosaicfull(shape=(m_ct, n_ct), out=output_data)
    assert np.allclose(output_data, orig_data)

    mos.parameters['Order'] = 'C'
    output_data = np.zeros(orig_data.shape, dtype=orig_data.dtype)
    mos.mosaicfull(shape=(m_ct, n_ct), out=output_data)
    assert not np.allclose(output_data, orig_data)
