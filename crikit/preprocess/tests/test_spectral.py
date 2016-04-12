# -*- coding: utf-8 -*-
"""

Test spectral preprocessing functions

Created on Tue Apr 12 17:16:57 2016

@author: chc
"""

import unittest
from crikit.preprocess.spectral import sub_mean_over_range
from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

import copy
import numpy as np

class SubMeanTest(unittest.TestCase):
    def setUp(self):
        self.x = np.linspace(0,100,10)
        self.y = np.linspace(0,100,10)
        self.freq = np.arange(20)
        self.data = np.ones((10,10,20))

    def test_submean_overwrite(self):

        hs = Hsi(data=copy.deepcopy(self.data), freq=self.freq, x=self.x, y=self.y)
        spa = Spectra(data=copy.deepcopy(self.data), freq=self.freq)
        sp = Spectrum(data=copy.deepcopy(self.data)[0,0,:], freq=self.freq)

        #3D
        out = sub_mean_over_range(hs, [5,8], overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(hs.data.mean(),0))

        #2D
        out = sub_mean_over_range(spa, [5,8], overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(spa.data.mean(),0))

        #1D
        out = sub_mean_over_range(sp, [5,8], overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(sp.data.mean(),0))

    def test_submean_not_overwrite(self):

        hs = Hsi(data=copy.deepcopy(self.data), freq=self.freq, x=self.x, y=self.y)
        spa = Spectra(data=copy.deepcopy(self.data), freq=self.freq)
        sp = Spectrum(data=copy.deepcopy(self.data)[0,0,:], freq=self.freq)

        #3D
        out = sub_mean_over_range(hs, [5,8], overwrite=False)
        self.assertFalse(np.allclose(hs.data.mean(),0))
        self.assertTrue(np.allclose(out.mean(),0))

        #2D
        out = sub_mean_over_range(spa, [5,8], overwrite=False)
        self.assertFalse(np.allclose(spa.data.mean(),0))
        self.assertTrue(np.allclose(out.mean(),0))

        #1D
        out = sub_mean_over_range(sp, [5,8], overwrite=False)
        self.assertFalse(np.allclose(sp.data.mean(),0))
        self.assertTrue(np.allclose(out.mean(),0))

    def test_submean_wrong_inputs(self):
        hs = Hsi(data=copy.deepcopy(self.data), freq=self.freq, x=self.x, y=self.y)

        self.assertRaises(TypeError, sub_mean_over_range, data_obj=[], rng=[5,7])
        self.assertRaises(TypeError, sub_mean_over_range, data_obj=hs, rng=[5,7,8])
        self.assertRaises(TypeError, sub_mean_over_range, data_obj=hs, rng={})
        self.assertRaises(TypeError, sub_mean_over_range,
                          data_obj=np.ones((3,3,3,3)), rng=[5,8])

        hs4D = Hsi(data=copy.deepcopy(self.data), freq=self.freq, x=self.x, y=self.y)
        hs4D._data = np.ones((3,3,3,3))  # Have to overwrite manually it to get it to 4D
        self.assertRaises(NotImplementedError, sub_mean_over_range,
                          data_obj=hs4D, rng=[5,7])
        self.assertRaises(NotImplementedError, sub_mean_over_range,
                          data_obj=hs4D._data, f=self.freq, rng=[5,7])

    def test_submean_ndarray_overwrite(self):

        #3D
        data = copy.deepcopy(self.data)
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(data.mean(),0))

        #2D
        data = copy.deepcopy(self.data[0,:,:].squeeze())
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(data.mean(),0))

        #1D
        data = copy.deepcopy(self.data[0,0,:].squeeze())
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(data.mean(),0))

    def test_submean_ndarray_not_overwrite(self):

        #3D
        data = copy.deepcopy(self.data)
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(np.allclose(out.mean(),0))

        #2D
        data = copy.deepcopy(self.data[0,:,:].squeeze())
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(np.allclose(out.mean(),0))

        #1D
        data = copy.deepcopy(self.data[0,0,:].squeeze())
        out = sub_mean_over_range(data, rng=[5,8], f=self.freq, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(np.allclose(out.mean(),0))


#    print('\n3D----------')
#    print('Initial mean: {}'.format(hs.data.mean()))
#
#    print('Final mean: {}\n'.format(hs.data.mean()))
#
#    print('2D----------')
#    print('Initial mean: {}'.format(spa.data.mean()))
#    out = sub_mean_over_range(spa, [5,8], overwrite=True)
#    print('Final mean: {}\n'.format(spa.data.mean()))
#
#    print('1D----------')
#    print('Initial mean: {}'.format(sp.data.mean()))
#    out = sub_mean_over_range(sp, [5,8], overwrite=True)
#    print('Final mean: {}'.format(sp.data.mean()))
#    def test_Freq_no_inputs(self):