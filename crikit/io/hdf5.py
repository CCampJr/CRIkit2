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
                print('Fail: {}'.count)
    return output_dict

def hdf_import_data(pfname,dset_list,output_cls_instance):
    if hdf_is_valid_dsets(pfname,dset_list) == False:
        print('Invalid filename or dataset list')
        return None
    else:

        f = _h5py.File(pfname,'r')

        # NOTE: order is important since Hsi and Spectra are subclasses of
        # Spectrum
        #if isinstance(output_cls_instance, _Hsi):
        if type(output_cls_instance) == _Hsi:
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

        else:
            raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')

    f.close()

if __name__ == '__main__':  # pragma: no cover

    from crikit.io.meta_configs import (special_nist_bcars2
                                            as _snb)
    rosetta = _snb()

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
    #hdf_process_attr(rosetta, spect_dark)

    print('Shape of dark spectra: {}'.format(spect_dark.shape))
    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))

    print('')
    img = _Hsi()
    hdf_import_data(filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))

