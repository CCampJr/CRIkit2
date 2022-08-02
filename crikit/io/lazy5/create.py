""" Macros for creation of HDF5 files and/or datasets"""
import h5py as _h5py

from .config import DefaultConfig
from .utils import (FidOrFile as _FidOrFile, fullpath as _fullpath)
from .inspect import (valid_dsets as _valid_dsets)
from .alter import (write_attr_dict as _write_attr_dict)

_h5py.get_config().complex_names = DefaultConfig().complex_names

def save(file, dset, data, pth=None, attr_dict=None, mode='a',
         dset_overwrite=False, sort_attrs=False,
         chunks=True, verbose=False):
    """
    Save an HDF5 file

    Parameters
    ----------

    file : str or h5py.File object (fid)
        Filename

    dset : str
        Dataset name (including groups if any)

    data : ndarray
        Data to write

    pth : str
        Path to file. Otherwise, will use present working directory (PWD)

    attr_dict : dict
        Attribute dictionary. Will be Ordered.

    mode : str
        h5py file mode.

    dset_overwrite : bool
        If a dset already exists, overwrite or raise error?

    sort_attrs : bool
        Sort the attribute dictionary (alphabetically) prior to saving

    chunks : str or tuple or list
        Chunking shape or True for auto-chunking

    verbose : bool
        Verbose output

    Returns
    -------

    bool : Saved with no errors

    """

    if isinstance(file, str):
        fp = _fullpath(file, pth)
        fof = _FidOrFile(fp, mode=mode)
    elif isinstance(file, _h5py.File):
        fof = _FidOrFile(file, mode=mode)
    else:
        raise TypeError('file needs to be a str or h5py.File object.')
        
    fid = fof.fid

    if not dset_overwrite:
        if _valid_dsets(fid, dset, pth=pth, verbose=False):
            err_str1 = 'Dataset {} exists. '.format(dset)
            err_str2 = 'Param dset_overwrite=False. Will not overwrite'
            raise IOError(err_str1 + err_str2)

    dset_id = fid.require_dataset(name=dset, data=data, shape=data.shape, 
                                  dtype=data.dtype, chunks=chunks)

    if attr_dict:
        _write_attr_dict(dset_id, attr_dict, sort_attrs=sort_attrs)

    fof.close_if_file_not_fid()

    return True
