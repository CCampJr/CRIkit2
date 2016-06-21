# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 14:28:49 2016

@author: chc
"""

import numpy as _np
import copy as _copy


class ZeroColumn:
    """
    Set first column that is not all 0's to 0.
    """
    def __init__(self, first_non_zero_col=None):
        self.first_non_zero_col = first_non_zero_col

    def _calc(self, data, ret_obj):
        assert data.ndim == 3
        try:
            if self.first_non_zero_col is None:
                row_sums = data.sum(axis=(0, -1))
                self.first_non_zero_col = _np.nonzero(row_sums)[0][0]

            ret_obj[:, self.first_non_zero_col, :] *= 0
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
    Set first row that is not all 0's to 0.
    """
    def __init__(self, first_non_zero_row=None):
        self.first_non_zero_row = first_non_zero_row

    def _calc(self, data, ret_obj):
        assert data.ndim == 3
        try:
            if self.first_non_zero_row is None:
                col_sums = data.sum(axis=(1, -1))
                self.first_non_zero_row = _np.nonzero(col_sums)[0][0]

            ret_obj[self.first_non_zero_row, :, :] *= 0
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
    z = ZeroColumn()
    z.transform(temp)
    print('Zero First Column')
    print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))

    temp = _np.random.rand(3,4,5)
    z = ZeroRow()
    z.transform(temp)
    print('\n\nZero First Row')
    print('Is first column sum-0?: {}'.format(temp.sum(axis=(0,-1))[0] == 0))
    print('Is first row sum-0?: {}'.format(temp.sum(axis=(1,-1))[0] == 0))