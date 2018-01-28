"""



Created on Mon May 23 10:17:16 2016

@author: chc
"""

import os as _os

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi


import h5py as _h5py
_h5py.get_config().complex_names = ('Re','Im')

import numpy as _np

__all__ = ['hdf_dset_list_rep','hdf_is_valid_dsets',
           'hdf_attr_to_dict','hdf_import_data']

def hdf_dset_list_rep(prefix,suffixes):
    """
    Create a list of dataset names
    """
    dset_list = []

    assert isinstance(prefix,str)

    for sfx in suffixes:
        dset_list.append(prefix + str(sfx))

    return dset_list

def hdf_is_valid_dsets(pth, filename, dset_list):
    """
    Validate file and datasets exist. Return boolean as to whether valid

    """
    
    isvalid = False
    fileexists = False

    try:
        # Join path and filename in an os-independant way
        pfname = _os.path.normpath(_os.path.join(pth, filename))
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
                print('dataset {} is invalid'.format(count))
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

    Notes
    -----
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
                print('Fail: {}'.format(count))
    
    # String in HDF are treated as numpy bytes_ literals
    # We want out instance in memeory to have Python Strings
    # This does a simple conversion
    # Also will check to see if a string is burried in an array
    for k in output_dict:
        if isinstance(output_dict[k], _np.bytes_):
            output_dict[k] = output_dict[k].decode('UTF-8')
        elif isinstance(output_dict[k], _np.ndarray):
            if output_dict[k].dtype.kind == 'S':  # String array
                # This is a cute way of taking an array of charcters and merging
                # them into a string. If just a single-element array,
                # will also return a string
                output_dict[k] = ''.join(output_dict[k].astype(_np.str))
    return output_dict

def hdf_import_data(pth, filename, dset_list, output_cls_instance=None):
    """
    Import dataset(s) from HDF file

    Parameters
    ----------
    pth : str
        Path

    filename : str
        File name

    dset_list : list
        List of 1 or more datasets

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
    pfname = _os.path.normpath(_os.path.join(pth, filename))

    if hdf_is_valid_dsets(pth, filename,dset_list) == False:
        print('Invalid filename or dataset list')
        return False
    else:
        try:
            f = _h5py.File(pfname,'r')

            if type(output_cls_instance) == _Hsi:
                print('Type Hsi')
                if isinstance(dset_list, str):
                    output_cls_instance.data = _convert_to_np_dtype(f[dset_list])
                    output_cls_instance.meta = hdf_attr_to_dict(f[dset_list].attrs)
                elif isinstance(dset_list, list):
                    if len(dset_list) > 1:
                        print('Cannot accept more than 1 HSI image at this time')
                    else:
                        for num, dname in enumerate(dset_list):
                            if num == 0:
                                output_cls_instance.data = _convert_to_np_dtype(f[dname])
                                output_cls_instance.meta = hdf_attr_to_dict(f[dname].attrs)
                            else:
                                output_cls_instance.data = _np.vstack((output_cls_instance.data, _convert_to_np_dtype(f[dname])))
                ret = True
            elif type(output_cls_instance) == _Spectra:
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
                ret = True
            elif type(output_cls_instance) == _Spectrum:
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
                ret = True
            elif output_cls_instance is None:
                if isinstance(dset_list, str):
                    data = _convert_to_np_dtype(f[dset_list])
                    meta = hdf_attr_to_dict(f[dset_list].attrs)
                elif isinstance(dset_list, list):
                    for num, dname in enumerate(dset_list):
                        if num == 0:
                            data = _convert_to_np_dtype(f[dname])
                            meta = hdf_attr_to_dict(f[dname].attrs)
                        else:
                            data = _np.vstack((data, _convert_to_np_dtype(f[dname])))
                ret = [data, meta]
            else:
                raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')
        except:
            raise TypeError('Something failed in import_hdf_nist_special')
            ret = False

        finally:
            f.close()
            return ret

def hdf_export_data(self, output_cls_instance, pth, filename, dsetname):
    """

    """

    save_grp = dsetname.rpartition('/')[0]
    save_dataset_name_no_grp = dsetname.rpartition('/')[-1]

    try:
        # Join path and filename in an os-independant way
        pfname_out = _os.path.normpath(_os.path.join(pth, filename))
        
        f_out = _h5py.File(pfname_out, 'a')
        loc = f_out.require_group(save_grp)
        dset = loc.create_dataset(save_dataset_name_no_grp, data=output_cls_instance.data)

        for attr_key in output_cls_instance.meta:
            try:
                attribute = output_cls_instance.meta[attr_key]
                if isinstance(attribute, str):
                    attribute = _np.array(attribute, dtype='S')
                dset.attrs.create(attr_key,attribute)
            except:
                print('Error in attributes')

        #  Breadcrumb attributes
        bc_attr_dict = self.bcpre.attr_dict
        for attr_key in bc_attr_dict:
            try:
                attribute = bc_attr_dict[attr_key]
                if isinstance(attribute, str):
                    attribute = _np.array(attribute, dtype='S')
                dset.attrs.create(attr_key,attribute)
            except:
                print('Error in attributes')
                
#            #print('Key: {}, Val: {}'.format(attr_key, bc_attr_dict[attr_key]))
#            val = bc_attr_dict[attr_key]
#            if isinstance(val, str):
#                dset.attrs[attr_key] = val
#            else:
#                try:
#                    dset.attrs.create(attr_key,bc_attr_dict[attr_key])
#                except:
#                    print('Could not create attribute')

    except:
        print('Something went wrong while saving')
    else:
        print('Saved without issues')
    finally:
        f_out.close()

if __name__ == '__main__':  # pragma: no cover

    from crikit.io.meta_configs import (special_nist_bcars2
                                            as _snb)
    rosetta = _snb()

    pth = '../../../'
    filename = 'mP2_w_small.h5'

    dset = '/Spectra/Dark_3_5ms_2'
    tester = hdf_is_valid_dsets(pth, 'fake.h5','fake')
    assert tester == False

    tester = hdf_is_valid_dsets(pth, filename,'fake_dset')
    assert tester == False

    tester = hdf_is_valid_dsets(pth, filename,['fake_dset1','fake_dset2'])
    assert tester == False

    tester = hdf_is_valid_dsets(pth, filename,dset)
    assert tester == True

    dset_list = hdf_dset_list_rep('/Spectra/Dark_3_5ms_',_np.arange(2))
    tester = hdf_is_valid_dsets(pth, filename,dset_list)
    assert tester == True

    print('--------------\n\n')

    spect_dark = _Spectra()
    tester = hdf_is_valid_dsets(pth, filename,['/Spectra/Dark_3_5ms_2'])
    hdf_import_data(pth, filename,'/Spectra/Dark_3_5ms_2',spect_dark)
    #hdf_process_attr(rosetta, spect_dark)

    print('Shape of dark spectra: {}'.format(spect_dark.shape))
    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))

    print('')
    img = _Hsi()
    hdf_import_data(pth, filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))

