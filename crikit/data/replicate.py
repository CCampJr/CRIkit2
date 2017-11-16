"""
Replicate class used for things such as repetitive measurements or even spatial \
vectors (e.g., x and y)

Created on Tue Apr 12 11:42:56 2016

@author: chc
"""

import numpy as _np

__all__ = ['Replicate']

class Replicate:
    """
    Replicate class

    Attributes
    ----------
    data : 1D ndarray [size]
        Replicate data

    calib : list [(start), stop, (step size)]
        Calibration descriptor. See Note.

    units : str
        Units of replicate data

    size : int, read-only

    Methods
    -------
    update_calib_from_data
        Calculate and set calib parameter from data

    update_data_from_calib
        Calculate and set data from calib parameter

    calib_data_agree
        Return bool as to whether data and that derived from calib agree

    Notes
    -----
    * input to calib can be a list or tuple or 1D ndarray or int or float

    Setting calib can take up to 3 entries :
        * 1 entry: stop = entry; start = 0, step size = 1
        * 2 entries: start = entry[0], stop = entry[1], step size = 1
        * 3 entries: [start, stop, step size]

    """


    def __init__(self, data=None, calib=None, units=None, label=None):
        self._data = None
        self._calib = None
        self._units = None
        self._label = None

        if data is not None:
            self.data = data
        if calib is not None:
            self.calib = calib
        if units is not None:
            self.units = units
        if label is not None:
            self.label = label

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if isinstance(value, _np.ndarray):
            if value.ndim == 1:
                self._data = value
            else:
                raise TypeError('data must be 1D ndarray')
        elif value is None:
            self._data = None
        else:
            raise TypeError('data must be 1D ndarray')

    @property
    def size(self):
        return self._data.size

    @property
    def calib(self):
        return self._calib

    @calib.setter
    def calib(self, value):
        if isinstance(value, _np.ndarray) or isinstance(value, list) or isinstance(value, tuple):
            if len(value) == 3:
                self._calib = list(value)
            elif len(value) == 2:
                temp = list(value)
                temp.append(1)
                self._calib = temp
            elif len(value) == 1:
                temp = [0]
                temp.append(value[0])
                temp.append(1)
                self._calib = temp
            else:
                raise TypeError('calib should have 1-3 components: [(start), stop, (step size)]')
        elif isinstance(value, int) or isinstance(value, float):
            temp = [0]
            temp.append(value)
            temp.append(1)
            self._calib = temp
        else:
            raise TypeError('calib should be an int or float [stop]; or a \
            1D ndarray, tuple, or list with 1-3 entires: [start, stop, step size]')

    @property
    def units(self):
        return self._units

    @units.setter
    def units(self, value):
        if isinstance(value, str) | (value is None):
            self._units = value
        else:
            raise TypeError('units should be of type str')

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if isinstance(value, str) | (value is None):
            self._label = value
        else:
            raise TypeError('label should be of type str')

    def update_data_from_calib(self):
        """
        Calculate and set data from calib parameter
        """
        if self._calib is not None:
            self.data = _np.arange(self._calib[0],self._calib[1], self._calib[2])
        else:
            raise TypeError('calib is not set')

    def update_calib_from_data(self):
        """
        Calculate and set calib parameter from data. Note: assumes uniform \
        spacing of data.
        """
        if self._data is not None:
            delta = self._data[1] - self._data[0]
            self.calib = [self._data[0], self._data[-1]+delta, delta]
        else:
            raise TypeError('data is not set')

    def calib_data_agree(self):
        if self._data is None:
            raise TypeError('data not set')
        if self._calib is None:
            raise TypeError('calib not set')

        temp = _np.arange(self._calib[0],self._calib[1],self._calib[2])

        if temp.size != self._data.size:
            return False
        else:
            return _np.allclose(temp, self._data)

if __name__ == '__main__':  # pragma: no cover

    start = 0
    stop = 10
    step_size = .1

    x = _np.arange(start, stop, step_size)

    rep = Replicate(data=x,calib=[start, stop, step_size])

    print('Calib and data agree: {}'.format(rep.calib_data_agree()))