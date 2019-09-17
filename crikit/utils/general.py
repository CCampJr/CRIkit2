"""
General utilities

    expand_1d_to_ndim_data : Match 1D data array dimensionality to that of \
        another array

    expand_1d_to_ndim : Expand 1D data array dimensionality to ndim

    find_nearest : Given a vector and a value, find the index and value
        of the closest match

    pad : Wrapper around numpy.pad that also returns a window defining the
        original signal

Notes
-----
"""
import numpy as _np

def pad(y, pad_width, mode):
    """
    Pad array with either constants or edge values.

    Note: For N-D arrays, pads the -1 axis

    Parameters
    ----------
    y : ndarray
        Input array

    pad_width : int
        Size of padding on each side of y

    mode : str
        'constant' (0), 'edge' currently accepted

    Returns
    -------
    y_pad, window
        Padded array and window. Window defines the region of the original signal
    """
    if pad_width <= 0:
        return y, _np.ones(y.shape[-1])
    else:
        shaper = list(y.shape)
        shaper_out = list(y.shape)
        shaper_out[-1] += 2*pad_width
        y_pad = _np.zeros(shaper_out, dtype=y.dtype)
        window = _np.zeros(shaper_out[-1], dtype=_np.integer)
        
        y_pad[...,pad_width:shaper[-1]+pad_width] = 1*y
        window[pad_width:shaper[-1]+pad_width] = 1

        if (mode == 'zeros') | (mode == 'constant') | (mode == 'zero'):
            pass
        elif mode == 'edge':
            y_pad[...,:pad_width] = _np.dot(y[...,0:1], _np.ones((1, pad_width)))
            y_pad[..., -pad_width:] = _np.dot(y[...,-1:-2:-1], _np.ones((1, pad_width)))

        return y_pad, window

def pad_dual(y, edge_pad_width, constant_pad_width):
    """
    Pad array with edge values followed by constant 0's.

    Note: For N-D arrays, pads the -1 axis

    Parameters
    ----------
    y : ndarray
        Input array

    edge_pad_width : int
        Size of edge-value padding on each side of y

    constant_pad_width : int
        Size of 0-padding on each side of y after edge-value padding

    Returns
    -------
    y_pad, window
        Padded array and window. Window defines the region of the original signal
    """
    y_pad_edge, win_edge = pad(y, edge_pad_width, 'edge')
    y_pad, win_constant = pad(y_pad_edge, constant_pad_width, 'constant')
    
    window = 0*win_constant
    window[_np.where(win_constant == 1)[0][win_edge == 1]] = 1

    return y_pad, window

def pad_edge_mean(y, pad_width, n_edge=1, axis=-1):
    """
    Pad data y with edge-values or near-edge mean values along axis
    
    Parameters
    ----------
    
    y : ndarray
        Input array
        
    pad_width : int
        Size of padding on each side of y
        
    n_edge : int
        Number of edge points to average for the pad value
        
    axis : int
        Axis to pad
        
    Returns
    -------
    (y_pad, window)
    
    y_pad : ndarray
        Padded y
        
    window : ndarray (1D)
        Mask with 0's for pad regions, 1's for original size
        
    """
    if pad_width == 0:  # No padding
        window = _np.ones((y.shape[axis]), dtype=_np.integer)
        y_pad = y
    elif pad_width > 0:
        orig_shape = y.shape
        pad_shape = list(orig_shape)
        pad_shape[axis] += pad_width*2
        
        window = _np.zeros((pad_shape[axis]), dtype=_np.integer)
        window[pad_width:-pad_width] = 1
        
        y_pad = _np.zeros(pad_shape, dtype=y.dtype)
        slice_vec = y.ndim*[slice(None)]
        slice_vec[axis] = slice(pad_width,-pad_width)
        y_pad[tuple(slice_vec)] = y
        
        y_slice_vec_low = y.ndim*[slice(None)]
        y_slice_vec_low[axis] = slice(0,n_edge)
        y_slice_vec_high = y.ndim*[slice(None)]
        y_slice_vec_high[axis] = slice(-n_edge,None)
        
        y_pad_slice_vec_low = y.ndim*[slice(None)]
        y_pad_slice_vec_low[axis] = slice(0,pad_width)
        y_pad_slice_vec_high = y.ndim*[slice(None)]
        y_pad_slice_vec_high[axis] = slice(-pad_width,None)
        
        y_pad[tuple(y_pad_slice_vec_low)] += y[tuple(y_slice_vec_low)].mean(axis=axis, keepdims=True)
        y_pad[tuple(y_pad_slice_vec_high)] += y[tuple(y_slice_vec_high)].mean(axis=axis, keepdims=True)
    else:
        raise ValueError('pad_width must be >= 0')
        
    return y_pad, window

def np_fcn_nd_to_1d(fcn, data, axis=-1):
    """
    Take in an n-dimensional array and return a 1D version operated on by fcn.\
    Works with many numpy functions that can take an "axis" parameter
    """
    if data.ndim > 1:
        dims = list(range(data.ndim))
        dims.pop(axis)
        vec = fcn(data, axis=tuple(dims))
    else:
        vec = data

    return vec

