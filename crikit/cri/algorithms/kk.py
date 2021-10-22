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
from crikit.utils.general import pad_edge_mean as _pad_edge_mean

__all__ = ['kkrelation', 'hilbertfft']

def kkrelation(bg, cri, conjugate=False, phase_offset=0.0, norm_to_nrb=True, pad_factor=1, n_edge=1, 
               axis=-1, no_iter=False, bad_value=1e-8, min_value=None, hilb_kwargs={}, **kwargs):
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
    conjugate : bool
        If spectra go from high-to-low-wavenumber (left-to-right), you should
        conjugate the KK output.
    phase_offset : float or ndarray, optional
        Global phase offset applied to the KK, which effecively controls \
        the real-to-imaginary components relationship
    norm_to_nrb : bool
        Should the output be normalized by the square-root of the \
        background/NRB spectrum(a)
    pad_factor : int
        The multiple number of spectra-length pads that will be
        applied before and after the original spectra
    n_edge : int, optional
        For edge values, take a mean of n_edge neighbors
    axis : int, optional
        Axis to perform over
    no_iter : bool
        (3D matrices with f-axis=-1) Force full matrix calculation in-memory, as
        opposed to column-by-column (default).
    min_value : float, optional
        Applies to cri/bg (the ratio). Values below min_value set to min_value
    bad_value : float, optional
        Applies to cri/bg (the ratio). Inf's and NaN's set to bad_value
    hilb_kwargs : dict
        kwargs sent to the hilbert transform. Only pad_factor, n_edge, and axis
        are automatically sent -- these will overwrite anything in hilb_kwargs.

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
    
    hilb_kwargs.update({'pad_factor':pad_factor, 'n_edge':n_edge, 'axis':axis})
    
    ratio = cri / bg
    if bad_value:
        ratio[_np.isnan(ratio)] = bad_value
        ratio[_np.isinf(ratio)] = bad_value
        ratio[ratio <= 0] = bad_value

    if (ratio.ndim == 3) & ((axis == -1) | (axis == 2)) & (not no_iter):
        ph = _np.zeros(ratio.shape, dtype = _np.complex)
        for num in range(ratio.shape[0]):
            ph[num, ...] = _np.exp(1j * (hilbertfft(0.5 * _np.log(ratio[num, ...]), **hilb_kwargs) + phase_offset))
    else:
        ph = _np.exp(1j * (hilbertfft(0.5 * _np.log(ratio), **hilb_kwargs) + phase_offset))
    
    if conjugate:
        _np.conjugate(ph, out=ph)
    
    if norm_to_nrb:
        ph *= _np.sqrt(ratio)
        return ph
    else:
        ph *= _np.sqrt(cri)
        return ph


def hilbertfft(y, pad_factor=1, n_edge=1, axis=-1, copy=True, bad_value=1e-8, min_value=None, return_pad=False, **kwargs):
    """
    Compute the one-dimensional Hilbert Transform.

    This function computes the one-dimentional Hilbert transform
    using the Fourier-domain implementation.

    Parameters
    ----------
    y : ndarray
        Input numpy array
    pad_factor : int, optional
        The multiple number of spectra-length pads that will be
        applied before and after the original spectra
    n_edge : int, optional
        For edge values, take a mean of n_edge neighbors
    axis : int, optional
        Axis to perform over
    copy : bool, optional
        Copy or over-write input data
    min_value : float, optional
        Values below min_value set to min_value
    bad_value : float, optional
        Inf's and NaN's set to bad_value
    return_pad: bool, optional
        Return the full padded signal.
    
    Returns
    -------
    ndarray
        Hilbert transformed data

    References
    ----------
    
    -    Camp Jr, C. H., Lee, Y. J., & Cicerone, M. T. (2016). Quantitative, comparable 
         coherent anti-Stokes Raman scattering (CARS) spectroscopy: correcting errors in 
         phase retrieval. Journal of Raman Spectroscopy, 47(4), 408–415. 
         https://doi.org/10.1002/jrs.4824 https://arxiv.org/abs/1507.06543
    -    C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable
          Coherent Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting
          Errors in Phase Retrieval," Journal of Raman Spectroscopy (2016).
          arXiv:1507.06543.
    -    A D Poularikas, "The Hilbert Transform," in The Handbook of
          Formulas and Tables for Signal Processing (ed., A. D. Poularikas),
          Boca Raton, CRC Press LLC (1999).
          
    """
    y_pad, window = _pad_edge_mean(y, pad_factor*y.shape[axis], n_edge=n_edge, axis=axis)
    len_axis = y_pad.shape[axis]
    time_vec = _fftpack.fftfreq(len_axis)
    
    slice_add_dims = y.ndim*[None]
    slice_add_dims[axis] = slice(None)
    slice_add_dims = tuple(slice_add_dims)

    y_pad = _fftpack.ifft(y_pad, axis=axis, overwrite_x=True)   
    y_pad *= 1j*_np.sign(time_vec[slice_add_dims])
    y_pad = _fftpack.fft(y_pad, axis=axis, overwrite_x=True)
    
    if bad_value:
        y_pad[_np.isnan(y_pad)] = bad_value
        y_pad[_np.isinf(y_pad)] = bad_value
        
    if min_value:
        y_pad[y_pad < min_value] = min_value

    slice_vec_get_y_from_pad = y.ndim*[slice(None)]
    slice_vec_get_y_from_pad[axis] = _np.where(window==1)[0]
    slice_vec_get_y_from_pad = tuple(slice_vec_get_y_from_pad)
    
    if return_pad:
        return y_pad.real
    
    if copy:
        return y_pad[slice_vec_get_y_from_pad].real
    else:
        y *= 0
        y += y_pad[slice_vec_get_y_from_pad].real


if __name__ == '__main__':  # pragma: no cover
    import timeit as _timeit

    x = _np.abs(10e3*_np.random.rand(330, 330, 900))+1.0

    start = _timeit.default_timer()
    out = kkrelation(x,x)
    
    start -= _timeit.default_timer()
    print('Scipy Time (Trial 1): {:.3g} sec'.format(-start))

