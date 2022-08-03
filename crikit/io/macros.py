"""
Created on Thu May 26 13:16:12 2016

@author: chc
"""

import crikit.io.lazy5 as lazy5

from crikit.io.meta_configs import (special_nist_bcars2 as _snb,
                                    special_nist_bcars1_sample_scan as _snb1ss)
from crikit.io.meta_process import meta_process as _meta_process
from crikit.io.hdf5 import (hdf_import_data as _hdf_import_data, hdf_import_data_macroraster as _hdf_import_data_macroraster)
from crikit.io.csv_nist import csv_nist_import_data as _csv_nist_import_data

__all__ = ['import_hdf_nist_special', 'import_csv_nist_special1']


def hdf_nist_special_macroraster(pth, filename, dset_list, output_cls_instance):
    print('\n')
    import_success = _hdf_import_data_macroraster(pth, filename, dset_list, output_cls_instance)
    if import_success is False:
        raise ValueError('hdf_import_data_macroraster failed')
        return False
    _meta_process(_snb(), output_cls_instance)
    return True


def import_hdf_nist_special(pth, filename, dset, output_cls_instance):
    """
    Import data from HDF File as specified by NIST-specific settings

    Returns
    -------
    Success : bool
        Whether import was successful
    """

    print('\n')
    import_success = _hdf_import_data(pth, filename, dset, output_cls_instance)
    if import_success is False:
        raise ValueError('hdf_import_data failed')
        return False
    _meta_process(_snb(), output_cls_instance)
    return True


def import_hdf_nist_special_ooc(pth, filename, dset, output_cls_instance):
    """
    Import data from HDF File (OUT-OF-CORE) as specified by NIST-specific settings

    Returns
    -------
    Success : bool
        Whether import was successful
    """

    print('\n')

    try:
        fid = lazy5.utils.FidOrFile(lazy5.utils.fullpath(filename, pth=pth)).fid
        output_cls_instance._data = fid[dset]
        output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dset)
        _meta_process(_snb(), output_cls_instance)
    except Exception:
        raise ValueError('hdf_import_data failed')
        return False
    else:
        return fid


def import_csv_nist_special1(pth, filename_header, filename_data,
                             output_cls_instance):
    """
    Import data from CSV File as specified by NIST-specific settings

    Returns
    -------
    Success : bool
        Whether import was successful
    """

    try:
        import_success = _csv_nist_import_data(pth, filename_header,
                                               filename_data, output_cls_instance)
        if import_success is None or import_success is False:
            raise ValueError('csv_import_data returned None')
        _meta_process(_snb1ss(), output_cls_instance)
    except Exception:
        print('Something failed in import_csv_nist_special')
        return False
    else:
        return True


if __name__ == '__main__':  # pragma: no cover

    from crikit.data.spectra import Hsi as _Hsi

    pth = '../'
    filename = 'mP2_w_small.h5'
    img = _Hsi()
    import_hdf_nist_special(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))
    print(img.y_rep.data)

    # from crikit.data.spectra import Spectrum as _Spectrum

    # sp = _Spectrum()
    # pth = '../../../Young_150617/'
    # filename_header = 'SH-03.h'
    # filename_data = 'base061715_152213_60ms.txt'

    # import_csv_nist_special1(pth, filename_header, filename_data,
    #                 output_cls_instance=sp)
