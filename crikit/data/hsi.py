"""
Hyperspectral imagery (hsi) class

Created on Tue Apr 12 13:06:30 2016

@author: chc
"""

import numpy as _np
import copy as _copy

from crikit.data.frequency import Frequency as _Frequency
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.replicate import Replicate as _Replicate

__all__ = ['Hsi']

class Hsi(_Spectrum):
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
        #                       dtype=_np.int)

        if self.freq is None or self.freq.op_list_pix is None:
            self._data = value.reshape(ax_rs)
        else:
            if value.shape[self.config['nd_axis']] == self.freq.op_range_pix.size:
                temp = _np.zeros((self._data.shape),dtype=value.dtype)
                temp[:,:,self.freq.op_range_pix] = value.reshape(ax_rs)
                self._data = 1*temp
                del temp
            elif value.shape[self.config['nd_axis']] == self._data.shape[self.config['nd_axis']]:
                temp = _np.zeros((self._data.shape),dtype=value.dtype)
                temp[..., self.freq.op_range_pix] = value.reshape(ax_rs)[..., self.freq.op_range_pix]
                self._data = 1*temp
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
        elif isinstance(spectra, _Spectrum):
            if overwrite:
                self.data -= spectra.data[None,None,:]
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
                    self.data -= spectra[None,None,:]
                    return None
                else:
                    return self.data - spectra[None,None,:]

    def get_rand_spectra(self, num, pt_sz=1, quads=False, full=False):

        mlen, nlen, freqlen = self.data.shape

        if quads:
            num_spectra = num + 5
        else:
            num_spectra = num

        if _np.iscomplexobj(self.data):
            dtype = _np.complex
        else:
            dtype = _np.float

        temp = _np.zeros((num_spectra, self.data.shape[-1]), dtype=dtype)

        quad_mid_row = int(_np.round(mlen/2))
        quad_mid_col = int(_np.round(nlen/2))
        center_row = (int(_np.round(mlen/3)), int(_np.round(2*mlen/3)))
        center_col = (int(_np.round(nlen/3)), int(_np.round(2*nlen/3)))

        start_count = 0
        if quads:
            # QUADS
            # Bottom-left
            temp[0, :] = _np.mean(self.data[0:quad_mid_row, 0:quad_mid_col, :], axis=(0, 1))

            # Upper-left
            temp[1, :] = _np.mean(self.data[0:quad_mid_row, quad_mid_col+1::, :], axis=(0, 1))

            # Upper-right
            temp[2, :] = _np.mean(self.data[quad_mid_row+1::, quad_mid_col+1::, :], axis=(0, 1))

            # Bottom-right
            temp[3, :] = _np.mean(self.data[quad_mid_row+1::, 0:quad_mid_col, :], axis=(0, 1))

            # Center
            temp[4, :] = _np.mean(self.data[center_row[0]:center_row[1], center_col[0]:center_col[1], :], axis=(0, 1))

            start_count += 5
        else:
            pass

        rand_rows = ((mlen-pt_sz-1)*_np.random.rand(num_spectra)).astype(int)
        rand_cols = ((nlen-pt_sz-1)*_np.random.rand(num_spectra)).astype(int)

        for count in _np.arange(start_count,num_spectra):
            if pt_sz == 1:
                temp[count, :] = _np.squeeze(self.data[rand_rows[count-start_count],
                                            rand_cols[count-start_count]])
            else:

                rows = [rand_rows[count-start_count]-(pt_sz-1),
                        rand_rows[count-start_count]+pt_sz]
                cols = [rand_cols[count-start_count]-(pt_sz-1),
                                 rand_cols[count-start_count]+pt_sz]

                if rows[0] < 0:
                    rows[0] = 0
                if rows[1] >= mlen:
                    rows[1] = mlen-1
                if cols[0] < 0:
                    cols[0] = 0
                if cols[1] >= nlen:
                    cols[1] = nlen-1

                if cols[0] == cols[1] or rows[0] == rows[1]:
                    pass
                else:
                    temp[count,:] = _np.squeeze(_np.mean(self.data[rows[0]:rows[1], cols[0]:cols[1], :], axis=(0, 1)))

        if (not full) and (self.freq.data is not None):
            temp = temp[..., self.freq.op_range_pix]

        return temp

    def __sub__(self, spectrum):
        return self.subtract(spectrum, overwrite=False)

if __name__ == '__main__': # pragma: no cover

    x = _np.linspace(0,100,10)
    y = _np.linspace(0,100,10)
    freq = _np.arange(20)
    data = _np.random.rand(10,10,20)


    hs = Hsi(data=data, freq=freq, x=x, y=y)
    print(hs.shape)
    print(isinstance(hs, _Spectrum))
