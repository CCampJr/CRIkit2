# -*- coding: utf-8 -*-
"""
Calculate Moran's I spatial autocorrelation value

Created on Fri Jun 10 14:08:30 2016

@author: chc
"""

import numpy as _np

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

from crikit.utils.gen_utils import row_col_from_lin as _row_col_from_lin
from crikit.utils.gen_utils import lin_from_row_col as _lin_from_row_col


class MoranI:
    """
    Moran's I class
    """
    def __init__(self, img_shp, img=None):

        self.I = None

        self.img_shape = img_shp  # Shape
        self.img_size = _np.array(img_shp).prod()  # Size

        self.row, self.col = _row_col_from_lin(_np.arange(self.img_size),
                                               self.img_shape)

        # Calculate static wij matrix (calc'd only on img shape)
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

        self.wij = _np.zeros((self.img_size, self.img_size))

        for num, loc in enumerate(zip(self.row, self.col)):
            rc = loc[0]
            cc = loc[1]

            # Rook's case using "dumb" math
            rc_rook = _np.array([rc - 1, rc + 1, rc, rc])
            cc_rook = _np.array([cc, cc, cc + 1, cc - 1])

            # Remove indices that are out-of-bounds
            loc_to_keep = _np.where((rc_rook >= 0) &
                                    (rc_rook < self.img_shape[0]) &
                                    (cc_rook >= 0) &
                                    (cc_rook < self.img_shape[1]))
            rc_rook = rc_rook[loc_to_keep]
            cc_rook = cc_rook[loc_to_keep]

            # Row, Col -> index
            loc_rook = _lin_from_row_col(rc_rook, cc_rook, self.img_shape)

            self.wij[num, loc_rook] = 1

    def calc(self, img):
        """
        Calculate the Moran's I value.
        """
        self.I = None

        input_img_shape = img.shape

        # Potentially, sub-divide the img into smaller images
        # if self.img_shape is smaller than the provided img

        r_steps = input_img_shape[0]//self.img_shape[0]
        c_steps = input_img_shape[1]//self.img_shape[1]

        I = _np.zeros((r_steps, c_steps))

        # Perform separate calculation for each (possible) sub-image
        for rc in range(r_steps):
            for cc in range(c_steps):
                sm_img = img[rc*self.img_shape[0]:(rc+1)*self.img_shape[0],cc*self.img_shape[1]:(cc+1)*self.img_shape[1]]
                I[rc,cc] = self._calc_I(sm_img)

        self.I = I.mean()

    def _calc_I(self, img):
        """
        Actual Moran's I calculation
        """

        img_mean = img.mean()
        img_r = img.ravel() - img_mean

        # Outter product of unraveled image
        cp = _np.dot(img_r[:,None],img_r[None,:])

        # Double-recursive numerator-portion in Moran's I calculation
        a = (self.wij*cp).sum()

        # Double-recursive denominator-portion in Moran's I calculation
        b = self.wij.sum()

        # Single-recursive denominator portion
        d = _np.sum(img_r**2)

        I = self.img_size*a/(b*d)

        return I

if __name__ == '__main__':

    import timeit as _timeit

    side_len = 51
    img = _np.zeros(side_len**2)
    img[::2] = 1
    img = img.reshape((side_len, side_len))

    tmr = _timeit.default_timer()
    mi = MoranI(img_shp=(side_len, side_len))
    mi.calc(img)
    tmr -= _timeit.default_timer()

    print('---------')
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('Moran\'s I of checkerboard: {:.3g}'.format(mi.I))
    print('Is close to ideal -1 value (+/- .01): {}'.format(_np.isclose(mi.I, -1, atol=1e-2)))

    tmr = _timeit.default_timer()
    mi = MoranI(img_shp=(10,10))
    mi.calc(img)
    tmr -= _timeit.default_timer()

    print('\n---------')
    print('Sub-image iterative calculation {} -> {}'.format(img.shape, (10,10)))
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('Moran\'s I of checkerboard: {:.3g}'.format(mi.I))
    print('Is close to ideal -1 value (+/- .01): {}'.format(_np.isclose(mi.I, -1, atol=1e-2)))

    img = _np.random.rand(side_len, side_len)

    tmr = _timeit.default_timer()
    mi = MoranI(img_shp=(side_len, side_len))
    mi.calc(img)
    tmr -= _timeit.default_timer()

    print('\n---------')
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('Moran\'s I of random: {:.3g}'.format(mi.I))
    print('Is close to ideal 0 value (+/- .1): {}'.format(_np.isclose(mi.I, 0,
          atol=1e-1)))

    tmr = _timeit.default_timer()
    mi = MoranI(img_shp=(10,10))
    mi.calc(img)
    tmr -= _timeit.default_timer()

    print('\n---------')
    print('Sub-image iterative calculation {} -> {}'.format(img.shape, (10,10)))
    print('Calculated in {:.3g} sec'.format(-tmr))
    print('Moran\'s I of random: {:.3g}'.format(mi.I))
    print('Is close to ideal 0 value (+/- .1): {}'.format(_np.isclose(mi.I, 0,
          atol=1e-1)))