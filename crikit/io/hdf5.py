"""



Created on Mon May 23 10:17:16 2016

@author: chc
"""

import numpy as np

from crikit.data.spectra import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.spectra import Hsi

import crikit.io.lazy5 as lazy5
from crikit.utils.general import find_nearest
from scipy.interpolate import interp1d


__all__ = ['hdf_import_data', 'hdf_import_data_macroraster']


def hdf_import_data_macroraster(pth, filename, dset_list, output_cls_instance, config_dict=None):
    """
    Import dataset(s) from HDF file with each dset being a single line scan.

    Parameters
    ----------
    pth : str
        Path

    filename : str
        File name

    dset_list : list
        List of 1 or more datasets

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

    config_dict_template = {'fast_start': 'Macro.Raster.Fast.Start',
                            'fast_stop': 'Macro.Raster.Fast.Stop',
                            'fast_steps': 'Macro.Raster.Fast.Steps',
                            'fast_pos_sampled': 'MicroStage.raster.fast.pos_sample_vec',
                            'n_imgs_at_sampled': 'MicroStage.raster.fast.n_images_at_pos_samples',
                            'slow_start': 'Macro.Raster.Slow.Start',
                            'slow_stop': 'Macro.Raster.Slow.Stop',
                            'slow_steps': 'Macro.Raster.Slow.Steps',
                            'slow_current_pos': 'MicroStage.raster.slow.pos',
                            'n_pix': 'Spectrometer.calib.n_pix'}
    config = {}
    config.update(config_dict_template)
    if config_dict is not None:
        config.update(config_dict)

    # Join path and filename in an os-independant way
    pfname = lazy5.utils.fullpath(filename, pth=pth)

    if not lazy5.inspect.valid_file(filename, pth=pth, verbose=True):
        return False
    elif not lazy5.inspect.valid_dsets(filename, dset_list, pth=pth, verbose=False):
        return False
    else:
        fof = lazy5.utils.FidOrFile(pfname, mode='r')
        fid = fof.fid

        assert isinstance(output_cls_instance, Hsi)
        assert isinstance(dset_list, list)

        all_xs = []
        all_ys = []

        for num, dname in enumerate(dset_list):
            # Convert to hardware-oriented dtype (endianess)
            # dset_dtype_import = fid[dname].dtype.newbyteorder('=')
            # dset_shp = fid[dname].shape

            curr_slice = fid[dname][:]
            meta = lazy5.inspect.get_attrs_dset(fid, dname)
            if num == 0:
                dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                dset_shp = (meta[config['slow_steps']], meta[config['fast_steps']],
                            meta[config['n_pix']])
                output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)

                x_vec = np.linspace(meta[config['fast_start']], meta[config['fast_stop']],
                                    meta[config['fast_steps']])
                y_vec = np.linspace(meta[config['slow_start']], meta[config['slow_stop']],
                                    meta[config['slow_steps']])

            curr_y_pos = meta[config['slow_current_pos']]

            curr_x_vec = meta[config['fast_pos_sampled']]
            curr_n_imgs_vec = meta[config['n_imgs_at_sampled']]

            all_xs.extend(curr_x_vec.tolist())
            all_ys.extend([curr_y_pos])

            intfcn = interp1d(curr_n_imgs_vec, curr_x_vec, kind='linear')

            int_fcn_intensity = interp1d(intfcn(np.arange(curr_slice.shape[0])),
                                         curr_slice, axis=0, bounds_error=False, kind='linear', fill_value='extrapolate')

            y_idx = find_nearest(y_vec, curr_y_pos)[1]
            output_cls_instance.data[y_idx, ...] = int_fcn_intensity(x_vec)

        # extent = [x_vec.min(), x_vec.max(), y_vec.min(), y_vec.max()]

        fid.close()
        output_cls_instance.meta = meta
        return True


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
    pfname = lazy5.utils.fullpath(filename, pth=pth)

    if not lazy5.inspect.valid_file(filename, pth=pth, verbose=True):
        return False
    elif not lazy5.inspect.valid_dsets(filename, dset_list, pth=pth, verbose=True):
        return False
    else:
        fof = lazy5.utils.FidOrFile(pfname, mode='r')
        fid = fof.fid

        if type(output_cls_instance) == Hsi:
            print('Type Hsi')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(output_cls_instance.data)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                if len(dset_list) > 1:
                    print('Cannot accept more than 1 HSI image at this time')
                else:
                    for num, dname in enumerate(dset_list):
                        # Convert to hardware-oriented dtype (endianess)
                        dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                        dset_shp = fid[dname].shape
                        if num == 0:
                            output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)
                            fid[dname].read_direct(output_cls_instance.data)

                            # output_cls_instance.data = fid[dname][:]
                            output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            output_cls_instance.data = np.vstack((output_cls_instance.data, fid[dname][:].astype(dset_dtype_import)))
            ret = True
        elif type(output_cls_instance) == Spectra:
            print('Type Spectra')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                if fid[dset_list].ndim == 2:  # Compatible dimensions-- use read-direct
                    dset_shp = fid[dset_list].shape
                    output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)
                    fid[dset_list].read_direct(output_cls_instance.data)
                else:
                    output_cls_instance.data = fid[dset_list].value.astype(dset_dtype_import)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dset_list)

            elif isinstance(dset_list, list):
                for num, dname in enumerate(dset_list):
                    # Convert to hardware-oriented dtype (endianess)
                    dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                    if num == 0:
                        output_cls_instance.data = fid[dname][:].astype(dset_dtype_import)
                        output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dname)
                    else:
                        output_cls_instance.data = np.vstack((output_cls_instance.data, fid[dname][:].astype(dset_dtype_import)))
            ret = True
        elif type(output_cls_instance) == Spectrum:
            print('Type Spectrum')
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(output_cls_instance.data)

                # output_cls_instance.data = fid[dset_list].value
                output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                if len > 1:
                    print('Will average spectra into a single spectrum')
                else:
                    for num, dname in enumerate(dset_list):
                        # Convert to hardware-oriented dtype (endianess)
                        dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                        dset_shp = fid[dname].shape
                        if num == 0:
                            output_cls_instance.data = np.zeros(dset_shp, dtype=dset_dtype_import)
                            fid[dname].read_direct(output_cls_instance.data)
                            # output_cls_instance.data = fid[dname][:]
                            output_cls_instance.meta = lazy5.inspect.get_attrs_dset(fid, dname)
                        else:
                            output_cls_instance.data += fid[dname][:].astype(dset_dtype_import)
                    output_cls_instance.data /= num + 1
            ret = True
        elif output_cls_instance is None:
            if isinstance(dset_list, str):
                # Convert to hardware-oriented dtype (endianess)
                dset_dtype_import = fid[dset_list].dtype.newbyteorder('=')
                dset_shp = fid[dset_list].shape
                data = np.zeros(dset_shp, dtype=dset_dtype_import)
                fid[dset_list].read_direct(data)

                # data = fid[dset_list].value
                meta = lazy5.inspect.get_attrs_dset(fid, dset_list)
            elif isinstance(dset_list, list):
                for num, dname in enumerate(dset_list):
                    # Convert to hardware-oriented dtype (endianess)
                    dset_dtype_import = fid[dname].dtype.newbyteorder('=')
                    dset_shp = fid[dname].shape
                    if num == 0:
                        data = np.zeros(dset_shp, dtype=dset_dtype_import)
                        fid[dname].read_direct(data)
                        # data = fid[dname][:]
                        meta = lazy5.inspect.get_attrs_dset(fid, dname)
                    else:
                        data = np.vstack((data, fid[dname][:].astype(dset_dtype_import)))
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
    tester = lazy5.inspect.valid_dsets(pth=pth, file='fake.h5', dset_list='fake')
    assert not tester

    tester = lazy5.inspect.valid_dsets(pth=pth, file='fake.h5', dset_list='fake_dset')
    assert not tester

    tester = lazy5.inspect.valid_dsets(pth=pth, file='fake.h5',
                                       dset_list=['fake_dset1', 'fake_dset2'])
    assert not tester

    print('Path: {}'.format(pth))
    tester = lazy5.inspect.valid_dsets(pth=pth, file=filename, dset_list=dset, verbose=True)
    assert tester

    print('--------------\n\n')

    spect_dark = Spectra()
    tester = lazy5.inspect.valid_dsets(pth=pth, file=filename,
                                       dset_list=['/Spectra/Dark_3_5ms_2'])
    hdf_import_data(pth, filename, '/Spectra/Dark_3_5ms_2', spect_dark)
    # hdf_process_attr(rosetta, spect_dark)

    print('Shape of dark spectra: {}'.format(spect_dark.shape))
    print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
    print('Dtype of dark spectra: {}'.format(spect_dark._data.dtype))
    print('')
    img = Hsi()
    hdf_import_data(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))
    print('Dtype of img: {}'.format(img._data.dtype))
    print('Dtype of img.mean(): {}'.format(img.mean().dtype))

    print('--------------\n\n')

    pth = 'C:/Users/chc/Documents/Data/2018/OliverJonas/180629/'
    filename = 'L1d1_pos0.h5'
    dsetname = '/BCARSImage/L1d1_pos0_0/NRB_Post_0'
    spect_nrb = Spectra()
    tester = lazy5.inspect.valid_dsets(pth=pth, file=filename,
                                       dset_list=[dsetname])
    out = hdf_import_data(pth, filename, dsetname, spect_nrb)
    print('HDF_import_data returned: {}'.format(out))
    # hdf_process_attr(rosetta, spect_nrb)

    # print('Shape of dark spectra: {}'.format(spect_dark.shape))
    # print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
    # print('Dtype of dark spectra: {}'.format(spect_dark._data.dtype))
    # print('')
    # img = Hsi()
    # hdf_import_data(pth, filename, '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small', img)
    # print('Shape of img: {}'.format(img.shape))
    # print('Shape of img.mean(): {}'.format(img.mean().shape))
    # print('Dtype of img: {}'.format(img._data.dtype))
    # print('Dtype of img.mean(): {}'.format(img.mean().dtype))
