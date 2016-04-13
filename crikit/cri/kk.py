# -*- coding: utf-8 -*-
"""
Kramers-Kronig relation phase retrieval.

References
----------
[1] Y. Liu, Y. J. Lee, and M. T. Cicerone, "Broadband CARS spectral
phase retrieval using a time-domain Kramers-Kronig transform,"
Opt. Lett. 34, 1363-1365 (2009).

[2] C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative, \
Comparable Coherent Anti-Stokes Raman Scattering (CARS) \
Spectroscopy: Correcting Errors in Phase Retrieval," Journal of Raman \
Spectroscopy 47, 408-415 (2016). arXiv:1507.06543.


"""

__all__ = ['kk']

import numpy as _np
import timeit as _timeit

if __name__ == '__main__':
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))

from crikit.cri.algorithms.kk import kkrelation as _kkrelation
from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

def kk(cars_obj, nrb_obj, cars_amp_offset=0.0, nrb_amp_offset=0.0, phase_offset=0.0,
       norm_to_nrb=True, pad_factor=1, overwrite=True):

    """
    Retrieve the real and imaginary components of coherent Raman data via the \
    Kramers-Kronig (KK) relation. See References.

    Parameters
    ----------
    cars_obj : Spectrum (or subclass) object. See Notes.
        Coherent Raman signal.

    nrb_obj : Spectrum (or subclass) object or ndarray. See Notes.
        Nonresonant background (NRB)

    cars_amp_offset : float, optional (default=0.0)
        DC offset applied to CARS spectrum(a) prior to KK relation. See Notes \
        and Ref. [2].

    nrb_amp_offset : float, optional (default=0.0)
        DC offset applied to NRB spectrum(a) prior to KK relation. See Notes \
        and Ref. [2].

    phase_offset : float or ndarray, optional (default=0.0)
        Phase constant or ndarray applied to retrieved phase prior to \
        separating the real and imaginary components. See Notes \
        and Ref. [2].

    norm_to_nrb : bool, optional (default=True)
        Normalize the amplitude by sqrt(NRB). This effectively removes several \
        system reponse functions. Highly recommended. See Ref. [2]

    pad_factor : int, optional (default=1)
        Multiple size of spectral-length to pad the ends of each spectra with. \
        Padded with a constant value corresponding to the value at that end of \
        the spectrum. See Ref. [1].

    overwrite : bool, optional (default=True)
        Overwrite data_cls with new values or simply return result as ndarray

    Returns
    -------
    ndarray
        Altered data if overwrite is False

    None
        Return None if overwrite is True

    Notes
    -----
    * The imaginary components provides the sponatenous Raman-like spectra(um).
    * This module assumes the spectra are oriented as such that the frequency \
    (wavenumber) increases with increasing index.  If this is not the case for \
    your spectra(um), apply a phase_offset of pi.

    References
    ----------
    [1] Y. Liu, Y. J. Lee, and M. T. Cicerone, "Broadband CARS spectral
    phase retrieval using a time-domain Kramers-Kronig transform,"
    Opt. Lett. 34, 1363-1365 (2009).

    [2] C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative, \
    Comparable Coherent Anti-Stokes Raman Scattering (CARS) \
    Spectroscopy: Correcting Errors in Phase Retrieval," Journal of Raman \
    Spectroscopy 47, 408-415 (2016). arXiv:1507.06543.

    """

    UNITS = 'Norm. Raman Int. (au)'

    if isinstance(cars_obj,_Spectrum) == False:  # True if type Spectrum **OR** a subclass of Spectrum
        raise TypeError('cars_obj must be of class (or subclass) Spectrum')
    ndim_cars = cars_obj.ndim
    if cars_obj.freq.op_list_pix is None or len(cars_obj.freq.op_list_pix) == 0:
        pixrange = _np.arange(0, cars_obj.freq.size)
    else:
        pixrange = _np.arange(cars_obj.freq.op_list_pix[0],cars_obj.freq.op_list_pix[1]+1)

    if isinstance(nrb_obj,_Spectrum):
        nrb = _np.squeeze(nrb_obj.data)
    elif isinstance(nrb_obj, _np.ndarray):
        nrb = _np.squeeze(nrb_obj)
    else:
        raise TypeError('nrb_obj must be of class (or subclass) Spectrum or ndarray')
    ndim_nrb = nrb.ndim

    if cars_obj.data.shape[-1] != nrb.shape[-1] or not \
        (ndim_nrb == ndim_cars or ndim_nrb == 1):
        raise TypeError('Cannot broadcast {} and {}'.format(cars_obj.shape,nrb.shape))

    shp = list(cars_obj.shape)
    shp[-1] = pixrange[-1] - pixrange[0] + 1
    kkd = _np.zeros(shp, dtype=complex)

    if ndim_cars == 1:
        kkd = _kkrelation(bg=nrb[pixrange] + nrb_amp_offset,
                          sri=cars_obj.data[pixrange] + cars_amp_offset,
                          phase_offset=phase_offset,
                          norm_by_bg=norm_to_nrb,
                          pad_factor=pad_factor)

    elif ndim_cars == 2:
        kkd = _kkrelation(bg=nrb[pixrange] + nrb_amp_offset,
                          sri=cars_obj.data[:,pixrange] + cars_amp_offset,
                          phase_offset=phase_offset,
                          norm_by_bg=norm_to_nrb,
                          pad_factor=pad_factor)

    elif ndim_cars == 3:
        for row_num, spa in enumerate(cars_obj.data):
            kkd[row_num,:,:] = _kkrelation(bg=nrb[pixrange] + nrb_amp_offset,
                          cri=spa[:,pixrange] + cars_amp_offset,
                          phase_offset=phase_offset,
                          norm_by_bg=norm_to_nrb,
                          pad_factor=pad_factor)

    elif ndim_cars > 3:
        raise NotImplementedError('cars_obj must be 1D, 2D, or 3D')
    else:
        raise TypeError('cars_obj must be 1D, 2D, or 3D')

    if overwrite:
        cars_obj.data = kkd
        cars_obj.units = UNITS
        return None
    else:
        return kkd

