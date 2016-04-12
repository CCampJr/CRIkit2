# -*- coding: utf-8 -*-
"""
Spectrum class and function

"""

import numpy as _np
import copy as _copy

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))
#    _sys.path.append(_os.path.abspath('./utils'))
from crikit.data.frequency import Frequency as _Frequency

__all__ = ['Spectrum']

class Spectrum:
    """
    Spectrum class

    Attributes
    ----------
    data : 1D ndarray
        Spectrum
    freq : crikit.data.Frequency instance
        Frequency [wavelength, wavenumber] object (i.e., the independent \
        variable)
    label : str
        Spectrum label (i.e., a string describing what the spectrum is)
    units : str
        Units of spectrum
    meta : dict
        Meta-data dictionary

    Methods
    -------

    Notes
    -----

    """

    def __init__(self, data=None, freq=None, label=None, units=None, meta=None):

        self._data = None
        self._freq = None
        self._label = None
        self._units = None
        self._meta = None

        if data is not None:
            self.data = data
        if freq is not None:
            self.freq = freq
        else:
            self.freq = _Frequency()
        if label is not None:
            self.label = label
        if units is not None:
            self.units = units
        if meta is not None:
            self.meta = meta

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, _np.ndarray):
            if value.ndim == 1:
                self._data = value
            else:
                raise TypeError('data must be a 1D ndarray')
        else:
               raise TypeError('data must be a 1D ndarray')

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        if isinstance(value, _Frequency):
            self._freq = value
        elif value is None:
            self.freq = _Frequency()
        else:
            raise TypeError('freq must be of type crikit.data.Frequency')

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if isinstance(value, str):
            self._units = value
        else:
            raise TypeError('units must be of type str')

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if isinstance(value, str):
            self._label = value
        else:
            raise TypeError('label must be of type str')

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, value):
        if isinstance(value, dict):
            self._meta = value
        else:
            raise TypeError('meta must be of type dict')


if __name__ == '__main__':  # pragma: no cover
    import timeit as _timeit

    a = Spectrum(data=_np.random.rand(300,300,1000))

    start = _timeit.default_timer()
    q = a.data[:,:,100:900]
    stop = _timeit.default_timer()
    print(stop-start)
    del q

    start = _timeit.default_timer()
    q = a.set_data[:,:,100:900]
    stop = _timeit.default_timer()
    print(stop-start)