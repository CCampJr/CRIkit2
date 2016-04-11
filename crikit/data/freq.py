# -*- coding: utf-8 -*-
"""
"Frequency" [,wavelength, and wavenumber] class and function.

"""

import numpy as _np
import copy as _copy

__all__ = ['Frequency', 'calib_pix_wn', 'calib_pix_wl']

class Frequency:
    """
    Frequency [,wavelength, and waevnumber] class

    Attributes
    ----------
    freq_vec : 1D ndarray, optional (see note)
        Frequency vector

    calib_in : object, optional (see note)
        Calibration object that is passed to calib_fcn

    calib_fcn : fcn, optional (see note)
        Function that accepts a calibration object and returns freq_vec and \
        units

    units : str, optional
        Units of freq_vec (the default is 'Frequency'). Over-written by return \
        from calib_fcn

    Methods
    -------

    Notes
    -----
    Some input is necessary, either:
        * freq_vec
        * calib and calib_fcn

    Currently, this implementation does not check whether the \
    attributes/parameters are contradictory:
        * calib
        * calib_orig
        * freq_vec

    """

    def __init__(self, freq_vec=None, calib=None, calib_fcn=None, units=None):


        self.freq_vec = freq_vec
        self.units=units
        self.calib = calib
        self.calib_fcn = calib_fcn
        self.calib_orig = None

        if freq_vec is not None:
            if calib is not None:
                self.calib = calib
                self.calib_orig = calib
            self.calib_fcn = calib_fcn
        elif calib is not None and calib_fcn is not None:
            self.calib = calib
            self.calib_orig = calib
            self.calib_fcn = calib_fcn
            self.freq_vec, self.units = self.calib_fcn(calib)
        elif ((calib is not None) and (calib_fcn is None)) or \
        (calib is None) and (calib_fcn is not None):
             raise TypeError('Requires either an input frequency vector or a \
                             calibration and conversion function')

        else:  # No inputs
           pass

    @property
    def size(self):
        return self.freq_vec.size

    def update(self):
        """
        Update freq_vec with calib and calib_fcn.
        """
        try:
            self.freq_vec, self.units = self.calib_fcn(self.calib)
        except:
            try:
                self.calib = self.calib_orig
                self.freq_vec, self.units = self.calib_fcn(self.calib)
            except:
                if self.calib is None:
                    raise TypeError('Calibration object not set')
                else:
                    raise TypeError('Calibration function not set')

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
        factor = 1e7
    elif calib['units'] == 'nm':
        factor = 1e7
    elif calib['units'] == 'um':
        factor = 1e4
    else:
        raise ValueError('Only nanometer (\'nm\') and micrometer (\'um\') units accepted')
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