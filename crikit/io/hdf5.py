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
        try:
            fof = _lazy5.utils.FidOrFile(pfname, mode='r')
            fid = fof.fid

            if type(output_cls_instance) == _Hsi:
                print('Type Hsi')
                if isinstance(dset_list, str):
                    output_cls_instance.data = fid[dset_list].value
                    output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
                elif isinstance(dset_list, list):
                    if len(dset_list) > 1:
                        print('Cannot accept more than 1 HSI image at this time')
                    else:
                        for num, dname in enumerate(dset_list):
                            if num == 0:
                                output_cls_instance.data = fid[dname].value
                                output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                            else:
                                output_cls_instance.data = _np.vstack((output_cls_instance.data, fid[dname].value))
                ret = True
            elif type(output_cls_instance) == _Spectra:
                print('Type Spectra')
                if isinstance(dset_list, str):
                    output_cls_instance.data = fid[dset_list].value
                    output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)

                elif isinstance(dset_list, list):
                    for num, dname in enumerate(dset_list):
                        if num == 0:
                            output_cls_instance.data = fid[dname].value
                            output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            output_cls_instance.data = _np.vstack((output_cls_instance.data, fid[dname].value))
                ret = True
            elif type(output_cls_instance) == _Spectrum:
                print('Type Spectrum')
                if isinstance(dset_list, str):
                    output_cls_instance.data = fid[dset_list].value
                    output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
                elif isinstance(dset_list, list):
                    if len > 1:
                        print('Will average spectra into a single spectrum')
                    else:
                        for num, dname in enumerate(dset_list):
                            if num == 0:
                                output_cls_instance.data = fid[dname].value
                                output_cls_instance.meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                            else:
                                output_cls_instance.data += fid[dname].value
                        output_cls_instance.data /= num+1
                ret = True
            elif output_cls_instance is None:
                if isinstance(dset_list, str):
                    data = fid[dset_list].value
                    meta = _lazy5.inspect.get_attrs_dset(fid, dset_list)
                elif isinstance(dset_list, list):
                    for num, dname in enumerate(dset_list):
                        if num == 0:
                            data = fid[dname].value
                            meta = _lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            data = _np.vstack((data, fid[dname].value))
                ret = [data, meta]
            else:
                raise TypeError('output_cls must be Spectrum, Spectra, or Hsi')
        except:
            raise TypeError('Something failed in import_hdf_nist_special')
            ret = False

        finally:
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

    print('')
    img = _Hsi()
    hdf_import_data(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))
