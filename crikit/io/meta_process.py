"""
Created on Mon May 23 16:55:09 2016

@author: chc
"""

from crikit.data.frequency import (calib_pix_wn as _calib_pix_wn,
                                   calib_pix_wl as _calib_pix_wl)

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

import numpy as _np

import traceback as _traceback

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
                        print('Using default meta_configs value for: {}'.format(key))
                        break
                    else:
                        temp_key = count
                        temp_val = output_cls_instance._meta[temp_key]
                        break
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
    calib_dict = {}

    print('Processing Meta Data\n------------------------------')
    temp = rosetta_query('ColorPolyVals',rosetta, output_cls_instance)
    print('{} from {}'.format(temp[0], temp[1]))
    calib_dict['a_vec'] = temp[0]
    del temp

    temp = rosetta_query('ColorChannels',rosetta, output_cls_instance)
    print('Color/Frequency-Channels: {} from {}'.format(temp[0], temp[1]))
    if temp[0] != output_cls_instance.shape[-1]:
        print('WARNING: Number of color channels assigned in meta data ({}) disagrees with datacube size ({})'.format(temp[0], output_cls_instance.shape[-1]))
        print('Setting to match dataset size...')
        calib_dict['n_pix'] = output_cls_instance.shape[-1]
    else:
        calib_dict['n_pix'] = temp[0]
    del temp


    temp = rosetta_query('ColorCenterWL',rosetta, output_cls_instance)
    print('{} from {}'.format(temp[0], temp[1]))
    calib_dict['ctr_wl'] = temp[0]
    del temp

    temp = rosetta_query('ColorCalibWL',rosetta, output_cls_instance)
    print('{} from {}'.format(temp[0], temp[1]))
    calib_dict['ctr_wl0'] = temp[0]
    del temp

    temp = rosetta_query('ColorProbe',rosetta, output_cls_instance)
    print('{} from {}'.format(temp[0], temp[1]))
    calib_dict['probe'] = temp[0]
    del temp

    temp = rosetta_query('ColorUnits',rosetta, output_cls_instance)
    print('{} from {}'.format(temp[0], temp[1]))
    calib_dict['units'] = temp[0]
    del temp

    output_cls_instance.freq.calib = calib_dict

    use_wn = rosetta_query('ColorWnMode',rosetta, output_cls_instance)[0]
    print('Use wavenumber: {}'.format(use_wn))
    if use_wn:  # Use wavenumber?
        output_cls_instance.freq.calib_fcn = _calib_pix_wn
    else:  # Use wavelength
        output_cls_instance.freq.calib_fcn = _calib_pix_wl

    output_cls_instance.freq.update()

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
            units = rosetta_query('XUnits',rosetta, output_cls_instance)
            label = rosetta_query('XLabel',rosetta, output_cls_instance)
            if units is not None:
                units = units[0]
            if label is not None:
                label = label[0]

            start = rosetta_query('XStart',rosetta, output_cls_instance)
            stop = rosetta_query('XStop',rosetta, output_cls_instance)
            steps = rosetta_query('XLength',rosetta, output_cls_instance)
            if (start is not None) & (stop is not None) & (steps is not None):
                start = start[0]
                stop = stop[0]
                steps = steps[0]
            else:
                temp = output_cls_instance.shape
                start = 0
                stop = temp[1] - 1
                steps = temp[1]
                units = 'pix'
                label = 'X'

            # HDF files store strings in np.bytes format
            if isinstance(units, bytes):
                units = units.decode()
            if isinstance(label, bytes):
                label = label.decode()

            if steps != output_cls_instance.shape[1]:
                print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
                print('WARNING: {}Steps assigned in meta data ({}) disagrees with datacube size ({})'.format(label, steps, output_cls_instance.shape[1]))
                print('Setting steps to match data...')
                steps = output_cls_instance.shape[1]

            if (start == stop) & (steps > 1):
                print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
                print('WARNING: XStart and XStop are the same, which causes plotting problems. Switching to pixel-units based on dataset shape')
                start = 0
                stop = output_cls_instance.shape[1]-1
                units = 'pix'

            print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
            # print('Start: {}, Stop: {}, Steps: {}'.format(start, stop, steps))
            output_cls_instance.x_rep.data = _np.squeeze(_np.linspace(start, stop, steps))
            output_cls_instance.x_rep.units = units
            output_cls_instance.x_rep.label = label
            output_cls_instance.x_rep.update_calib_from_data()

            del start, stop, steps, units, label

            units = rosetta_query('YUnits',rosetta, output_cls_instance)
            label = rosetta_query('YLabel',rosetta, output_cls_instance)
            if units is not None:
                units = units[0]
            if label is not None:
                label = label[0]

            start = rosetta_query('YStart',rosetta, output_cls_instance)
            stop = rosetta_query('YStop',rosetta, output_cls_instance)
            steps = rosetta_query('YLength',rosetta, output_cls_instance)
            if (start is not None) & (stop is not None) & (steps is not None):
                start = start[0]
                stop = stop[0]
                steps = steps[0]
            else:
                temp = output_cls_instance.shape
                start = 0
                stop = temp[0] - 1
                steps = temp[0]
                units = 'pix'
                label = 'Y'

            # HDF files store strings in np.bytes format
            if isinstance(units, bytes):
                units = units.decode()
            if isinstance(label, bytes):
                label = label.decode()

            if steps != output_cls_instance.shape[0]:
                print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
                print('Warning: {}Steps assigned in meta data ({}) disagrees with datacube size ({})'.format(label, steps, output_cls_instance.shape[0]))
                print('Setting steps to match data...')
                steps = output_cls_instance.shape[0]

            if (start == stop) & (steps > 1):
                print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
                print('WARNING: YStart and YStop are the same, which causes plotting problems. Switching to pixel-units based on dataset shape')
                start = 0
                stop = output_cls_instance.shape[0]-1
                units = 'pix'

            print('{} ({}): Start={}\tStop={}\tSteps={}'.format(label, units, start, stop, steps))
            output_cls_instance.y_rep.data = _np.squeeze(_np.linspace(start, stop, steps))
            output_cls_instance.y_rep.units = units
            output_cls_instance.y_rep.label = label
            output_cls_instance.y_rep.update_calib_from_data()

            del start, stop, steps, units
        except Exception as e:
            _traceback.print_exc(limit=1)
            print('Something failed in meta_process: HSI-spatial calib: {}'.format(e))

    elif type(output_cls_instance) == _Spectra:
        try:
            print('Type Spectra')
            output_cls_instance.reps.units = None
            output_cls_instance.reps.label = 'Acq Number'
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
    import os as _os
    rosetta = _snb()

    filename = _os.path.abspath('../../../mP2_w_small.h5')

    spect_dark = _Spectra()
    _hdf_import_data(filename, '/Spectra/Dark_3_5ms_2',spect_dark)
    meta_process(rosetta, spect_dark)
    print(spect_dark.reps)

    print('')
    img = _Hsi()
    _hdf_import_data(filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    meta_process(rosetta, img)
    print(img.freq.__dict__)


