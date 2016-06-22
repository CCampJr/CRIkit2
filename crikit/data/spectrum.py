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
    data : 1D ndarray [f_pix]
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

    f_pix : int, read-only
        Size of data. Note: this matches the size of data and does NOT check \
        the size of freq.freq_vec.

    ndim : int, read-only
        Number of data dimensions

    shape : tuple, read-only
        Shape of data

    size : int, read-only
        Size of data (i.e., total number of entries)

    Methods
    -------
    mean : int
        Mean value. If extent [a,b] is provided, calculate mean over that\
        inclusive region.

    std : int
        Standard deviation. If extent [a,b] is provided, calculate standard\
        deviation over that inclusive region.

    subtract : 1D ndarray or None
        Subtract spectrum or object

    Note
    ----
    * freq object contains some useful parameters such as op_range_\* and \
    plot_range_\*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    def __init__(self, data=None, freq=None, label=None, units=None, meta=None):

        self._data = None
        self._freq = _Frequency()
        self._label = None
        self._units = None
        self._meta = None

        if data is not None:
            self.data = _copy.deepcopy(data)
        if freq is not None:
            self.freq = _copy.deepcopy(freq)
        else:
            self.freq = _Frequency()
        if label is not None:
            self.label = _copy.deepcopy(label)
        if units is not None:
            self.units = _copy.deepcopy(units)
        if meta is not None:
            self.meta = _copy.deepcopy(meta)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, _np.ndarray):
            if value.ndim == 1:
                if self.freq is not None and self.freq.op_list_pix is not None:
                    if value.shape[-1] == self.freq.op_range_pix.size:
                        temp = _np.zeros((self.freq.size),dtype=value.dtype)
                        temp[self.freq.op_range_pix] = value
                        self._data = temp
                    else:
                        raise TypeError('data is of an unrecognized shape: {}'.format(value.shape))
                else:
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
        elif isinstance(value, _np.ndarray):
            self.freq = _Frequency(data=value)
        else:
            raise TypeError('freq must be of type crikit.data.Frequency')

    @property
    def f(self):
        """
        Convenience attribute: return frequency vector within operating (op) \
        range
        """
        return self.freq.op_range_freq

    @property
    def f_full(self):
        """
        Convenience attribute: return full frequency vector
        """
        return self.freq.data

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

    @property
    def f_pix(self):
        if self._data is not None:
            return self._data.shape[-1]

    @property
    def ndim(self):
        return self._data.ndim

    @property
    def shape(self):
        return self._data.shape

    @property
    def size(self):
        return self._data.size

    def mean(self, extent=None, over_space=None):
        """
        Return mean value or mean value over extent (inclusive).

        Note
        ----
        over_space only included for consistency: with 1 spectrum there is\
        no spatial (rep) component.
        """
        if extent is None:
            return self._data.mean()
        else:
            return self._data[extent[0]:extent[1]+1].mean()

    def std(self, extent=None):
        """
        Return standard deviation value (or over extent [inclusive])
        """
        if extent is None:
            return self._data.std()
        else:
            return self._data[extent[0]:extent[1]+1].std()

    def subtract(self, spectrum, overwrite=True):
        """
        Subtract spectrum from data
        """
        if isinstance(spectrum, Spectrum):
            if overwrite:
                self.data -= spectrum.data
                return None
            else:
                return self.data - spectrum.data
        elif isinstance(spectrum, _np.ndarray):
            if overwrite:
                self.data -= spectrum
                return None
            else:
                return self.data - spectrum

    def __sub__(self, spectrum):
        return self.subtract(spectrum, overwrite=False)


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