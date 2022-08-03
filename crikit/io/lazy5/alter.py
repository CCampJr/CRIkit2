""" Macros for inspection of HDF5 files """
import h5py as _h5py

from .utils import (FidOrFile as _FidOrFile, fullpath as _fullpath)
from .nonh5utils import (check_type_compat as _check_type_compat)

from .config import DefaultConfig
_h5py.get_config().complex_names = DefaultConfig().complex_names

def alter_attr(dset, attr_key, attr_val, file=None, pth=None, verbose=False,
               check_same_type=False, must_exist=False):
    """
    Alter attribute dset['attr_key'] with attr_val.

    Parameters
    ----------
    dset : str or h5py.Dataset
        String to or Dataset-object for dataset in HDF5 file. If string,
        file/fid must be provided.

    attr_key : str
        Attribute name (key)

    attr_val : str
        Attribute value to write (replace old)

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    pth : str
        Path

    verbose : bool
        Verbose output to stdout

    check_same_type : bool
        Check that the inputs are compatible types as defined in
        lazy5.nonh5utils.check_type_compat or lazy5.utils.return_family_type

    must_exist : bool
        The attribute must already exist.

    Notes
    -----
    None
    """

    if file is not None:
        fp = _fullpath(file, pth)
        # Get fid for a file (str or open fid)
        fof = _FidOrFile(fp, mode='r+')  # Read/write, file must exist
        fid = fof.fid
        if isinstance(dset, str):
            dset_object = fid[dset]
        elif isinstance(dset, _h5py.Dataset):
            if isinstance(file, str):
                raise TypeError('Cannot provide h5py.Dataset dset and a filename str.')
            dset_object = dset
        else:
            raise TypeError('dset unknown')
    else:
        fof = None
        if isinstance(dset, _h5py.Dataset):
            dset_object = dset
        else:
            raise TypeError('With no file or fid given, dset must be an h5py.Dataset object')

    if must_exist:
        if dset_object.attrs.get(attr_key) is None:
            err_str1 = 'Attribute {} does not exist and '.format(attr_key)
            raise KeyError(err_str1 + 'must_exist set to True')

    if check_same_type & (dset_object.attrs.get(attr_key) is not None):
        if not _check_type_compat(dset_object.attrs[attr_key], attr_val):
            err_str1 = 'New attribute value type ({}) '.format(type(attr_val))
            err_str2 = 'must be of the same type as the original '
            err_str3 = '({})'.format(type(dset_object.attrs[attr_key]))
            raise TypeError(err_str1 + err_str2 + err_str3)

    if verbose:
        if dset_object.attrs.get(attr_key) is None:
            print('Attribute {} does not exist. Creating.'.format(attr_key))
        else:
            print('Dataset[{}] = {} -> {}'.format(attr_key, dset_object.attrs[attr_key],
                                                  attr_val))

    dset_object.attrs[attr_key] = attr_val

    if fof is not None:
        fof.close_if_file_not_fid()

def alter_attr_same(dset, attr_key, attr_val, file=None, pth=None, verbose=True,
                    must_exist=False):
    """
    Alter attribute dset['attr_key] with attr_val checkint to make sure that
    the original and new attribute values are of similar type e.g., int and
    np.int32.

    Parameters
    ----------
    dset : str or h5py.Dataset
        String to or Dataset-object for dataset in HDF5 file. If string,
        file/fid must be provided.

    attr_key : str
        Attribute name (key)

    attr_val : str
        Attribute value to write (replace old)

    file : str or h5py.File
        Filename or File-object for open HDF5 file

    pth : str
        Path

    verbose : bool
        Verbose output to stdout

    Notes
    -----
    None
    """
    return alter_attr(dset, attr_key, attr_val, file, pth, verbose,
                      check_same_type=True, must_exist=must_exist)

def write_attr_dict(dset, attr_dict, fid=None, sort_attrs=False, verbose=False):
    """
    Write entire dictionary of attrbutes to dataset.

    Parameters
    ----------
    dset : str or h5py.Dataset
        String to or Dataset-object for dataset in HDF5 file. If string,
        fid must be provided.

    attr_dict : dict
        Attribute dictionary

    fid : h5py.File
        If dset is a string, file-object for open HDF5 file must be provided.

    sort_attrs : bool
        Sort attribute keys alphabetically prior to writing

    verbose : bool
        Verbose output to stdout
    """

    attr_key_list = list(attr_dict)
    if sort_attrs:
        attr_key_list.sort()

    for attr_key in attr_key_list:
        attr_val = attr_dict[attr_key]
        alter_attr(dset, attr_key, attr_val, file=fid, verbose=verbose,
                   check_same_type=False, must_exist=False)

    return True