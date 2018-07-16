import numpy as _np
import h5py as _h5py

class Mosaic:
    """
    Mosaic Class

    Notes
    -----

    - input objects mts be ndarray
    - input objects must be 2D/3D  # ! Higher-D?
    - For 3D objects, assumed to be Y, X, Color

    """
    def __init__(self):
        self._data = None

        self.parameters = {}
        self.parameters['StartC'] = 0
        self.parameters['StartR'] = 0
        self.parameters['EndC'] = -0
        self.parameters['EndR'] = -0
        self.parameters['Transpose'] = False
        self.parameters['FlipVertical'] = False
        self.parameters['FlipHorizontally'] = False

    def __repr__(self):  # pragma: no cover
        if self._data:
            return 'Mosaic contains {} component(s)'.format(self.size)
        else:
            return 'Empty Collection'

    @property
    def shape(self):
        if self._data:
            return tuple([q.shape for q in self._data])

    @property
    def size(self):
        if self._data:
            return len(self._data)

    def append(self, obj):
        """ Append new object to data. Check dimensions """
        if not (isinstance(obj, _np.ndarray) | isinstance(obj, _h5py.Dataset)):
            raise TypeError('Appended object must be a numpy array')
        if not ((obj.ndim > 1) & (obj.ndim <= 3)):
            raise TypeError('Appended object must be a numpy array with ndim 2 or 3')

        if not self._data:
            self._data = []

        if self._data:
            if not _np.unique([q.ndim for q in self._data])[0] == obj.ndim:
                err_str1 = 'New component ndim must match existing ndim'
                err_str2 = ' ({})'.format(self._data[0].ndim)
                raise TypeError(err_str1 + err_str2)

        self._data.append(obj)

    @property
    def issamedim(self):
        if self._data:
            return _np.unique([q.ndim for q in self._data]).size == 1

    @property
    def is2d(self):
        if self._data:
            if not self.issamedim:
                raise TypeError('Not every component is of the same dimension')
            return len(self.unitshape) == 2

    @property
    def is3d(self):
        if self._data:
            if not self.issamedim:
                raise TypeError('Not every component is of the same dimension')
            return len(self.unitshape) == 3


    @property
    def unitshape(self):
        if self.parameters['EndR'] > 0:
            raise ValueError('parameter EndR must be <= 0')
        if self.parameters['EndC'] > 0:
            raise ValueError('parameter EndC must be <= 0')

        if self._data:
            temp = list(self.unitshape_orig)

            sr = self.parameters['StartR']
            er = self.parameters['EndR']
            sc = self.parameters['StartC']
            ec = self.parameters['EndC']

            temp[0] -= (sr - er)
            temp[1] -= (sc - ec)

            return tuple(temp)

    @property
    def unitshape_orig(self):
        if self._data:
            return tuple(_np.array(self.shape).max(axis=0).tolist())


    @property
    def dtype(self):
        """ Return the highest dtype """
        if self._data:
            dt = [q.dtype.kind for q in self._data]

            if dt.count('c') > 0:
                return _np.complex
            elif dt.count('f') > 0:
                return _np.float
            elif dt.count('i') > 0:
                return _np.int


    def mosaic_shape(self, shape, idx=None):
        """ Return the shape of a would-be mosaic """
        if self._data:
            if not len(shape) == 2:
                raise ValueError('Shape must be a tuple/list with 2 entries (Y, X)')

            if _np.prod(shape) < self.size:
                raise ValueError('The total number of subimages (shape) need be >= number of components ({})'.format(self.size))

            us = list(self.unitshape)

            if self.parameters['Transpose']:
                temp = 1*us[0]
                us[0] = us[1]
                us[1] = temp

            if (len(us) == 3):
                if idx is None:
                    out_is2d = False
                else:
                    out_is2d = True
            else:
                out_is2d = True

            if out_is2d:
                return (shape[0]*us[0], shape[1]*us[1])
            else:
                return (shape[0]*us[0], shape[1]*us[1], us[2])

    def _mosaic(self, shape, idx=None, out=None, order='R'):
        """ Mosaic super method """

        if self._data:
            if not len(shape) == 2:
                raise ValueError('Shape must be a tuple/list with 2 entries (Y, X)')

            if _np.prod(shape) < self.size:
                raise ValueError('The total number of subimages (shape) need be >= number of components ({})'.format(self.size))

            sr = 1*self.parameters['StartR']
            sc = 1*self.parameters['StartC']
            er = 1*self.parameters['EndR']
            ec = 1*self.parameters['EndC']
            if sr == 0:
                sr = None
            if sc == 0:
                sc = None
            if er == 0:
                er = None
            if ec == 0:
                ec = None

            # Slice to take on each sub-image
            slice_sub_r = slice(sr, er, 1)
            slice_sub_c = slice(sc, ec, 1)

            if self.parameters['FlipVertical']:
                slice_sub_r = slice(slice_sub_r.stop, slice_sub_r.start, -1*slice_sub_r.step)

            if self.parameters['FlipHorizontally']:
                slice_sub_c = slice(slice_sub_c.stop, slice_sub_c.start, -1*slice_sub_c.step)

            us = list(self.unitshape)

            if self.parameters['Transpose']:
                temp = 1*us[0]
                us[0] = us[1]
                us[1] = temp


            in_is2d = self.is2d
            if (len(us) == 3):
                if idx is None:
                    out_is2d = False
                else:
                    out_is2d = True
            else:
                out_is2d = True


            out_provided = None
            if out is None:
                if out_is2d:
                    out = _np.zeros((shape[0]*us[0], shape[1]*us[1]), dtype=self.dtype)
                else:
                    out = _np.zeros((shape[0]*us[0], shape[1]*us[1], us[2]), dtype=self.dtype)
                out_provided = False
            else:
                out_provided = True

            sub_img_counter = 0
            num_components = self.size

            if order == 'C':
                sh_outter = shape[0]
                sh_inner = shape[1]
            else:  # Order == 'R'
                sh_outter = shape[1]
                sh_inner = shape[0]

            for num_outter in range(sh_outter):
                for num_inner in range(sh_inner):
                    if order == 'C':
                        numR = num_outter
                        numC = num_inner
                    else:  # Order == 'R'
                        numC = num_outter
                        numR = num_inner

                    if sub_img_counter < num_components:
                        data = self._data[sub_img_counter]
                        if idx is not None:
                            data = data[..., idx]
                        if self.parameters['Transpose']:
                            if in_is2d:
                                data = data.T
                            else:
                                data = _np.transpose(data, axes=(1,0,2))
                        out[(numR*us[0]):(numR+1)*us[0],
                                (numC*us[1]):(numC+1)*us[1]] = 1*data[slice_sub_r, slice_sub_c]
                        sub_img_counter += 1

            if not out_provided:
                return out

    def mosaic2d(self, shape, idx=None, out=None, order='R'):
        """ Return 2D mosaic image"""

        if self._data:
            if (self.is3d & (idx is None)):
                raise ValueError('With 3D components, idx must be provided')

            return self._mosaic(shape=shape, idx=idx, out=out, order=order)

    def mosaicfull(self, shape, out=None, order='R'):
        """ Return full mosaic """

        if self._data:
            return self._mosaic(shape=shape, idx=None, out=out, order=order)

if __name__ == '__main__':
    orig_data = _np.random.randn(40,5)
    
    mos = Mosaic()

    m_unit_size = 10
    n_unit_size = 5

    m_ct = orig_data.shape[0]//m_unit_size
    n_ct = orig_data.shape[1]//n_unit_size

    for ct in range(m_ct):
        mos.append(orig_data[ct*m_unit_size:(ct+1)*m_unit_size,:])

    assert _np.allclose(mos.mosaic2d(shape=(m_ct, n_ct), order='R'), orig_data)