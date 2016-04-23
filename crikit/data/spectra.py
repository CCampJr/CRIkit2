# -*- coding: utf-8 -*-
"""
Spectra class and function (very similar to Spetcrum except this deals with
multiple entries)

"""

import numpy as _np

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))
from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum

__all__ = ['Spectra']

class Spectra(_Spectrum):
    """
    Spectra class

    Attributes
    ----------
    data : 2D ndarray [n_pix, f_pix]
        Spectra. Note: input can be a ndarray of any dimension: it will be \
        CONVERTED to [n_pix, f_pix] shape, assuming that shape[-1] is the f_pix \
        long.

    freq : crikit.data.frequency.Frequency instance
        Frequency [wavelength, wavenumber] object (i.e., the independent \
        variable)

    label : str
        Spectrum label (i.e., a string describing what the spectrum is)

    units : str
        Units of spectrum

    reps : crikit.data.replicate.Replicate instance, Not implemented yet
        Object describing the meaning of multiple spectra (i.e., the physical \
        meaning of n_pix).

    meta : dict
        Meta-data dictionary

    f_pix : int, read-only
        Size of data's frequency axis. Note: this matches the size of data and \
        does NOT check the size of freq.freq_vec.

    shape : tuple, read-only
        Shape of data

    n_pix : int, read-only
        Size of data's replicate/spectral number axis.

    Methods
    -------
    mean : 1D ndarray, read-only
        Mean spectrum

    std : 1D ndarray, read-only
        Standard deviation of spectrum

    Notes
    -----
    * freq object contains some useful parameters such as op_range_\* and \
    plot_range_\*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    def __init__(self, data=None, freq=None, label=None, units=None, meta=None):

        self._data = None
        self._freq = None
        self._label = None
        self._units = None
        self._meta = None
        self._reps = None

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
            if self.freq is None or self.freq.op_list_pix is None:
                if value.ndim == 1:
                    print('Spectra: converting data input from 1D to 2D ndarray')
                    self._data = value[None,:]
                elif value.ndim == 2:
                    self._data = value
                else:
                    print('Spectra: converting data input from {}D to 2D ndarray'.format(value.ndim))
                    f_sh = value.shape[-1]
                    self._data = value.reshape((-1, f_sh))
            else:
                if value.shape[-1] == self.freq.op_range_pix.size:
                    temp = _np.zeros((self._data.shape),dtype=value.dtype)
                    temp[:,self.freq.op_range_pix] = value
                    self._data = temp
                else:
                    raise TypeError('data is of an unrecognized shape: {}'.format(value.shape))
        else:
               raise TypeError('data must be a ndarray')

    @property
    def n_pix(self):
        return self._data.shape[0]

    @property
    def reps(self):
        raise NotImplementedError

    def mean(self):
        return self._data.mean(axis=0)

    def std(self):
        return self._data.std(axis=0)

if __name__ == '__main__': # pragma: no cover
    sp = Spectra()
    print(sp.__dict__)
    print('Subclass? : {}'.format(issubclass(Spectra,_Spectrum)))
    print('Instance of Spectra? : {}'.format(isinstance(sp,Spectra)))
    print('Instance of Spectrum? : {}'.format(isinstance(sp,_Spectrum)))
    print('Type(sp) == Spectrum? : {}'.format(type(sp)==_Spectrum))
    print('Type(sp) == Spectra? : {}'.format(type(sp)==Spectra))