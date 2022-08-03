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
        self.parameters['Order'] = 'R'
        self.parameters['Compress'] = False
        self.parameters['Shape'] = [1, 1]

    def __repr__(self):  # pragma: no cover
        if self._data:
            return 'Mosaic contains {} component(s)'.format(self.size)
        else:
            return 'Empty Collection'

    def attr_dict(self, prefix='Mosaic.'):
        temp = {}
        for k in self.parameters:
            temp.update({prefix+k:self.parameters[k]})
        return temp

    @property
    def shape(self):
        if self._data:
            return tuple([q.shape for q in self._data])

    @property
    def size(self):
        if isinstance(self._data, list):
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
                return complex
            elif dt.count('f') > 0:
                return float
            elif dt.count('i') > 0:
                return int


    def mosaic_shape(self, shape=None, idx=None):
        """ Return the shape of a would-be mosaic """
        if shape is None:
            shape = self.parameters['Shape']
        else:
            self.parameters['Shape'] = shape

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

    def _mosaic(self, shape=None, idx=None, out=None, mask=False):
        """ Mosaic super method """
        if shape is None:
            shape = self.parameters['Shape']
        else:
            self.parameters['Shape'] = shape

        compress = self.parameters['Compress']

        if self._data:
            if mask:
                idx = 0

            if not len(shape) == 2:
                raise ValueError('Shape must be a tuple/list with 2 entries (Y, X)')

            if _np.prod(shape) < self.size:
                raise ValueError('The total number of subimages (shape) need be >= number of components ({})'.format(self.size))

            if out is None:
                if not mask:
                    out = _np.zeros(self.mosaic_shape(shape=shape, idx=idx),
                                    dtype=self.dtype)
                else:
                    # For mask, start at -1
                    out = -1 + _np.zeros(self.mosaic_shape(shape=shape, idx=idx),
                                    dtype=self.dtype)
                out_provided = False
            else:
                out_provided = True

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

            sub_img_counter = 0
            num_components = self.size

            order = self.parameters['Order']

            if order == 'C':
                sh_outter = shape[0]
                sh_inner = shape[1]
            else:  # Order == 'R'
                sh_outter = shape[1]
                sh_inner = shape[0]

            # * h5 write_direct has strict limitations
            cannot_write_direct = (self.parameters['Transpose'] |
                                   self.parameters['FlipVertical'] |
                                   self.parameters['FlipHorizontally'])

            # * Only used by out matrix
            us = list(self.unitshape)
            if self.parameters['Transpose']:
                temp = 1*us[0]
                us[0] = us[1]
                us[1] = temp

            for num_outter in range(sh_outter):
                for num_inner in range(sh_inner):
                    if order == 'C':
                        numR = num_outter
                        numC = num_inner
                    else:  # Order == 'R'
                        numC = num_outter
                        numR = num_inner

                    if sub_img_counter < num_components:
                        if mask:
                            data = sub_img_counter * \
                                   _np.ones(self._data[sub_img_counter][slice_sub_r,
                                                                        slice_sub_c].shape[0:2],
                                           dtype=int)
                        elif idx is None:
                            data = self._data[sub_img_counter][slice_sub_r, slice_sub_c]
                        else:
                            data = self._data[sub_img_counter][slice_sub_r, slice_sub_c, idx]

                        data_is2d = (data.ndim == 2)

                        if self.parameters['FlipHorizontally']:
                            data = _np.flip(data, axis=1)
                        if self.parameters['FlipVertical']:
                            data = _np.flip(data, axis=0)
                        if self.parameters['Transpose']:
                            if data_is2d:
                                data = data.T
                            else:
                                data = _np.transpose(data, axes=(1,0,2))

                        # * Using this in case m/ndata is smaller than u[0/1]
                        mdata, ndata = data.shape[0], data.shape[1]

                        if isinstance(out, _h5py.Dataset) & (not cannot_write_direct):
                            out.write_direct(source=data,
                                             dest_sel=_np.s_[(numR*us[0]):(numR*us[0] + mdata),
                                                             (numC*us[1]):(numC*us[1] + ndata)])
                        else:   
                            out[(numR*us[0]):(numR*us[0] + mdata),
                                (numC*us[1]):(numC*us[1] + ndata)] = 1*data
                        sub_img_counter += 1

            if not out_provided:
                if not compress:
                    return out
                else:
                    if mask:  # Cute trick since first ROI is +0 and blank is -1
                        out += 1

                    if out.ndim == 3:
                        out = out[:, (out.sum(axis=0)[:, 0] != 0), :]
                        out = out[(out.sum(axis=1)[:, 0] != 0), :, :]

                    else:  # 2D
                        out = out[:, (out.sum(axis=0) != 0)]
                        out = out[(out.sum(axis=1) != 0), :]
                    if mask:  # Cute trick since first ROI is +0 and blank is -1
                        out -= 1
                    return out

    def mosaic2d(self, shape=None, idx=None, out=None):
        """ Return 2D mosaic image"""

        if self._data:
            if (self.is3d & (idx is None)):
                raise ValueError('With 3D components, idx must be provided')

            return self._mosaic(shape=shape, idx=idx, out=out)

    def mosaic_mask(self, shape=None, out=None):
        """ Returns a 2D mosaic image with integer values for which img is where """

        return self._mosaic(shape=shape, out=out, mask=True)

    def mosaicfull(self, shape=None, out=None):
        """ Return full mosaic """

        if self._data:
            return self._mosaic(shape=shape, idx=None, out=out)

if __name__ == '__main__':
    mos = Mosaic()
    mos.parameters['StartR'] = 1
    mos.parameters['EndR'] = -1
    mos.parameters['StartC'] = 1
    mos.parameters['EndC'] = -1
    mos.parameters['Transpose'] = True
    mos.parameters['FlipVertical'] = True
    mos.parameters['FlipHorizontally'] = True

    m_obj = 3
    n_obj = 4
    p_obj = 5

    # MANUALLY SET BASED ON PARAMS ABOVE
    m_obj_crop = m_obj - 2
    n_obj_crop = n_obj - 2
    p_obj_crop = p_obj

    new_obj = _np.ones((m_obj, n_obj, p_obj))
    m_side = 2
    n_side = 2

    n = m_side * n_side

    for ct in range(n):
        mos.append(new_obj)

    # NOT AFFECTED BY START* END*
    assert mos.shape == tuple(n*[new_obj.shape])
    assert mos.size == n
    assert mos.issamedim
    assert mos.dtype == float

    # AFFECTED BY START* END*
    assert mos.unitshape == (m_obj_crop, n_obj_crop, p_obj_crop)
    assert mos.unitshape_orig == (m_obj, n_obj, p_obj)

    mos.parameters['Order'] = 'R'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                                      n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side,
                                                                                       n_side))[:-1]
    mos.parameters['Order'] = 'C'
    assert mos.mosaic2d((m_side, n_side), idx=0).T.shape == (m_side * m_obj_crop,
                                                                      n_side * n_obj_crop)
    assert mos.mosaic2d((m_side, n_side), idx=0).shape == mos.mosaic_shape((m_side, n_side))[:-1]

    mos.parameters['Order'] = 'R'
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                 n_side * n_obj_crop, p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))

    mos.parameters['Order'] = 'C'
    assert mos.mosaicfull((m_side, n_side)).transpose(1,0,2).shape == (m_side * m_obj_crop,
                                                                       n_side * n_obj_crop,
                                                                       p_obj_crop)
    assert mos.mosaicfull((m_side, n_side)).shape == mos.mosaic_shape((m_side, n_side))