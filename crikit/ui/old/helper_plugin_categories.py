"""
Created on Tue Feb 16 16:07:39 2016

@author: camp
"""

class DeNoiser(object):
    """
    Plugins of this class denoise hyperspectral data (crikit.data.HSData)
    """
 
    name = 'Do Nothing'
 
    def denoiseHSData(self, hsdatacls):
        return 1

class ErrorCorrect(object):
    """
    Plugins of this class perform error correction (phase, baseline, etc) on
    hyperspectral data
    """
    
    name = 'Do Nothing'
    
    def errorCorrectHSData(self, hsdatacls):
        return 1