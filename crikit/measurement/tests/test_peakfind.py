"""
Testing for Hilbert transform method

Using the math relation a^2 / (a^2 + x^2) (Lorentz/Cauchy) has an 
analytical Hilbert transform: x^2 / (a^2 + x^2)
"""

import numpy as np
from numpy.testing import assert_allclose

from crikit.measurement.peakfind import PeakFinder

def test_peakfind():
    x = np.linspace(0,100,1000)

    A = np.array([80, 100])
    Omega = np.array([30, 50])
    Sigma = np.array([3, 4])

    y = np.zeros(x.shape)

    for a, o, s in zip(A, Omega, Sigma):
        y += a*np.exp(-(x-o)**2/(2*s**2))
    
    noise_sigma = 0.001
    noise = noise_sigma*np.random.randn(*x.shape)
    y_noisy = y + noise
    
    pkfind = PeakFinder(noise_sigma=noise_sigma, cwt_width=50, n_noise_tests=1000,
                        cutoff_d1=None, cutoff_d2=None, verbose=False)

    print('\n====================================\n')
    pkfind.calculate(y, x=x, recalc_cutoff=True, method='fft')

    assert_allclose(np.array(Omega), pkfind.centers, rtol=0.01)
    assert_allclose(np.array(A), pkfind.amps, rtol=0.01)
    assert_allclose(np.array(Sigma), pkfind.sigmas, rtol=0.1)
    assert_allclose(np.array([False, False]), pkfind.shoulder)
       
    print('\nActual Center: {}'.format(Omega))
    print('Calculated Centers: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.centers]))

    print('\nActual Amplitudes: {}'.format(A))
    print('Calculated Amplitudes: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.amps]))

    print('\nActual Widths: {}'.format(Sigma))
    print('Calculated Widths: {}\n'.format(['{:.2f}'.format(x) for x in pkfind.sigmas]))

    print('Is Shoulder: {}\n'.format(pkfind.shoulder))
if __name__ == '__main__':
    test_peakfind()