"""Variance Stabilization

Routines:
    gen_anscombe_forward
        Generalized forward Anscombe transformation

    gen_anscombe_inverse_closed_form
        Closed-form approximation of the exact unbiased inverse of Generalized \
        Anscombe variance-stabilizing transformation

    gen_anscombe_exact_unbiased
        Exact unbiased inverse of Generalized Anscombe variance-stabilizing

Notes
-----
This software is a direct translation (with minor alterations) of the \
original MATLAB software created by Alessandro Foi and Markku Mäkitalo \
(Tampere University of Technology - 2011-2012). Please cite the references \
below if using this software. http://www.cs.tut.fi/~foi/

References
----------
[1] M. Mäkitalo and A. Foi, "Optimal inversion of the generalized Anscombe
    transformation for Poisson-Gaussian noise", IEEE Trans. Image Process.,
    doi:10.1109/TIP.2012.2202675

[2] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and  Data
    Analysis, Cambridge University Press, Cambridge, 1998)

"""

import numpy as _np
#import numexpr as _ne
import os as _os

resource_dir = None
resource_dir = _os.path.join(_os.path.abspath(_os.path.dirname(__file__)),
                             'resources')

if _os.path.exists(resource_dir):
    #print('Resource directory: {}'.format(_os.path.abspath(resource_dir)))
    pass
else:  # pragma: no cover
    raise IOError('Cannot find resource directory for Anscombe')

def gen_anscombe_forward(signal, gauss_std, gauss_mean = 0, poisson_multi = 1):
    """
    Applies the generalized Anscombe variance-stabilization transform
    assuming a mixed Poisson-Gaussian noise model as:

    signal = poisson_multi*Poisson{signal0} + Gauss{gauss_mean, gauss_std},

    where Poisson{} and Gauss{} are generalized descriptions of Poisson and
    Gaussian noise.

    Parameters
    ----------
    signal : ndarray
        Noisy signal (1-,2-,3D)

    gauss_std : float, int
        Standard deviation of Gaussian noise

    poisson_multi : float or int, optional (default = 1)
        Effectively a multiplier that scales the effect of the Poisson
        noise

    gauss_mean : float or int, optional (default = 0)
        Mean Gaussian noise level

    Returns
    -------
    fsignal : ndarray (matched to signal shape)
        "Anscombe-transformed" signal with an approximate unity standard \
        deviation/variance (~ 1)

    Notes
    -----
    This software is a direct translation (with minor alterations) of the
    original MATLAB software created by Alessandro Foi and Markku Mäkitalo
    (Tampere University of Technology - 2011-2012). Please cite the references
    below if using this software. http://www.cs.tut.fi/~foi/

    References
    ----------
    [1] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and
    Data Analysis, Cambridge University Press, Cambridge, 1998)

    """

    SMALL_VAL = 1

    fsignal = 2/poisson_multi * _np.sqrt(_np.fmax(SMALL_VAL,poisson_multi*signal +
                                    (3/8)*poisson_multi**2 +
                                    gauss_std**2 -
                                    poisson_multi*gauss_mean))
#    fsignal = _ne.evaluate('2/poisson_multi * sqrt(where(poisson_multi*signal + (3/8)*poisson_multi**2 +\
#                            gauss_std**2 - poisson_multi*gauss_mean > SMALL_VAL,\
#                            poisson_multi*signal + (3/8)*poisson_multi**2 +\
#                            gauss_std**2 - poisson_multi*gauss_mean, SMALL_VAL))')
    #fsignal = 2/poisson_multi * _np.sqrt(_np.fmax(SMALL_VAL,fsignal))
    return fsignal

