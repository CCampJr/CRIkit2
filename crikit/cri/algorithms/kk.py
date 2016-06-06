# -*- coding: utf-8 -*-
"""
Kramers-Kronig Relation Phase Retrieval (crikit.process.maths.kk)
=======================================================

    kkrelation : Retrieve real and imaginary components from a
    spectrum that is the modulus of a function\n

    hilbertfft : Fourier-domain Hilbert transform\n

Citation ref
------------------
C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("15.10.02")

"""

__all__ = ['kkrelation', 'hilbertfft']

_DEFAULT_THREADS = 1

import numpy as _np
import numexpr as _ne

# Conditional modules
# Check for and load pyFFTW if available (kkrelation, hilbertfft)

try:  # pragma: no cover
    import pyfftw as _pyfftw
    _pyfftw_available = True
except ImportError:  # pragma: no cover
    print("No pyFFTW found. Using Scipy instead. \n\
    You may want to install pyFFTW and FFTW for [potentially]\n\
    significant performance enhancement")
    from scipy import fftpack as _fftpack
    _pyfftw_available = False

# Check for and load multiprocessing to determine number of CPUs
try:
    import multiprocessing as _multiprocessing
    _thread_num = _multiprocessing.cpu_count()
except ImportError:  # pragma: no cover
    print("No multiprocessing module found. \n\
    Default thread number set to 1. This can be\n\
    changed within the .py file")
    _thread_num = _DEFAULT_THREADS


def kkrelation(bg, cri, phase_offset=0.0, norm_by_bg=True, pad_factor=1):
    """
    Retrieve the real and imaginary components of a CRI spectra(um) via
    the Kramers-Kronig (KK) relation.

    Parameters
    ----------
    bg : ndarray
        Coherent background (bg) spectra(um) array that can be one-, two-, \
        or three-dimensional
    cri : ndarray
        CRI spectra(um) array that can be one-,two-,or three-dimensional \
    (phase_offset) : int, float, or ndarray, optional
        Global phase offset applied to the KK, which effecively controls \
        the real-to-imaginary components relationship
    (norm_by_bg) : bool
        Should the output be normalized by the square-root of the \
        background (bg) spectrum(a)
    (pad_factor) : int
        The multiple number of spectra-length pads that will be
        applied before and after the original spectra


    Returns
    -------
    out : complex ndarray
        The real and imaginary components of KK.

    Note
    ----
    (1) The imaginary components provides the sponatenous Raman-like \
    spectra(um).

    (2) This module assumes the spectra are oriented as such that the \
    frequency (wavenumber) increases with increasing index.  If this is \
    not the case for your spectra(um), apply a phase_offset of _np.pi

    References
    ----------
    Y Liu, Y J Lee, and M T Cicerone, "Broadband CARS spectral phase \
    retrieval using a time-domain Kramers-Kronig transform," Opt. Lett. 34, \
    1363-1365 (2009).

    C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable \
    Coherent Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting \
    Errors in Phase Retrieval," Journal of Raman Spectroscopy (2016). \
    arXiv:1507.06543.

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.10.02")
    """

    # Return the complex KK relation using the Hilbert transform.
#    print('1')
    ratio = _ne.evaluate('cri/bg')
#    print('2')
    ratio[_np.isnan(ratio)] = 1e-12
    ratio[_np.isinf(ratio)] = 1e-12

    ratio[ratio <= 0] = 1e-12

    if ratio.ndim == 3:
        h = _np.zeros(ratio.shape, dtype=float)
        for count in range(ratio.shape[0]):
            h[count, :, :] = hilbertfft(0.5 * _np.log(ratio[count, :, :]),
                                        pad_factor=pad_factor)
    else:
        h = hilbertfft(0.5 * _np.log(ratio), pad_factor=pad_factor)
#    print('3')

    if norm_by_bg is True:
        out = _ne.evaluate('sqrt(ratio)*exp(1j*phase_offset + 1j*h)')
#        print('4')
        return out
    else:
        return _ne.evaluate('sqrt(cri)*exp(1j*phase_offset + 1j*h)')


def hilbertfft(spectra, pad_factor=1):
    """
    Compute the one-dimensional Hilbert Transform.

    This function computes the one-dimentional Hilbert transform
    using the Fourier-domain implementation.

    NEW v1.2: Just returns the Hilbert transformed component (not
    the analytic function)

    Parameters
    ----------
    spectra : ndarray
        Input array that can be one-,two-,or three-dimensional
    (pad_factor) : int, optional
        The multiple number of spectra-length pads that will be
        applied before and after the original spectra

    Returns
    -------
    out : ndarray
        Hilbert transformed data

    References
    ----------
    C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable \
    Coherent Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting \
    Errors in Phase Retrieval," Journal of Raman Spectroscopy (2016). \
    arXiv:1507.06543.

    A D Poularikas, "The Hilbert Transform," in The Handbook of \
    Formulas and Tables for Signal Processing (ed., A. D. Poularikas), \
    Boca Raton, CRC Press LLC (1999).

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("15.6.28")

    """

    spectrum_len = spectra.shape[-1]

    shape = list(spectra.shape)
    shape_pad = list(spectra.shape)
    shape[-1] = shape[-1] + 2 * shape[-1] * pad_factor
    shape_pad[-1] = shape_pad[-1]*pad_factor

    time_vec = _np.fft.fftfreq(shape[-1])

    # Pad the spectra (elongate). The pad value is the end-points intensity
    padL = _np.dot(_np.expand_dims(spectra.T[0].T, axis=-1),
                   _np.ones((1, shape_pad[-1]), dtype=complex))
    padR = _np.dot(_np.expand_dims(spectra.T[-1].T, axis=-1),
                   _np.ones((1, shape_pad[-1]), dtype=complex))
    padded = _np.concatenate((padL, spectra, padR), axis=-1)

    # Use pyFFTW (supposed optimal) library or Scipy
    # Note (although not obvious with pyFFTW) these functions overwrite
    # the input variable-- saves memory and increases speed
    if _pyfftw_available is True:
        _pyfftw.interfaces.cache.enable()
        padded = _pyfftw.interfaces.scipy_fftpack.ifft(padded, axis=-1,
                                              overwrite_x=True,
                                              threads=_thread_num,
                                              auto_align_input=True,
                                              planner_effort='FFTW_MEASURE')
        padded *= 1j*_np.sign(time_vec)

        padded = _pyfftw.interfaces.scipy_fftpack.fft(padded, axis=-1,
                                              overwrite_x=True,
                                              threads=_thread_num,
                                              auto_align_input=True,
                                              planner_effort='FFTW_MEASURE')
    else: # Perform Hilbert Transform with Scipy FFTPACK
        _fftpack.ifft(padded, axis=-1, overwrite_x=True)
        padded *= 1j*_np.sign(time_vec)
        _fftpack.fft(padded, axis=-1, overwrite_x=True)

    # Set inf's and NaN's to arbitrarily small value
    padded[_np.isnan(padded)] = 1e-12
    padded[_np.isinf(padded)] = 1e-12

    return _np.real(padded.T[spectrum_len * pad_factor:
                    spectrum_len * pad_factor+spectrum_len].T)

if __name__ == '__main__':
    import numpy as _np

    x = _np.random.rand(100,1000)
    kkrelation(x,x)