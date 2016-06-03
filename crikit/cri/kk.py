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

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

from crikit.cri.algorithms.kk import kkrelation as _kkrelation

from crikit.utils.gen_utils import find_nearest as _find_nearest

def kk(cars, nrb, cars_amp_offset=0.0, nrb_amp_offset=0.0, phase_offset=0.0,
       norm_to_nrb=True, pad_factor=1, rng=None, freq=None):

    """
    Retrieve the real and imaginary components of coherent Raman data via the \
    Kramers-Kronig (KK) relation. See References.

    Parameters
    ----------
    cars_obj : ndarray
        Coherent Raman signal.

    nrb_obj : ndarray
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

    rng : list/tuple, optional (default=None)
        Range of pixels/frequencies (if freq provided) to perform over

    freq : ndarray (1D), optional (default=None)
        Frequency vector

    Returns
    -------
    ndarray
        KK of cars

    Notes
    -----
    * This function does NOT overwrite input data
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

    ndim_cars = cars.ndim
    if rng is None or len(rng) == 0:
        pixrange = _np.arange(0, cars.shape[-1])
    elif freq is not None:  # rng in units of frequency; thus, find pixels
        pix_lims = _find_nearest(freq, rng)[-1]
        pix_lims[-1] += 1  # +1 for inclusiveness
        pixrange = _np.arange(pix_lims[0], pix_lims[1])
    else:  # rng in units of pixels
        rng[-1] += 1  # +1 for inclusiveness
        pixrange = _np.arange(rng[0],rng[1])

    # Ensure minimum NRB dimensionality
    nrb = _np.squeeze(nrb)
    ndim_nrb = nrb.ndim

    # Assume that an nD nrb should be averaged to be 1D
    if ndim_nrb > 1:
        nrb = nrb.mean(axis=tuple(range(ndim_nrb-1)))

    # Shape of output data between pixrange
    shp = list(cars.shape)
    shp[-1] = pixrange[-1] - pixrange[0] + 1
    kkd = _np.zeros(shp, dtype=complex)

    if ndim_cars < 3:
        kkd = _kkrelation(bg=nrb[pixrange] + nrb_amp_offset,
                          cri=cars[...,pixrange] + cars_amp_offset,
                          phase_offset=phase_offset,
                          norm_by_bg=norm_to_nrb,
                          pad_factor=pad_factor)

    elif ndim_cars == 3:
        for row_num, spa in enumerate(cars):
            print
            kkd[row_num,:,:] = _kkrelation(bg=nrb[pixrange] + nrb_amp_offset,
                          cri=spa[...,pixrange] + cars_amp_offset,
                          phase_offset=phase_offset,
                          norm_by_bg=norm_to_nrb,
                          pad_factor=pad_factor)

    elif ndim_cars > 3:
        raise NotImplementedError('cars_obj must be 1D, 2D, or 3D')
    else:
        raise TypeError('cars_obj must be 1D, 2D, or 3D')

    return kkd

if __name__ == '__main__': # pragma: no cover

    from crikit.data.spectrum import Spectrum as _Spectrum
    from crikit.data.spectra import Spectra as _Spectra
    from crikit.data.hsi import Hsi as _Hsi

    hsi = _Hsi()
    nrb = _Spectra()

    WN = _np.linspace(-1386,3826,400)
    X = .055 + 1/(1000-WN-1j*20) + 1/(3000-WN-1j*20)
    XNR = 0*X + 0.055
    E = 1*_np.exp(-(WN-2000)**2/(2*3000**2))

    # Simulated spectrum
    CARS = _np.abs(E+X)**2
    NRB = _np.abs(E+XNR)**2
    nrb.data = NRB

    # Copies of spectrum
    temp = _np.dot(_np.ones((300,300,1)),CARS[None,:])

    # Create an HSData class instance
    hsi.data = temp
    num_spectra = int(hsi.size/WN.size)

    hsi.freq = WN

    start = _timeit.default_timer()
    kkd = _kkrelation(NRB,CARS)
    stop = _timeit.default_timer()
    print('Single spectrum -- Total time: {:.6f} sec'.format(stop-start))
    _timeit.time.sleep(2)

    start = _timeit.default_timer()
    kkd = _kkrelation(NRB,temp)
    stop = _timeit.default_timer()
    print('Data-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))
    _timeit.time.sleep(2)


    start = _timeit.default_timer()
    kk(hsi.data, nrb.data, cars_amp_offset=0, nrb_amp_offset=0, norm_to_nrb=False, pad_factor=1)
    stop = _timeit.default_timer()
    print('Class-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))

    hsi.data = temp
    _timeit.time.sleep(2)


    import matplotlib as mpl
    mpl.rcParams['font.size'] = 14
    import matplotlib.pyplot as plt

    hsi.freq.op_list_freq = [500, 4000]

    #plt.plot(hsi.freq.freq_vec[hsi.freq.op_range_pix], hsi.data[0,0,hsi.freq.op_range_pix])

    start = _timeit.default_timer()
    kkd = kk(hsi.data, nrb.data, cars_amp_offset=0, nrb_amp_offset=0,
       norm_to_nrb=False, rng=hsi.freq.op_list_freq, freq=hsi.freq.data,
       pad_factor=1)
    stop = _timeit.default_timer()
    print('Pixrange Class-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))

    hsi.data = kkd
    _timeit.time.sleep(2)

    plt.plot(WN, X.imag, label='Imag.{$\chi_{R}$}')
    plt.plot(hsi.freq.data[hsi.freq.op_range_pix],
             hsi.data[0,0,hsi.freq.op_range_pix].imag, 'r*',
             label='KK-Retrieved')
    plt.legend(loc='best')
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Raman Int. (au)')
    plt.title('Raman vs KK-Retrieved CARS')
    plt.show()

    print(_np.allclose(X.imag[hsi.freq.op_range_pix], hsi.data[0,0,hsi.freq.op_range_pix].imag,rtol=1))