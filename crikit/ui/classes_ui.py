"""
User Interface and Visualization Classes (crikit.ui.classes_ui)
=======================================================

BW : Grayscale images

SingleColor : Single-color images

_ColorMath : Container of math operations

"""

import numpy as _np

class BW:
    """

    """
    XUNITS = 'Pixels'
    YUNITS = 'Pixels'

    _grayscaleimage = _np.array(None)  # Spectral plane image to construct color from
    title = None  # Title of IMG
    setflag = 0
    setmax = None
    setmin = None
    compress = None
    setgain = 1
    setoutlierstds = None
    #setnorm = None

    _x = _np.array(None)
    _y = _np.array(None)

    _xunits = XUNITS
    _yunits = YUNITS

    def __init__(self):
        pass

    @property
    def image(self):
        """
        Note: Outlier removal is BEFORE min/max and compression
        """
        if self.setoutlierstds is not None:
            mask_pass = (self.grayscaleimage <= self.mean + self.std*self.setoutlierstds)*\
                        (self.grayscaleimage >= self.mean - self.std*self.setoutlierstds)
            img = self.grayscaleimage*mask_pass
        else:
            img = self.grayscaleimage

        if (self.setmax is None or self.setmin is None):
            return img*self.setgain
        else:
            if self.compress == True:
                mask_pass = (img >= self.setmin)*(img <= self.setmax)
                mask_low = (img < self.setmin)
                mask_high = (img > self.setmax)
                return mask_pass*img + mask_low*self.setmin + mask_high*self.setmax
            else:
                mask = (img >= self.setmin)*(img <= self.setmax)
                return img*mask*self.setgain

    @property
    def winextent(self):
        return (self._x.min(),
                     self._x.max(),
                     self._y.min(),
                     self._y.max())
    @property
    def maxer(self):
        return self.grayscaleimage.max()

    @property
    def minner(self):
        return self.grayscaleimage.min()

    @property
    def std(self):
        try:
            temp = self.grayscaleimage.std()
            return temp
        except:
            return None

    @property
    def mean(self):
        try:
            temp = self.grayscaleimage.mean()
            return temp
        except:
            return None

    @property
    def xunits(self):
        return self._xunits

    @property
    def yunits(self):
        return self._yunits

    @property
    def ylen(self):
        return self.grayscaleimage.shape[0]

    @property
    def xlen(self):
        return self.grayscaleimage.shape[1]

    @property
    def grayscaleimage(self):
        return self._grayscaleimage

    @grayscaleimage.setter
    def grayscaleimage(self, value):
        try:
            if value.ndim == 2:
                self._grayscaleimage = value
                if (_np.equal(self._x,None).any() or
                    _np.equal(self._y,None).any() or
                    self._x.size != value.shape[1] or
                    self._y.size != value.shape[0]):

                    self._x = _np.linspace(1, value.shape[1], value.shape[1])
                    self._y = _np.linspace(1, value.shape[0], value.shape[0])
                    self.xunits = self.XUNITS
                    self.yunits = self.YUNITS

                else:
                    pass
        except:
            pass

    @grayscaleimage.deleter
    def grayscaleimage(self):
        self.__init__()

    @property
    def x(self):
        return self._x

    @x.deleter
    def x(self):
        self._x = _np.linspace(1, self.xlen, self.xlen)
        self.xunits = self.XUNITS

    @property
    def y(self):
        return self._y

    @y.deleter
    def y(self):
        self._y = _np.linspace(1, self.ylen, self.ylen)
        self.yunits = self.YUNITS

    def set_x(self, value, units = None):
        if self.xlen == value.size:
            self._x = value
            if units is not None:
                self._xunits = units
        else:
            pass

    def set_y(self, value, units = None):
        if self.ylen == value.size:
            self._y = value
            if units is not None:
                self._yunits = units
        else:
            pass


class _ColorMath:

    opfreq1 = None
    opfreq2 = None
    opfreq3 = None

    operation = None

    condfreq1 = None
    condfreq2 = None
    condfreq3 = None

    condoperation = None
    inequality = None
    inequalityval = None

    def __init__(self):
        pass

