"""
"Frequency" [,wavelength, and wavenumber] class and function.

"""

import numpy as _np
import copy as _copy
from crikit.utils.general import find_nearest as _find_nearest

__all__ = ['Frequency', 'calib_pix_wn', 'calib_pix_wl']

class Frequency:
    """
    Frequency [,wavelength, and wavenumber] class

    Attributes
    ----------
    data : 1D ndarray, optional (see note)
        Frequency vector

    calib : object, optional (see note)
        Calibration object that is passed to calib_fcn

    calib_orig : object, optional (see note)
        Calibration object ('original'). Set during initial setting of calib. \
        Useful for backing-up calibration)

    calib_fcn : fcn, optional (see note)
        Function that accepts a calibration object and returns data and \
        units

    units : str, optional
        Units of data (the default is 'Frequency'). Over-written by return \
        from calib_fcn

    op_list_pix : list or tuple or 1D ndarray
        Range of pixels to perform operations over. Must be even lengthed.

    op_list_freq : list or tuple or 1D ndarray
        Range of frequencies (or wavelength, or wavenumber) to perform \
        operations over. Must be even lengthed.

    plot_list_pix : list or tuple or 1D ndarray
        Range of pixels to plot. Must be even lengthed.

    plot_list_freq : list or tuple or 1D ndarray
        Range of frequencies (or wavelength, or wavenumber) to plot. \
        Must be even lengthed.

    size : int, read-only
        Length of data

    pix_vec : 1D ndarray, read-only
        Pixel vector (0-indexed)

    op_range_freq : 1D ndarray, read-only
        Range of operarational frequencies

    plot_range_freq : 1D ndarray, read-only
        Range of printing frequencies (not implemented)

    Methods
    -------
    update
        Updates data based on contents of calib (or calib_orig) and calib_fcn

    get_index_of_closest_freq
        Find the closest frequency in freq to a given freq value and RETURN
        the pixel value.

    get_closest_freq
        Find the closest frequency in freq to a given freq value.

    Notes
    -----
    Currently, this implementation does not check whether the 
    attributes/parameters are contradictory:
    - calib
    - calib_orig
    - data

    - The purpose of _list_ is to limit the range over which operation \
    or plotting is performed. In some instances, for example, one may collect \
    a larger set of frequencies that of interest or there may be blank (i.e., \
    no signal) regions. Limiting these regions enables faster computation, may \
    minimize "edge effects", and may allow for zoomed-in plotting when there \
    are items of interest or a large dynamic range across a spectrum.

    - For functions, methods, etc. that take into account _list_ \
    parameters, they should default to op_list_* if plot_list_* are set to \
    None.

    """

    def __init__(self, data=None, calib=None, calib_orig=None,
                 calib_fcn=None, units=None):


        self._data = None
        self._calib = None
        self._calib_orig = None
        self._calib_fcn = None
        self._label = None
        self._units = None
        self._op_list_pix = None
        self._op_list_freq = None
        self._plot_list_pix = None
        self._plot_list_freq = None

        if data is not None:
            self.data = data
        if calib is not None:
            self.calib = calib
        if calib_orig is not None:
            self.calib_orig = calib_orig
        if calib_fcn is not None:
            self.calib_fcn = calib_fcn
        if units is not None:
            self.units = units

        if (self._data is None) and (self._calib is not None) and \
            (self._calib_fcn is not None):
            self.update()

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
        elif value is None:
            self._data = None
        else:
            raise TypeError('data must be a 1D ndarray')

    @property
    def calib(self):
        return self._calib

    @calib.setter
    def calib(self, value):
        if isinstance(value, dict):
            self._calib = value
            if self._calib_orig is None:
                self._calib_orig = value
        elif value is None:
            self._calib = None
            self.update()
        else:
            raise TypeError('calib must be of type dict')
            
    @calib.deleter
    def calib(self):
        self._calib = None
        self.update()


    @property
    def calib_orig(self):
        return self._calib_orig

    @calib_orig.setter
    def calib_orig(self, value):
        if isinstance(value, dict):
            self._calib_orig = value
        else:
            raise TypeError('calib_orig must be of type dict')


    @property
    def calib_fcn(self):
        return self._calib_fcn

    @calib_fcn.setter
    def calib_fcn(self, value):
        if callable(value):
            self._calib_fcn = value
        else:
            raise TypeError('calib_fcn must be a callable function')

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
    def size(self):
        return self.data.size

    @property
    def pix_vec(self):
        return _np.arange(self.data.size)

    def update(self):
        """
        Update data with calib and calib_fcn.
        """
        if self._calib_fcn is None:
            raise TypeError('Calibration function not set')
        if self._calib is None:
            if self._calib_orig is None:
                raise TypeError('Calibration object not set')
            else:
                self.calib = self._calib_orig

        self.data, self.units = self.calib_fcn(self.calib)  # pylint: disable=not-callable

    @property
    def op_list_pix(self):
        return self._op_list_pix

    @op_list_pix.setter
    def op_list_pix(self,value):
        if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, _np.ndarray):
            if len(value) == 2:
                value = list(value)
                value.sort()
                self._op_list_pix = value
                # if self.data is not None:  # ! Allow setting without freq or not?
                self._op_list_freq = self.get_closest_freq(value)
                self._op_list_freq.sort()
            elif len(value) != 2 and _np.mod(len(value),2) == 0 and len(value) != 0:
                raise NotImplementedError('op_list_pix can only currently handle 2 entries')
            else:
                raise TypeError('op_list_pix should be a list, tuple, or ndarray with an even number of entries')
        else:
            raise TypeError('op_list_pix should be a list, tuple, or ndarray')

    @op_list_pix.deleter
    def op_list_pix(self):
        self._op_list_pix = None
        self._op_list_freq = None

    @property
    def op_list_freq(self):
        return self._op_list_freq

    @op_list_freq.setter
    def op_list_freq(self,value):
        if isinstance(value, list) or isinstance(value, tuple) or isinstance(value, _np.ndarray):
            if len(value) == 2:
                value = list(value)
                value.sort()
                self._op_list_pix = self.get_index_of_closest_freq(value)
                self._op_list_pix.sort()
                self._op_list_freq = self.get_closest_freq(value)
                self._op_list_freq.sort()
            elif len(value) != 2 and _np.mod(len(value),2) == 0 and len(value) != 0:
                raise NotImplementedError('op_list_freq can only currently handle 2 entries')
            elif len(value) == 0:
                self._op_list_freq = None
                self._op_list_pix = None
            else:
                raise TypeError('op_list_freq should be a list, tuple, or ndarray with an even number of entries')
        else:
            raise TypeError('op_list_freq should be a list, tuple, or ndarray')

    @op_list_freq.deleter
    def op_list_freq(self):
        self._op_list_pix = None
        self._op_list_freq = None

    @property
    def op_range_pix(self):
        if self._op_list_pix is not None:
            return _np.arange(self._op_list_pix[0],self._op_list_pix[1]+1)
        else:
            return self.pix_vec

    @property
    def op_range_freq(self):
        if self._op_list_pix is not None:
            return self.data[self.op_range_pix]
        else:
            return self.data

    @property
    def op_size(self):
        if self._op_list_pix is None:
            return self.data.size
        else:
            return self._op_list_pix[-1] - self._op_list_pix[0] + 1

    @property
    def plot_list_pix(self):
        raise NotImplementedError('plot_list_pix is not yet implemented')

    @property
    def plot_list_freq(self):
        raise NotImplementedError('plot_list_freq is not yet implemented')


    def get_index_of_closest_freq(self, in_freqs):
        """
        Return index(-es) of frequency(-ies) in freq closest to in_freqs
        """
        return _find_nearest(self.data, in_freqs)[1]

    def get_closest_freq(self, in_freqs):
        """
        Return frequency(-ies) in freq closest to in_freqs
        """
        return _find_nearest(self.data, in_freqs)[0]

