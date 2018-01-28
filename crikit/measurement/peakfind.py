"""
Peak-finding utilities


Notes
-----
"""
import copy as _copy
import numpy as _np
import timeit as _timeit

from scipy.signal import (convolve as _convolve,
                          argrelmin as _argrelmin)

class PeakFinder:
    """
    Find peaks and shoulders of a signal.
    
    Parameters
    ----------
    QQ : int
        Peak location in pixel coordinates
    
    Attributes
    ----------
    amp : float or ndarray
        Amplitude of peak
    
    Methods
    -------
    calculate : Calculate the amplitude
    
    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)
    
    """
    def __init__(self, noise_sigma, cwt_width=10, n_noise_tests=1000,
                 cutoff_d1=None, cutoff_d2=None, verbose=True):
        self.cwt_width = cwt_width  # Width, in pixels, of wavelet
        self.noise_sigma = noise_sigma  # Standard deviation of signal noise
        
        # If cutoffs not specified, # of Monte Carlo tests to estimate cutoff values
        self.n_noise_tests = n_noise_tests
        self.cutoff_d1 = cutoff_d1  # Amplitude cutoff for 1st derivative
        self.cutoff_d2 = cutoff_d2  # Amplitude cutoff for 2nd derivative

        self.verbose = verbose

        # Array elements
        self.x = None  # Independent variable
        self.y = None  # Dependent variable
        self.x_pix = None # Independent variable (pixel-units)

        self.amps = None  # Retrieved amplitudes
        self.centers = None  # Retrieved peak centers (x-units)
        self.sigmas = None  # Retrieved Gaussian widths (x-units)
        self.shoulder = None  # Is a peak a shoulder

        self.centers_pix = None  # Retrieved peak centers (pixel-units)
        self.sigmas_pix = None  # Retrieved peak widths (standard deviation) (pixel-units)

        self.y_retrieved = None  # Estimated coarse peak fitting

    @property
    def cwt_width(self):
        return self._cwt_width

    @cwt_width.setter
    def cwt_width(self, value):
        if value <= 0:
            raise ValueError('cwt_width must be positive')
        else:
            self._cwt_width = value

    @property
    def noise_sigma(self):
        return self._noise_sigma

    @noise_sigma.setter
    def noise_sigma(self, value):
        if value < 0:
            raise ValueError('noise_sigma must be non-negtaive')
        else:
            self._noise_sigma = value

    @staticmethod
    def haar(width):
        """
        Create Haar wavelet (wv) with specified width (width)
        """
        wv = _np.zeros((width))
        midpoint = int(_np.floor(width/2))
        wv[0:midpoint] = 1
        wv[midpoint::] = -1

        # Set midpoint == 0 for odd-length. Not technically correct, but needed
        # for computations
        if width % 2 == 1:
            wv[midpoint] = 0
    
        return wv

    @staticmethod
    def cwt_diff(signal, wv_width, order=1, method='auto'):
        """
        Take a numerical derivative using a Haar wavelet (noise-supression)
        
        Parameters
        ----------
        signal : ndarray (1D)
            Signal data
        
        wv_width : int
            Width of wavelet to use (balance noise suppression and distortion)
            
        order : int, optional (default=1)
            Order of derivative (e.g., 1st-order derivative)

        method : str {'auto' (default), 'fft', 'direct'}
            
        Returns
        -------
        deriv : ndarray (1D)
            Derivative of input signal
        """
        deriv = _copy.deepcopy(signal)
        for count in range(order):
            try:
                deriv = _convolve(deriv, PeakFinder.haar(wv_width), mode='same', 
                                  method=method)
            except:
                print('peakfind.py | cwt_diff: Likely using an old version of SciPy (no convolve method parameter)')
                deriv = _convolve(deriv, PeakFinder.haar(wv_width), mode='same')
        return deriv

    # @staticmethod
    # def measure(signal, noise_sigma, x=None, cwt_width=10, n_noise_tests=1000,
    #             cutoff_d1=None, cutoff_d2=None, verbose=True):
    #     pass

    def calculate(self, y, x=None, recalc_cutoff=True, method='auto'):
        """ Find peaks """
        self.y = y
        self.x_pix = _np.arange(self.y.size)

        # Will update in the future for 1D x and ND y
        if x is not None:
            if x.size == y.size:
                self.x = x
            else:
                self.x = None
            
        self._calc_cutoff(recalc_cutoff=recalc_cutoff, method=method)
        
        tmr = _timeit.default_timer()
        d1 = PeakFinder.cwt_diff(self.y, wv_width=self._cwt_width, order=1, method=method)
        d2 = PeakFinder.cwt_diff(self.y, wv_width=self._cwt_width, order=2, method=method)

        loc_mins_d2 = _argrelmin(d2, order=10)[0]
        loc_mins_d2 = loc_mins_d2[d2[loc_mins_d2] < 0]
        loc_mins_d2 = loc_mins_d2[_np.abs(d2[loc_mins_d2]) > self.cutoff_d2]
        loc_mins_d2 = loc_mins_d2[loc_mins_d2 > 10]
        loc_mins_d2 = loc_mins_d2[loc_mins_d2 < (d2.size - 10)]
        peak = _np.sign(d1[loc_mins_d2-10])+_np.sign(d1[loc_mins_d2+10])==0
        shoulder = ~peak
        
        
        loc_mins_d1 = _argrelmin(d1, order=10)[0]
        loc_mins_d1 = loc_mins_d1[d1[loc_mins_d1] < 0]
        loc_mins_d1 = loc_mins_d1[_np.abs(d1[loc_mins_d1]) > self.cutoff_d1]

        sigma_retr = []
        sigma_retr_locs = []
        for l in loc_mins_d2:
            if self.x is not None:
                sigma_retr.append(x[l] - x[loc_mins_d1[_np.argmin(_np.abs(l - loc_mins_d1))]])
            sigma_retr_locs.append(loc_mins_d1[_np.argmin(_np.abs(l - loc_mins_d1))])
        
        if self.x is not None:
            sigma_retr = _np.abs(_np.array(sigma_retr))
            omegas_retr = x[loc_mins_d2]
        sigma_retr_locs = _np.array(sigma_retr_locs)       
        omegas_retr_locs = loc_mins_d2
        
        amps_retr = []
        for l, s in zip(omegas_retr_locs, sigma_retr_locs):
            dl = _np.abs(_np.ceil((l - s)/10)).astype(_np.integer)
            amps_retr.append(_np.median(y[l-dl:l+dl+1]))
        amps_retr = _np.array(amps_retr)

        tmr -= _timeit.default_timer()
        self._timer = 1*tmr

        if self.verbose:
            print('Time for peak finding: {:.2e} sec'.format(-tmr))
        
        y_retrieved = _np.zeros(*self.x_pix.shape)

        for num, (a, o, s) in enumerate(zip(amps_retr, omegas_retr_locs, sigma_retr_locs)):
            y_retrieved += a*_np.exp(-(self.x_pix-o)**2/(2*(s)**2))
        
        self.amps = 1*amps_retr  # Retrieved amplitudes

        if self.x is not None:
            self.centers = 1*omegas_retr  # Retrieved peak centers (x-units)
            self.sigmas = 1*sigma_retr  # Retrieved Gaussian widths (x-units)
        self.shoulder = shoulder  # Is a peak a shoulder

        self.centers_pix = 0+omegas_retr_locs  # Retrieved peak centers (pixel-units)
        self.sigmas_pix = 1*sigma_retr_locs  # Retrieved peak widths (standard deviation) (pixel-units)

        self.y_retrieved = 1*y_retrieved  # Estimated coarse peak fitting

    def _calc_cutoff(self, recalc_cutoff=True, method='auto'):
        if (self.cutoff_d1 is None) or (self.cutoff_d2 is None) or (recalc_cutoff == True):
            y_blank = self._noise_sigma*_np.random.randn(self.n_noise_tests,self.x_pix.size)
            y_blank_d2 = _np.zeros(y_blank.shape)
            y_blank_d1 = _np.zeros(y_blank.shape)
            for num, temp in enumerate(y_blank):
                y_blank_d1[num, :] = PeakFinder.cwt_diff(temp, wv_width=self._cwt_width, order=1, method=method)
                y_blank_d2[num, :] = PeakFinder.cwt_diff(temp, wv_width=self._cwt_width, order=2, method=method)

            if (self.cutoff_d2 is None) or (recalc_cutoff == True):
                self.cutoff_d2 = _np.max(_np.abs(y_blank_d2))
            if (self.cutoff_d1 is None) or (recalc_cutoff == True):
                self.cutoff_d1 = _np.max(_np.abs(y_blank_d1))
            
        if self.verbose:
            print('1st-Deriv cutoff: {:.2f}'.format(self.cutoff_d1))
            print('2nd-Deriv cutoff: {:.2f}'.format(self.cutoff_d2))
        