def gen_anscombe_inverse_closed_form(fsignal, gauss_std, gauss_mean = 0,
                                     poisson_multi = 1):
    """
    Applies a closed-form approximation of the exact unbiased inverse of the
    generalized Anscombe variance-stabilizing transformation assuming a
    mixed Poisson-Gaussian noise model as:

    signal = poisson_multi*Poisson{signal0} + Gauss{gauss_mean, gauss_std},

    where Poisson{} and Gauss{} are generalized descriptions of Poisson and
    Gaussian noise.

    Parameters
    ----------
    fsignal : ndarray
        Forward Anscombe-transformed noisy signal (1-,2-,3D)

    gauss_std : float, int
        Standard deviation of Gaussian noise

    (poisson_multi) : float, int (default = 1)
        Effectively a multiplier that scales the effect of the Poisson
        noise

    (gauss_mean) : float, int (default = 0)
        Mean Gaussian noise level

    Returns
    -------
    signal : ndarray (matched to signal shape)
        Inverse Anscombe-transformed signal with mixed Gaussian-Poisson
        noise

    Notes
    -----
    This software is a direct translation (with minor alterations) of the
    original MATLAB software created by Alessandro Foi and Markku Mäkitalo
    (Tampere University of Technology - 2011-2012). Please cite the references
    below if using this software. http://www.cs.tut.fi/~foi/

    References
    ----------
    [1] M. Mäkitalo and A. Foi, "Optimal inversion of the generalized Anscombe
        transformation for Poisson-Gaussian noise", IEEE Trans. Image Process.,
        doi:10.1109/TIP.2012.2202675

    [2] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and  Data
        Analysis, Cambridge University Press, Cambridge, 1998)

    """

    SMALL_VAL = 0

    gauss_std = gauss_std/poisson_multi

#    signal = _ne.evaluate('poisson_multi*where((fsignal/2)**2 + \
#                    1/4*sqrt(3/2)*fsignal**-1 -\
#                    (11/8)*fsignal**-2 + 5/8*sqrt(3/2)*fsignal**-3 -\
#                    (1/8) - gauss_std**2 > SMALL_VAL, (fsignal/2)**2 + \
#                    1/4*sqrt(3/2)*fsignal**-1 -\
#                    (11/8)*fsignal**-2 + 5/8*sqrt(3/2)*fsignal**-3 -\
#                    (1/8) - gauss_std**2, SMALL_VAL) + gauss_mean')
    
    signal = _np.fmax(SMALL_VAL, (fsignal/2)**2 + 1/4*_np.sqrt(3/2)*fsignal**-1 - 
              (11/8)*fsignal**-2 + 5/8*_np.sqrt(3/2)*fsignal**-3 - 
              (1/8) - gauss_std**2)
    #signal[signal < SMALL_VAL] = SMALL_VAL
    signal *= poisson_multi
    
#    signal = poisson_multi*where((fsignal/2)**2 + \
#                                1/4*sqrt(3/2)*fsignal**-1 -\
#                                (11/8)*fsignal**-2 + 5/8*sqrt(3/2)*fsignal**-3 -\
#                                (1/8) - gauss_std**2 > SMALL_VAL, (fsignal/2)**2 + \
#                                1/4*sqrt(3/2)*fsignal**-1 -\
#                                (11/8)*fsignal**-2 + 5/8*sqrt(3/2)*fsignal**-3 -\
#                                (1/8) - gauss_std**2, SMALL_VAL) \
#                     + gauss_mean')

    return signal

