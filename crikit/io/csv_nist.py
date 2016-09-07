# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 12:36:36 2016

@author: chc
"""

import os as _os
import csv as _csv
import numpy as _np
import copy as _copy

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

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

    output_cls_instance : crikit.data.spectrum.Spectrum (or subclass)
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
    except:
        print('Invalid header filename')
    else:
        valid_import_locs += 1
        
    try:
        with open(pfname_data,'r') as _:
            pass
    except:
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
                        except:
                            try:  # float
                                v = float(each_val)
                            except:  # string
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
                except:  # In case typo is corrected in the future
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
                        except:
                            try:  # float
                                v = float(each_val)
                            except:  # string
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
                    
                except:
                    pass
                else:
                    output_cls_instance.data = data
                    output_cls_instance.meta = attr
                    return True

        except:
            print('Something failed in import')
#            f = _h5py.File(pfname,'r')
#
#            if type(output_cls_instance) == _Hsi:
#                print('Type Hsi')
#                if isinstance(dset_list, str):
#                    output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
#                    output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
#                elif isinstance(dset_list, list):
#                    if len(dset_list) > 1:
#                        print('Cannot accept more than 1 HSI image at this time')
#                    else:
#                        for num, dname in enumerate(dset_list):
#                            if num == 0:
#                                output_cls_instance.data = _convert_to_np_dtype(f[dname])
#                                output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
#                            else:
#                                output_cls_instance.data = _np.vstack((output_cls_instance.data, _convert_to_np_dtype(f[dname])))
#                ret = True
#            elif type(output_cls_instance) == _Spectra:
#                print('Type Spectra')
#                if isinstance(dset_list,str):
#                    output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
#                    output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
#
#                elif isinstance(dset_list, list):
#                    for num, dname in enumerate(dset_list):
#                        if num == 0:
#                            output_cls_instance.data = _convert_to_np_dtype(f[dname])
#                            output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
#                        else:
#                            output_cls_instance.data = _np.vstack((output_cls_instance.data, _convert_to_np_dtype(f[dname])))
#                ret = True
#            elif type(output_cls_instance) == _Spectrum:
#                print('Type Spectrum')
#                if isinstance(dset_list, str):
#                    output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
#                    output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
#                elif isinstance(dset_list, list):
#                    if len > 1:
#                        print('Will average spectra into a single spectrum')
#                    else:
#                        for num, dname in enumerate(dset_list):
#                            if num == 0:
#                                output_cls_instance.data = _convert_to_np_dtype(f[dname])
#                                output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
#                            else:
#                                output_cls_instance.data += _convert_to_np_dtype(f[dname])
#                        output_cls_instance.data /= num+1
#                ret = True
#            elif output_cls_instance is None:
#                if isinstance(dset_list, str):
#                    data = _convert_to_np_dtype(f[dset_list])
#                    meta = hdf_attr_to_dict(f[dset_list].attrs)
#                elif isinstance(dset_list, list):
#                    for num, dname in enumerate(dset_list):
#                        if num == 0:
#                            data = _convert_to_np_dtype(f[dname])
#                            meta = hdf_attr_to_dict(f[dname].attrs)
#                        else:
#                            data = _np.vstack((data, _convert_to_np_dtype(f[dname])))
#                ret = [data, meta]
#            else:
#                raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')
#        except:
#            raise TypeError('Something failed in import_hdf_nist_special')
#            ret = False
#
#        finally:
#            f.close()
#            return ret

#def hdf_dset_list_rep(prefix,suffixes):
#    """
#    Create a list of dataset names
#    """
#    dset_list = []
#
#    assert isinstance(prefix,str)
#
#    for sfx in suffixes:
#        dset_list.append(prefix + str(sfx))
#
#    return dset_list
#
#def hdf_is_valid_dsets(pth, filename, dset_list):
#    """
#    Validate file and datasets exist. Return boolean as to whether valid
#
#    """
#    # Join path and filename in an os-independant way
#    pfname = _os.path.normpath(_os.path.join(pth, filename))
#
#
#    isvalid = False
#    fileexists = False
#
#    try:
#        f = _h5py.File(pfname, 'r')
#        print('File exists: \'{}\''.format(pfname))
#        fileexists = True
#    except OSError:
#        print('File does not exist: \'{}\''.format(pfname))
#        fileexists = False
#    else:
#        if isinstance(dset_list, list):  # List of dataset(s)
#            try:
#                for count in dset_list:
#                    f[count]
#            except:
#                print('dataset: {} is invalid'.format(count))
#            else:
#                print('All datasets are valid')
#                isvalid = True
#        elif isinstance(dset_list, str):  # Single dataset string name
#            try:
#                f[dset_list]
#            except:
#                print('dataset {} is invalid'.format(count))
#            else:
#                print('Dataset is valid')
#                isvalid = True
#        else:
#            print('dset_list is unrecognized type')
#    finally:
#        if fileexists:
#            f.close()
#
#        return isvalid
#
#def _convert_to_np_dtype(dset):
#    """
#    Given an HDF5 dataset, return the values in a numpy-builtin datatype
#
#    Parameters
#    ----------
#    dset : h5py.Dataset
#        HDF5 (h5py) dataset
#
#    Returns
#    -------
#    out : numpy.ndarray (dtype = numpy built-in)
#
#    Note
#    ----
#    The software accounts for big-/little-endianness, and the inability of \
#    hdf5 to natively store complex numbers.
#
#    """
#    assert isinstance(dset, _h5py.Dataset), 'Input is not of type h5py.Dataset'
#    # Single datatype
#    if len(dset.dtype) == 0:
#        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
#        dset.read_direct(converted)
#        if issubclass(converted.dtype.type, _np.integer):  # Integer to float
#            converted = converted.astype(_np.float)
#        return converted
#    #Compound datatype of length 2-- assumed ('Re','Im')
#    elif len(dset.dtype) == 2:
#        print('Warning: h5py.complex_names set incorrectly using \'{}\' and \'{}\' \
#for Re and Im, respectively'.format(dset.dtype.names[0], dset.dtype.names[1]))
#        _h5py.get_config().complex_names = (dset.dtype.names[0],dset.dtype.names[1])
#        dset = dset.file[dset.name]
#        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
#        dset.read_direct(converted)
#    # Unknown datatype
#    else:
#        print('Warning: Unknown datatype. Returning dataset values as is.')
#        return dset.value
#    return converted
#
#def hdf_attr_to_dict(attr):
#    """
#    Convert from HDF attributes to valid dict
#    """
#
#    try:
#        output_dict = dict(attr)
#    except:
#        output_dict = {}
#        for count in attr:
#            try:
#                output_dict[count] = attr[count]
#            except:
#                print('Fail: {}'.count)
#    return output_dict
#

