# -*- coding: utf-8 -*-
"""
Functions to check and (if needed) convert input variables

Created on Sat Jun 18 00:16:27 2016

@author: chc
"""

import numpy as _np


def _rng_is_pix_vec(rng):
    """
    Make sure rng is a vector; except if None, then leave as None

    """
    if rng is None:
        return None
    elif len(rng) == 2:
        rng.sort()
        return _np.arange(rng[0], rng[1])
    else:
        return rng