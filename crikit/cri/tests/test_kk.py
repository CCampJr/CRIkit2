# -*- coding: utf-8 -*-
"""
Test Kramers-Kronig

Created on Wed Apr 13 10:32:22 2016

@author: chc
"""

import unittest
from crikit.data.hsi import Hsi
from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
import crikit.data.frequency as freq
from crikit.cri.kk import kk
from crikit.cri.algorithms.kk import kkrelation
from crikit.utils.gen_utils import find_nearest

import copy
import numpy as np

class FreqTest(unittest.TestCase):

    def setUp(self):

        self.WN = np.linspace(-1386,3826,400)
        self.X = .055 + 1/(1000-self.WN-1j*20) + 1/(3000-self.WN-1j*20)
        self.XNR = 0*self.X + 0.055
        self.E = 1*np.exp(-(self.WN-2000)**2/(2*3000**2))

        # Simulated spectrum
        self.CARS = np.abs(self.E+self.X)**2
        self.NRB = np.abs(self.E+self.XNR)**2

    def test_kk_overwrite(self):
        self.cars3 = Hsi()
        self.cars2 = Spectra()
        self.cars1 = Spectrum()
        self.nrb1 = Spectrum()
        self.nrb2 = Spectra()

        self.cars3.data = np.dot(np.ones((10,10,1)),self.CARS[None,:])
        self.cars3.freq = self.WN

        self.cars2.data = np.dot(np.ones((10,1)),self.CARS[None,:])
        self.cars2.freq = self.WN

        self.cars1.data = self.CARS
        self.cars1.freq = self.WN

        self.nrb1.data = self.NRB
        self.nrb2.data = self.NRB

        out = kk(self.cars3,self.nrb1)
        self.assertIsNone(out)
        self.assertTrue(issubclass(self.cars3.data.dtype.type,np.complex))
        out = kk(self.cars2,self.nrb1)
        self.assertIsNone(out)
        out = kk(self.cars1,self.nrb1)
        self.assertIsNone(out)

        self.cars2.data = np.dot(np.ones((10,1)),self.CARS[None,:])
        self.cars2.freq = self.WN
        out = kk(self.cars2,self.nrb2)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(self.X.imag, self.cars1.data.imag,rtol=1))

    def test_kk_no_overwrite(self):
        self.cars3 = Hsi()
        self.cars2 = Spectra()
        self.cars1 = Spectrum()
        self.nrb1 = Spectrum()
        self.nrb2 = Spectra()

        self.cars3.data = np.dot(np.ones((10,10,1)),self.CARS[None,:])
        self.cars3.freq = self.WN

        self.cars2.data = np.dot(np.ones((10,1)),self.CARS[None,:])
        self.cars2.freq = self.WN

        self.cars1.data = self.CARS
        self.cars1.freq = self.WN

        self.nrb1.data = self.NRB
        self.nrb2.data = self.NRB

        out = kk(self.cars3,self.nrb1, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))

        out = kk(self.cars3,self.nrb1.data, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))

        out = kk(self.cars2,self.nrb1, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))

        out = kk(self.cars1,self.nrb1, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))
        self.assertTrue(np.allclose(self.X.imag, out.imag,rtol=1))

        self.cars2.data = np.dot(np.ones((100,1)),self.CARS[None,:])
        self.cars2.freq = self.WN
        out = kk(self.cars2,self.nrb2, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))

    def test_kk_pixrange(self):
        self.cars3 = Hsi()
        self.cars2 = Spectra()
        self.cars1 = Spectrum()
        self.nrb1 = Spectrum()
        self.nrb2 = Spectra()

        self.cars3.data = np.dot(np.ones((10,10,1)),self.CARS[None,:])
        self.cars3.freq = self.WN
        self.cars3.freq.op_list_freq = [500,4000]

        self.nrb1.data = self.NRB

        out = kk(self.cars3,self.nrb1, overwrite=False)
        self.assertIsNotNone(out)
        self.assertTrue(issubclass(out.dtype.type,np.complex))
        self.assertNotEqual(out.shape,self.cars3.shape)

        sh = self.cars3.shape
        out = kk(self.cars3,self.nrb1, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(issubclass(self.cars3.data.dtype.type,np.complex))
        self.assertEqual(sh,self.cars3.shape)
        self.assertTrue(np.allclose(self.X.imag[self.cars3.freq.op_range_pix],
                                    self.cars3.data[0,0,self.cars3.freq.op_range_pix].imag,rtol=1))

    def test_kk_wrong_inputs(self):
        self.cars3 = Hsi()
        self.cars2 = Spectra()
        self.cars1 = Spectrum()
        self.nrb1 = Spectrum()
        self.nrb2 = Spectra()

        self.cars3._data = np.random.rand(10,10,10,10)
        self.cars3.freq = self.WN
        self.nrb1.data = self.NRB

        self.assertRaises(TypeError,kk,self.cars3,self.nrb1,overwrite=False)

        self.cars3._data = np.random.rand(10,10,10,400)
        self.cars3.freq = self.WN
        self.nrb1.data = self.NRB

        self.assertRaises(NotImplementedError,kk,self.cars3,self.nrb1,overwrite=False)

    def test_kk_alg(self):
        self.cars3 = Hsi()
        self.cars2 = Spectra()
        self.cars1 = Spectrum()
        self.nrb1 = Spectrum()
        self.nrb2 = Spectra()

        self.cars3.data = np.dot(np.ones((10,10,1)),self.CARS[None,:])
        self.cars3.freq = self.WN

        self.cars2.data = np.dot(np.ones((10,1)),self.CARS[None,:])
        self.cars2.freq = self.WN

        self.cars1.data = self.CARS
        self.cars1.freq = self.WN

        self.nrb1.data = self.NRB
        self.nrb2.data = self.NRB

        out = kkrelation(self.nrb1.data,self.cars3.data)
        out = kkrelation(self.cars3.data,self.cars3.data)
        out = kkrelation(self.cars1.data,self.cars1.data)
        out = kkrelation(self.cars1.data,self.cars1.data, norm_by_bg=False)
#        self.assertIsNone(out)
#        self.assertTrue(issubclass(self.cars3.data.dtype.type,np.complex))
#        out = kk(self.cars2,self.nrb1)
#        self.assertIsNone(out)
#        out = kk(self.cars1,self.nrb1)
#        self.assertIsNone(out)
#
#        self.cars2.data = np.dot(np.ones((10,1)),self.CARS[None,:])
#        self.cars2.freq = self.WN
#        out = kk(self.cars2,self.nrb2)
#        self.assertIsNone(out)