# -*- coding: utf-8 -*-
"""
Test denoise

Created on Sat Apr 23 01:14:16 2016

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

from crikit.preprocess.denoise import svd

class SVDTest(unittest.TestCase):

    def setUp(self):
        self.signal2D = np.random.randn(100,1000)
        self.signal3D = np.random.randn(10,10,1000)
        self.signal2D_obj = Spectra(self.signal2D)
        self.signal3D_obj = Hsi(self.signal3D)

    def test_basic(self):
        output, [U,s,Vh] = svd(self.signal2D)
        self.assertTrue(np.allclose(output,np.dot(U,np.dot(np.diag(s),Vh))))

    def test_no_svs(self):
        # ndarray
        output, _ = svd(self.signal2D,svs=[])
        self.assertTrue(np.allclose(output,0))
        self.assertTrue(self.signal2D.shape==output.shape)

        # Spectra
        output, _ = svd(self.signal2D_obj,svs=[])
        self.assertTrue(np.allclose(output,0))
        self.assertTrue(self.signal2D.shape==output.shape)

        # Hsi
        output, _ = svd(self.signal3D_obj,svs=[])
        self.assertTrue(np.allclose(output,0))
        self.assertTrue(self.signal3D.shape==output.shape)

    def test_1_svs(self):
        output, _ = svd(self.signal2D,svs=[0])
        self.assertFalse(np.allclose(output,0))
        self.assertTrue(np.isclose(np.median(output[0,:]/output[50,:]),output[0,0]/output[50,0]))

    def test_shape(self):
        output, _ = svd(self.signal2D,svs=[])
        self.assertTrue(self.signal2D.shape==output.shape)

        output3D, _ = svd(self.signal3D,svs=[])
        self.assertTrue(self.signal3D.shape==output3D.shape)

    def test_overwrite(self):
        #ndarray
        signal2D_copy = copy.deepcopy(self.signal2D)
        signal3D_copy = copy.deepcopy(self.signal3D)
        self.assertTrue(np.allclose(self.signal2D,signal2D_copy))
        self.assertTrue(np.allclose(self.signal3D,signal3D_copy))
        _ = svd(self.signal2D,svs=[],overwrite=True)
        _ = svd(self.signal3D,svs=[],overwrite=True)
        self.assertFalse(np.allclose(self.signal2D,signal2D_copy))
        self.assertFalse(np.allclose(self.signal3D,signal3D_copy))
        self.assertTrue(np.allclose(self.signal2D,0))
        self.assertTrue(np.allclose(self.signal3D,0))

        #Spectra
        signal2D_obj_copy = copy.deepcopy(self.signal2D_obj)
        signal3D_obj_copy = copy.deepcopy(self.signal3D_obj)

        self.assertTrue(np.allclose(self.signal2D_obj.data,signal2D_obj_copy.data))
        self.assertTrue(np.allclose(self.signal3D_obj.data,signal3D_obj_copy.data))

        self.assertFalse(np.allclose(self.signal2D_obj.data,0))
        self.assertFalse(np.allclose(self.signal3D_obj.data,0))

        _ = svd(self.signal2D_obj,svs=[],overwrite=True)
        _ = svd(self.signal3D_obj,svs=[],overwrite=True)

        self.assertFalse(np.allclose(self.signal2D_obj.data,signal2D_obj_copy.data))
        self.assertFalse(np.allclose(self.signal3D_obj.data,signal3D_obj_copy.data))
        self.assertTrue(np.allclose(self.signal2D_obj.data,0))
        self.assertTrue(np.allclose(self.signal3D_obj.data,0))

    def test_err(self):
        signal1d = np.random.randn(100)
        signal1d_obj = Spectrum()
        self.assertRaises(TypeError, svd, signal1d)
        self.assertRaises(TypeError, svd, signal1d_obj)
        self.assertRaises(TypeError, svd, [])
        #_ = svd(self.signal2D,svs=[],overwrite=True)
