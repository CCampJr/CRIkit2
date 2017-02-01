"""
Functions to check and (if needed) convert input variables

Created on Sat Jun 18 00:16:27 2016

@author: chc
"""

import numpy as _np


def _rng_is_pix_vec(rng, vec_size=None):
    """
    Make sure rng is a vector, unless None (then returns None).

    Parameters
    ----------

    rng : int, list, tuple, or ndarray(1D)
        * int: number of pixels in rng
        * list, tuple, ndarray with length 2: Start and end of rng
        * ndarray (length > 2): actual rng vector

    Returns
    -------

    rng : ndarray (1D)
        Array of pixel range
    """
    if rng is None:
        return None
    elif isinstance(rng, (int, float)):
        return _np.arange(rng)
    elif len(rng) == 2:
        rng.sort()
        return _np.arange(rng[0], rng[1])
    else:
        return rng