def gen_anscombe_inverse_exact_unbiased(fsignal, gauss_std, gauss_mean = 0,
                                        poisson_multi = 1):
    """
    Applies an exact, unbiased inverse of the generalized Anscombe
    variance-stabilizing transformation assuming a mixed Poisson-Gaussian
    noise model as:

    signal = poisson_multi*Poisson{signal0} + Gauss{gauss_mean, gauss_std},

    where Poisson{} and Gauss{} are generalized descriptions of Poisson and
    Gaussian noise.

    Parameters
    ----------
    fsignal : ndarray
        Forward Anscombe-transformed noisy signal (1-,2-,3D)

    gauss_std : float, int
        Standard deviation of Gaussian noise

    (poisson_multi) : float, int (default = 1)
        Effectively a multiplier that scales the effect of the Poisson
        noise

    (gauss_mean) : float, int (default = 0)
        Mean Gaussian noise level

    Returns
    -------
    signal : ndarray (matched to signal shape)
        Inverse Anscombe-transformed signal with mixed Gaussian-Poisson
        noise

    Notes
    -----
    This software is a direct translation (with minor alterations) of the
    original MATLAB software created by Alessandro Foi and Markku Mäkitalo
    (Tampere University of Technology - 2011-2012). Please cite the references
    below if using this software. http://www.cs.tut.fi/~foi/

    References
    ----------
    [1] M. Mäkitalo and A. Foi, "Optimal inversion of the generalized Anscombe
        transformation for Poisson-Gaussian noise", IEEE Trans. Image Process.,
        doi:10.1109/TIP.2012.2202675

    [2] J.L. Starck, F. Murtagh, and A. Bijaoui, Image  Processing  and  Data
        Analysis, Cambridge University Press, Cambridge, 1998)

    """
    from scipy.io import loadmat
    from scipy.interpolate import InterpolatedUnivariateSpline, interp2d

    SMALL_VAL = 0

    mat_dict = loadmat(_os.path.join(resource_dir,'GenAnscombe_vectors.mat'))

    Efzmatrix = _np.squeeze(mat_dict['Efzmatrix'])
    Ez = _np.squeeze(mat_dict['Ez'])
    sigmas = _np.squeeze(mat_dict['sigmas'])

    gauss_std = gauss_std/poisson_multi;


    # interpolate the exact unbiased inverse for the desired gauss_std
    # gauss_std is given as input parameter
    if (gauss_std > _np.max(sigmas)):
        # for very large sigmas, use the exact unbiased inverse of
        # Anscombe modified by a -gauss_std^2 addend
        exact_inverse = anscombe_inverse_exact_unbiased(fsignal) - gauss_std**2

        # this should be necessary, since anscombe_inverse_exact_unbiased(fsignal) is >=0 and gauss_std>=0.

        exact_inverse = _np.fmax(_np.zeros(exact_inverse.shape),exact_inverse)

    elif gauss_std > 0:
        # interpolate Efz

        Efz = interp2d(sigmas,Ez,Efzmatrix,kind='linear')(gauss_std,Ez)

        # apply the exact unbiased inverse
        exact_inverse = InterpolatedUnivariateSpline(Efz,Ez,k=1)(fsignal)

        # outside the pre-computed domain, use the exact unbiased inverse
        # of Anscombe modified by a -gauss_std^2 addend
        # (the exact unbiased inverse of Anscombe takes care of asymptotics)
        outside_exact_inverse_domain = fsignal > _np.max(Efz.flatten())
        asymptotic = anscombe_inverse_exact_unbiased(fsignal) - gauss_std**2
        exact_inverse[outside_exact_inverse_domain] = asymptotic[outside_exact_inverse_domain]
        outside_exact_inverse_domain = fsignal < _np.min(Efz);
        exact_inverse[outside_exact_inverse_domain] = 0;
    elif gauss_std == 0:
        # if gauss_std is zero, then use exact unbiased inverse of Anscombe
        # transformation (higher numerical precision)
        exact_inverse = anscombe_inverse_exact_unbiased(fsignal);
    else:  # gauss_std < 0
        raise ValueError('Error: gauss_std must be non-negative!')

    # reverse the initial variable change

    exact_inverse *= poisson_multi;
    exact_inverse += gauss_mean;

    return exact_inverse

def anscombe_inverse_exact_unbiased(fsignal):
    """
    Applies an exact, unbiased inverse of the Anscombe
    variance-stabilizing transformation assuming a mixed Poisson-Gaussian
    noise model as:

    signal = poisson_multi*Poisson{signal0} + Gauss{gauss_mean, gauss_std},

    where Poisson{} and Gauss{} are generalized descriptions of Poisson and
    Gaussian noise.

    Parameters
    ----------
    fsignal : ndarray
        Forward Anscombe-transformed noisy signal (1-,2-,3D)

    Returns
    -------
    signal : ndarray (matched to signal shape)
        Inverse Anscombe-transformed signal

    Notes
    -----
    This software is a direct translation (with minor alterations) of the
    original MATLAB software created by Alessandro Foi and Markku Mäkitalo
    (Tampere University of Technology - 2011-2012). Please cite the references
    below if using this software. http://www.cs.tut.fi/~foi/

    References
    ----------
    [1] M. Mäkitalo and A. Foi, "On the inversion of the Anscombe
        transformation in low-count Poisson image denoising", Proc. Int.
        Workshop on Local and Non-Local Approx. in Image Process., LNLA 2009,
        Tuusula, Finland, pp. 26-32, August 2009. doi:10.1109/LNLA.2009.5278406

    [2] M. Mäkitalo and A. Foi, "Optimal inversion of the Anscombe
        transformation in low-count Poisson image denoising", IEEE Trans.
        Image Process., vol. 20, no. 1, pp. 99-109, January 2011.
        doi:10.1109/TIP.2010.2056693

    [3] Anscombe, F.J., "The transformation of Poisson, binomial and
        negative-binomial data", Biometrika, vol. 35, no. 3/4, pp. 246-254,
        Dec. 1948.

    """
    import time

    from scipy.io import loadmat
    from scipy.interpolate import InterpolatedUnivariateSpline

    mat_dict = loadmat(_os.path.join(resource_dir,'Anscombe_vectors.mat'))

    Efz = mat_dict['Efz']
    Ez = mat_dict['Ez']

    asymptotic = (fsignal/2)**2 - 1/8;  # asymptotically unbiased inverse [3]
