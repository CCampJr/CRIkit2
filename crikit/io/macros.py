# -*- coding: utf-8 -*-
"""
Created on Thu May 26 13:16:12 2016

@author: chc
"""

if __name__ == '__main__':  # pragma: no cover
    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../../'))

#from crikit.data.spectrum import Spectrum as _Spectrum
#from crikit.data.spectra import Spectra as _Spectra
#


import h5py as _h5py
_h5py.get_config().complex_names = ('Re','Im')

from crikit.io.meta_configs import (special_nist_bcars2 as _snb)
from crikit.io.meta_process import meta_process as _meta_process
from crikit.io.hdf5 import hdf_import_data as _hdf_import_data

__all__ = []


def import_hdf_nist_special(pth, filename, dset, output_cls_instance):

#    pfname = pth + filename
    _hdf_import_data(pth, filename,dset,output_cls_instance)
    _meta_process(_snb(), output_cls_instance)

if __name__ == '__main__':  # pragma: no cover

    from crikit.data.hsi import Hsi as _Hsi

    filename = _os.path.abspath('../../../mP2_w_small.h5')
    img = _Hsi()
    import_hdf_nist_special(filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
    print('Shape of img: {}'.format(img.shape))
    print('Shape of img.mean(): {}'.format(img.mean().shape))
    print(img.y_rep.data)