class CompositeColor(BW):
    """

    """
    def __init__(self, sgl_color_list = None):
        if sgl_color_list is None:
            self.sgl_color_list = []
        else:
            self.sgl_color_list = sgl_color_list

    @property
    def image(self):
        #print(self.sgl_color_list)
        if len(self.sgl_color_list) == 0:
            return _np.zeros(self.grayscaleimage.shape)
        else:
            temp = self.sgl_color_list[0].image

            if len(self.sgl_color_list) > 1:
                for count in self.sgl_color_list[1::]:
                    # temp -= count.image
                    temp += count.image
            # temp = abs(temp)
            # temp /= temp.max()
            # if temp.min() < 0:
            #     temp -= temp.min()
            # if temp.max() > 1:
            #     temp /= temp.max()

            temp[temp > 1] = 1
            return temp

    @property
    def ylen(self):
        return self.sgl_color_list[0].image.shape[0]
#        return self.grayscaleimage.shape[0]

    @property
    def xlen(self):
        return self.sgl_color_list[0].image.shape[1]
#        return self.grayscaleimage.shape[1]

class SingleColor(BW, _ColorMath):
    """

    """
    COLORMAP = [0, 0, 1]

    def __init__(self):
        self.colormap = self.COLORMAP

    def __add__(self, other):
        return self.image + other.image

    @property
    def image(self):

        if (self.setmax is None or self.setmin is None):
            scaled_gs = SingleColor._imgnorm(self.grayscaleimage)
            scaled_gain_gs = scaled_gs*self.setgain
            final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
            return SingleColor._bwtocolor(final_scaled_gs, self.colormap)

        else:
            fudge_factor = .001
            fudge_amt = _np.abs((self.setmax - self.setmin)*fudge_factor)
            fudged_min = self.setmin - fudge_amt
            fudged_max = self.setmax + fudge_amt
            
            if self.compress == True:
                mask_pass = (self.grayscaleimage >= fudged_min) * \
                            (self.grayscaleimage <= fudged_max)
                mask_low = (self.grayscaleimage < fudged_min)
                mask_high = (self.grayscaleimage > fudged_max)
                masked_img = mask_pass*self.grayscaleimage + \
                             mask_low*fudged_min + \
                             mask_high*fudged_max

                scaled_gs = SingleColor._imgnorm(masked_img)
                scaled_gain_gs = scaled_gs*self.setgain
                final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
                return SingleColor._bwtocolor(final_scaled_gs, self.colormap)

            else:
                mask = (self.grayscaleimage >= fudged_min) * \
                       (self.grayscaleimage <= fudged_max)
                masked_img = self.grayscaleimage*mask

                scaled_gs = SingleColor._imgnorm(masked_img)
                scaled_gain_gs = scaled_gs*self.setgain
                final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
                return SingleColor._bwtocolor(final_scaled_gs, self.colormap)

    @property
    def imageGS(self):
        """
        Returns self.grayscaleimage with limits applied
        """
        if (self.setmax is None or self.setmin is None):
            return self.grayscaleimage

        else:
            if self.compress == True:
                mask_pass = (self.grayscaleimage >= self.setmin)*(self.grayscaleimage <= self.setmax)
                mask_low = (self.grayscaleimage < self.setmin)
                mask_high = (self.grayscaleimage > self.setmax)
                masked_img = mask_pass*self.grayscaleimage + mask_low*self.setmin + mask_high*self.setmax

                return masked_img

            else:
                mask = (self.grayscaleimage >= self.setmin)*(self.grayscaleimage <= self.setmax)
                masked_img = self.grayscaleimage*mask

                return masked_img

    @staticmethod
    def _imgnorm(img, low = None, high = None):
        """
        Normalize intensity (B&W) image. Values at
        low -> 0
        high -> 1

        """

        # If now provided low or high values, set to min() and max()
        if low is None:
            low = img.min()
        if high is None:
            high = img.max()

        # Ensure high and low values are different
        if high == low:
            return 0*img  # Return 0's, if same
        else:
            return (img - low)/(high - low)

    @staticmethod
    def _imgnormcompress(img):
        """
        Compress normalized image. Values:
        > 1 -> 1
        < 0 -> 0
        """
        mask_pass = (img <= 1)*(img >= 0)
        mask_high = (img > 1)

        return mask_pass*img + mask_high

    @staticmethod
    def _bwtocolor(gs, colormap):
        """
        Convert normalized [0,1] B&W image (gs) to color, applying a
        3-value list colormap (colormap)
        """
        img = _np.ones((gs.shape[0], gs.shape[1], 3))
        gs_3d = _np.dot(gs[:,:,None],_np.ones((1,3)))
        return (img*colormap)*gs_3d