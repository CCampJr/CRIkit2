# -*- coding: utf-8 -*-
"""
General utilities

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

