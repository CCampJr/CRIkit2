""" Macros for inspection of HDF5 files """
import os as _os
from collections import OrderedDict as _OrderedDict

import h5py as _h5py
import numpy as _np

from .utils import (FidOrFile as _FidOrFile, hdf_is_open as _hdf_is_open,
                    fullpath as _fullpath)

from .config import DefaultConfig
_h5py.get_config().complex_names = DefaultConfig().complex_names

__all__ = ['get_groups', 'get_datasets', 'get_hierarchy',
           'get_attrs_dset', 'valid_dsets', 'valid_file']

def get_groups(file, pth=None):
    """
    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    Notes
    -----
    Gets groups in a hierarchical list starting from the base '/'. Thus if
    Group2 is INSIDE Group1, it will return Group1, Group1/Group2 -- NOT Group2
    inidividually.
    """

    fp = _fullpath(file, pth)
    # Get fid for a file (str or open fid)
    fof = _FidOrFile(fp)
    fid = fof.fid

    all_items_list = []
    fid.visit(lambda x: all_items_list.append('/{}'.format(x)))

    # list-set-list removes duplicates
    grp_list = list(set([item for item in all_items_list if isinstance(fid[item], _h5py.Group)]))

    grp_list.append('/')  # Add in base level group
    grp_list.sort()

    fof.close_if_file_not_fid()

    return grp_list

def get_datasets(file, pth=None, fulldsetpath=True):
    """
    Parameters
    ----------

    file : str or _h5py.File
        Filename or File-object for open HDF5 file

    fulldsetpath : bool
        Return just the dataset names with group names or not.
    """
    
    if isinstance(file, str):
        fp = _fullpath(file, pth)
        fof = _FidOrFile(fp)

    else:
        fof = _FidOrFile(file)

    fid = fof.fid

    all_items_list = []
    fid.visit(lambda x: all_items_list.append('/{}'.format(x)))
    dset_list = []

    # list-set-list removes duplicates
    dset_list = list(set([item for item in all_items_list if isinstance(fid[item], _h5py.Dataset)]))
    dset_list.sort()

    if not fulldsetpath:
        for num, dset in enumerate(dset_list):
            split_out = dset.rsplit('/', maxsplit=1)
            if len(split_out) == 1:
                pass
            else:
                dset_list[num] = split_out[-1]

    fof.close_if_file_not_fid()

    return dset_list

def get_hierarchy(file, pth=None, fulldsetpath=False, grp_w_dset=False):
    """
    Return an ordered dictionary, where the keys are groups and the items are
    the datasets

    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    fulldsetpath : bool
        If True, a dataset name will be prepended with the group down to the
        base level, '/'. If False, it will just be the dset name.

    grp_w_dset : bool
        If True, only return groups that contain datasets. If False, include
        empty groups

    Returns
    -------
    OrderedDict : (group, [dataset list])
        Group and dataset names

    """
    fp = _fullpath(file, pth)

    # Get fid for a file (str or open fid)
    fof = _FidOrFile(fp)
    fid = fof.fid

    grp_list = get_groups(fid)
    dset_list = get_datasets(fid, fulldsetpath=True)

    grp_dict = _OrderedDict([[grp, []] for grp in grp_list])

    for dset in dset_list:
        split_out = dset.rsplit('/', maxsplit=1)
        if (len(split_out) == 1) or (split_out[0] == ''):
            if dset[0] == '/':
                grp_dict['/'].append(dset[1:])
            else:
                grp_dict['/'].append(dset)
        else:
            if fulldsetpath:
                grp_dict[split_out[0]].append(dset)
            else:
                grp_dict[split_out[0]].append(split_out[1])

    # Only keep groups with datasets
    if grp_w_dset:
        to_pop = []
        for k in grp_dict:
            if not grp_dict[k]:  # is empty
                to_pop.append(k)

        for empty_grp in to_pop:
            grp_dict.pop(empty_grp)

    fof.close_if_file_not_fid()

    return grp_dict

