# -*- coding: utf-8 -*-
"""
Hyperspectral imagery (hsi) class

Created on Tue Apr 12 13:06:30 2016

@author: chc
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

__all__ = ['Hsi']

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

    shape : tuple, read-only
        Shape of data

    size : int, read-only
        Size of data (i.e., total number of entries)

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
            self.data = _copy.deepcopy(data)
        if freq is not None:
            self.freq = _copy.deepcopy(freq)
        else:
            self.freq = _Frequency()

        self._x_rep = _Replicate(data=x)
        self._y_rep = _Replicate(data=y)

        if x is None and x_rep is not None:
            self.x_rep = _copy.deepcopy(x_rep)
        if y is None and y_rep is not None:
            self.y_rep = _copy.deepcopy(y_rep)

        if label is not None:
            self.label = _copy.deepcopy(label)
        if units is not None:
            self.units = _copy.deepcopy(units)
        if meta is not None:
            self.meta = _copy.deepcopy(meta)

    @property
    def x_rep(self):
        return self._x_rep

    @x_rep.setter
    def x_rep(self, value):
        if isinstance(value, _Replicate):
            self._x_rep = value
        elif isinstance(value, _np.ndarray):
            self._x_rep.data = value

    @property
    def y_rep(self):
        return self._y_rep

    @property
    def x(self):
        return self._x_rep.data

    @x.setter
    def x(self, value):
        self._x_rep.data = value

    @property
    def y(self):
        return self._y_rep.data

    @y.setter
    def y(self, value):
        self._y_rep.data = value


    @y_rep.setter
    def y_rep(self, value):
        if isinstance(value, _Replicate):
            self._y_rep = value
        elif isinstance(value, _np.ndarray):
            self._y_rep.data = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, _np.ndarray):
            if value.ndim == 3:
                if self.freq is None or self.freq.op_list_pix is None:
                    self._data = value
                else:
                    if value.shape[-1] == self.freq.op_range_pix.size:
                        temp = _np.zeros((self._data.shape),dtype=value.dtype)
                        temp[:,:,self.freq.op_range_pix] = value
                        self._data = temp
                    else:
                        #raise TypeError('data is of an unrecognized shape: {}'.format(value.shape))
                        raise TypeError('pre-data: {}, value: {}'.format(self._data.shape,value.shape))
            else:
                raise TypeError('data must be 3D')
        else:
           raise TypeError('data must be a 3D ndarray')


if __name__ == '__main__': # pragma: no cover

    x = _np.linspace(0,100,10)
    y = _np.linspace(0,100,10)
    freq = _np.arange(20)
    data = _np.random.rand(10,10,20)


    hs = Hsi(data=data, freq=freq, x=x, y=y)
    print(hs.shape)
    print(isinstance(hs, _Spectrum))
