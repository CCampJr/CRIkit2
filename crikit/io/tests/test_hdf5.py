# -*- coding: utf-8 -*-
"""

Test crikit.io.hdf5 module

Created on Wed May 25 13:04:31 2016

@author: chc
"""
import unittest
import os, sys

from crikit.data.hsi import Hsi
from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

import copy
import numpy as np

from crikit.io.meta_configs import (special_nist_bcars2
                                        as _snb)

from crikit.io.hdf5 import *
class HDF5IOTest(unittest.TestCase):

    def setUp(self):
        self.rosetta = _snb()
        self.filename = os.path.abspath('../mP2_w_small.h5')
        self.spectra_dset = '/Spectra/Dark_3_5ms_2'
        self.hsi_dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small'

    def test_invalid_file(self):
        self.assertFalse(hdf_is_valid_dsets('fake.h5','fake'))
        self.assertIsNone(hdf_import_data('fake.h5','fake',Spectra()))

    def test_invalid_dset(self):
        self.assertFalse(hdf_is_valid_dsets(self.filename,'fake'))
        self.assertIsNone(hdf_import_data(self.filename,'fake',Spectra()))

    def test_valid_spectra(self):
        self.assertTrue(hdf_is_valid_dsets(self.filename, self.spectra_dset))
        spect = Spectra()
        self.assertIsNone(spect.data)
        hdf_import_data(self.filename,self.spectra_dset,spect)
        self.assertIsNotNone(spect.data)

    def test_valid_hsi(self):
        self.assertTrue(hdf_is_valid_dsets(self.filename, self.hsi_dset))
        hsi = Hsi()
        self.assertIsNone(hsi.data)
        hdf_import_data(self.filename,self.hsi_dset,hsi)
        self.assertIsNotNone(hsi.data)

#filename = _os.path.abspath('../../../mP2_w_small.h5')
#dset = '/Spectra/Dark_3_5ms_2'
#tester = hdf_is_valid_dsets('fake.h5','fake')
#assert tester == False
#
#tester = hdf_is_valid_dsets(filename,'fake_dset')
#assert tester == False
#
#tester = hdf_is_valid_dsets(filename,['fake_dset1','fake_dset2'])
#assert tester == False
#
#tester = hdf_is_valid_dsets(filename,dset)
#assert tester == True
#
#dset_list = hdf_dset_list_rep('/Spectra/Dark_3_5ms_',_np.arange(2))
#tester = hdf_is_valid_dsets(filename,dset_list)
#assert tester == True
#
#print('--------------\n\n')
#
#spect_dark = _Spectra()
#hdf_import_data(filename,'/Spectra/Dark_3_5ms_2',spect_dark)
##hdf_process_attr(rosetta, spect_dark)
#
#print('Shape of dark spectra: {}'.format(spect_dark.shape))
#print('Shape of dark spectra.mean(): {}'.format(spect_dark.mean().shape))
#
#print('')
#img = _Hsi()
#hdf_import_data(filename,'/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small',img)
#print('Shape of img: {}'.format(img.shape))
#print('Shape of img.mean(): {}'.format(img.mean().shape))