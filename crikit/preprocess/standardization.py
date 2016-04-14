# -*- coding: utf-8 -*-
"""
Standardization

Created on Thu Apr 14 08:53:08 2016

@author: chc
"""

__all__ = ['anscombe, anscombe_inverse']

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('.'))

import timeit as _timeit

import numpy as _np
from crikit.data.spectrum import Spectrum as _Spectrum

from crikit.preprocess.algorithms.anscombe import (gen_anscombe_forward as ansc,
                                                   gen_anscombe_inverse_exact_unbiased as inv_ansc)

def anscombe(data_obj, gauss_std, gauss_mean=0.0, poisson_multi=1.0, overwrite=True):
    """
    Implement the generalized forward Anscombe transformation.

    Signal : :math:`X`

    Mean of Gaussian noise :  :math:`<g>`

    Standard deviation of Gaussian noise :  :math:`\sigma_g`

    Noise of type 'type' : :math:`N_{type}`

    Poisson noise multiplier : :math:`\\alpha`

    Model : :math:`X = \\alpha*N_{Poisson}\{X\} + N_{Gauss}\{<g>, \sigma_g\},`

    Parameters
    ----------
    data_obj : Spectrum (or subclass) object or ndarray.
        Signal with mixed Gaussian and Poisson noise to transform.

    gauss_std : float
        Standard deviation of Gaussian noise. :math:`\sigma_g` in model.

    poisson_multi : float, optional (default=1.0)
        A multiplier that scales the effect of the Poisson noise. \
        :math:`\\alpha` in model.

    gauss_mean : float, optional (default=0.0)
        Mean Gaussian noise level. :math:`<g>` in model.

    overwrite : bool, optional (default=True)

    Returns
    -------
    ndarray
        Altered data if overwrite is False

    None
        Return None if overwrite is True

    See Also
    -----
    * See the docstring of ./algorithms/anscombe for more information.

    Citation Refs
    ------------------
    [1] M. Mäkitalo and A. Foi, "Optimal inversion of the generalized Anscombe \
        transformation for Poisson-Gaussian noise", IEEE Trans. Image Process., \
        doi:10.1109/TIP.2012.2202675

    [2] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and  Data \
        Analysis, Cambridge University Press, Cambridge, 1998)

    [3] C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative, \
        comparable coherent anti-Stokes Raman scattering (CARS) \
        spectroscopy: Correcting errors in phase retrieval," Journal of Raman \
        Spectroscopy 47, 408-415 (2016). arXiv:1507.06543.
    """
    if isinstance(data_obj,_Spectrum):
        if overwrite:
            out = ansc(data_obj.data, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
#            data_obj.data *= 0
#            data_obj.data += out
            data_obj.data = out
            return None
        else:
            out = ansc(data_obj.data, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
            return out
    elif isinstance(data_obj, _np.ndarray):
        if overwrite:
            out = ansc(data_obj, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)

            # NOTE: In a pass-by-value situation, like this, need to perform
            # in-line math to overwrite the variable
            data_obj *= 0
            data_obj += out

            return None
        else:
            out = ansc(data_obj, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
            return out
    else:
        raise TypeError('data_obj should be of class (or subclass) Spectrum or ndarray')

def anscombe_inverse(data_obj, gauss_std, gauss_mean=0.0, poisson_multi=1.0, overwrite=True):
    """
    Applies an exact, unbiased inverse of the generalized Anscombe \
    variance-stabilizing transformation assuming a mixed Poisson-Gaussian \
    noise model as:


    Signal : :math:`X`

    Mean of Gaussian noise :  :math:`<g>`

    Standard deviation of Gaussian noise :  :math:`\sigma_g`

    Noise of type 'type' : :math:`N_{type}`

    Poisson noise multiplier : :math:`\\alpha`

    Model : :math:`X = \\alpha*N_{Poisson}\{X\} + N_{Gauss}\{<g>, \sigma_g\},`

    Parameters
    ----------
    data_obj : Spectrum (or subclass) object or ndarray.
        Signal with mixed Gaussian and Poisson noise to transform.

    gauss_std : float
        Standard deviation of Gaussian noise. :math:`\sigma_g` in model.

    poisson_multi : float, optional (default=1.0)
        A multiplier that scales the effect of the Poisson noise. \
        :math:`\\alpha` in model.

    gauss_mean : float, optional (default=0.0)
        Mean Gaussian noise level. :math:`<g>` in model.

    overwrite : bool, optional (default=True)

    See Also
    -----
    * See the docstring of ./algorithms/anscombe for more information.

    Citation Refs
    ------------------
    [1] M. Mäkitalo and A. Foi, "Optimal inversion of the generalized Anscombe \
        transformation for Poisson-Gaussian noise", IEEE Trans. Image Process., \
        doi:10.1109/TIP.2012.2202675

    [2] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and  Data \
        Analysis, Cambridge University Press, Cambridge, 1998)

    [3] C. H. Camp Jr, Y. J. Lee, and M. T. Cicerone, "Quantitative, \
        comparable coherent anti-Stokes Raman scattering (CARS) \
        spectroscopy: Correcting errors in phase retrieval," Journal of Raman \
        Spectroscopy 47, 408-415 (2016). arXiv:1507.06543.
    """
    if isinstance(data_obj,_Spectrum):
        if overwrite:
            out = inv_ansc(data_obj.data, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)

            data_obj.data = out
            return None
        else:
            out = inv_ansc(data_obj.data, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
            return out
    elif isinstance(data_obj, _np.ndarray):
        if overwrite:
            out = inv_ansc(data_obj, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
            # NOTE: In a pass-by-value situation, like this, need to perform
            # in-line math to overwrite the variable
            data_obj *= 0
            data_obj += out
            return None
        else:
            out = inv_ansc(data_obj, gauss_std=gauss_std,
                                 gauss_mean=gauss_mean,
                                 poisson_multi=poisson_multi)
            return out
    else:
        raise TypeError('data_obj should be of class (or subclass) Spectrum or ndarray')

if __name__ == '__main__': # pragma: no cover
        stddev = 20
        gain = 1

        f = _np.linspace(500,4000,1000)
        sig = 10e4*_np.exp(-(f-2000)**2/(500**2))

        gnoise = stddev*_np.random.randn(f.size)

        sig_mix = _np.random.poisson(sig) + gnoise

        import matplotlib.pyplot as _plt

        sig2 = _Spectrum(sig)
        out = anscombe(sig2, gauss_std=stddev, poisson_multi=gain, overwrite=False)
        _plt.plot(out, label='No overwrite')
        anscombe(sig2, gauss_std=stddev, poisson_multi=gain, overwrite=True)
        _plt.plot(sig2.data, label='Overwrite')
        _plt.legend(loc='best')
        _plt.show()

        print(_np.allclose(out, sig2.data))

        # Recalc sig
        sig = 10e4*_np.exp(-(f-2000)**2/(500**2))

        _plt.figure()
        sig_ansc = anscombe(sig, gauss_std=stddev, poisson_multi=gain, overwrite=False)
        out = anscombe_inverse(sig_ansc, gauss_std=stddev, poisson_multi=gain, overwrite=False)
        _plt.plot(sig)
        _plt.plot(out)
        anscombe_inverse(sig_ansc, gauss_std=stddev, poisson_multi=gain, overwrite=True)
        _plt.plot(sig_ansc)
        _plt.show()