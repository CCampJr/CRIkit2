# -*- coding: utf-8 -*-
"""



Created on Mon May 23 10:17:16 2016

@author: chc
"""

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

import h5py as _h5py
_h5py.get_config().complex_names = ('Re','Im')

import numpy as _np



def hdf_dset_list_rep(prefix,suffixes):
    """
    Create a list of dataset names
    """
    dset_list = []

    assert isinstance(prefix,str)

    for sfx in suffixes:
        dset_list.append(prefix + str(sfx))

    return dset_list

def hdf_is_valid_dsets(pfname,dset_list):
    """
    Validate file and datasets exist. Return boolean as to whether valid

    """
    isvalid = False
    fileexists = False

    try:
        f = _h5py.File(pfname, 'r')
        print('File exists: \'{}\''.format(pfname))
        fileexists = True
    except OSError:
        print('File does not exist: \'{}\''.format(pfname))
        fileexists = False
    else:
        if isinstance(dset_list, list):  # List of dataset(s)
            try:
                for count in dset_list:
                    f[count]
            except:
                print('dataset: {} is invalid'.format(count))
            else:
                print('All datasets are valid')
                isvalid = True
        elif isinstance(dset_list, str):  # Single dataset string name
            try:
                f[dset_list]
            except:
                print('dataset: {} is invalid'.format(count))
            else:
                print('Dataset is valid')
                isvalid = True
        else:
            print('dset_list is unrecognized type')
    finally:
        if fileexists:
            f.close()

        return isvalid

def _convert_to_np_dtype(dset):
    """
    Given an HDF5 dataset, return the values in a numpy-builtin datatype

    Parameters
    ----------
    dset : h5py.Dataset
        HDF5 (h5py) dataset

    Returns
    -------
    out : numpy.ndarray (dtype = numpy built-in)

    Note
    ----
    The software accounts for big-/little-endianness, and the inability of \
    hdf5 to natively store complex numbers.

    """
    assert isinstance(dset, _h5py.Dataset), 'Input is not of type h5py.Dataset'
    # Single datatype
    if len(dset.dtype) == 0:
        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
        dset.read_direct(converted)
        if issubclass(converted.dtype.type, _np.integer):  # Integer to float
            converted = converted.astype(_np.float)
        return converted
    #Compound datatype of length 2-- assumed ('Re','Im')
    elif len(dset.dtype) == 2:
        print('Warning: h5py.complex_names set incorrectly using \'{}\' and \'{}\' \
for Re and Im, respectively'.format(dset.dtype.names[0], dset.dtype.names[1]))
        _h5py.get_config().complex_names = (dset.dtype.names[0],dset.dtype.names[1])
        dset = dset.file[dset.name]
        converted = _np.ndarray(dset.shape, dtype = dset.dtype.newbyteorder('='))
        dset.read_direct(converted)
    # Unknown datatype
    else:
        print('Warning: Unknown datatype. Returning dataset values as is.')
        return dset.value
    return converted

#def retrieve_dataset_attribute_dict(filename,datasetfullname):
#    """
#    Given an HDF5 filename and dataset, return a dictionary with keys named \
#    with parameters and values
#
#    Parameters
#    ----------
#    filename : str
#        filename of HDF5 file
#
#    datasetfullname : str
#        full pathname to dataset (e.g., /group/subgroup/dataset)
#
#    Returns
#    -------
#    out : dict
#        {parameter : value}
#
#    """
#    assert hdf_is_valid_dsets(filename, datasetfullname) == True
#
#    f = _h5py.File(filename,'r')
#    attrs = f[datasetfullname].attrs
#
#    try:  # Try simple copy first
#        temp =  dict(attrs)
#    except:  # Go 1-by-1 and get valid attributes
#        print('Error in attributes... Usually an empty one')
#        temp = {}
#        for count in attrs:
#            try:
#                temp[count] = attrs[count]
#            except:
#                pass
#    finally:
#        f.close()
#        return temp

