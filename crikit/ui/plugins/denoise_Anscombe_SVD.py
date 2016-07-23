# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 15:27:50 2016

@author: chc
"""

from crikit.ui.helper_plugin_categories import DeNoiser
import crikit.ui.subui_SVD
from crikit.process.varstabilize import gen_anscombe_forward
from crikit.process.varstabilize import gen_anscombe_inverse_exact_unbiased

from crikit.ui.dialog_options import DialogAnscombeOptions

import copy as _copy

class DeNoiseSVD(DeNoiser):
    name = 'Anscombe SVD'

    def denoiseHSData(self, hsdatacls):
        data = _copy.deepcopy(hsdatacls.spectra)
        result = DialogAnscombeOptions.dialogAnscombeOptions()
        if result[0] is not None:
            stddev = result[0]
            gain = result[1]
            data = gen_anscombe_forward(data, gauss_std=stddev, poisson_multi=gain)
            ret = crikit.ui.subui_SVD.DialogSVD.dialogSVD(data=data)
            if ret is None:
                return None
            else:
                data = gen_anscombe_inverse_exact_unbiased(ret[0], gauss_std=stddev, poisson_multi=gain)
                hsdatacls.spectra = data
                ret[1][0] = 'AnscSVD'
                return ret[1]
        else:
            return None


