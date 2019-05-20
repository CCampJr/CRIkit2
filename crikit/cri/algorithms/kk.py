"""
Kramers-Kronig Relation Phase Retrieval (crikit.process.maths.kk)
=================================================================

    kkrelation : Retrieve real and imaginary components from a
    spectrum that is the modulus of a function

    hilbertfft : Fourier-domain Hilbert transform

References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent 
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase 
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

"""

import numpy as _np
from scipy import fftpack as _fftpack

from crikit.utils.general import pad as _pad

__all__ = ['kkrelation', 'hilbertfft']

_DEFAULT_THREADS = 1

# Conditional modules
# Check for and load pyFFTW if available (kkrelation, hilbertfft)
try:  # pragma: no cover
    import pyfftw as _pyfftw
    _pyfftw_available = True
except ImportError:  # pragma: no cover
    print("No pyFFTW found. Using Scipy instead. \n\
    You may want to install pyFFTW and FFTW for [potentially]\n\
    significant performance enhancement")
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

    Notes
    -----
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
    """

    ratio = cri / bg
    ratio[_np.isnan(ratio)] = 1e-8
    ratio[_np.isinf(ratio)] = 1e-8

    ratio[ratio <= 0] = 1e-8

    if ratio.ndim == 3:
        h = _np.zeros(ratio.shape, dtype=float)
        for row_num, blk in enumerate(ratio):
            h[row_num, :, :] = hilbertfft(0.5 * _np.log(blk),
                                          pad_factor=pad_factor)
    else:
        h = hilbertfft(0.5 * _np.log(ratio), pad_factor=pad_factor)

    # Note: disabled numexpr eval due to stability issues
    if norm_by_bg is True:
        out = _np.sqrt(ratio) * _np.exp(1j * phase_offset + 1j * h)
        # out = _ne.evaluate('sqrt(ratio)*exp(1j*phase_offset + 1j*h)')
        return out
    else:
        out = _np.sqrt(cri) * _np.exp(1j * phase_offset + 1j * h)
        return out
        # return _ne.evaluate('sqrt(cri)*exp(1j*phase_offset + 1j*h)')

def hilbertfft(spectra, pad_factor=1, use_pyfftw=True):
    """
    Compute the one-dimensional Hilbert Transform.

    This function computes the one-dimentional Hilbert transform
    using the Fourier-domain implementation.

    Parameters
    ----------
    spectra : ndarray
        Input array that can be one-,two-,or three-dimensional
    pad_factor : int, optional
        The multiple number of spectra-length pads that will be
        applied before and after the original spectra
    use_pyfftw : bool, optional
        If available, use pyfftw. Else use scipy scipack implementation

    Returns
    -------
    ndarray
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
    """

    assert spectra.ndim <= 2, 'Input data need be 1D or 2D for memory'

    freq_len = spectra.shape[-1]
    freq_pad_len = freq_len*(2*pad_factor+1)
    time_vec = _np.fft.fftfreq(freq_pad_len)

    if pad_factor > 0:
        padded, window = _pad(spectra, pad_factor*spectra.shape[-1], 'edge')
    else:
        padded = spectra
        window = None

    padded = padded.astype(_np.complex)
    
    # Use pyFFTW (supposed optimal) library or Scipy
    # Note (although not obvious with pyFFTW) these functions overwrite
    # the input variable-- saves memory and increases speed
    if _pyfftw_available and use_pyfftw:
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
    padded[_np.isnan(padded)] = 1e-8
    padded[_np.isinf(padded)] = 1e-8

    if window is not None:
        return padded[..., window == 1].real
    else:
        return padded.real

if __name__ == '__main__':  # pragma: no cover
    import timeit as _timeit

    x = _np.random.rand(300,900)
    print(x.dtype)
    y = _np.random.rand(300,900)
    
    
    if _pyfftw_available:
        start = _timeit.default_timer()
        #out = kkrelation(x,y)
        out = hilbertfft(x)
        start -= _timeit.default_timer()
        print('PyFFTW Time (Trial 1): {:.3g} sec'.format(-start))

        start = _timeit.default_timer()
        #out = kkrelation(x,y)
        out = hilbertfft(x)
        start -= _timeit.default_timer()
        print('PyFFTW Time (Trial 2): {:.3g} sec'.format(-start))

    start = _timeit.default_timer()
    #out = kkrelation(x,y)
    out = hilbertfft(x, use_pyfftw=False)
    start -= _timeit.default_timer()
    print('Scipy Time (Trial 1): {:.3g} sec'.format(-start))

    start = _timeit.default_timer()
    #out = kkrelation(x,y)
    out = hilbertfft(x, use_pyfftw=False)
    start -= _timeit.default_timer()
    print('Scipy Time (Trial 2): {:.3g} sec'.format(-start))

