# -*- coding: utf-8 -*-
"""
Spectra class and function (very similar to Spetcrum except this deals with
multiple entries)

"""

import numpy as _np
import copy as _copy

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))
from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.replicate import Replicate as _Replicate

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
        does NOT check the size of freq.data.

    shape : tuple, read-only
        Shape of data

    n_pix : int, read-only
        Size of data's replicate/spectral number axis.

    Methods
    -------
    mean : 1D ndarray
        Mean spectrum. If extent [a,b] is provided, calculate mean over that\
        inclusive region.

    std : 1D ndarray
        Standard deviation of spectrum. If extent [a,b] is provided, calculate standard\
        deviation over that inclusive region.

    subtract : 2D ndarray or None
        Subtract spectrum or object

    Notes
    -----
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
        self._reps = _Replicate()

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
            if self.freq.data is None or self.freq.op_list_pix is None:
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
        return self._reps

    @reps.setter
    def reps(self, value):
        if isinstance(value, _Replicate):
            self._reps = value
        elif isinstance(value, _np.ndarray):
            self._reps.data = value


    def mean(self, extent=None, over_space=True):
        """
        Return mean spectrum (or mean over extent [list with 2 elements]). If\
        over_space is False, returns reps-number of mean spectra
        """
        if self._data is None:
            return None
        else:
            if over_space:  # Mean over all space
                if extent is None:
                    return self._data.mean(axis=0)
                else:
                    return self._data[:,extent[0]:extent[1]+1].mean(axis=0)
            else:
                if extent is None:
                    return self._data.mean(axis=-1)
                else:
                    return self._data[:,extent[0]:extent[1]+1].mean(axis=-1)

    def std(self, extent=None):
        """
        Return standard deviation spectrum
        """
        if self._data is None:
            return None
        else:
            if extent is None:
                return self._data.std(axis=0)
            else:
                return self._data[:,extent[0]:extent[1]+1].std(axis=0)

    def subtract(self, spectra, overwrite=True):
        """
        Subtract spectrum from data
        """
        # Order IS important
        if isinstance(spectra, Spectra):
            if overwrite:
                self.data -= spectra.data
                return None
            else:
                return self.data - spectra.data
        elif isinstance(spectra, _Spectrum):
            if overwrite:
                self.data -= spectra.data[None,:]
                return None
            else:
                return self.data - spectra.data[None,:]
        elif isinstance(spectra, _np.ndarray):
            if spectra.shape == self.data.shape:
                if overwrite:
                    self.data -= spectra
                    return None
                else:
                    return self.data - spectra
            else:
                if overwrite:
                    self.data -= spectra[None,:]
                    return None
                else:
                    return self.data - spectra[None,:]

    def __sub__(self, spectrum):
        return self.subtract(spectrum, overwrite=False)

if __name__ == '__main__': # pragma: no cover
    sp = Spectra()
    print(sp.__dict__)
    print('Subclass? : {}'.format(issubclass(Spectra,_Spectrum)))
    print('Instance of Spectra? : {}'.format(isinstance(sp,Spectra)))
    print('Instance of Spectrum? : {}'.format(isinstance(sp,_Spectrum)))
    print('Type(sp) == Spectrum? : {}'.format(type(sp)==_Spectrum))
    print('Type(sp) == Spectra? : {}'.format(type(sp)==Spectra))