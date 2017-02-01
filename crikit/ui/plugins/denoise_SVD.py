"""
Created on Tue Feb 16 17:23:25 2016

@author: camp
"""
from crikit.ui.helper_plugin_categories import DeNoiser
import crikit.ui.subui_SVD

class DeNoiseSVD(DeNoiser):
    name = 'SVD'

    def denoiseHSData(self, hsdatacls):
        ret = crikit.ui.subui_SVD.DialogSVD.dialogSVD(data=hsdatacls.spectra)
        if ret is None:
            return None
        else:
            hsdatacls.spectra = ret[0]
            return ret[1]