def hdf_attr_to_dict(attr):
    """
    Convert from HDF attributes to valid dict
    """

    try:
        output_dict = dict(attr)
    except:
        output_dict = {}
        for count in attr:
            try:
                output_dict[count] = attr[count]
            except:
                pass
    return output_dict

def hdf_import_data(pfname,dset_list,output_cls_instance):
    if hdf_is_valid_dsets(pfname,dset_list) == False:
        print('Invalid filename or dataset list')
        return None
    else:

        f = _h5py.File(pfname,'r')

        # NOTE: order is important since Hsi and Spectra are subclasses of
        # Spectrum
        if isinstance(output_cls_instance, _Hsi):
            print('Type Hsi')
            if isinstance(dset_list, str):
                output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
                output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
            elif isinstance(dset_list, list):
                if len > 1:
                    print('Cannot accept more than 1 HSI image at this time')
                else:
                    for num, dname in enumerate(dset_list):
                        if num == 0:
                            output_cls_instance.data = _convert_to_np_dtype(f[dname])
                            output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
                        else:
                            output_cls_instance.data = _np.vstack((output_cls_instance.data, _convert_to_np_dtype(f[dname])))

        elif isinstance(output_cls_instance, _Spectra):
            print('Type Spectra')
            if isinstance(dset_list,str):
                output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
                output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)

            elif isinstance(dset_list, list):
                for num, dname in enumerate(dset_list):
                    if num == 0:
                        output_cls_instance.data = _convert_to_np_dtype(f[dname])
                        output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
                    else:
                        output_cls_instance.data = _np.vstack((output_cls_instance.data, _convert_to_np_dtype(f[dname])))
        elif isinstance(output_cls_instance, _Spectrum):
            print('Type Spectrum')
            if isinstance(dset_list, str):
                output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
                output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
            elif isinstance(dset_list, list):
                if len > 1:
                    print('Will average spectra into a single spectrum')
                else:
                    for num, dname in enumerate(dset_list):
                        if num == 0:
                            output_cls_instance.data = _convert_to_np_dtype(f[dname])
                            output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
                        else:
                            output_cls_instance.data += _convert_to_np_dtype(f[dname])
                    output_cls_instance.data /= num+1
        else:
            raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')

    f.close()

if __name__ == '__main__':

    from crikit.imports.hdf_configs import (special_nist_bcars2_import_attr
                                            as _import_attr)

    filename = _os.path.abspath('../../../mP2_w_small.h5')
    dset = '/Spectra/Dark_3_5ms_2'
    tester = hdf_is_valid_dsets('fake.h5','fake')
    assert tester == False

    tester = hdf_is_valid_dsets(filename,'fake_dset')
    assert tester == False

    tester = hdf_is_valid_dsets(filename,['fake_dset1','fake_dset2'])
    assert tester == False

    tester = hdf_is_valid_dsets(filename,dset)
    assert tester == True

    dset_list = hdf_dset_list_rep('/Spectra/Dark_3_5ms_',_np.arange(2))
    tester = hdf_is_valid_dsets(filename,dset_list)
    assert tester == True

    print('--------------\n\n')

    spect_dark = _Spectra()
    hdf_import_data(filename,'/Spectra/Dark_3_5ms_2',spect_dark)
    print('Shape of dark spectra: {}'.format(spect_dark.shape))
    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))

    print('')
    img = _Hsi()
    hdf_import_data(filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))

#    print(_import_attr())
#    print(spect.shape)
#    print(spect.__dict__)
#    try:
#        f = _h5py.File(pfname, 'r')
#        #print('Opened file')
#    except OSError:
#        print('File does not exist...')
#
#    else:
#            # Load data and convert to builti-and-native numpy datatype
#            clsinst.spectrafull = _convert_to_np_dtype(f[datasetname[0]])

