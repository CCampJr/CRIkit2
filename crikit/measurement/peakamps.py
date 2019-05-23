"""
Measurement methods to quantify peak relationships

Note
-----

For complex-valued measurements, all methods perform the math separately for real and imag
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
    def measure(cls, signal, f1):
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
        if _np.iscomplexobj(signal):
            self.output = self._calc(signal.real) + 1j*self._calc(signal.imag)
        else:
            self.output = self._calc(signal)

        return self.output

    @classmethod
    def measure(cls, signal, f1, f2):
        inst = cls(f1, f2)
        return inst.calculate(signal)

    def _calc(self, signal):
        raise NotImplementedError

class AbstractMeasureTwoOrdered(AbstractMeasureTwo):
    """ 
    Abstract class for measurements that take 2 things,
    where f1 < f2
    """
    def __init__(self, f1, f2):
        if f1 <= f2:
            super().__init__(f1, f2)
        else:
            super().__init__(f2, f1)

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

        if _np.iscomplexobj(signal):
            self.output = self._calc(signal.real) + 1j*self._calc(signal.imag)
        else:
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
        super().__init__(f1,f2)

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
        super().__init__(f1,f2)

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
        super().__init__(f1,f2)

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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = signal[..., self.f1] / signal[..., self.f2]

        return output

class MeasurePeakSum(AbstractMeasureTwoOrdered):
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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.sum(signal[..., self.f1:self.f2+1], axis=-1)

        return output

class MeasurePeakSumAbsReImag(AbstractMeasureTwoOrdered):
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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.sum(_np.abs(signal[..., self.f1:self.f2+1]), axis=-1)

        return output

class MeasurePeakMax(AbstractMeasureTwoOrdered):
    """
    Meausure the maximum across the range [f1,f2]. Note
     that real and imag are treated separately.

    Parameters
    ----------
    f1 : int
        Peak location in pixel coordinates
    f2 : int
        Peak location in pixel coordinates

    Attributes
    ----------
    output : float or ndarray
        Amplitude

    Methods
    -------
    calculate : Calculate the amplitude

    Static Methods
    --------------
    measure : Same as calculate but static (returns the amplitude directly)

    """
    def __init__(self, f1, f2):
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.max(signal[..., self.f1:self.f2+1], axis=-1)
        return output

class MeasurePeakMin(AbstractMeasureTwoOrdered):
    """
    Meausure the minimum across the range [f1,f2]. Note
     that real and imag are treated separately.

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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.min(signal[..., self.f1:self.f2+1], axis=-1)

        return output


