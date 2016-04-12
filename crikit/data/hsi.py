# -*- coding: utf-8 -*-
"""
Hyperspectral imagery (hsi) class

Created on Tue Apr 12 13:06:30 2016

@author: chc
"""

import numpy as _np

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))
from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum

__all__ = ['Spectra']

class Hsi(_Spectrum):
    """
    Hyperspectral imagery class

    Attributes
    ----------
    data : 3D ndarray [y_pix, x_pix, f_pix]
        HSI image

    freq : crikit.data.frequency.Frequency instance
        Frequency [wavelength, wavenumber] object (i.e., the independent \
        variable)

    label : str
        Image label (i.e., a string describing what the image is)

    units : str
        Units of image (e.g., intensity)

    x_rep : crikit.data.replicate.Replicate instance, Not implemented yet
        x-axis spatial object

    y_rep : crikit.data.replicate.Replicate instance, Not implemented yet
        x-axis spatial object

    x : 1D ndarray
        x-axis spatial vector

    y : 1D ndarray
        y-axis spatial vector

    meta : dict
        Meta-data dictionary

    f_pix : int, read-only
        Size of data's frequency axis. Note: this matches the size of data and \
        does NOT check the size of freq.freq_vec.

    Methods
    -------

    Notes
    -----
    * freq object contains some useful parameters such as op_range_\* and \
    plot_range_\*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    def __init__(self, data=None, freq=None, x=None, y=None, x_rep=None,
                 y_rep=None, label=None, units=None, meta=None):

        self._data = None
        self._freq = None
        self._label = None
        self._units = None
        self._meta = None
        self._x_rep = None
        self._y_rep = None

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
                print('Spectra: converting data input from 1D to 2D ndarray')
                self._data = value[None,:]
            elif value.ndim == 2:
                self._data = value
            else:
                print('Spectra: converting data input from {}D to 2D ndarray'.format(value.ndim))
                f_sh = value.shape[-1]
                self._data = value.reshape((-1, f_sh))
        else:
               raise TypeError('data must be a ndarray')

    @property
    def n_pix(self):
        return self._data.shape[0]

    @property
    def reps(self):
        raise NotImplementedError


if __name__ == '__main__': # pragma: no cover
    sp = Spectra()
    print(sp.__dict__)
    print('Subclass? : {}'.format(issubclass(Spectra,_Spectrum)))
    print('Instance of Spectra? : {}'.format(isinstance(sp,Spectra)))
    print('Instance of Spectrum? : {}'.format(isinstance(sp,_Spectrum)))
    print('Type(sp) == Spectrum? : {}'.format(type(sp)==_Spectrum))
    print('Type(sp) == Spectra? : {}'.format(type(sp)==Spectra))