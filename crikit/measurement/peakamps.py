# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 01:28:44 2016

@author: chc
"""

import numpy as _np


class MeasurePeakBWTroughs:
    """

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

    def _calc(self, signal):
        baseline = _np.linspace(signal[self.tr_left], signal[self.tr_right],
                                self.tr_right-self.tr_left + 1)
        return signal[self.pk] - baseline[self.pk-self.tr_left]

if __name__ == '__main__':
    import matplotlib.pyplot as _plt

    x = _np.arange(100)
    y1 = 100*_np.exp(-(x-50)**2/(10**2))
    y2 = x
    y = y1 + y2

    _plt.plot(x, y)
    _plt.plot(x, y1)

    pbwt = MeasurePeakBWTroughs(pk=50, tr1=20, tr2=80)

    baseline = _np.linspace(y[20], y[80], 61)

    _plt.plot(x[20:81],baseline)
    _plt.plot(x[20:81],y[20:81] - baseline)

    out = pbwt.calculate(y)
    print(out)

    _plt.show()