if __name__ == '__main__':

    hsi = _Hsi()
    nrb = _Spectra()

    WN = _np.linspace(-1386,3826,1600)
    X = .055 + 1/(1000-WN-1j*20) + 1/(3000-WN-1j*20)
    XNR = 0*X + 0.055
    E = 1*_np.exp(-(WN-2000)**2/(2*3000**2))

    # Simulated spectrum
    CARS = _np.abs(E+X)**2
    NRB = _np.abs(E+XNR)**2
    nrb.data = NRB

    # Copies of spectrum
    temp = _np.dot(_np.ones((100,100,1)),CARS[None,:])

    # Create an HSData class instance
    hsi.data = temp
    num_spectra = int(hsi.size/WN.size)

    hsi.freq = WN

    start = _timeit.default_timer()
    kkd = _kkrelation(NRB,CARS)
    stop = _timeit.default_timer()
    print('Single spectrum -- Total time: {:.6f} sec'.format(stop-start))

    start = _timeit.default_timer()
    kkd = _kkrelation(NRB,temp)
    stop = _timeit.default_timer()
    print('Data-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))

    start = _timeit.default_timer()
    kk(hsi, nrb, cars_amp_offset=0, nrb_amp_offset=0, norm_to_nrb=False, pad_factor=1)
    stop = _timeit.default_timer()
    print('Class-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))

    hsi.data = temp

    import matplotlib.pyplot as plt
    hsi.freq.op_list_freq = [500,4000]

    plt.plot(hsi.freq.freq_vec[hsi.freq.op_range_pix], hsi.data[0,0,hsi.freq.op_range_pix])

    start = _timeit.default_timer()
    kk(hsi, nrb, cars_amp_offset=0, nrb_amp_offset=0, norm_to_nrb=False, pad_factor=1)
    stop = _timeit.default_timer()
    print('Pixrange Class-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))


    plt.plot(hsi.freq.freq_vec[hsi.freq.op_range_pix],hsi.data[0,0,:].imag)
    plt.show()