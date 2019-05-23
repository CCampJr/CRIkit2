"""
Created on Wed Jun 29 01:28:44 2016

@author: chc
"""

import numpy as _np

class MeasurePeak:
    """
    Meausure peak amplitude.

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1):
        self.output = None

        self.f1 = f1

    def calculate(self, signal):
        self.output = self._calc(signal)

        return self.output

    @classmethod
    def measure(signal, f1):
        inst = cls(f1)
        return inst.calculate(signal)

    def _calc(self, signal):
        output = signal[..., self.f1]

        return output


class AbstractMeasureTwo:
    """ Abstract class for measurements that take 2 things """
    def __init__(self, f1, f2):
        """

        Parameters
        ----------
        f1 : int
            Frequency 1 entry

        f2 : int
            Frequency 2 entry

        Attributes
        ----------
        output : ndarray
            Output of measurement operation

        """
        self.output = None

        self.f1 = f1
        self.f2 = f2

    def calculate(self, signal):
        self.output = self._calc(signal)

        return self.output

    @classmethod
    def measure(cls, signal, f1, f2):
        inst = cls(f1, f2)
        return inst.calculate(signal)

    def _calc(self, signal):
        raise NotImplementedError

class AbstractMeasureThree:
    """ Abstract class for measurements that take 3 things """
    def __init__(self, f1, f2, f3):
        """

        Parameters
        ----------
        f1 : int
            Frequency 1 entry

        f2 : int
            Frequency 2 entry

        f3 : int
            Frequency 3 entry

        Attributes
        ----------
        output : ndarray
            Output of measurement operation

        """
        self.output = None

        self.f1 = f1
        self.f2 = f2
        self.f3 = f3

    def calculate(self, signal):
        self.output = self._calc(signal)

        return self.output

    @classmethod
    def measure(cls, signal, f1, f2, f3):
        inst = cls(f1, f2, f3)
        return inst.calculate(signal)

    def _calc(self, signal):
        raise NotImplementedError

class MeasurePeakMinus (AbstractMeasureTwo):
    """
    Meausure the difference (subtraction) of two peaks (f1 - f2).

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = signal[..., self.f1] - signal[..., self.f2]

        return output

class MeasurePeakAdd(AbstractMeasureTwo):
    """
    Meausure the addition of two peaks (f1 + f2).

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = signal[..., self.f1] + signal[..., self.f2]

        return output

class MeasurePeakMultiply(AbstractMeasureTwo):
    """
    Meausure the multiplication of two peak.

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = signal[..., self.f1] * signal[..., self.f2]

        return output

class MeasurePeakDivide(AbstractMeasureTwo):
    """
    Meausure the ratio (division) of two peaks. f1/f2

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = signal[..., self.f1] / signal[..., self.f2]

        return output

class MeasurePeakSummation(AbstractMeasureTwo):
    """
    Meausure the summation of all amplitudes between (inclusive) two peak
    locations.

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = _np.sum(signal[..., self.f1:self.f2+1], axis=-1)

        return output

class MeasurePeakSummationAbsReImag(AbstractMeasureTwo):
    """
    Meausure the summation of the absolute value of all amplitudes
    between (inclusive) two peak locations. Note that the absolute value
    is performed on the real and imaginary parts separately -- it's not a
    true absolute value.

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """

    def __init__(self, f1, f2):
        super.__init__(f1,f2)

    def _calc(self, signal):
        output = _np.sum(_np.abs(signal[..., self.f1:self.f2+1].real) +
                      1j*_np.abs(signal[..., self.f1:self.f2+1].imag), axis=-1)

        return output

class MeasurePeakBWTroughs(AbstractMeasureThree):
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
    output : float or ndarray
        Amplitude of peak

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, pk, tr1, tr2):
        if tr1 <= tr2:
            super().__init__(pk, tr1, tr2)
        else:
            super().__init__(pk, tr2, tr1)

    def _calc(self, signal):
        slope = (signal[..., self.f3]-signal[..., self.f2])/ \
                 (self.f3 - self.f2)
        output = signal[..., self.f1] - (slope*(self.f1 - self.f2) + \
                signal[..., self.f2])

        return output

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
