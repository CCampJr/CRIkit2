# -*- coding: utf-8 -*-
"""
Configuration settings for HDF imports

Use '!' as the first entry in a list to denote to use the value rather \
than querying for it

Created on Mon May 23 10:35:19 2016

@author: chc
"""

def special_nist_bcars2():
    """
    Return import attributes particular to the "BCARS 2" system at NIST
    """
    rosetta = {}

    rosetta['XPixelSize'] = 'RasterScanParams.FastAxisStepSize'
    rosetta['XStart'] = 'RasterScanParams.FastAxisStart'
    rosetta['XStop'] = 'RasterScanParams.FastAxisStop'
    rosetta['XLength'] = 'RasterScanParams.FastAxisSteps'
    rosetta['XLabel'] = 'RasterScanParams.FastAxis'
    rosetta['XUnits'] = ['RasterScanParams.FastAxisUnits','!','$\mu m$']

    rosetta['YPixelSize'] = 'RasterScanParams.SlowAxisStepSize'
    rosetta['YStart'] = 'RasterScanParams.SlowAxisStart'
    rosetta['YStop'] = 'RasterScanParams.SlowAxisStop'
    rosetta['YLength'] = 'RasterScanParams.SlowAxisSteps'
    rosetta['YLabel'] = 'RasterScanParams.SlowAxis'
    rosetta['YUnits'] = ['RasterScanParams.SlowAxisUnits','!','$\mu m$']

    rosetta['ZPosition'] = 'RasterScanParams.FixedAxisPosition'
    rosetta['ZLabel'] = 'RasterScanParams.FixedAxis'

    rosetta['ColorCenterWL'] = ['Spectro.CenterWavelength','!',730.0]
    rosetta['ColorUnits'] = ['!','nm']
    rosetta['ColorChannels'] = ['!', 1600]
    rosetta['ColorCalibWL'] = ['!', 730.0]
    rosetta['ColorSlope'] = ['!', -0.167740721307557]
    rosetta['ColorIntercept'] = ['!', 863.8736708961577]
    rosetta['ColorProbe'] = ['!', 771.461]
    rosetta['ColorWnMode'] = ['!', True]
    rosetta['ColorCalibWN'] = ['Processing.WNCalib','Processing.WNCalibOrig']

    return rosetta
    
def special_nist_bcars1_sample_scan():
    """
    Return import attributes particular to the "BCARS 1" system at NIST
    """
    rosetta = {}

    rosetta['XPixelSize'] = 'X scan Parameters.x step size (um)'
    rosetta['XStart'] = 'X scan Parameters.x start (um)'
    rosetta['XStop'] = 'RasterScanParams.FastAxisStop'
    rosetta['XLength'] = 'X scan Parameters.x steps'
    rosetta['XLabel'] = 'RasterScanParams.FastAxis'
    rosetta['XUnits'] = ['RasterScanParams.FastAxisUnits', '!', '$\mu m$']

    rosetta['YPixelSize'] = 'Y scan Paramters.y step size (um)'
    rosetta['YStart'] = 'Y scan Paramters.y start (um)'
    rosetta['YStop'] = 'RasterScanParams.SlowAxisStop'
    rosetta['YLength'] = 'Y scan Paramters.y steps'
    rosetta['YLabel'] = 'RasterScanParams.SlowAxis'
    rosetta['YUnits'] = ['RasterScanParams.SlowAxisUnits', '!', '$\mu m$']

    rosetta['ZPosition'] = 'Z scan parameters.z start (um)'
    rosetta['ZLabel'] = 'RasterScanParams.FixedAxis'

    rosetta['ColorCenterWL'] = ['Frequency Calibration.CenterWavelength','!',696.831]
    rosetta['ColorUnits'] = ['!','nm']
    rosetta['ColorChannels'] = ['Frequency Calibration.freq index length','!',512]
    rosetta['ColorCalibWL'] = ['Frequency Calibration.CenterWavelength','!',696.831]
    rosetta['ColorSlope'] = ['Frequency Calibration.Slope','!', -0.50418919]
    rosetta['ColorIntercept'] = ['Frequency Calibration.Intercept','!', 825.651318]
    rosetta['ColorProbe'] = ['Frequency Calibration.probe(nm)','!', 830.0]
    rosetta['ColorWnMode'] = ['!', True]
    rosetta['ColorCalibWN'] = ['Processing.WNCalib','Processing.WNCalibOrig']

    return rosetta