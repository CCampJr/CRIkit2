"""
Factored data class

Created on Fri Apr 22 23:42:40 2016

@author: chc
"""

import numpy as _np

from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.replicate import Replicate as _Replicate
from crikit.data.hsi import Hsi as _Hsi

class _Factorized:
    """
    Factorized class. Contains items unique to factorized spectral data.
    """

    def __init__(self):
        raise NotImplementedError

class FactorizedHsi(_Hsi, _Factorized):
    """
    Factorized Hsi Class

    Attributes
    ----------

    Methods
    -------

    Notes
    -----
    * TODO: deside on

    """
    def __init__(self):
        raise NotImplementedError

class FactorizedSpectra(_Spectra, _Factorized):
    """
    Factorized Spectra Class

    Attributes
    ----------

    Methods
    -------

    Notes
    -----
    * TODO: deside on

    """
    def __init__(self):
        raise NotImplementedError