#    asymptotic = _ne.evaluate('(fsignal/2)**2 - 1/8')  # asymptotically unbiased inverse [3]

    #start = time.process_time()
    signal = InterpolatedUnivariateSpline(Efz,Ez,k=1)(fsignal)   # exact unbiased inverse [1,2]
    #stop = time.process_time()
    #print(stop-start)

    outside_exact_inverse_domain = fsignal > _np.max(Efz)    # for large values use asymptotically unbiased inverse instead of linear extrapolation of exact unbiased inverse outside of pre-computed domain

    signal[outside_exact_inverse_domain] = asymptotic[outside_exact_inverse_domain];

    outside_exact_inverse_domain = fsignal < 2*_np.sqrt(3/8) # min(Efz(:));

    signal[outside_exact_inverse_domain] = 0;
    return signal

if __name__ == '__main__':  # pragma: no cover
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    stddev = 20
    gain = 1

    x = np.linspace(500,4000,10000)
    y = 10e4*np.exp(-(x-2000)**2/(500**2))
    gnoise = stddev*np.random.randn(x.size)
    ygn = y + gnoise
    ymix = np.random.poisson(y) + gnoise
#    ymix = _np.dot(_np.ones((1000,1)), ymix[None,:])
    ymix_ansc = gen_anscombe_forward(ymix, gauss_std=stddev, poisson_multi=gain)
    y_ansc = gen_anscombe_forward(y, gauss_std=stddev, poisson_multi=gain)

    y_inv_ansc = gen_anscombe_inverse_exact_unbiased(y_ansc, gauss_std=stddev,
                                                     poisson_multi=gain)

    if ymix.ndim == 1:
        plt.subplot(211)
        plt.plot(x,y, label='Signal')
        plt.hold(True)
        plt.plot(x,ymix, label='Mixed Noise Signal')
        plt.title('Signal')
        plt.legend(loc='best')
    
        plt.subplot(212)
        plt.plot(x,ymix-y, label='Mixed - Signal')
        plt.title('Difference ($\sigma =$ {:.3f})'.format((ymix - y).std()))
        plt.legend(loc='best')
    
        plt.figure()
        plt.subplot(211)
        plt.plot(x,ymix_ansc, label='Anscombe Mixed Signal')
        plt.plot(x,y_ansc, label='Anscombe Signal')
        plt.title('Anscombe Transformed')
        plt.legend(loc='best')
    
        plt.subplot(212)
        plt.plot(x,ymix_ansc - y_ansc, label='Ansc. Mixed - Ansc. Signal')
        plt.title('Difference ($\sigma =$ {:.3f})'.format((ymix_ansc - y_ansc).std()))
        plt.legend(loc='best')
    
        plt.figure()
        plt.subplot(211)
        plt.plot(x,y_inv_ansc, label='Inv. Anscombe Signal')
        plt.plot(x,y, label='Signal')
        plt.title('Inverse Anscombe Transformed')
        plt.legend(loc='best')
    
        plt.subplot(212)
        plt.plot(x,y_inv_ansc - ymix, label='Inv. Ansc. Signal - Mixed')
        plt.title('Difference ($\sigma =$ {:.3f})'.format((y_inv_ansc - ymix).std()))
        plt.legend(loc='best')
        plt.show()
