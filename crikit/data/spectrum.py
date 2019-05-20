"""
Spectrum class and function

"""

import numpy as _np
import copy as _copy

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

    Notes
    -----
    * freq object contains some useful parameters such as op_range* and \
    plot_range*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    # Configurations
    config = {}
    config['nd_axis'] = -1
    config['nd_fcn'] = _np.mean

    def __init__(self, data=None, freq=None, label=None, units=None, meta=None):

        self._data = None
        self._freq = _Frequency()
        self._label = None
        self._units = None
        self._meta = {}

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
            self._meta = _copy.deepcopy(meta)

    @staticmethod
    def _mean_axes(ndim, axis):
        """
        Parameters
        ----------
        ndim : int
            Number of dimensions of input data (target is 1D spectrum)

        axis : int
            For ND data, axis is remaining axis

        Returns
        -------
            Vector that describes what axes to operate (using a mean or similar method) with
            axis parameter
        """
        if axis < 0:
            axis2 = ndim + axis
        else:
            axis2 = axis
        return tuple([n for n in range(ndim) if n != axis2])

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, _np.ndarray):
            raise TypeError('data must be of type ndarray')
        
        # If sub-range of operation is defined. Only perform action over op_range_pix
        if self.freq is not None and self.freq.op_list_pix is not None:
            if value.shape[self.config['nd_axis']] == self.freq.op_range_pix.size:
                temp = _np.zeros((self.freq.size), dtype=value.dtype)
                if value.ndim == 1:
                    temp[self.freq.op_range_pix] = value
                else:
                    print('Input data is {}-dim. Performing {}'.format(value.ndim, self.config['nd_fcn'].__name__))
                    nd_ax = self._mean_axes(value.ndim, axis=self.config['nd_axis'])
                    temp[self.freq.op_range_pix] = self.config['nd_fcn'](value, axis=nd_ax)
            elif value.shape[self.config['nd_axis']] == self.freq.size:
                temp = _np.zeros((self.freq.size), dtype=value.dtype)
                if value.ndim == 1:
                    temp[self.freq.op_range_pix] = value[self.freq.op_range_pix]
                else:
                    print('Input data is {}-dim. Performing {}'.format(value.ndim, self.config['nd_fcn'].__name__))
                    nd_ax = self._mean_axes(value.ndim, axis=self.config['nd_axis'])
                    temp[self.freq.op_range_pix] = self.config['nd_fcn'](value, axis=nd_ax)[self.freq.op_range_pix]

            else:
                raise TypeError('data is of an unrecognized shape: {}'.format(value.shape))
            self._data = 1*temp
            del temp
        else:
            if value.ndim == 1:
                self._data = value
            else:
                print('Input data is {}-dim. Performing {}'.format(value.ndim, self.config['nd_fcn'].__name__))
                nd_ax = self._mean_axes(value.ndim, axis=self.config['nd_axis'])
                self._data = self.config['nd_fcn'](value, axis=nd_ax)


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
        temp_dict = self._meta.copy()

        if self.freq.calib is not None:
            try:
                calib_dict = {}
                calib_prefix = 'Calib.'

                calib_dict[calib_prefix + 'a_vec'] = self.freq.calib['a_vec']
                calib_dict[calib_prefix + 'ctr_wl'] = self.freq.calib['ctr_wl']
                calib_dict[calib_prefix + 'ctr_wl0'] = self.freq.calib['ctr_wl0']
                calib_dict[calib_prefix + 'n_pix'] = self.freq.calib['n_pix']
                calib_dict[calib_prefix + 'probe'] = self.freq.calib['probe']

                try:  # Doesn't really matter if we have the units
                    calib_dict[calib_prefix + 'units'] = self.freq.calib['units']
                except:
                    pass

            except:
                print('Could not get calibration information')
            else:
                temp_dict.update(calib_dict)

        if self.freq.calib_orig is not None:
            try:
                calib_dict = {}
                calib_prefix = 'CalibOrig.'

                calib_dict[calib_prefix + 'a_vec'] = self.freq.calib_orig['a_vec']
                calib_dict[calib_prefix + 'ctr_wl'] = self.freq.calib_orig['ctr_wl']
                calib_dict[calib_prefix + 'ctr_wl0'] = self.freq.calib_orig['ctr_wl0']
                calib_dict[calib_prefix + 'n_pix'] = self.freq.calib_orig['n_pix']
                calib_dict[calib_prefix + 'probe'] = self.freq.calib_orig['probe']

                try:  # Doesn't really matter if we have the units
                    calib_dict[calib_prefix + 'units'] = self.freq.calib_orig['units']
                except:
                    pass

            except:
                print('Could not get calibration information')
            else:
                temp_dict.update(calib_dict)

        # return self._meta
        return temp_dict

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
        if self._data is None:
            return None
        elif isinstance(self._data, _np.ndarray):
            return self._data.ndim
        else:
            return len(self._data.shape)

    @property
    def shape(self):
        if self._data is None:
            return None
        else:
            return self._data.shape

    @property
    def size(self):
        if self._data is None:
            return None
        else:
            return self._data.size

    def mean(self, extent=None, over_space=True):
        """
        Return mean spectrum (or mean over extent [list with 2 elements]). If\
        over_space is False, returns reps-number of mean spectra
        """
        if self._data is None:
            return None

        ndim = len(self._data.shape)

        if ndim == 1:
            if isinstance(self._data, _np.ndarray):
                return self._data.mean()
            else:
                return _np.mean(self._data)

        if ndim > 1:
            if over_space == True:
                axes = tuple(_np.arange(ndim-1))
            else:
                axes = -1

        if isinstance(self._data, _np.ndarray):
            if extent is None:
                return self._data.mean(axis=axes)
            else:
                return self._data[:,extent[0]:extent[1]+1].mean(axis=axes)
        else:
            if extent is None:
                return _np.mean(self._data, axis=axes)
            else:
                return _np.mean(self._data[:,extent[0]:extent[1]+1],
                                axis=axes)

    def std(self, extent=None, over_space=True):
        """
        Return standard deviation (std) spectrum (or std over extent
        [list with 2 elements]). If over_space is False, reps (or reps x reps)
        number of std's.
        """
        if self._data is None:
            return None

        ndim = len(self._data.shape)

        if ndim == 1:
            if isinstance(self._data, _np.ndarray):
                return self._data.std()
            else:
                return _np.std(self._data)

        if ndim > 1:
            if over_space == True:
                axes = tuple(_np.arange(ndim-1))
            else:
                axes = -1

        if isinstance(self._data, _np.ndarray):
            if extent is None:
                return self._data.std(axis=axes)
            else:
                return self._data[:,extent[0]:extent[1]+1].std(axis=axes)
        else:
            if extent is None:
                return _np.std(self._data, axis=axes)
            else:
                return _np.std(self._data[:,extent[0]:extent[1]+1],
                                axis=axes)

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

    N = 10001
    wn = _np.linspace(500,3000,N)
    sp = Spectrum(data=_np.random.rand(N) + 1j*_np.random.rand(N), freq=wn)

    tmr = _timeit.default_timer()
    sp.data[200:500]
    tmr -= _timeit.default_timer()
    print(-tmr)