class MeasurePeakMaxAbs(AbstractMeasureTwoOrdered):
    """
    Meausure the maximum across the absolute value across
    the range [f1,f2]. Note that real and imag are
     treated separately.

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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.max(_np.abs(signal[..., self.f1:self.f2+1]), axis=-1)

        return output


class MeasurePeakMinAbs(AbstractMeasureTwoOrdered):
    """
    Meausure the summation of all amplitudes between (inclusive) two peak
    locations. Note that real and imag are treated
     separately.

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
        super().__init__(f1,f2)

    def _calc(self, signal):
        output = _np.min(_np.abs(signal[..., self.f1:self.f2+1]), axis=-1)

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
    data_m, data_n, data_p = [2, 3, 5]
    spectrum = _np.array([0,1,2,3,4])
    hsi = _np.dot(_np.ones((data_m*data_n, 1)), spectrum[None,:])
    hsi = hsi.reshape((data_m, data_n, data_p))

    
    output = MeasurePeakBWTroughs.measure(hsi,2,0,4)
    print(output)

    m_inst = MeasurePeakBWTroughs(2,0,4)
    m_inst.calculate(hsi)
    print(m_inst.output)

    # import matplotlib.pyplot as _plt

    # print('\n\n--------- 1-Signal Test--------')
    # amp = 100
    # pk = 50
    # tr1 = 20
    # tr2 = 80

    # x = _np.arange(100)
    # signal = amp*_np.exp(-(x-pk)**2/(10**2))
    # baseline = x
    # y = signal + baseline

    # _plt.plot(x, y.T, label='Signal')
    # _plt.plot(x,baseline, label='baseline')
    # _plt.plot(x, signal.T,label='Signal - Baseline')

    # # non-static method
    # #pbwt = MeasurePeakBWTroughs(pk=pk, tr1=tr1, tr2=tr2)
    # #out = pbwt.calculate(y)

    # # static method
    # out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)

    # _plt.plot((pk, pk), (0, out), 'k', lw=3, label='Calculated Amp')
    # _plt.xlabel('X')
    # _plt.ylabel('Amplitude (au)')
    # _plt.legend(loc='best')
    # _plt.show()

    # print('Actual peak amp: {:.2f}. Retrieved peak amp: {:.2f}.'.format(amp, out))
    # print('Within 1% agreement: {}'.format(_np.isclose(amp, out, rtol=.01)))

    # print('\n\n--------- 2D Simple Test--------')
    # _plt.figure()

    # amp = 100
    # pk = 50
    # tr1 = 20
    # tr2 = 80

    # N=2

    # x = _np.arange(100)
    # signal = amp*_np.exp(-(x-pk)**2/(10**2))
    # baseline = x
    # y = signal + baseline
    # mask = _np.ones((N,N))
    # y = _np.dot(mask[...,None], y[None,:])

    # _plt.plot(y.reshape((-1,x.size)).T, label='Signal')
    # _plt.plot(x,baseline, label='baseline')
    # _plt.plot(x, signal.T,label='Signal - Baseline')

    # out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)

    # for out_pk in out.ravel():
    #     _plt.plot((pk, pk), (0, out_pk), 'k', lw=3, label='Calculated Amp')
    # _plt.xlabel('X')
    # _plt.ylabel('Amplitude (au)')
    # _plt.legend(loc='best')

    # print('Actual peak(s) amp: {:.2f}. Retrieved peak amps: {}.'.format(amp, out.ravel()))
    # print('Within 1% agreement: {}'.format(_np.isclose(amp, out.ravel(), rtol=.01)))
    # print('All agree within 1%: {}'.format(_np.allclose(amp, out.ravel(), rtol=.01)))

    # _plt.show()

    # print('\n\n--------- 2D More Complicated Test--------')
    # _plt.figure()

    # amp = 100
    # pk = 50
    # tr1 = 20
    # tr2 = 80

    # N=2

    # x = _np.arange(100)
    # signal = amp*_np.exp(-(x-pk)**2/(10**2))
    # mask = _np.ones((N,N))
    # rndm = _np.random.randint(0,10,size=(N,N))
    # baseline = _np.dot((rndm*mask)[...,None],x[None,:])

    # y = signal[None,None,:] + baseline

    # #y = _np.dot(mask[...,None], y[None,:])

    # _plt.plot(y.reshape((-1,x.size)).T, label='Signal')
    # _plt.plot(x,baseline.reshape((-1,x.size)).T, label='baseline')
    # _plt.plot(x, signal.T,label='Signal - Baseline')

    # #pbwt = MeasurePeakBWTroughs(pk=pk, tr1=tr1, tr2=tr2)
    # #out = pbwt.calculate(y)
    # out = MeasurePeakBWTroughs.measure(signal, pk, tr1, tr2)

    # for out_pk in out.ravel():
    #     _plt.plot((pk, pk), (0, out_pk), 'k', lw=3, label='Calculated Amp')
    # _plt.xlabel('X')
    # _plt.ylabel('Amplitude (au)')
    # _plt.legend(loc='best')

    # print('Actual peak(s) amp: {:.2f}. Retrieved peak amps: {}.'.format(amp, out.ravel()))
    # print('Within 1% agreement: {}'.format(_np.isclose(amp, out.ravel(), rtol=.01)))
    # print('All agree within 1%: {}'.format(_np.allclose(amp, out.ravel(), rtol=.01)))

    # _plt.show()