if __name__ == '__main__':

    x = _np.linspace(0,100,1000)

    A = _np.array([80, 100, 40])
    Omega = _np.array([30, 50, 60])
    Sigma = _np.array([3, 4, 4])

    y = _np.zeros(x.shape)

    for a, o, s in zip(A, Omega, Sigma):
        y += a*_np.exp(-(x-o)**2/(2*s**2))
    
    noise_sigma = 3
    noise = noise_sigma*_np.random.randn(*x.shape)
    y_noisy = y + noise
    
    pkfind = PeakFinder(noise_sigma=noise_sigma, cwt_width=50, n_noise_tests=1000,
                        cutoff_d1=None, cutoff_d2=None, verbose=True)

    print('\n====================================\n')
    pkfind.calculate(y, x=x, recalc_cutoff=True, method='fft')

    
    print('\nActual Center: {}'.format(Omega))
    print('Calculated Centers: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.centers]))

    print('\nActual Amplitudes: {}'.format(A))
    print('Calculated Amplitudes: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.amps]))

    print('\nActual Widths: {}'.format(Sigma))
    print('Calculated Widths: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.sigmas]))

    print('Is Shoulder: {}\n'.format(pkfind.shoulder))
    # print(pkfind.sigmas)
    # print(pkfind.__dict__)