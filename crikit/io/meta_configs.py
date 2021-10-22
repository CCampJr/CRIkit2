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

    rosetta['XPixelSize'] = ['RasterScanParams.FastAxisStepSize', 
                             'Raster.Fast.StepSize','!',1]
    rosetta['XStart'] = ['RasterScanParams.FastAxisStart', 'Raster.Fast.Start']
    rosetta['XStop'] = ['RasterScanParams.FastAxisStop', 'Raster.Fast.Stop']
    rosetta['XLength'] = ['RasterScanParams.FastAxisSteps', 'Raster.Fast.Steps']
    rosetta['XLabel'] = ['RasterScanParams.FastAxis','Raster.Fast.Axis','!','X']
    rosetta['XUnits'] = ['RasterScanParams.FastAxisUnits','!','$\\mu$m']

    rosetta['YPixelSize'] = ['RasterScanParams.SlowAxisStepSize', 
                            'Raster.Slow.StepSize','!',1]
    rosetta['YStart'] = ['RasterScanParams.SlowAxisStart', 'Raster.Slow.Start']
    rosetta['YStop'] = ['RasterScanParams.SlowAxisStop', 'Raster.Slow.Stop']
    rosetta['YLength'] = ['RasterScanParams.SlowAxisSteps', 'Raster.Slow.Steps']
    rosetta['YLabel'] = ['RasterScanParams.SlowAxis','Raster.Slow.Axis','!','Y']
    rosetta['YUnits'] = ['RasterScanParams.SlowAxisUnits','!','$\\mu$m']

    rosetta['ZPosition'] = ['RasterScanParams.FixedAxisPosition', 
                            'Raster.Stack.Position','!',0]
    rosetta['ZLabel'] = ['RasterScanParams.FixedAxis', 'Raster.Stack.Axis','!','Z']

    # Color Calibration
    rosetta['ColorCenterWL'] = ['Spectro.CenterWavelength', 
                                'Spectro.CurrentWavelength', 'Calib.ctr_wl',
                                '!', 729.994]
    rosetta['ColorUnits'] = ['Calib.units', '!', 'nm']
    rosetta['ColorChannels'] = ['Calib.n_pix', 'Spectro.SpectralPixels','!', 1600]
    rosetta['ColorCalibWL'] = ['Calib.ctr_wl0', 'Spectro.CalibWavelength', '!', 729.994]
    rosetta['ColorPolyVals'] = ['Calib.a_vec', 'Spectro.Avec', '!', [-0.167740721307557,
                                                     863.8736708961577]]

    rosetta['ColorProbe'] = ['Calib.probe', 'Spectro.ProbeWavelength', '!', 771.461]
    rosetta['ColorWnMode'] = ['!', True]

    # Color Calibration Original
    rosetta['OrigColorCenterWL'] = ['CalibOrig.ctr_wl',
                                    'Spectro.CenterWavelength',
                                    'Spectro.CurrentWavelength',
                                   ]
    rosetta['OrigColorUnits'] = ['CalibOrig.units']
    rosetta['OrigColorChannels'] = ['CalibOrig.n_pix']
    rosetta['OrigColorCalibWL'] = ['CalibOrig.ctr_wl']

    rosetta['OrigColorPolyVals'] = ['CalibOrig.a_vec']

    rosetta['OrigColorProbe'] = ['CalibOrig.probe']
    rosetta['OrigColorWnMode'] = ['!', True]

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

    rosetta['ColorCenterWL'] = ['Frequency Calibration.CenterWavelength', '!', 696.831]
    rosetta['ColorUnits'] = ['!','nm']
    rosetta['ColorChannels'] = ['Frequency Calibration.freq index length', '!', 512]
    rosetta['ColorCalibWL'] = ['Frequency Calibration.CenterWavelength', '!', 696.831]

    # Will become deprecated in favor of ColorPolyVals
    rosetta['ColorSlope'] = ['Frequency Calibration.Slope', '!', -0.50418919]
    rosetta['ColorIntercept'] = ['Frequency Calibration.Intercept', '!', 825.651318]

    rosetta['ColorPolyVals'] = ['Frequency Calibration.Polyvals', '!',
                                [-0.50418919, 825.651318]]

    rosetta['ColorProbe'] = ['Frequency Calibration.probe(nm)','!', 830.0]
    rosetta['ColorWnMode'] = ['!', True]
    # rosetta['ColorCalibWN'] = ['Processing.WNCalib','Processing.WNCalibOrig']

    return rosetta