"""
Created on Wed Sep  7 12:36:36 2016

@author: chc
"""

import os as _os
import csv as _csv
import numpy as _np
import copy as _copy

from crikit.data.spectra import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.spectra import Hsi as _Hsi

from configparser import ConfigParser as _ConfigParser
#
#__all__ = ['hdf_dset_list_rep','hdf_is_valid_dsets',
#           'hdf_attr_to_dict','hdf_import_data']
#

def csv_nist_import_data(pth, filename_header, filename_data,
                    output_cls_instance=None):
    """
    Import dataset(s) from HDF file

    Parameters
    ----------
    pth : str
        Path

    filename_header : str
        File name of header
        
    filename_data : str
        File name of data

    output_cls_instance : crikit.data.spectra.Spectrum (or subclass)
        Spectrum class (or sub) object

    Returns
    -------
        Success : bool
            Success of import
        Data, Meta : list (ndarray, dict)
            If output_cls_instance is None and import is successful, will \
            return the data from dset_list and associated meta data.

    """
    # Join path and filename in an os-independant way
    pfname_header = _os.path.normpath(_os.path.join(pth, filename_header))
    pfname_data = _os.path.normpath(_os.path.join(pth, filename_data))

    valid_import_locs = 0
    
    try:
        with open(pfname_header,'r') as _:
            pass
    except Exception:
        print('Invalid header filename')
    else:
        valid_import_locs += 1
        
    try:
        with open(pfname_data,'r') as _:
            pass
    except Exception:
        print('Invalid data filename')
    else:
        valid_import_locs += 1
        
    if valid_import_locs != 2:
        return False
    else:
        try:
            config = _ConfigParser()
            config.read(pfname_header)
            
            # Frequency calibration
            probe = config.getfloat('Frequency Calibration','probe(nm)')
            wl1 = config.getfloat('Frequency Calibration','wavelength1(nm)')
            wl2 = config.getfloat('Frequency Calibration','wavelength2(nm)')
            pixel1 = config.getint('Frequency Calibration','pixel1')
            pixel2 = config.getint('Frequency Calibration','pixel2')
            f_begin = config.getfloat('Frequency Calibration','freq index begin')
            f_size = config.getint('Frequency Calibration','freq index length')
            f_min = config.getfloat('Frequency Calibration','freq Min')
            f_max = config.getfloat('Frequency Calibration','freq Max')
            
            pix = _np.linspace(pixel1,pixel2,f_size)
            wl = _np.linspace(wl1,wl2,f_size)
            wn = 1e7*(1/wl - 1/probe)
            
            # Config is apparently backwards so flip order
            pix = _np.flipud(pix)
            wl = _np.flipud(wl)
            wn = _np.flipud(wn)
            
            # Frequency calibration stuff
            wl_center = wl.mean()
            wl_slope, wl_intercept = _np.polyfit(pix, wl,1)
            
                
            # Get data
            with open(pfname_data,'r') as csvfile:
                reader = _csv.reader(csvfile, delimiter='\t')
                data = []
                for count in reader:
                    data.append(count)
            data = _np.array(data).astype(float)
            
            if (data.shape[-1] == 3) | (data.shape[-1] == 2):  # Spectra
                print('Spectra')
                wn = data[:,0]
                temp = data[:,-1]
                if data.shape[-1] == 3:
                    wl = data[:,1]
                data = temp
                
                # Meta data
                attr = {}
                for each_section in config.sections():
                    #print('Section: {}'.format(each_section))
                    for (each_key, each_val) in config.items(each_section):
                        k = each_section + '.' + each_key
                        try:  # int
                            v = int(each_val)
                            #print('Integer')
                        except Exception:
                            try:  # float
                                v = float(each_val)
                            except Exception:  # string
                                v = str.strip(each_val,'"')
                        #print('{}.{}: {}'.format(each_section,each_key, v))
                        attr.update({k:v})
                    
                # Add in frequency calibration info
                attr['Frequency Calibration.Slope'] = wl_slope
                attr['Frequency Calibration.Intercept'] = wl_intercept
                attr['Frequency Calibration.CenterWavelength'] = wl_center
    
                # Convert meta keys to match those of HDF5 version
                # Note: will not overwrite, just add-to
                # Note: Subject to change
                
                output_cls_instance.data = data
                output_cls_instance.meta = attr
                return True
                
            else:
                data = data.reshape((data.shape[0],-1,f_size))
                # Spatial Info
                x_start = config.getfloat('X scan Parameters','X start (um)')
                x_steps = config.getint('X scan Parameters','X steps')
                x_step_size = config.getfloat('X scan Parameters','X step size (um)')
                x = _np.linspace(x_start, x_start + x_step_size * (x_steps-1), x_steps)
    
                try:  # Exists a typo in header info in LabView program
                    y_start = config.getfloat('Y scan Paramters','Y start (um)')
                    y_steps = config.getint('Y scan Paramters','Y steps')
                    y_step_size = config.getfloat('Y scan Paramters','Y step size (um)')
                    y = _np.linspace(y_start, y_start + y_step_size * (y_steps-1), y_steps)
                except Exception:  # In case typo is corrected in the future
                    y_start = config.getfloat('Y scan Parameters','Y start (um)')
                    y_steps = config.getint('Y scan Parameters','Y steps')
                    y_step_size = config.getfloat('Y scan Parameters','Y step size (um)')
                    y = _np.linspace(y_start, y_start + y_step_size * (y_steps-1), y_steps)
                
                # Meta data
                attr = {}
                for each_section in config.sections():
                    #print('Section: {}'.format(each_section))
                    for (each_key, each_val) in config.items(each_section):
                        k = each_section + '.' + each_key
                        try:  # int
                            v = int(each_val)
                            #print('Integer')
                        except Exception:
                            try:  # float
                                v = float(each_val)
                            except Exception:  # string
                                v = str.strip(each_val,'"')
                        #print('{}.{}: {}'.format(each_section,each_key, v))
                        attr.update({k:v})
                    
                # Add in frequency calibration info
                attr['Frequency Calibration.Slope'] = wl_slope
                attr['Frequency Calibration.Intercept'] = wl_intercept
                attr['Frequency Calibration.CenterWavelength'] = wl_center
    
                # Convert meta keys to match those of HDF5 version
                # Note: will not overwrite, just add-to
                # Note: Subject to change
                try:
                    ax1 = attr['Image data.1st axis']
    
                    if ax1 == 0:
                        attr['RasterScanParams.FastAxis'] = 'X'
                    elif ax1 == 1:
                        attr['RasterScanParams.FastAxis'] = 'Y'
                    elif ax1 == 2:
                        attr['RasterScanParams.FastAxis'] = 'Z'
                        
                    attr['RasterScanParams.FastAxisStart'] = x_start
                    attr['RasterScanParams.FastAxisStepSize'] = x_step_size
                    attr['RasterScanParams.FastAxisSteps'] = x_steps
                    attr['RasterScanParams.FastAxisStop'] = x[-1]
    
                    ax2 = attr['Image data.2nd axis']
                    
                    if ax2 == 0:
                        attr['RasterScanParams.SlowAxis'] = 'X'
                    elif ax2 == 1:
                        attr['RasterScanParams.SlowAxis'] = 'Y'
                    elif ax2 == 2:
                        attr['RasterScanParams.SlowAxis'] = 'Z'
                        
                    attr['RasterScanParams.SlowAxisStart'] = y_start
                    attr['RasterScanParams.SlowAxisStepSize'] = y_step_size
                    attr['RasterScanParams.SlowAxisSteps'] = y_steps
                    attr['RasterScanParams.SlowAxisStop'] = y[-1]
    
                    ax3 = attr['Image data.3rd axis']
    
                    if ax3 == 0:
                        attr['RasterScanParams.FixedAxis'] = 'X'
                    elif ax3 == 1:
                        attr['RasterScanParams.FixedAxis'] = 'Y'
                    elif ax3 == 2:
                        attr['RasterScanParams.FixedAxis'] = 'Z'
                        
                    # Figure out fixed positions later
                    
                except Exception:
                    pass
                else:
                    output_cls_instance.data = data
                    output_cls_instance.meta = attr
                    return True

        except Exception:
            print('Something failed in import')

if __name__ == '__main__':
    #from crikit.data.spectra import Spectra as _Spectra
    
    sp = _Spectra()
    pth = '../../../Young_150617/'
    filename_header = 'SH-03.h'
    filename_data = 'base061715_152213_60ms.txt'
    
    csv_nist_import_data(pth, filename_header, filename_data,
                    output_cls_instance=sp)
    
    print(sp.__dict__)