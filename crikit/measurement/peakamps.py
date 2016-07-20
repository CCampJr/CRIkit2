# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 01:28:44 2016

@author: chc
"""

import numpy as _np


class MeasurePeakBWTroughs:
    """
    Meausure the amplitude of a peak between troughs.
    
    Parameters
    ----------
    pk : int
        Peak location in pixel coordinates
    tr1 : int
        Trough 1 location in pixel coordinates
    tr2 : int
        Trough 2 location in pixel coordinates
    
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
    def __init__(self, pk, tr1, tr2):
        self.amp = None

        self.pk = pk

        if tr1 < tr2:
            self.tr_left = tr1
            self.tr_right = tr2
        else:
            self.tr_left = tr2
            self.tr_right = tr1

    def calculate(self, signal):
#        try:
        self.amp = self._calc(signal)
#        except:
#            return None
#        else:
        return self.amp
        
    @staticmethod
    def measure(signal, pk, tr1, tr2):
        inst = MeasurePeakBWTroughs(pk, tr1, tr2)
        return inst.calculate(signal)

    def _calc(self, signal):
        slope = (signal[..., self.tr_right]-signal[..., self.tr_left])/ \
                 (self.tr_right - self.tr_left)
        amp = signal[..., self.pk] - (slope*(self.pk - self.tr_left) + \
                signal[..., self.tr_left])

        return amp
        
if __name__ == '__main__':
    import matplotlib.pyplot as _plt

    print('\n\n--------- 1-Signal Test--------')
    amp = 100
    pk = 50
    tr1 = 20
    tr2 = 80
    
    x = _np.arange(100)
    signal = amp*_np.exp(-(x-pk)**2/(10**2))
    baseline = x
    y = signal + baseline

    _plt.plot(x, y.T, label='Signal')
    _plt.plot(x,baseline, label='baseline')
    _plt.plot(x, signal.T,label='Signal - Baseline')

    # non-static method
    #pbwt = MeasurePeakBWTroughs(pk=pk, tr1=tr1, tr2=tr2)
    #out = pbwt.calculate(y)

    # static method
    out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)
    
    _plt.plot((pk, pk), (0, out), 'k', lw=3, label='Calculated Amp')
    _plt.xlabel('X')
    _plt.ylabel('Amplitude (au)')
    _plt.legend(loc='best')
    _plt.show()
    
    print('Actual peak amp: {:.2f}. Retrieved peak amp: {:.2f}.'.format(amp, out))
    print('Within 1% agreement: {}'.format(_np.isclose(amp, out, rtol=.01)))
   
    print('\n\n--------- 2D Simple Test--------')
    _plt.figure()
    
    amp = 100
    pk = 50
    tr1 = 20
    tr2 = 80
    
    N=2
    
    x = _np.arange(100)
    signal = amp*_np.exp(-(x-pk)**2/(10**2))
    baseline = x
    y = signal + baseline
    mask = _np.ones((N,N))
    y = _np.dot(mask[...,None], y[None,:])

    _plt.plot(y.reshape((-1,x.size)).T, label='Signal')
    _plt.plot(x,baseline, label='baseline')
    _plt.plot(x, signal.T,label='Signal - Baseline')

    out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)
    
    for out_pk in out.ravel():
        _plt.plot((pk, pk), (0, out_pk), 'k', lw=3, label='Calculated Amp')
    _plt.xlabel('X')
    _plt.ylabel('Amplitude (au)')
    _plt.legend(loc='best')
    
    print('Actual peak(s) amp: {:.2f}. Retrieved peak amps: {}.'.format(amp, out.ravel()))
    print('Within 1% agreement: {}'.format(_np.isclose(amp, out.ravel(), rtol=.01)))
    print('All agree within 1%: {}'.format(_np.allclose(amp, out.ravel(), rtol=.01)))

    _plt.show()
    
    print('\n\n--------- 2D More Complicated Test--------')
    _plt.figure()
    
    amp = 100
    pk = 50
    tr1 = 20
    tr2 = 80
    
    N=2
    
    x = _np.arange(100)
    signal = amp*_np.exp(-(x-pk)**2/(10**2))
    mask = _np.ones((N,N))
    rndm = _np.random.randint(0,10,size=(N,N))
    baseline = _np.dot((rndm*mask)[...,None],x[None,:])
    
    y = signal[None,None,:] + baseline
    
    #y = _np.dot(mask[...,None], y[None,:])

    _plt.plot(y.reshape((-1,x.size)).T, label='Signal')
    _plt.plot(x,baseline.reshape((-1,x.size)).T, label='baseline')
    _plt.plot(x, signal.T,label='Signal - Baseline')

    #pbwt = MeasurePeakBWTroughs(pk=pk, tr1=tr1, tr2=tr2)
    #out = pbwt.calculate(y)
    out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)
    
    for out_pk in out.ravel():
        _plt.plot((pk, pk), (0, out_pk), 'k', lw=3, label='Calculated Amp')
    _plt.xlabel('X')
    _plt.ylabel('Amplitude (au)')
    _plt.legend(loc='best')
    
    print('Actual peak(s) amp: {:.2f}. Retrieved peak amps: {}.'.format(amp, out.ravel()))
    print('Within 1% agreement: {}'.format(_np.isclose(amp, out.ravel(), rtol=.01)))
    print('All agree within 1%: {}'.format(_np.allclose(amp, out.ravel(), rtol=.01)))

    _plt.show()
