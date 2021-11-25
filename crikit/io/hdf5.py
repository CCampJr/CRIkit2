"""



Created on Mon May 23 10:17:16 2016

@author: chc
"""

import os as _os

import numpy as _np

from crikit.data.spectrum import Spectrum as _Spectrum
from crikit.data.spectra import Spectra as _Spectra
from crikit.data.hsi import Hsi as _Hsi

import lazy5 as _lazy5

__all__ = ['hdf_import_data']

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
    pfname = _lazy5.utils.fullpath(filename, pth=pth)

    if not _lazy5.inspect.valid_file(filename, pth=pth, verbose=True):
        return False
    elif not _lazy5.inspect.valid_dsets(filename, dset_list, pth=pth, verbose=True):
        return False
    else:
        fof = _lazy5.utils.FidOrFile(pfname, mode='r')
        fid = fof.fid

        if type(output_cls_instance) == _Hsi:
            print('Type Hsi')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                output_cls_instance.data = _np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(output_cls_instance.data)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                if len(dset_list) > 1:
                    print('Cannot accept more than 1 HSI image at this time')
                else:
                    for num, dname in enumerate(dset_list):
                        # Convert to hardware-oriented dtype (endianess)
                        dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                        dset_shp = fid[dname].shape
                        if num == 0:
                            output_cls_instance.data = _np.zeros(dset_shp,
                                                                    dtype=dset_dtype_import)
                            fid[dname].read_direct(output_cls_instance.data)

                            # output_cls_instance.data = fid[dname][:]
                            output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            output_cls_instance.data = _np.vstack((output_cls_instance.data,
                                                                    fid[dname][:].astype(dset_dtype_import)))
            ret = True
        elif type(output_cls_instance) == _Spectra:
            print('Type Spectra')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                if fid[dset_list].ndim == 2:  # Compatible dimensions-- use read-direct
                    dset_shp = fid[dset_list].shape
                    output_cls_instance.data = _np.zeros(dset_shp, dtype=dset_dtype_import)
                    fid[dset_list].read_direct(output_cls_instance.data)
                else:
                    output_cls_instance.data = fid[dset_list].value.astype(dset_dtype_import)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)

            elif isinstance(dset_list, list):
                for num, dname in enumerate(dset_list):
                    # Convert to hardware-oriented dtype (endianess)
                    dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                    if num == 0:
                        output_cls_instance.data = fid[dname][:].astype(dset_dtype_import)
                        output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                    else:
                        output_cls_instance.data = _np.vstack((output_cls_instance.data,
                                                               fid[dname][:].astype(dset_dtype_import)))
            ret = True
        elif type(output_cls_instance) == _Spectrum:
            print('Type Spectrum')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                output_cls_instance.data = _np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(output_cls_instance.data)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                if len > 1:
                    print('Will average spectra into a single spectrum')
                else:
                    for num, dname in enumerate(dset_list):
                        # Convert to hardware-oriented dtype (endianess)
                        dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                        dset_shp = fid[dname].shape
                        if num == 0:
                            output_cls_instance.data = _np.zeros(dset_shp,
                                                                    dtype=dset_dtype_import)
                            fid[dname].read_direct(output_cls_instance.data)
                            # output_cls_instance.data = fid[dname][:]
                            output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            output_cls_instance.data += fid[dname][:].astype(dset_dtype_import)
                    output_cls_instance.data /= num+1
            ret = True
        elif output_cls_instance is None:
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                data = _np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(data)

                # data = fid[dset_list].value
                meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                for num, dname in enumerate(dset_list):
                    # Convert to hardware-oriented dtype (endianess)
                    dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                    dset_shp = fid[dname].shape
                    if num == 0:
                        data = _np.zeros(dset_shp,
                                                                dtype=dset_dtype_import)
                        fid[dname].read_direct(data)
                        # data = fid[dname][:]
                        meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                    else:
                        data = _np.vstack((data, fid[dname][:].astype(dset_dtype_import)))
            ret = [data, meta]
        else:
            raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')


        fid.close()
        return ret

if __name__ == '__main__':  # pragma: no cover

    from crikit.io.meta_configs import (special_nist_bcars2 as _snb)
    rosetta = _snb()

    pth = '../'
    filename = 'mP2_w_small.h5'


    dset = '/Spectra/Dark_3_5ms_2'
    tester = _lazy5.inspect.valid_dsets(pth=pth, file='fake.h5', dset_list='fake')
    assert not tester

    tester = _lazy5.inspect.valid_dsets(pth=pth, file='fake.h5', dset_list='fake_dset')
    assert not tester

    tester = _lazy5.inspect.valid_dsets(pth=pth, file='fake.h5',
                                        dset_list=['fake_dset1', 'fake_dset2'])
    assert not tester

    print('Path: {}'.format(pth))
    tester = _lazy5.inspect.valid_dsets(pth=pth, file=filename, dset_list=dset, verbose=True)
    assert tester

    print('--------------\n\n')

    spect_dark = _Spectra()
    tester = _lazy5.inspect.valid_dsets(pth=pth, file=filename,
                                        dset_list=['/Spectra/Dark_3_5ms_2'])
    hdf_import_data(pth, filename, '/Spectra/Dark_3_5ms_2', spect_dark)
    #hdf_process_attr(rosetta, spect_dark)

    print('Shape of dark spectra: {}'.format(spect_dark.shape))
    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
    print('Dtype of dark spectra: {}'.format(spect_dark._data.dtype))
    print('')
    img = _Hsi()
    hdf_import_data(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))
    print('Dtype of img: {}'.format(img._data.dtype))
    print('Dtype of img.mean(): {}'.format(img.mean().dtype))

    print('--------------\n\n')

    pth = 'C:/Users/chc/Documents/Data/2018/OliverJonas/180629/'
    filename = 'L1d1_pos0.h5'
    dsetname = '/BCARSImage/L1d1_pos0_0/NRB_Post_0'
    spect_nrb = _Spectra()
    tester = _lazy5.inspect.valid_dsets(pth=pth, file=filename,
                                        dset_list=[dsetname])
    out = hdf_import_data(pth, filename, dsetname, spect_nrb)
    print('HDF_import_data returned: {}'.format(out))
    # hdf_process_attr(rosetta, spect_nrb)

    # print('Shape of dark spectra: {}'.format(spect_dark.shape))
    # print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
    # print('Dtype of dark spectra: {}'.format(spect_dark._data.dtype))
    # print('')
    # img = _Hsi()
    # hdf_import_data(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    # print('Shape of img: {}'.format(img.shape))
    # print('Shape of img.mean(): {}'.format(img.mean().shape))
    # print('Dtype of img: {}'.format(img._data.dtype))
    # print('Dtype of img.mean(): {}'.format(img.mean().dtype))
