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

    # Frequency-related
    calib_dict = {}
    calibrated = rosetta_query('ColorCalibWN',rosetta, output_cls_instance)

    if calibrated is not None:  # Contains a calibration in the meta
        print('Using calibration from {}'.format(calibrated[1]))
        
        if isinstance(calibrated[0], _np.ndarray):  # Calib vec style
            calib_vec = calibrated[0]
            calib_dict = {}
            calib_dict['n_pix'] = calib_vec[0]
            calib_dict['ctr_wl'] = calib_vec[1]
            calib_dict['ctr_wl0'] = calib_vec[2]
            calib_dict['probe'] = calib_vec[5]
            calib_dict['a_vec'] = [calib_vec[3], calib_vec[4]]
            
            output_cls_instance.freq.calib_fcn = _calib_pix_wn
            output_cls_instance.freq.calib = calib_dict
            output_cls_instance.freq.update()

    else:
        temp = rosetta_query('ColorChannels',rosetta, output_cls_instance)
        print('Color channels: {}'.format(temp))
        calib_dict['n_pix'] = temp[0]
        del temp

        temp = rosetta_query('ColorCenterWL',rosetta, output_cls_instance)
        print('Center wavelength: {}'.format(temp))
        calib_dict['ctr_wl'] = temp[0]
        del temp

        temp = rosetta_query('ColorCalibWL',rosetta, output_cls_instance)
        print('Center wavelength calibrated for: {}'.format(temp))
        calib_dict['ctr_wl0'] = temp[0]
        del temp

        temp1 = rosetta_query('ColorSlope',rosetta, output_cls_instance)
        temp2 = rosetta_query('ColorIntercept',rosetta, output_cls_instance)
        calib_dict['a_vec'] = (temp1[0], temp2[0])

        print('Slope: {}'.format(temp1))
        print('Intercept: {}'.format(temp2))
        del temp1, temp2


        temp = rosetta_query('ColorProbe',rosetta, output_cls_instance)
        print('Probe wavelength: {}'.format(temp))
        calib_dict['probe'] = temp[0]
        del temp

        temp = rosetta_query('ColorUnits',rosetta, output_cls_instance)
        print('Color units: {}'.format(temp))
        calib_dict['units'] = temp[0]
        del temp

        output_cls_instance.freq.calib = calib_dict

        temp = rosetta_query('ColorWnMode',rosetta, output_cls_instance)
        print('Use wavenumber: {}'.format(temp[0]))
        if temp:  # Use wavenumber?
            output_cls_instance.freq.calib_fcn = _calib_pix_wn
        else:  # Use wavelength
            output_cls_instance.freq.calib_fcn = _calib_pix_wl
        del temp

        output_cls_instance.freq.update()


    if type(output_cls_instance) == _Hsi:
        print('Type Hsi')
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

    elif type(output_cls_instance) == _Spectra:
        print('Type Spectra')
        output_cls_instance.reps.units = 'acq number'
        output_cls_instance.reps.data = _np.arange(output_cls_instance.data.shape[0])
#        print(output_cls_instance.reps.data.shape)
        output_cls_instance.reps.update_calib_from_data()

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