#def HDFtoClass(cls, filename, datasetname):
#        """
#        Load HDF5-stored dataset(s) into HSIData class
#        """
#
#        #DEFAULT_SPATIAL_UNITS = '($\mu m$)'
#        #DEFAULT_SPECTRAL_UNITS = 'Wavenumber (cm$^{-1}$)'
#
#        clsinst = cls()
#
#        try:
#            f = _h5py.File(filename, 'r')
#            #print('Opened file')
#        except OSError:
#            print('File does not exist...')
#            return None
#        else:
#            # Load data and convert to builti-and-native numpy datatype
#            clsinst.spectrafull = _convert_to_np_dtype(f[datasetname[0]])
#
#            # Load attributes
#            try:
#                clsinst.attr = _get_hdf_attr(filename, datasetname[0])
#            except:
#                raise Warning('Could not load attributes from dataset')
#                return clsinst
#            # Attributes loaded -- setup rest of class
#            else:
#                # Set frequency/spectral vector
#                # (1) Calibrated vector, (2) Uncalibrated vector,
#                # (3) Center wavelength of acquisition
#                try:  # Processing Calibration provided
#                    calibration_vector = clsinst.attr['Processing.WNCalib']
#                    clsinst.freqvecfull, clsinst.freqcalib = _make_freq_vector(calibration_vector)[0::2]
#                    try:
#                        calibration_vector = clsinst.attr['Processing.WNCalibOrig']
#                        clsinst._freqcaliborig = _make_freq_vector(calibration_vector)[2]
#                    except:
#                        clsinst._freqcaliborig = clsinst.freqcalib
#                except:  # Maybe only Original Processing Calibration provided
#                    try:
#                        calibration_vector = clsinst.attr['Processing.WNCalibOrig']
#                        clsinst.freqvecfull, clsinst._freqcaliborig = _make_freq_vector(calibration_vector)[0::2]
#                    except: # No Processing.WNCalib* provided
#                        try: # Center wavelength provided-- use default calibration
#                            center_wavelength = clsinst.attr['Spectro.CenterWavelength']
#                            if (isinstance(center_wavelength, list) or isinstance(center_wavelength, _np.ndarray)):
#                                center_wavelength = center_wavelength[0]
#                            clsinst.freqvecfull, clsinst._freqcaliborig = _make_freq_vector(center_wavelength)[0::2]
#                        except:  # Nothing provided. Use stock calibration from make_freq_vec
#                            clsinst.freqvecfull, clsinst._freqcaliborig = _make_freq_vector()[0::2]
#                        finally:
#                            clsinst.attr['Processing.WNCalibOrig'] = clsinst.freqcaliborig_vec
#                    finally:
#                        clsinst._freqcalib = clsinst._freqcaliborig
#
#                # Set spatial information
#                if clsinst.spectrafull.ndim == 3:
#                    try:
#                        clsinst.nvec = clsinst.attr['Processing.X']
#                    except:
#                        try:
#                            start = clsinst.attr['RasterScanParams.FastAxisStart'][0]
#                            stop = clsinst.attr['RasterScanParams.FastAxisStop'][0]
#                            steps = clsinst.attr['RasterScanParams.FastAxisSteps']
#
#                            clsinst.nvec = _np.linspace(start, stop, steps)
#                        except:
#                            pass
#                    try:
#                        clsinst.nvec = clsinst.attr['Processing.Y']
#                    except:
#                        try:
#                            start = clsinst.attr['RasterScanParams.SlowAxisStart'][0]
#                            stop = clsinst.attr['RasterScanParams.SlowAxisStop'][0]
#                            steps = clsinst.attr['RasterScanParams.SlowAxisSteps']
#
#                            clsinst.mvec = _np.linspace(start, stop, steps)
#                        except:
#                            pass
#                elif len(clsinst.spectrafull) == 2:
#                    pass
#                elif len(clsinst.spectrafull) == 1:
#                    pass
#                else:
#                    pass
#            finally:
#                f.close()
#        return clsinst