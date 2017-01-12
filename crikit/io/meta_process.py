# -*- coding: utf-8 -*-
"""
Created on Mon May 23 16:55:09 2016

@author: chc
"""

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

from crikit.data.frequency import (calib_pix_wn as _calib_pix_wn,
                                   calib_pix_wl as _calib_pix_wl)

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

import numpy as _np

def rosetta_query(key, rosetta, output_cls_instance):
    """
    Return the highest-priority value
    """

    if isinstance(rosetta[key],list):  # There is a priority list
        for num, count in enumerate(rosetta[key]):
            temp_val = None
            temp_key = None

            try:
                if isinstance(count,str):
                    if count == '!':
                        temp_key = key
                        temp_val = rosetta[key][num+1]
                        break
                    else:
                        temp_key = count
                        temp_val = output_cls_instance._meta[temp_key]
                        break
#                        print('{}:{}'.format(count, temp_val))
                else:
                    pass
            except:
                temp_val = None
                temp_key = None

        if temp_val is not None:
            return(temp_val, temp_key)
        else:
            return None

    elif isinstance(rosetta[key],str):
        try:
            temp = output_cls_instance._meta[rosetta[key]]
        except:
            return None
        else:
            return (temp, rosetta[key])
    else:  # the value is likely a predefined answer-- no need to query meta
        return None

def meta_process(rosetta, output_cls_instance):
    """
    Uses a conversion dict (rosetta) to process the meta data in \
    output_cls_instance
    """

    # Frequency-calibration
    try:
        calib_dict = {}

        calib_dict['a_vec'] = rosetta_query('ColorPolyVals',rosetta, output_cls_instance)[0]
        calib_dict['n_pix'] = rosetta_query('ColorChannels',rosetta, output_cls_instance)[0]
        calib_dict['ctr_wl'] = rosetta_query('ColorCenterWL',rosetta, output_cls_instance)[0]
        calib_dict['ctr_wl0'] = rosetta_query('ColorCalibWL',rosetta, output_cls_instance)[0]
        calib_dict['probe'] = rosetta_query('ColorProbe',rosetta, output_cls_instance)[0]
        calib_dict['units'] = rosetta_query('ColorUnits',rosetta, output_cls_instance)[0]

        output_cls_instance.freq.calib = calib_dict

        use_wn = rosetta_query('ColorWnMode',rosetta, output_cls_instance)[0]
        print('Use wavenumber: {}'.format(use_wn))
        if use_wn:  # Use wavenumber?
            output_cls_instance.freq.calib_fcn = _calib_pix_wn
        else:  # Use wavelength
            output_cls_instance.freq.calib_fcn = _calib_pix_wl

        output_cls_instance.freq.update()
    except:
        print('Something failed in meta_process: freq-calib')

    # See if an original calibration is found
    try:
        calib_orig_dict = {}

        calib_orig_dict['a_vec'] = rosetta_query('OrigColorPolyVals',rosetta, output_cls_instance)[0]
        if calib_orig_dict['a_vec'] is None:
            raise ValueError
        calib_orig_dict['n_pix'] = rosetta_query('OrigColorChannels',rosetta, output_cls_instance)[0]
        if calib_orig_dict['n_pix'] is None:
            raise ValueError
        calib_orig_dict['ctr_wl'] = rosetta_query('OrigColorCenterWL',rosetta, output_cls_instance)[0]
        if calib_orig_dict['ctr_wl'] is None:
            raise ValueError
        calib_orig_dict['ctr_wl0'] = rosetta_query('OrigColorCalibWL',rosetta, output_cls_instance)[0]
        if calib_orig_dict['ctr_wl0'] is None:
            raise ValueError
        
        # Probe and Units are not necessary for calibration
        # Probe is only needed for wavelength-to-wavenumber conversion
        calib_orig_dict['probe'] = rosetta_query('OrigColorProbe',rosetta, output_cls_instance)[0]
        calib_orig_dict['units'] = rosetta_query('OrigColorUnits',rosetta, output_cls_instance)[0]

    except:
        print('Original calibration not found.')
    else:
        print('Original calibration found.')
        output_cls_instance.freq.calib_orig = calib_orig_dict
    
    # Spatial for HSI
    if type(output_cls_instance) == _Hsi:
        print('Type Hsi')
        try:
            start = rosetta_query('XStart',rosetta, output_cls_instance)[0]
            stop = rosetta_query('XStop',rosetta, output_cls_instance)[0]
            steps = rosetta_query('XLength',rosetta, output_cls_instance)[0]
            units = rosetta_query('XUnits',rosetta, output_cls_instance)[0]

            output_cls_instance.x_rep.data = _np.linspace(start, stop, steps)
            output_cls_instance.x_rep.units = units
            output_cls_instance.x_rep.update_calib_from_data()

            del start, stop, steps, units

            start = rosetta_query('YStart',rosetta, output_cls_instance)[0]
            stop = rosetta_query('YStop',rosetta, output_cls_instance)[0]
            steps = rosetta_query('YLength',rosetta, output_cls_instance)[0]
            units = rosetta_query('YUnits',rosetta, output_cls_instance)[0]

            output_cls_instance.y_rep.data = _np.linspace(start, stop, steps)
            output_cls_instance.y_rep.units = units
            output_cls_instance.y_rep.update_calib_from_data()

            del start, stop, steps, units
        except:
            print('Something failed in meta_process: HSI-spatial calib')

    elif type(output_cls_instance) == _Spectra:
        try:
            print('Type Spectra')
            output_cls_instance.reps.units = 'acq number'
            output_cls_instance.reps.data = _np.arange(output_cls_instance.data.shape[0])
    #        print(output_cls_instance.reps.data.shape)
            output_cls_instance.reps.update_calib_from_data()
        except:
            print('Something failed in meta_process: Spectra rep-calib')

    elif type(output_cls_instance) == _Spectrum:
        print('Type Spectrum')

if __name__ == '__main__':

    from crikit.io.meta_configs import (special_nist_bcars2
                                            as _snb)

    from crikit.io.hdf5 import hdf_import_data as _hdf_import_data
    rosetta = _snb()

    filename = _os.path.abspath('../../../mP2_w_small.h5')

    spect_dark = _Spectra()
    _hdf_import_data(filename,'/Spectra/Dark_3_5ms_2',spect_dark)
    meta_process(rosetta, spect_dark)
    print(spect_dark.reps)

    print('')
    img = _Hsi()
    _hdf_import_data(filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    meta_process(rosetta, img)
    print(img.freq.__dict__)


