"""
Created on Mon Jul 25 13:57:24 2016

@author: chc
"""
import sys as _sys
# import timeit
import numpy as _np

from PyQt5.QtWidgets import (QApplication as _QApplication, QWidget as _QWidget)

from crikit.ui.dialog_AbstractFactorization import DialogAbstractFactorization

from scipy.linalg import diagsvd as _diagsvd

class DialogSVD(DialogAbstractFactorization):
    """
    SVD Class
    """
    def __init__(self, data, img_shape, mask=None, use_imag=True, img_all=None, spect_all=None,
                 parent=None):
        super(DialogSVD, self).__init__(parent=parent) ### EDIT ###
        self.setup(parent=parent)
        self.setupData(img_shape=img_shape)
        self.ui_changes()

        self.U = data[0]
        self.s = data[1]
        self.Vh = data[2]
        self._n_factors = self.s.size

        self.mask = mask

        self._use_imag = use_imag # By default, use imag portion of complex data

        if (img_all is None) and (spect_all is None):
            cube_all = self.combiner(selections=_np.arange(self._n_factors))
            self.img_all = self.mean_spatial(cube_all)
            self.spect_all = self.mean_spectral(cube_all)
        else:
            self.img_all = img_all.real
            if _np.iscomplexobj(spect_all):
                if self._use_imag:    
                    self.spect_all = spect_all.imag
                else:
                    self.spect_all = spect_all.real
            else: 
                self.spect_all = spect_all

        self.updatePlots(0)
        self.updateCurrentRemainder()

    @staticmethod
    def dialogSVD(data, img_shape, mask=None, use_imag=True, img_all=None, spect_all=None, parent=None):
        dialog = DialogSVD(data=data, img_shape=img_shape, mask=mask,
                           use_imag=use_imag, img_all=img_all, spect_all=spect_all, parent=parent)
        result = dialog.exec_()

        if result == 1:
            svs = list(dialog.selected_factors)
            if len(svs) == 0:
                svs = None
            else:
                svs.sort()
                svs = _np.array(svs)
        else:
            svs = None
        return svs

    def max_factors(self):
        """
        Return maximum number of factors. Since DialogAbstractFactorization
        (parent) is initialized first (before self.s), need to return None
        at first.
        """
        try:
            return self.s.size
        except Exception:
            return None

    def combiner(self, selections=None):
        """Performs U*S*Vh"""

        # Straight-forward way, but slow
        # tmr = timeit.default_timer()
        # S = self.s_from_selected(selections=selections)
        # ret = _np.dot(self.U, _np.dot(S, self.Vh))
        # tmr -= timeit.default_timer()
        # # print('Selections: {}'.format(selections))
        # print('S (head): {}'.format(_np.diag(S)[0:10]))
        # print('Old way: {}'.format(-tmr))

        # New faster method
        # tmr = timeit.default_timer()
        ret = _np.dot(self.U[:, list(selections)], _np.dot(_np.diag(self.s[list(selections)]), self.Vh[list(selections), :]))
        # tmr -= timeit.default_timer()
        # print('S (head): {}'.format(self.s[list(selections)]))
        # print('New way: {}'.format(-tmr))
        # print('Old == New: {}\n'.format(_np.allclose(ret,ret2)))
        
        return ret

    def mean_spatial(self, cube):
        ret = cube.mean(axis=-1)
        ret = ret.reshape((self._n_y, self._n_x))
        if _np.iscomplexobj(ret):
            if self._use_imag:
                return _np.imag(ret)
            else:
                return _np.real(ret)
        else:
            return ret

    def mean_spectral(self, cube):
        ret = cube.mean(axis=0)

        if _np.iscomplexobj(ret):
            if self._use_imag:
                return _np.imag(ret)
            else:
                return _np.real(ret)
        else:
            return ret

    def s_from_selected(self, selections=None):
        """
        Return SVD S-matrix of SELECTED singular values
        """
        M = self.U.shape[-1]
        N = self.Vh.shape[0]

        if selections is None:
            S = _diagsvd(self.s, M, N)
            return S
        else:
            if isinstance(selections, set):
                selections = list(selections)
            s_select = _np.zeros(self.s.size)
            s_select[selections] = self.s[selections]

            S = _diagsvd(s_select, M, N)
            return S

    def get_spatial_slice(self, num):
        img = self.U[...,num].reshape((self._n_y, self._n_x))
        return _np.real(img)

        # Used to return complex, but the SVD of complex numbers tends to
        # shove everything in U into the real component

        # if _np.iscomplexobj(img):
        #     if self._use_imag:
        #         return _np.imag(img)
        #     else:
        #         return _np.real(img)
        # else:
        #     return img



    def get_spectral_slice(self, num):
        spect = self.Vh[num,:]

        if _np.iscomplexobj(spect):
            if self._use_imag:
                return _np.imag(spect)
            else:
                return _np.real(spect)
        else:
            return spect

if __name__ == '__main__':
    from scipy.linalg import svd as _svd

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    x = _np.linspace(100, 200, 100)
    y = _np.linspace(200, 300, 100)


    f = _np.linspace(500,3000,900)
    Ex = 30*_np.exp((-(f-1750)**2/(200**2)))
    Spectrum = _np.convolve(_np.flipud(Ex),Ex,mode='same')
#
    hsi = _np.zeros((y.size,x.size,f.size))
#
    for count in range(y.size):
        # hsi[count,:,:] = y[count]*_np.random.poisson(_np.dot(x[:,None],Spectrum[None,:]))
        hsi[count,:,:] = y[count]*_np.dot(x[:,None],Spectrum[None,:])
    hsi = 0*hsi + 1j*hsi

    data = _svd(hsi.reshape((-1,f.size)), full_matrices=False)

    # Class method route
    #ret = DialogSVD.main(data, hsi.shape)
    #print(ret)

    # Full route
    obj = _QWidget()
    svs = DialogSVD.dialogSVD(data, hsi.shape, img_all=hsi.mean(axis=-1), spect_all=hsi.mean(axis=(0,1)) ,parent=obj)

    print('Factors selected: {}'.format(svs))

##    app.exec_()
    _sys.exit()
