# -*- coding: utf-8 -*-
"""
CRIKit2: Hyperspectral imaging toolkit
==============================================================

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform (user interface, UI).

HSI Processing:
    * Dark subtraction
    * Detrending
    * Denoising

Coherent Raman-Specific Processing:
    * Kramers-Kronig phase retrieval
    * Phase- and scale-error correction

Analysis:
    * Coming soon

Usage
-----
python -m crikit

Authors
-------
* Charles H. Camp Jr. <charles.camp@nist.gov>
"""

import sys as _sys
import os as _os

_sys.path.append(_os.path.abspath('../'))

# M.N.P.Q (Major, Minor, Year, Month)
__version__ = '0.1.16.07'