def mean_nd_to_1d(data, axis=-1):
    """
    Take the mean of an nd array, except axis, returning a 1D array
    """
    vec = np_fcn_nd_to_1d(_np.mean, data, axis=axis)

    return vec

def std_nd_to_1d(data, axis=-1):
    """
    Take the mean of an nd array, except axis, returning a 1D array
    """
    vec = np_fcn_nd_to_1d(_np.std, data, axis=axis)

    return vec


def arange_nonzero(start, stop, dtype=_np.float):
    """
    Similar to numpy arange but only returns non-zero elements
    """
    vec = _np.arange(start, stop+1)
    vec = vec[vec != 0]
    return vec


def expand_1d_to_ndim_data(data, data_to_match):
    """
    Make 1D data array equal in dimensions to data_to_match
    """
    if data.ndim > 1:
        print('data must be 1D')
    else:
        nd = data_to_match.ndim
        return expand_1d_to_ndim(data, nd)


def expand_1d_to_ndim(data, ndim):
    """
    Make 1D array into ndim dimensions
    """
    if data.ndim > 1:
        print('data must be 1D')
    else:
        sh = _np.ones((ndim-1),dtype=int)
        sh = _np.append(sh,-1)
        return data.reshape(sh)

def find_nearest(np_vec,to_find = 0):
    """
    Given a vector and a value (or list/vector of values), find the index and
    value of the closest match


    Parameters
    ----------
    np_vec : numpy.ndarray
        Numpy array (list) of values

    to_find : int, float, numpy.ndarray, or list

    Returns
    -------
    out : tuple (nearest_value(s), index(es))
        Closest value (nearest_value) and index (index)

    """

    # Number of values (to_find) to find
    len_to_find = 0

    if isinstance(to_find, int) or isinstance(to_find, float):
        len_to_find = 1
    elif isinstance(to_find, list) or isinstance(to_find, tuple):
        len_to_find = len(to_find)
    elif isinstance(to_find, _np.ndarray):
        len_to_find = to_find.size
    else:
        pass

    if len_to_find == 0:
        return (None, None)
    elif len_to_find == 1:  # Single value
        test = _np.abs(_np.array(np_vec)-to_find)
        nearest_loc = test.argmin()
        nearest_val = np_vec[nearest_loc]
    else:  # Series of values
        nearest_val = []
        nearest_loc = []

        for val in to_find:
            loc = _np.argmin(_np.abs(_np.array(np_vec)-val))
            nearest_loc.append(loc)
            nearest_val.append(np_vec[loc])

    return (nearest_val, nearest_loc)


def row_col_from_lin(ct, sh):
    """
    Convert a 1D counter into a col and row counter
    """

    assert len(sh) == 2, 'Shape must be 2D'

    tot_rows = sh[0]
    tot_cols = sh[1]

    if isinstance(ct, _np.ndarray):
        if (ct > tot_rows*tot_cols).any():
            print('Count is out-of-range. Returning None.')
            return None
    else:
        if ct > tot_rows*tot_cols:
            print('Count is out-of-range. Returning None.')
            return None

    row = _np.mod(ct, tot_rows)
    col = ct//tot_rows

    return [row, col]


def lin_from_row_col(row, col, sh):
    """
    Convert a col and row counter to 1D linear count
    """

    assert len(sh) == 2, 'Shape must be 2D'

    tot_rows = sh[0]
    # tot_cols = sh[1]

    ct = col*tot_rows + row

    return ct

if __name__ == '__main__':
    import timeit as _timeit

    print('Test 1.....')
    x = _np.random.rand(10,11)

    for ct in range(x.size):
        row, col = row_col_from_lin(ct, x.shape)
        print('R: {} C: {}'.format(row,col))
    print('Total number iterated through: {}'.format(ct+1))

    print('Test 2...')
    x = _np.random.rand(100,100,878)
    y = _np.zeros(x.shape, dtype=complex)

    tmr = _timeit.default_timer()
    for rc, blk in enumerate(x):
        for cc, sp in enumerate(blk):
            y[rc,cc,:] = _np.fft.fft(sp)
    tmr -= _timeit.default_timer()
    print('Time with 2 for-loops: {:.3g} sec'.format(-tmr))

    tmr = _timeit.default_timer()
    shp = x.shape
    x = x.reshape((-1, shp[-1]))
    y = _np.zeros(x.shape, dtype=complex)
    for num, sp in enumerate(x):
        y[num,:] = _np.fft.fft(sp)
    y = y.reshape(shp)
    tmr -= _timeit.default_timer()
    print('Time with reshaping and 1 for-loops: {:.3g} sec'.format(-tmr))
    x = x.reshape(shp)

    tmr = _timeit.default_timer()
    space_shp = _np.array(x.shape)[0:-1]
    num_sp = space_shp.prod()
    for num in range(num_sp):
        rc, cc = row_col_from_lin(num, space_shp)
        y[rc, cc, :] = _np.fft.fft(x[rc, cc, :])
    tmr -= _timeit.default_timer()
    print('Time with 1 for-loops: {:.3g} sec'.format(-tmr))

