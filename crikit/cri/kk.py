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

import timeit as _timeit

import numpy as _np

from crikit.cri.algorithms.kk import kkrelation as _kkrelation
from crikit.utils.datacheck import _rng_is_pix_vec
from crikit.utils.general import find_nearest as _find_nearest
from crikit.utils.general import mean_nd_to_1d as _mean_nd_to_1d

class KramersKronig:
    """
    Retrieve the real and imaginary components of coherent Raman data via the \
    Kramers-Kronig (KK) relation. See References.

    Parameters
    ----------

    cars_amp_offset : float, optional (default=0.0)
        DC offset applied to CARS spectrum(a) prior to KK relation. See Notes \
        and Ref. [2].

    nrb_amp_offset : float, optional (default=0.0)
        DC offset applied to NRB spectrum(a) prior to KK relation. See Notes \
        and Ref. [2].

    conjugate : bool
        If spectra go from high-to-low-wavenumber (left-to-right), you should
        conjugate the KK output.

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

    rng : ndarray (1D), optional (default=None)
        Range of pixels/frequencies (if freq provided) to perform over

    n_edge : int, optional
        For edge values, take a mean of n_edge neighbors

    axis : int, optional
        Axis to perform over

    min_value : float, optional
        Applies to cars/nrb (the ratio). Values below min_value set to min_value

    bad_value : float, optional
        Applies to cars/nrb (the ratio). Inf's and NaN's set to bad_value

    hilb_kwargs : dict
        kwargs sent to the hilbert transform. Only pad_factor, n_edge, and axis
        are automatically sent -- these will overwrite anything in hilb_kwargs.

    Returns
    -------
    ndarray
        KK of cars

    Notes
    -----
    
    -   This function does NOT overwrite input data
    -   The imaginary components provides the sponatenous Raman-like spectra(um).
    -   This module assumes the spectra are oriented as such that the frequency 
         (wavenumber) increases with increasing index.  If this is not the case for
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
    def __init__(self, cars_amp_offset=0.0, nrb_amp_offset=0.0, conjugate=False,
                 phase_offset=0.0, norm_to_nrb=True, pad_factor=1, 
                 rng=None, n_edge=1, axis=-1, bad_value=1e-8, min_value=None,
                 hilb_kwargs={}, **kwargs):

        # Hilbert transform kwargs
        self.hilb_kwargs = hilb_kwargs

        # KK kwargs
        self.kk_kwargs = {'conjugate':conjugate,
                          'phase_offset':phase_offset,
                          'norm_to_nrb':norm_to_nrb,
                          'pad_factor':pad_factor,
                          'n_edge':n_edge, 
                          'axis':axis,
                          'bad_value':bad_value,
                          'min_value':min_value}

        self.cars_amp_offset = cars_amp_offset
        self.nrb_amp_offset = nrb_amp_offset

        # Check range of operation
        self.rng = _rng_is_pix_vec(rng)

    @property
    def phase_offset(self):
        """ Phase offset """
        return self.kk_kwargs['phase_offset']

    @phase_offset.setter
    def phase_offset(self, value):
        """ Set Phase Offset """
        self.kk_kwargs['phase_offset'] = value

    @property
    def norm_to_nrb(self):
        """ norm_to_nrb """
        return self.kk_kwargs['norm_to_nrb']

    @norm_to_nrb.setter
    def norm_to_nrb(self, value):
        """ Set norm_to_nrb """
        self.kk_kwargs['norm_to_nrb'] = value

    @property
    def pad_factor(self):
        """ pad_factor """
        return self.kk_kwargs['pad_factor']

    @pad_factor.setter
    def pad_factor(self, value):
        """ Set pad_factor """
        self.kk_kwargs['pad_factor'] = value

    def _calc(self, cars, nrb, ret_obj):

        # Assume that an nD nrb should be averaged to be 1D
        # TODO: Change this in the future to accept matching NRB's
        nrb = _mean_nd_to_1d(nrb)
        
        if self.rng is None:
            kkd = _kkrelation(bg=nrb + self.nrb_amp_offset,
                                cri=cars + self.cars_amp_offset,
                                hilb_kwargs=self.hilb_kwargs, **self.kk_kwargs)
            ret_obj *= 0
            ret_obj += kkd
        else:
            slice_cars_rng = cars.ndim*[slice(None)]
            slice_cars_rng[self.kk_kwargs['axis']] = self.rng
            slice_cars_rng = tuple(slice_cars_rng)

            slice_ret_obj = ret_obj.ndim*[slice(None)]
            slice_ret_obj[self.kk_kwargs['axis']] = self.rng
            slice_ret_obj = tuple(slice_ret_obj)

            kkd = _kkrelation(bg=nrb[self.rng] + self.nrb_amp_offset,
                                cri=cars[slice_cars_rng] + self.cars_amp_offset,
                                hilb_kwargs=self.hilb_kwargs, **self.kk_kwargs)
            ret_obj *= 0
            ret_obj[slice_ret_obj] += kkd
        
        return True

    def calculate(self, cars, nrb):
        """
        cars : ndarray
        Coherent Raman signal.

        nrb : ndarray
            Nonresonant background (NRB)
        """

        kkd = _np.zeros(cars.shape, dtype=complex)
        self._calc(cars, nrb, ret_obj=kkd)
        return kkd
        
    def _transform(self, cars, nrb):
        if issubclass(cars.dtype.type, complex):
            success = self._calc(cars, nrb, ret_obj=cars)
            return success
        else:
            return False


if __name__ == '__main__': # pragma: no cover

    from crikit.data.spectra import Spectrum as _Spectrum
    from crikit.data.spectra import Spectra as _Spectra
    from crikit.data.spectra import Hsi as _Hsi

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
    temp = _np.dot(_np.ones((30,30,1)),CARS[None,:])

    # Create an HSData class instance
    hsi.data = temp
    num_spectra = int(hsi.size/WN.size)

    hsi.freq.data = WN

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


    kk = KramersKronig(cars_amp_offset=0, nrb_amp_offset=0, norm_to_nrb=False, pad_factor=1)
    start = _timeit.default_timer()
    kk.calculate(hsi.data, nrb.data)
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

    kk = KramersKronig(cars_amp_offset=0, nrb_amp_offset=0,
                       norm_to_nrb=False, rng=hsi.freq.op_range_pix,
                       pad_factor=1)
    start = _timeit.default_timer()
    del kkd
    kkd = kk.calculate(hsi.data, nrb.data)
    stop = _timeit.default_timer()
    print('Pixrange Class-based -- Total time: {:.6f} sec ({:.6f} sec/spectrum)'.format(stop-start,
          (stop-start)/num_spectra))

    hsi.data = kkd
    del kkd
    _timeit.time.sleep(2)

    plt.plot(WN, X.imag, label='Imag.{$\chi_{R}$}')
    plt.plot(hsi.freq.data[hsi.freq.op_range_pix],
             hsi.data[10,10,hsi.freq.op_range_pix].imag, 'r*',
             label='KK-Retrieved')
    plt.legend(loc='best')
    plt.xlabel('Wavenumber (cm$^{-1}$)')
    plt.ylabel('Raman Int. (au)')
    plt.title('Raman vs KK-Retrieved CARS')
    plt.show()

    print(_np.allclose(X.imag[hsi.freq.op_range_pix], hsi.data[10,10,hsi.freq.op_range_pix].imag,rtol=1))
