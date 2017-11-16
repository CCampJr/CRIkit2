"""
Created on Fri Jun 10 16:16:17 2016

@author: chc
"""

import numpy as _np

class FFTSignalMetric:
    """
    FFT Spatial Noise Metric (Ratio - 1)
    """
    def __init__(self, img_shp, cutoff=0.5, img=None):

        self.value = None
        self.cutoff = cutoff
        self.img_shape = img_shp
        self.img_size = self.img_shape[0]*self.img_shape[1]

        self._calc_mtxs()

        if img is None:
            pass
        else:
            self.calc(img)

    def _calc_mtxs(self):
        """
        Calculate binary spatial weight maxtrix, wij.

        Note: Currently only supports 1st-order "rook's" case continuity
        """

        self.cutoff_row = [int(self.img_shape[0]/2*self.cutoff),
                           int(self.img_shape[0]/2*(1+self.cutoff))]
        self.cutoff_col = [int(self.img_shape[1]/2*self.cutoff),
                           int(self.img_shape[1]/2*(1+self.cutoff))]

        self.n_inner_pix = (self.cutoff_row[1]-self.cutoff_row[0]+1) * \
                           (self.cutoff_col[1]-self.cutoff_col[0]+1)

        self.n_outter_pix = self.img_size - self.n_inner_pix

        self.scaler = self.n_outter_pix/self.n_inner_pix

    def calc(self, img):
        """

        """
        self.value = None

        f_img = _np.abs(_np.fft.fftshift(_np.fft.fft2(img-img.mean())))
        sum_inner = f_img[self.cutoff_row[0]:self.cutoff_row[1]+1,
                          self.cutoff_col[0]:self.cutoff_col[1]+1].sum()
        sum_outter = f_img.sum() - sum_inner
        
        if sum_outter == 0:
            self.value = 1e6
        else:
            self.value = self.scaler*sum_inner/sum_outter

        self.value -= 1

if __name__ == '__main__':

    import timeit as _timeit

    side_len = 301
    img = _np.zeros(side_len**2)
    img[::1] = 1.0
    img = img.reshape((side_len, side_len))

    tmr = _timeit.default_timer()
    fmet = FFTSignalMetric(img_shp=(side_len, side_len))
    fmet.calc(img)
    tmr -= _timeit.default_timer()

    print('---------')
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('FFT Signal Metric of checkerboard: {:.3g}'.format(fmet.value))
    print('Is close to ideal -1 value (?) (+/- .1): {}'.format(_np.isclose(fmet.value, -1, atol=1e-1)))

    img = _np.random.rand(side_len, side_len)

    tmr = _timeit.default_timer()
    fmet = FFTSignalMetric(img_shp=(side_len, side_len))
    fmet.calc(img)
    tmr -= _timeit.default_timer()

    print('\n---------')
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('FFT Signal Metric of random: {:.3g}'.format(fmet.value))
    print('Is close to ideal 0 value (+/- .1): {}'.format(_np.isclose(fmet.value, 0,
          atol=1e-1)))
    
    img = _np.random.rand(1, side_len)

    tmr = _timeit.default_timer()
    fmet = FFTSignalMetric(img_shp=(1, side_len))
    fmet.calc(img)
    tmr -= _timeit.default_timer()

    print('\n---------')
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('FFT Signal Metric of random: {:.3g}'.format(fmet.value))
    print('Is close to ideal 0 value (+/- .1): {}'.format(_np.isclose(fmet.value, 0,
          atol=1e-1)))
