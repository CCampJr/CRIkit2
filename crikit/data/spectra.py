"""
Spectra class and function (very similar to Spetcrum except this deals with
multiple entries)

"""

import numpy as _np
import copy as _copy

from crikit.data.frequency import Frequency as _Frequency
from crikit.data.replicate import Replicate as _Replicate

__all__ = ['Spectrum', 'Spectra', 'Hsi']


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
            self._data = 1 * temp
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
                except Exception:
                    pass

            except Exception:
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
                except Exception:
                    pass

            except Exception:
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
            if over_space is True:
                axes = tuple(_np.arange(ndim - 1))
            else:
                axes = -1

        if isinstance(self._data, _np.ndarray):
            if extent is None:
                return self._data.mean(axis=axes)
            else:
                return self._data[:, extent[0]:extent[1] + 1].mean(axis=axes)
        else:
            if extent is None:
                return _np.mean(self._data, axis=axes)
            else:
                return _np.mean(self._data[:, extent[0]:extent[1] + 1],
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
            if over_space is True:
                axes = tuple(_np.arange(ndim - 1))
            else:
                axes = -1

        if isinstance(self._data, _np.ndarray):
            if extent is None:
                return self._data.std(axis=axes)
            else:
                return self._data[:, extent[0]:extent[1] + 1].std(axis=axes)
        else:
            if extent is None:
                return _np.std(self._data, axis=axes)
            else:
                return _np.std(self._data[:, extent[0]:extent[1] + 1],
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


class Hsi(Spectrum):
    """
    Hyperspectral imagery class

    Parameters
    ----------
    data : 3D ndarray [y_pix, x_pix, f_pix]
        HSI image

    mask : 3D ndarray (int) [y_pix, x_pix, f_pix]
        0,1 mask with 1 is a usable pixel and 0 is not

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

    Attributes
    ----------
    shape : tuple, read-only
        Shape of data

    size : int, read-only
        Size of data (i.e., total number of entries)

    extent : list, read-only
        Extent of image [xmin, xmax, ymin, ymax]

    Methods
    -------
    mean : 1D ndarray
        Mean spectrum. If extent [a,b] is provided, calculate mean over that\
        inclusive region.

    std : 1D ndarray
        Standard deviation of spectrum. If extent [a,b] is provided, calculate standard\
        deviation over that inclusive region.

    subtract : 3D ndarray or None
        Subtract spectrum or object

    Notes
    -----
    * freq object contains some useful parameters such as op_range_* and \
    plot_range_*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    # Configurations
    config = {}
    config['nd_axis'] = -1

    def __init__(self, data=None, freq=None, x=None, y=None, x_rep=None,
                 y_rep=None, label=None, units=None, meta=None):

        super().__init__(data, freq, label, units, meta)
        self._x_rep = _Replicate()
        self._y_rep = _Replicate()
        self._mask = None

        self._x_rep = _Replicate(data=x)
        self._y_rep = _Replicate(data=y)

        if x is None and x_rep is not None:
            self.x_rep = _copy.deepcopy(x_rep)
        if y is None and y_rep is not None:
            self.y_rep = _copy.deepcopy(y_rep)

    @staticmethod
    def _mean_axes(*args, **kwargs):
        """ Inhereted from Spectrum """
        raise NotImplementedError('Only applicable to Spectrum class.')

    @staticmethod
    def _reshape_axes(shape, spectral_axis):
        """
        Parameters
        ----------
        shape : tuple
            Input data shape

        spectral_axis : int
            Spectral axis

        Returns
        -------
            Reshape vector
        """
        ndim = len(shape)

        if ndim == 1:
            out = [1, 1, 1]
            out[spectral_axis] = shape[0]
        elif ndim == 2:  # ! Super-wonky
            out = [1, shape[0], shape[1]]
        elif ndim == 3:
            out = shape
        elif ndim > 3:
            out = [-1, shape[-2], shape[-1]]
        else:
            raise ValueError('Shape error')

        return tuple(out)

    @property
    def extent(self):
        if (self.x is not None) & (self.y is not None):
            return [self.x.min(), self.x.max(), self.y.min(), self.y.max()]

    @property
    def mask(self):
        return self._mask

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
        if not isinstance(value, _np.ndarray):
            raise TypeError('data must be of type ndarray, not {}'.format(type(value)))

        ax_rs = self._reshape_axes(value.shape, self.config['nd_axis'])

        # self._mask = _np.ones(tuple([n for n in range(3) if n != self.config['nd_axis']]),
        #                       dtype=int)

        if self.freq is None or self.freq.op_list_pix is None:
            self._data = value.reshape(ax_rs)
        else:
            if value.shape[self.config['nd_axis']] == self.freq.op_range_pix.size:
                temp = _np.zeros((self._data.shape), dtype=value.dtype)
                temp[:, :, self.freq.op_range_pix] = value.reshape(ax_rs)
                self._data = 1 * temp
                del temp
            elif value.shape[self.config['nd_axis']] == self._data.shape[self.config['nd_axis']]:
                temp = _np.zeros((self._data.shape), dtype=value.dtype)
                temp[..., self.freq.op_range_pix] = value.reshape(ax_rs)[..., self.freq.op_range_pix]
                self._data = 1 * temp
                del temp

    def check(self):
        """
        Check x, y, and freq to make sure the dimensions agree with data
        """
        if self._data is None:
            print('Hsi check: data is None, not checking')
        else:
            if self._x_rep._data is None:
                self._x_rep._data = _np.arange(self.shape[1])
                self._x_rep._label = 'X'
                self._x_rep._units = 'pix'
                print('Hsi check: setting x to pixels')
            elif self._x_rep._data.size != self._data.shape[1]:
                self._x_rep = _Replicate()
                self._x_rep._data = _np.arange(self.shape[1])
                self._x_rep._label = 'X'
                self._x_rep._units = 'pix'
                print('Hsi check: setting x to pixels')

            if self._y_rep._data is None:
                self._y_rep._data = _np.arange(self.shape[0])
                self._y_rep._label = 'Y'
                self._y_rep._units = 'pix'
                print('Hsi check: setting y to pixels')
            elif self._y_rep._data.size != self._data.shape[0]:
                self._y_rep = _Replicate()
                self._y_rep._data = _np.arange(self.shape[0])
                self._y_rep._label = 'Y'
                self._y_rep._units = 'pix'
                print('Hsi check: setting y to pixels')

            if self.freq._data is None:
                self.freq._data = _np.arange(self.shape[-1])
                self.freq._label = 'Frequency'
                self.freq._units = 'pix'
                print('Hsi check: setting freq to pixels')
            elif self.freq._data.size != self._data.shape[-1]:
                self.freq = _Frequency()
                self.freq._data = _np.arange(self.shape[-1])
                print('Hsi check: setting freq to pixels')
        return None

    def subtract(self, spectra, overwrite=True):
        """
        Subtract spectrum from data
        """
        # Order IS important
        if isinstance(spectra, Hsi):
            if overwrite:
                self.data -= spectra.data
                return None
            else:
                return self.data - spectra.data
        elif isinstance(spectra, Spectrum):
            if overwrite:
                self.data -= spectra.data[None, None, :]
                return None
            else:
                return self.data - spectra.data
        elif isinstance(spectra, _np.ndarray):
            if spectra.shape == self.data.shape:
                if overwrite:
                    self.data -= spectra
                    return None
                else:
                    return self.data - spectra
            else:
                if overwrite:
                    self.data -= spectra[None, None, :]
                    return None
                else:
                    return self.data - spectra[None, None, :]

    def get_rand_spectra(self, num, pt_sz=1, quads=False, full=False):

        mlen, nlen, freqlen = self.data.shape

        if quads:
            num_spectra = num + 5
        else:
            num_spectra = num

        if _np.iscomplexobj(self.data):
            dtype = complex
        else:
            dtype = float

        temp = _np.zeros((num_spectra, self.data.shape[-1]), dtype=dtype)

        quad_mid_row = int(_np.round(mlen / 2))
        quad_mid_col = int(_np.round(nlen / 2))
        center_row = (int(_np.round(mlen / 3)), int(_np.round(2 * mlen / 3)))
        center_col = (int(_np.round(nlen / 3)), int(_np.round(2 * nlen / 3)))

        start_count = 0
        if quads:
            # QUADS
            # Bottom-left
            temp[0, :] = _np.mean(self.data[0:quad_mid_row, 0:quad_mid_col, :], axis=(0, 1))

            # Upper-left
            temp[1, :] = _np.mean(self.data[0:quad_mid_row, quad_mid_col + 1::, :], axis=(0, 1))

            # Upper-right
            temp[2, :] = _np.mean(self.data[quad_mid_row + 1::, quad_mid_col + 1::, :], axis=(0, 1))

            # Bottom-right
            temp[3, :] = _np.mean(self.data[quad_mid_row + 1::, 0:quad_mid_col, :], axis=(0, 1))

            # Center
            temp[4, :] = _np.mean(self.data[center_row[0]:center_row[1], center_col[0]:center_col[1], :], axis=(0, 1))

            start_count += 5
        else:
            pass

        rand_rows = ((mlen - pt_sz - 1) * _np.random.rand(num_spectra)).astype(int)
        rand_cols = ((nlen - pt_sz - 1) * _np.random.rand(num_spectra)).astype(int)

        for count in _np.arange(start_count, num_spectra):
            if pt_sz == 1:
                temp[count, :] = _np.squeeze(self.data[rand_rows[count - start_count],
                                             rand_cols[count - start_count]])
            else:

                rows = [rand_rows[count - start_count] - (pt_sz - 1),
                        rand_rows[count - start_count] + pt_sz]
                cols = [rand_cols[count - start_count] - (pt_sz - 1),
                        rand_cols[count - start_count] + pt_sz]

                if rows[0] < 0:
                    rows[0] = 0
                if rows[1] >= mlen:
                    rows[1] = mlen - 1
                if cols[0] < 0:
                    cols[0] = 0
                if cols[1] >= nlen:
                    cols[1] = nlen - 1

                if cols[0] == cols[1] or rows[0] == rows[1]:
                    pass
                else:
                    temp[count, :] = _np.squeeze(_np.mean(self.data[rows[0]:rows[1], cols[0]:cols[1], :], axis=(0, 1)))

        if (not full) and (self.freq.data is not None):
            temp = temp[..., self.freq.op_range_pix]

        return temp

    def __sub__(self, spectrum):
        return self.subtract(spectrum, overwrite=False)


class Spectra(Spectrum):
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
    * freq object contains some useful parameters such as op_range* and \
    plot_range*, which define spectral regions-of-interest. (It's debatable \
    as to whether those parameters should be in Frequency or Spectrum classes)

    """

    # Configurations
    config = {}
    config['nd_axis'] = -1

    def __init__(self, data=None, freq=None, label=None, units=None, meta=None):
        super().__init__(data, freq, label, units, meta)
        self._reps = _Replicate()

    @staticmethod
    def _mean_axes(*args, **kwargs):
        """ Inhereted from Spectrum """
        raise NotImplementedError('Only applicable to Spectrum class.')

    @staticmethod
    def _reshape_axes(shape, spectral_axis):
        """
        Parameters
        ----------
        shape : tuple
            Input data shape

        spectral_axis : int
            Spectral axis

        Returns
        -------
            Reshape vector
        """
        ndim = len(shape)

        if ndim >= 2:
            out = [-1, -1]
        else:
            out = [1, 1]

        out[spectral_axis] = shape[spectral_axis]
        return tuple(out)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if not isinstance(value, _np.ndarray):
            raise TypeError('data must be of type ndarray')

        if self.freq.data is None or self.freq.op_list_pix is None:
            if value.ndim != 2:
                print('Spectra: converting data input from {}D to 2D ndarray'.format(value.ndim))
            ax_rs = self._reshape_axes(value.shape, spectral_axis=self.config['nd_axis'])
            self._data = value.reshape(ax_rs)
        else:
            if value.ndim != 2:
                print('Spectra: converting data input from {}D to 2D ndarray'.format(value.ndim))
            if value.shape[-1] == self.freq.op_range_pix.size:
                temp = _np.zeros((self._data.shape), dtype=value.dtype)
                temp[:, self.freq.op_range_pix] = value
                self._data = temp
            elif value.shape[-1] == self.freq.size:
                temp = _np.zeros((self._data.shape), dtype=value.dtype)
                temp[..., self.freq.op_range_pix] = value[..., self.freq.op_range_pix].reshape((-1, len(self.freq.op_range_pix)))
                self._data = temp
            else:
                raise TypeError('data is of an unrecognized shape: {}'.format(value.shape))

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
        elif isinstance(spectra, Spectrum):
            if overwrite:
                self.data -= spectra.data[None, :]
                return None
            else:
                return self.data - spectra.data[None, :]
        elif isinstance(spectra, _np.ndarray):
            if spectra.shape == self.data.shape:
                if overwrite:
                    self.data -= spectra
                    return None
                else:
                    return self.data - spectra
            else:
                if overwrite:
                    self.data -= spectra[None, :]
                    return None
                else:
                    return self.data - spectra[None, :]

    def __sub__(self, spectrum):
        return self.subtract(spectrum, overwrite=False)


if __name__ == '__main__':  # pragma: no cover
    sp = Spectra()
    print(sp.__dict__)
    print('Subclass? : {}'.format(issubclass(Spectra, Spectrum)))
    print('Instance of Spectra? : {}'.format(isinstance(sp, Spectra)))
    print('Instance of Spectrum? : {}'.format(isinstance(sp, Spectrum)))
    print('Type(sp) == Spectrum? : {}'.format(type(sp) == Spectrum))
    print('Type(sp) == Spectra? : {}'.format(type(sp) == Spectra))