def calib_pix_wl(calib_obj):
    """
    Return a wavelength (wl) vector based on calibration (calib) object

    Parameters
    ----------
    calib_obj : dict or list or 1D ndarray
        Calibration object (see below).

    calib_obj : dict {'n_pix', 'ctr_wl', 'ctr_wl0', 'units', 'a_vec'}
        Calibration dict with 5 key-value pairs (see Notes)

    calib_obj : list or 1D ndarray
        Calibration array ['n_pix', 'ctr_wl', 'ctr_wl0', 'units',
        'a_0', 'a_1', ..., 'a_n']
    Returns
    -------
    wl_vec : 1D ndarray
        Wavelength vector
    units : str
        Units string 'Wavelength (' + calib_obj['units'] + ')'

    Notes
    -----
    calib_obj dict key-value pairs:
        * n_pix : int, number of pixels (0-index)
        * ctr_wl : float, center wavelength
        * ctr_wl0 : float, center calibration wavelength
        * units : str, wavelength units, optional (default is 'nm')
        * a_vec : list or 1D ndarray, polynomial coefficients, [a_n, a_n-1,..., \
        a_1, a_0]. a_2...a_n, optional.

    calibration model:
        .. math::
            wl\_{vec} = a_n*(n\_{pix})^n + a_{n-1}*(n\_{pix})^{n-1} + ~...~ +  \
            n\_{pix}*a_1 + a_0 + ctr\_{wl} - ctr\_{wl0}

    """


    calib = {}

    if len(calib_obj) < 4:
        raise TypeError('Calibration object does not contain enough entries')

    if isinstance(calib_obj, dict):
        key_list = ['n_pix','ctr_wl', 'ctr_wl0', 'a_vec']
        for k in key_list:
            if k not in calib_obj:
                raise KeyError('Calibration dict missing: {}'.format(k))
            else:
                calib[k] = calib_obj[k]
        if 'units' in calib_obj:
            calib['units'] = calib_obj['units']
        else:
            calib['units'] = 'nm'

    pix = _np.arange(calib['n_pix'])
    wl_vec = _np.polyval(calib['a_vec'], pix)
    wl_vec += calib['ctr_wl'] - calib['ctr_wl0']

    return (wl_vec, calib['units'])

