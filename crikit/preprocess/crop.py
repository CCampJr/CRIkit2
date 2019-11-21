"""
Created on Tue Jun 21 14:28:49 2016

@author: chc
"""

import numpy as _np
import copy as _copy


class ZeroColumn:
    """
    Set first or last column that is not all 0's to 0.

    Parameters
    ----------
    first_or_last : int, optional (default = 0 [first])
        Find first (= 0) or last (= -1)

    zero_col : int, optional (default = None)
        Zero a specified column
    """
    def __init__(self, first_or_last=0, zero_col=None):
        self.zero_col = zero_col
        self.fol = first_or_last

    def _calc(self, data, ret_obj):
        assert data.ndim == 3
        try:
            if self.zero_col is None:
                row_sums = data.sum(axis=(0, -1))
                self.zero_col = _np.nonzero(row_sums)[0][self.fol]

            ret_obj[:, self.zero_col, :] *= 0
        except:
            return False
        else:
            return True

    def transform(self, data):
        success = self._calc(data, ret_obj=data)
        return success

    def calculate(self, data):
        data_copy = _copy.deepcopy(data)
        success = self._calc(data, ret_obj=data_copy)
        if success:
            return data_copy
        else:
            return None


class ZeroRow:
    """
    Set first or last row that is not all 0's to 0.

    Parameters
    ----------
    first_or_last : int, optional (default = 0 [first])
        Find first (= 0) or last (= -1)

    zero_row : int, optional (default = None)
        Zero a specified row
    """
    def __init__(self, first_or_last=0, zero_row=None):
        self.zero_row = zero_row
        self.fol = first_or_last

    def _calc(self, data, ret_obj):
        assert data.ndim == 3
        try:
            if self.zero_row is None:
                col_sums = data.sum(axis=(1, -1))
                self.zero_row = _np.nonzero(col_sums)[0][self.fol]

            ret_obj[self.zero_row, :, :] *= 0
        except:
            return False
        else:
            return True

    def transform(self, data):
        success = self._calc(data, ret_obj=data)
        return success

    def calculate(self, data):
        data_copy = _copy.deepcopy(data)
        success = self._calc(data, ret_obj=data_copy)
        if success:
            return data_copy
        else:
            return None

class CutEveryNSpectra:
    """
    Cut m spectra between every n spectra

    Parameters
    ----------
    offset : int, option (default = 0)
        Start the process at the offset-th position

    cut_m : int, optional (default = 1)
        Cut m spectra at a time

    every_n : int, optional (default = 100)
        Spacing between cuts
    
    action : str
        Whether to 'cut', use the 'mean' of the remaining, replace with the spectrum 'before' or 'after'

    Returns
    -------
        ndarray

    Note
    -----
    Currently, this class performs the action on a copy of the data, returning a copy

    """
    def __init__(self, offset=0, cut_m=1, every_n=100, action='cut'):
        self.offset = offset
        self.cut_m = cut_m
        self.every_n = every_n
        self.action = action.lower()

    def _calc(self, data, ret_obj):
        assert data.ndim == 2
        try:
            pix_to_affect = _np.array([_np.arange(r, r + self.cut_m) for r in _np.arange(start=self.offset, stop=data.shape[0], step=self.every_n)]).ravel()
            pix_to_stay = _np.array(list(set(_np.arange(data.shape[0])) - set(pix_to_affect)))
            if self.action == 'mean':
                meaner = data[pix_to_stay, :].mean(axis=0)
                ret_obj[pix_to_stay, :] = data[pix_to_stay,:]
                ret_obj[pix_to_affect, :] = data[pix_to_stay,:].mean(keepdims=True)
            elif self.action == 'cut':
                ret_obj[...] = data[pix_to_stay, :]
            elif self.action == 'before':
                ret_obj[pix_to_stay, :] = data[pix_to_stay,:]
                new_pix = _np.array([r - 1 for r in pix_to_affect])
                ret_obj[pix_to_affect, :] = data[new_pix,:]
            elif self.action == 'after':
                ret_obj[pix_to_stay, :] = data[pix_to_stay,:]
                # The modulus is so if the +1 the last pix is selected
                # it goes back to the first pix
                new_pix = _np.array([r + 1 for r in pix_to_affect]) % data.shape[0]
                ret_obj[pix_to_affect, :] = data[new_pix,:]
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def transform(self, data):
        raise NotImplementedError('Currently, this class can only return a copy of the data.')

    def calculate(self, data):
        if self.action != 'cut':
            data_copy = _copy.deepcopy(data)
        else:
            n_pix_to_affect = _np.array([_np.arange(r, r + self.cut_m) for r in _np.arange(start=self.offset, stop=data.shape[0], step=self.every_n)]).ravel().size
            data_copy = 0*data[n_pix_to_affect:,:]
        success = self._calc(data, ret_obj=data_copy)
        if success:
            return data_copy
        else:
            return None


if __name__ == '__main__':


    # temp = _np.random.rand(3,4,5)
    # z = ZeroColumn(first_or_last=0)
    # z.transform(temp)
    # print('Zero First Column')
    # print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    # print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))

    # temp = _np.random.rand(3,4,5)
    # z = ZeroRow(first_or_last=0)
    # z.transform(temp)
    # print('\n\nZero First Row')
    # print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    # print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))

    # temp = _np.random.rand(3,4,5)
    # z = ZeroColumn(first_or_last=-1)
    # z.transform(temp)
    # print('\n\nZero Last Column')
    # print('Is last column sum-0?: {}'.format(temp.sum(axis=(0,-1))[-1] == 0))
    # print('Is last row sum-0?: {}'.format(temp.sum(axis=(1,-1))[-1] == 0))

    # temp = _np.random.rand(3,4,5)
    # z = ZeroRow(first_or_last=-1)
    # z.transform(temp)
    # print('\n\nZero First Row')
    # print('Is last column sum-0?: {}'.format(temp.sum(axis=(0,-1))[-1] == 0))
    # print('Is last row sum-0?: {}'.format(temp.sum(axis=(1,-1))[-1] == 0))

    temp = _np.array([1, 1, 0, 0, 1, 1, 0, 0])
    temp =  _np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=2, every_n=4, action='cut')
    assert c.calculate(temp).sum() == 0
    
    c = CutEveryNSpectra(offset=2, cut_m=2, every_n=4, action='cut')
    assert c.calculate(temp).mean() == 1

    temp = _np.array([0, 1, 2, 0, 1, 2])
    temp =  _np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=1, every_n=3, action='before')
    assert c.calculate(temp).mean() == 10/6

    temp = _np.array([0, 1, 2, 0, 1, 2])
    temp =  _np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=1, every_n=3, action='after')
    assert c.calculate(temp).mean() == 8/6

