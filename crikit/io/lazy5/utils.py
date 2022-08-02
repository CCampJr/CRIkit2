""" Utility functions """
import os as _os

import h5py as _h5py
import numpy as _np

from .config import DefaultConfig
_h5py.get_config().complex_names = DefaultConfig().complex_names

__all__ = ['FidOrFile', 'hdf_is_open', 'fullpath']

class FidOrFile:
    """
    Class for opening an HDF5 file and returning a file ID (fid) or if passed
    and already open fid, passing it along (pass-thru). Primarily for enabling
    functions and methods to operate on open and closed files.

    Parameters
    ----------
    file : str or h5py.File
        Filename or File-object for open HDF5 file

    mode : str
        If opening a file, open with mode. Available: r,r+,w,w-,x,a

    Attributes
    ----------
    is_fid : bool
        Was the input file actually an fid.

    fid : h5py.File object
        File ID
    """
    def __init__(self, file=None, mode='r'):
        self.is_fid = None
        self.fid = None
        if file is not None:
            self.return_fid_from_file(file, mode=mode)

    def return_fid_from_file(self, file, mode='r'):
        """
        Return an open fid (h5py.File). If provided a string, open file, else
        pass-thru given fid.

        Parameters
        ----------
        file : str or h5py.File
            Filename or File-object for open HDF5 file

        mode : str
            If opening a file, open with mode. Available: r,r+,w,w-,x,a

        Returns
        -------
        fid : h5py.File object
            File ID

        """
        self.is_fid = isinstance(file, _h5py.File)
        if not self.is_fid:
            self.fid = _h5py.File(file, mode=mode)
        else:
            self.fid = file
        return self.fid

    def close_if_file_not_fid(self):
        """ Close the file if originally a filename (not a fid) was passed """
        if not self.is_fid:
            return self.fid.close()
        else:
            return None

def hdf_is_open(fid):
    """ Is an HDF file open via fid """
    # ! New h5py v 2.9.*: id instead of fid
    try:
        status = fid.id.valid
    except AttributeError:
        status = fid.fid.valid

    if status == 0:
        return False
    elif status == 1:
        return True
    else:
        return None

def fullpath(filename, pth=None):
    """ Return a full path by joining a pth and filename """
    if not pth:
        return filename
    else:
        return _os.path.join(pth, filename)