def calib_pix_wn(calib_obj):
    """
    Return a wavenumber (wn) vector based on calibration (calib) object

    Parameters
    ----------
    calib_obj : dict or list or 1D ndarray
        Calibration object (see below).

    calib_obj : dict {'n_pix', 'ctr_wl', 'ctr_wl0', 'probe', 'units', 'a_vec'}
        Calibration dict with 6 key-value pairs (see Notes)

    calib_obj : list or 1D ndarray
        Calibration array ['n_pix', 'ctr_wl', 'ctr_wl0', 'probe', 'units',
        'a_0', 'a_1', ..., 'a_n']

    Returns
    -------
    wn_vec : 1D ndarray
        Wavenumber vector
    units : str
        Wavenumber units. Always 'cm$^-1$'

    Notes
    -----
    calib_obj dict key-value pairs:
        * n_pix : int, number of pixels (0-index)
        * ctr_wl : float, center wavelength
        * ctr_wl0 : float, center calibration wavelength
        * probe : float, center wavelength of probe source (in units)
        * units : {'nm', 'um'}, wavelength units, optional (default is 'nm')
        * a_vec : list or 1D ndarray, polynomial coefficients, [a_n, a_n-1,..., \
        a_1, a_0]. a_2...a_n, optional.

    calibration model :
        Wavelength vector:
            .. math::
                wl\_{vec} = a_n*(n\_{pix})^n + a_{n-1}*(n\_{pix})^{n-1} + ~...~ +  \
                n\_{pix}*a_1 + a_0 + ctr\_{wl} - ctr\_{wl0}
        Wavenumber vector:
            .. math::
                wl\_{vec} = a_n*(n\_{pix})^n + a_{n-1}*(n\_{pix})^{n-1} + ~...~ +  \
                n\_{pix}*a_1 + a_0 + ctr\_{wl} - ctr\_{wl0}

    """
    calib = _copy.deepcopy(calib_obj)

    if 'probe' not in calib:
        raise KeyError('\'probe\' key not in calib_obj')

    if 'units' not in calib:
        calib['units'] = 'nm'
    elif isinstance(calib['units'], bytes):
        calib['units'] = calib['units'].decode()

    if calib['units'] == 'nm':
        factor = 1e7
    elif calib['units'] == 'um':
        factor = 1e4
    else:
        errstr1 = 'Only nanometer (\'nm\') and micrometer (\'um\') units accepted. '
        errstr2 = '{} provided of type {}.'.format(calib['units'], type(calib['units']))
        raise ValueError(errstr1 + errstr2)
    wl_vec, _ = calib_pix_wl(calib_obj)
    wn_vec = factor/wl_vec - factor/calib['probe']
    return (wn_vec, 'cm$^{-1}$')

if __name__ == '__main__':  # pragma: no cover
    import matplotlib as _mpl
    _mpl.use('Qt5Agg')
    _mpl.rcParams['font.family'] = 'sans-serif'
    _mpl.rcParams['font.size'] = 12
    import matplotlib.pyplot as _plt

    _calib_dict = {}
    _calib_dict['n_pix'] = 1600
    _calib_dict['ctr_wl'] = 730.0
    _calib_dict['ctr_wl0'] = 730.0
    _calib_dict['probe'] = 771.461
    _calib_dict['units'] = 'nm'
    _calib_dict['a_vec'] = (-0.167740721307557, 863.8736708961577)  # slope, intercept

    _wl_vec, _units_wl = calib_pix_wl(_calib_dict)
    _wn_vec, _units_wn = calib_pix_wn(_calib_dict)
    _plt.plot(_wl_vec, _wn_vec)
    _plt.xlabel('Wavelength ({})'.format(_units_wl))
    _plt.ylabel('Wavenumber ({})'.format(_units_wn))
    _plt.title('Wavenumber vs Wavelength')
    _plt.show()