def get_attrs_dset(file, dset, pth=None, convert_to_str=True, convert_sgl_np_to_num=False):
    """
    Get dictionary of attribute values for a given dataset

    Parameters
    ----------

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    dset : str
        Full dataset name with preprended group names. E.g., '/Group1/Dataset'

    convert_to_str : bool
        If an attribute is a numpy.bytes_ string-like object, but not a str, try
        to decode into utf-8.

    convert_sgl_np_to_num : bool
        If an attribute is a numpy array with a single entry, convert to non-numpy
        numeric type. E.g. np.array([1.0]) -> 1.0

    Returns
    -------
    OrderedDict : (key, value)

    """
    fp = _fullpath(file, pth)

    # Get fid for a file (str or open fid)
    fof = _FidOrFile(fp)
    fid = fof.fid

    ds_attrs = fid[dset].attrs

    attr_keys_list = list(ds_attrs)
    attr_keys_list.sort()

    attr_list = []
    for k in attr_keys_list:
        try:
            attr_val = ds_attrs[k]
        except (TypeError, ValueError):
            print('Could not get value for attribute: {}. Set to None'.format(k))
            attr_list.append([k, None])
        else:
            if isinstance(attr_val, _np.ndarray):
                if (isinstance(attr_val, _np.bytes_) | (attr_val.dtype.type == _np.bytes_)) & convert_to_str: # pylint: disable=no-member
                    # * tostring() added in \x00 to end of string; thus, used list comprehension
                    np_byte_to_str = [q for q in attr_val][0].decode()
                    attr_list.append([k, np_byte_to_str])
                elif (_np.issubdtype(attr_val.dtype, _np.number) & (attr_val.size == 1)) & convert_sgl_np_to_num:
                    attr_list.append([k, attr_val.item()])
                else:
                    attr_list.append([k, attr_val])
            elif isinstance(attr_val, bytes) & convert_to_str:
                attr_list.append([k, attr_val.decode()])
            else:
                attr_list.append([k, attr_val])

    attr_dict = _OrderedDict(attr_list)

    fof.close_if_file_not_fid()

    return attr_dict

def valid_file(file, pth=None, verbose=False):
    """ Validate whether a file exists (or if a fid, is-open """

    if isinstance(file, str):
        fp = _fullpath(file, pth)
        isvalid = _os.path.isfile(fp)

        if verbose:
            if isvalid:
                print('{} is a valid file.'.format(fp))
            else:
                print('{} is a not valid file.'.format(fp))

    elif isinstance(file, _h5py.File):
        isvalid = _hdf_is_open(file)
    else:
        raise TypeError('file need be of type str or h5py.File object.')
    
    return isvalid

def valid_dsets(file, dset_list, pth=None, verbose=False):
    """ Check whether 1 or more datasets are valid """

    def _add_leading_slash(str_to_check):
        """ Return string sans leading '/' if there is one """
        if str_to_check[0] == '/':
            return str_to_check
        else:
            return '/' + str_to_check

    file_is_valid = valid_file(file, pth=pth, verbose=verbose)

    if not file_is_valid:
        return False

    dset_in_file = get_datasets(file, pth=pth, fulldsetpath=True)

    if isinstance(dset_list, (list, tuple)):
        hits = 0
        for dset in dset_list:
            dset_to_test = _add_leading_slash(dset)
            if dset_in_file.count(dset_to_test) > 0:
                hits += 1
                if verbose:
                    print('{} : VALID'.format(dset_to_test))
            else:
                if verbose:
                    print('{} : NOT VALID'.format(dset_to_test))
        if hits == len(dset_list):
            if verbose:
                print('All datasets are valid')
            return True
        else:
            if verbose:
                print('Some or all datasets are NOT valid')
            return False
    elif isinstance(dset_list, str):
        if dset_in_file.count(_add_leading_slash(dset_list)) > 0:
            if verbose:
                print('{} : VALID'.format(dset_list))
            return True
        else:
            if verbose:
                print('{} : NOT VALID'.format(dset_list))
            return False
    else:
        err_str1 = 'dset_list: {} of type {} '.format(dset_list, type(dset_list))
        err_str2 = 'is not a str, list, or tuple'
        raise TypeError(err_str1 + err_str2)

