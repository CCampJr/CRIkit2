"""
User Interface and Visualization Classes (crikit.ui.classes_ui)
===============================================================

BW : Grayscale images

SingleColor : Single-color images

_ColorMath : Container of math operations

"""

import numpy as _np
import copy as _copy
import matplotlib as _mpl

class BW:
    """

    """
    
    def __init__(self, **kwargs):
        self._default_attributes = {
            'title':None,
            'setflag':0,
            'setmax':None,
            'setmin':None,
            'compress_low':None,
            'compress_high':None,
            'setgain':1,
            'xunits':'Pixels',
            'yunits':'Pixels'
        }
        self._default_attributes.update(kwargs)

        self._grayscaleimage = None
        self.title = self._default_attributes['title']
        self.setflag = self._default_attributes['setflag']
        self.setmax = self._default_attributes['setmax']
        self.setmin = self._default_attributes['setmin']
        self.compress_high = self._default_attributes['compress_high']
        self.compress_low = self._default_attributes['compress_low']
        self.setgain = self._default_attributes['setgain']
        self.xunits = self._default_attributes['xunits']
        self.yunits = self._default_attributes['yunits']
        self._x = None
        self._y = None

    @property
    def image(self):
        """
        For image from property settings (limits, compression, etc)
        """    
        img = self.grayscaleimage

        if (self.setmax is None or self.setmin is None):
            return img*self.setgain
        else:
            mask_pass = (img >= self.setmin)*(img <= self.setmax)
            mask_low = (img < self.setmin)
            mask_high = (img > self.setmax)
            img = (mask_pass*img + self.compress_low*mask_low*self.setmin + 
                    self.compress_high*mask_high*self.setmax)
            return img*self.setgain

    @property
    def winextent(self):
        return (self.x.min(), self.x.max(), self.y.min(), self.y.max())

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
        except Exception:
            return None

    @property
    def mean(self):
        try:
            temp = self.grayscaleimage.mean()
            return temp
        except Exception:
            return None

    @property
    def ylen(self):
        return self._grayscaleimage.shape[0]

    @property
    def xlen(self):
        return self._grayscaleimage.shape[1]

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
                    

                else:
                    pass
        except Exception:
            print('Set grayscaleimage error')

    @grayscaleimage.deleter
    def grayscaleimage(self):
        self.__init__()

    @property
    def x(self):
        if self._x is not None:
            return self._x
        else:
            self._x = _np.arange(self.xlen)
            self.xunits = self._default_attributes['xunits']
            return self._x

    @x.deleter
    def x(self):
        self._x = _np.linspace(1, self.xlen, self.xlen)
        self.xunits = self.XUNITS

    @property
    def y(self):
        if self._y is not None:
            return self._y
        else:
            self._y = _np.arange(self.ylen)
            self.yunits = self._default_attributes['yunits']
            return self._y

    @y.deleter
    def y(self):
        self._y = _np.linspace(1, self.ylen, self.ylen)
        self.yunits = self.YUNITS

    def set_x(self, value, units = None):
        if value is None:
            pass
        else:
            if self.xlen == value.size:
                self._x = value
                if units is not None:
                    self.xunits = units
            else:
                pass

    def set_y(self, value, units = None):
        if value is None:
            pass
        else:
            if self.ylen == value.size:
                self._y = value
                if units is not None:
                    self.yunits = units
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
        BW.__init__(self)
        self.bgcolor = [0,0,0]
        self.mode = 0  # 0: emission; 1: absorption

        if sgl_color_list is None:
            self.sgl_color_list = []
        else:
            self.sgl_color_list = sgl_color_list

    @property
    def mode_txt(self):
        if self.mode == 0:
            return 'Emission'
        else:
            return 'Absorption'
        
    @property
    def image(self):
        #print(self.sgl_color_list)
        if len(self.sgl_color_list) == 0:
            return _np.zeros(self.grayscaleimage.shape)
        else:
            if self.mode == 0:  # Emission
                img_emission = _np.zeros(self.sgl_color_list[0].image.shape)
            
                list_imgs = _copy.deepcopy(self.sgl_color_list)
            
                for img in list_imgs:
                    img.bgcolor = [0,0,0]
                    img_emission += img.image
                img_emission[img_emission>1] = 1
                return img_emission
            elif self.mode == 1:  # Absorption
                img_absorption = _np.zeros(self.sgl_color_list[0].image.shape)
                img_frac_coverage = _np.zeros(self.sgl_color_list[0].grayscaleimage.shape)
                img_num_covered = _np.zeros(self.sgl_color_list[0].grayscaleimage.shape)

                list_imgs = _copy.deepcopy(self.sgl_color_list)
                
                for img in list_imgs:
                    if (img.grayscaleimage.nonzero()[0].size == 0) | (img.setgain == 0.0):
                        pass
                    else:
                        img.bgcolor = [0,0,0]

                        temp = 1*img.imageGS
                        temp -= temp.min()
                        if temp.max() != 0:
                            temp /= temp.max()

                        img_absorption += temp[:,:,None]*img.colormap
                        img_frac_coverage += temp
                        img_num_covered += (temp > 0)
                img_frac_coverage[img_frac_coverage>1] = 1
                img_absorb_bg = (1-img_frac_coverage)[:,:,None]*[1,1,1]
                img_absorb_bg[img_absorb_bg<0] = 0
                img_absorption /= (img_num_covered+1e-10)[:,:,None]
                img_absorption += img_absorb_bg
                return img_absorption
            elif self.mode == 2: # Absorption version 2
                
                img_emission = _np.zeros(self.sgl_color_list[0].image.shape)
                list_imgs = _copy.deepcopy(self.sgl_color_list)
            
                # Start with emission image BUT white background
                # This addition will BRIGHTEN as well
                # thus needs contrast enhancement later
                num = 0
                for img in list_imgs:
                    img.bgcolor = [1,1,1]
                    temp = img.image
                    if (temp.max() != temp.min()) & (img.setgain != 0.0):
                        img_emission += temp
                        num += 1

                # Average
                if num != 0:
                    img_emission /= num
                    
                    # This enhances contrast
                    # Yes, the first step cancels out the step above
                    # but this keep the norm. and contrast steps separate
                    img_emission *= num
                    img_emission -= (num-1)

                img_emission[img_emission<0] = 0
                img_emission[img_emission>1] = 1
                
                return img_emission

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
    
    def __init__(self):
        BW.__init__(self)
        self.bgcolor = [0,0,0]
        self.colormap = [1,0,0]

    def __add__(self, other):
        return self.image + other.image

    @property
    def image(self):
        
        if (self.setmax is None or self.setmin is None):
            scaled_gs = SingleColor._imgnorm(self.grayscaleimage)
            scaled_gain_gs = scaled_gs*self.setgain
            final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
            return SingleColor._bwtocolor(final_scaled_gs, self.colormap, self.bgcolor)

        else:
            fudge_factor = .001
            fudge_amt = _np.abs((self.setmax - self.setmin)*fudge_factor)
            fudged_min = self.setmin - fudge_amt
            fudged_max = self.setmax + fudge_amt
            
            # if self.compress == True:
            mask_pass = (self.grayscaleimage >= fudged_min) * \
                        (self.grayscaleimage <= fudged_max)
            mask_low = (self.grayscaleimage < fudged_min)
            mask_high = (self.grayscaleimage > fudged_max)
            masked_img = mask_pass*self.grayscaleimage + \
                            self.compress_low*mask_low*fudged_min + \
                            self.compress_high*mask_high*fudged_max

            scaled_gs = SingleColor._imgnorm(masked_img)
            scaled_gain_gs = scaled_gs*self.setgain
            final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
            return SingleColor._bwtocolor(final_scaled_gs, self.colormap, self.bgcolor)

            # else:
            #     mask = (self.grayscaleimage >= fudged_min) * \
            #            (self.grayscaleimage <= fudged_max)
            #     masked_img = self.grayscaleimage*mask

            #     scaled_gs = SingleColor._imgnorm(masked_img)
            #     scaled_gain_gs = scaled_gs*self.setgain
            #     final_scaled_gs = SingleColor._imgnormcompress(scaled_gain_gs)
            #     return SingleColor._bwtocolor(final_scaled_gs, self.colormap)

    @property
    def imageGS(self):
        """
        Returns self.grayscaleimage with limits applied
        """
        if (self.setmax is None or self.setmin is None):
            return self.grayscaleimage

        else:
            # if self.compress == True:
            mask_pass = (self.grayscaleimage >= self.setmin)*(self.grayscaleimage <= self.setmax)
            mask_low = (self.grayscaleimage < self.setmin)
            mask_high = (self.grayscaleimage > self.setmax)
            masked_img = (mask_pass*self.grayscaleimage + self.compress_low*mask_low*self.setmin +
                          self.compress_high*mask_high*self.setmax)

            return masked_img

            # else:
            #     mask = (self.grayscaleimage >= self.setmin)*(self.grayscaleimage <= self.setmax)
            #     masked_img = self.grayscaleimage*mask

            #     return masked_img

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
    def _bwtocolor(gs, colormap, bgcolor=[0,0,0]):
        """
        Convert normalized [0,1] B&W image (gs) to color, applying a
        3-value list colormap (colormap)
        """
        # img = _np.ones((gs.shape[0], gs.shape[1], 3))
        # gs_3d = _np.dot(gs[:,:,None],_np.ones((1,3)))
        # return (img*colormap)*gs_3d
        return (1-gs[:,:,None])*bgcolor + gs[:,:,None]*colormap