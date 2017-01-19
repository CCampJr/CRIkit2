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

if __name__ == '__main__':


    temp = _np.random.rand(3,4,5)
    z = ZeroColumn(first_or_last=0)
    z.transform(temp)
    print('Zero First Column')
    print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))

    temp = _np.random.rand(3,4,5)
    z = ZeroRow(first_or_last=0)
    z.transform(temp)
    print('\n\nZero First Row')
    print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))

    temp = _np.random.rand(3,4,5)
    z = ZeroColumn(first_or_last=-1)
    z.transform(temp)
    print('\n\nZero Last Column')
    print('Is last column sum-0?: {}'.format(temp.sum(axis=(0,-1))[-1] == 0))
    print('Is last row sum-0?: {}'.format(temp.sum(axis=(1,-1))[-1] == 0))

    temp = _np.random.rand(3,4,5)
    z = ZeroRow(first_or_last=-1)
    z.transform(temp)
    print('\n\nZero First Row')
    print('Is last column sum-0?: {}'.format(temp.sum(axis=(0,-1))[-1] == 0))
    print('Is last row sum-0?: {}'.format(temp.sum(axis=(1,-1))[-1] == 0))