#
#def hdf_export_data(output_cls_instance, pth, filename, dsetname):
#    """
#
#    """
#
#    save_grp = dsetname.rpartition('/')[0]
#    save_dataset_name_no_grp = dsetname.rpartition('/')[-1]
#
#    try:
#        # Join path and filename in an os-independant way
#        pfname_out = _os.path.normpath(_os.path.join(pth, filename))
#        
#        f_out = _h5py.File(pfname_out, 'a')
#        loc = f_out.require_group(save_grp)
#        dset = loc.create_dataset(save_dataset_name_no_grp, data=output_cls_instance.data)
#
#        for attr_key in output_cls_instance.meta:
#            try:
#                dset.attrs.create(attr_key,output_cls_instance.meta[attr_key])
#            except:
#                print('Error in attributes')
#
##  Breadcrumb attributes
##        bc_attr_dict = self.bcpre.attr_dict
##        for attr_key in bc_attr_dict:
##            #print('Key: {}, Val: {}'.format(attr_key, bc_attr_dict[attr_key]))
##            val = bc_attr_dict[attr_key]
##            if isinstance(val, str):
##                dset.attrs[attr_key] = val
##            else:
##                try:
##                    dset.attrs.create(attr_key,bc_attr_dict[attr_key])
##                except:
##                    print('Could not create attribute')
#
#    except:
#        print('Something went wrong while saving')
#    else:
#        print('Saved without issues')
#    finally:
#        f_out.close()
#
#if __name__ == '__main__':  # pragma: no cover
#
#    from crikit.io.meta_configs import (special_nist_bcars2
#                                            as _snb)
#    rosetta = _snb()
#
#    pth = '../../../'
#    filename = 'mP2_w_small.h5'
#
#    dset = '/Spectra/Dark_3_5ms_2'
#    tester = hdf_is_valid_dsets(pth, 'fake.h5','fake')
#    assert tester == False
#
#    tester = hdf_is_valid_dsets(pth, filename,'fake_dset')
#    assert tester == False
#
#    tester = hdf_is_valid_dsets(pth, filename,['fake_dset1','fake_dset2'])
#    assert tester == False
#
#    tester = hdf_is_valid_dsets(pth, filename,dset)
#    assert tester == True
#
#    dset_list = hdf_dset_list_rep('/Spectra/Dark_3_5ms_',_np.arange(2))
#    tester = hdf_is_valid_dsets(pth, filename,dset_list)
#    assert tester == True
#
#    print('--------------\n\n')
#
#    spect_dark = _Spectra()
#    tester = hdf_is_valid_dsets(pth, filename,['/Spectra/Dark_3_5ms_2'])
#    hdf_import_data(pth, filename,'/Spectra/Dark_3_5ms_2',spect_dark)
#    #hdf_process_attr(rosetta, spect_dark)
#
#    print('Shape of dark spectra: {}'.format(spect_dark.shape))
#    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
#
#    print('')
#    img = _Hsi()
#    hdf_import_data(pth, filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
#    print('Shape of img: {}'.format(img.shape))
#    print('Shape of img.mean(): {}'.format(img.mean().shape))
#
