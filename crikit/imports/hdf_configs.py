# -*- coding: utf-8 -*-
"""
Configuration settings for HDF imports

Created on Mon May 23 10:35:19 2016

@author: chc
"""

def special_nist_bcars2_import_attr():
    """
    Return import attributes particular to the "BCARS 2" system at NIST
    """
    import_attr = {}

    import_attr['XPixelSize'] = 'RasterScanParams.FastAxisStepSize'
    import_attr['XStart'] = 'RasterScanParams.FastAxisStart'
    import_attr['XStop'] = 'RasterScanParams.FastAxisStop'
    import_attr['XLength'] = 'RasterScanParams.FastAxisSteps'
    import_attr['XLabel'] = 'RasterScanParams.FastAxis'

    import_attr['YPixelSize'] = 'RasterScanParams.SlowAxisStepSize'
    import_attr['YStart'] = 'RasterScanParams.SlowAxisStart'
    import_attr['YStop'] = 'RasterScanParams.SlowAxisStop'
    import_attr['YSize'] = 'RasterScanParams.SlowAxisSteps'
    import_attr['YLabel'] = 'RasterScanParams.SlowAxis'

    import_attr['XPosition'] = 'RasterScanParams.FixedAxisPosition'
    import_attr['XLabel'] = 'RasterScanParams.FixedAxis'

    import_attr['ColorCenterWL'] = 'Spectro.CenterWavelength'
    import_attr['ColorUnits'] = 'nm'
    import_attr['ColorChannels'] = 1600
    import_attr['ColorCalibWL'] = 730
    import_attr['ColorSlope'] = -0.167740721307557
    import_attr['ColorIntercept'] = -0.167740721307557
    import_attr['ColorProbe'] = 771.461
    import_attr['ColorWavenumberMode'] = True

    return import_attr