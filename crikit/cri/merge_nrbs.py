"""
Created on Wed Nov  2 11:04:43 2016

@author: chc
"""

import copy as _copy

if __name__ == '__main__':
    import matplotlib.pyplot as _plt
    import numpy as _np

    
class MergeNRBs:
    """
    Merge two NRBs: a left-side and a right-side
    
    """
    def __init__(self, nrb_left, nrb_right, pix, left_side_scale=True):
        """
        Attributes
        ----------
        pix : int
            Pixel number to make the merge
            
        left_side_scale : bool
            Scale the left-side to match the right-side. If FALSE, scales the
            right-side. If None, scales neither.

        Note
        -----
        If left_side_scale is None (no scaling). The output will match the nrb_left from [0:pix),
        and nrb_right from [pix:].
            
        """
        self.nrb_left = nrb_left
        self.nrb_right = nrb_right
        self.nrb_merge = None
        
        self.pix = pix
        self.scale_left = left_side_scale

    def calculate(self):
        """
        
        """
        if self.nrb_left.size != self.nrb_right.size:
            print('NRB size mismatch')
            return None
        else:
            pass
        
        self.nrb_merge = _copy.deepcopy(0*self.nrb_left)
        
        success = self._calc(self.nrb_merge, ret_obj=self.nrb_merge)
        if success:
            return self.nrb_merge
        else:
            return None
        
    def _calc(self, data, ret_obj):
        try:
            ret_obj *= 0
            scaler = self.nrb_left[self.pix]/self.nrb_right[self.pix]
            if self.scale_left == True:
                ret_obj += self.nrb_left/scaler
                ret_obj[self.pix::] = self.nrb_right[self.pix::]
            elif self.scale_left == False:
                ret_obj += self.nrb_left
                ret_obj[self.pix::] = self.nrb_right[self.pix::]*scaler
            elif self.scale_left is None:
                ret_obj[0:self.pix] = self.nrb_left[0:self.pix]
                ret_obj[self.pix::] = self.nrb_right[self.pix::]
                
            else:
                raise ValueError('self.scale_left must be True, False, or None')
        except Exception:
            return False
        else:
            return True
           
if __name__ == '__main__':  # pragma: no cover
    x = _np.arange(0,1000)
    
    nrb_left = _np.exp(-(x-500)**2/(100**2))
    nrb_right = _np.exp(-(x-700)**2/(120**2))
    
    pix = 625
    
    _plt.plot(x, nrb_left, label='left')
    _plt.plot(x, nrb_right, label='right')
    _plt.title('Raw NRBs')
    
    
    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=True)
    out_scaled_left = merge.calculate()
    _plt.plot(x, out_scaled_left, ls='--', label='Left Scaled')
    
    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=False)
    out_scaled_right = merge.calculate()
    _plt.plot(x, out_scaled_right, ls='--', label='Right Scaled')
    
    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=None)
    out_scaled_none = merge.calculate()
    _plt.plot(x, out_scaled_none, ls='--', lw=3, label='NOT Scaled')
    
    _plt.legend(loc='best')
    _plt.show()