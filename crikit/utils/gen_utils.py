# -*- coding: utf-8 -*-
"""
General utilities

    expand_1d_to_ndim_data : Match 1D data array dimensionality to that of \
        another array

    expand_1d_to_ndim : Expand 1D data array dimensionality to ndim

    find_nearest : Given a vector and a value, find the index and value
        of the closest match

Note
----
"""
if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))

import numpy as _np

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


def lin_count_row_col(ct, sh):
    """
    Convert a 1D counter into a col and row counter
    """

    assert len(sh) == 2, 'Shape must be 2D'

    tot_rows = sh[0]
    tot_cols = sh[1]

    if ct > tot_rows*tot_cols:
        print('Count is out-of-range. Returning None.')
        return None

    row = _np.mod(ct, tot_rows)
    col = ct//tot_rows

    return [row, col]

if __name__ == '__main__':
    import timeit as _timeit

    print('Test 1.....')
    x = _np.random.rand(10,11)

    for ct in range(x.size):
        row, col = lin_count_row_col(ct, x.shape)
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
        rc, cc = lin_count_row_col(num, space_shp)
        y[rc, cc, :] = _np.fft.fft(x[rc, cc, :])
    tmr -= _timeit.default_timer()
    print('Time with 1 for-loops: {:.3g} sec'.format(-tmr))

