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

from crikit.preprocess.denoise import svd_decompose, svd_recompose

class SVDDecomposeTest(unittest.TestCase):

    def setUp(self):
        self.signal2D = np.random.randn(100,1000)
        self.signal3D = np.random.randn(10,10,1000)
        self.signal2D_obj = Spectra(self.signal2D)
        self.signal3D_obj = Hsi(self.signal3D)

    def test_basic(self):
        [U,s,Vh] = svd_decompose(self.signal2D)
        output = np.dot(U,np.dot(np.diag(s),Vh))
        self.assertTrue(np.allclose(output,np.dot(U,np.dot(np.diag(s),Vh))))

    def test_no_svs(self):
        # ndarray
        [U,s,Vh] = svd_decompose(self.signal2D)
        s2 = np.zeros(s.shape)
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertTrue(np.allclose(output,0))
        self.assertTrue(self.signal2D.shape==output.shape)

        # Spectra
        [U,s,Vh] = svd_decompose(self.signal2D_obj)
        s2 = np.zeros(s.shape)
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertTrue(np.allclose(output,0))
        self.assertTrue(self.signal2D.shape==output.shape)

        # Hsi
        [U,s,Vh] = svd_decompose(self.signal3D_obj)
        s2 = np.zeros(s.shape)
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertTrue(np.allclose(output,0))
        self.assertFalse(self.signal3D.shape==output.shape)

    def test_1_svs(self):
        [U,s,Vh] = svd_decompose(self.signal2D)
        s2 = np.zeros(s.shape)
        s2[0] = s[0]
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertFalse(np.allclose(output,0))
        self.assertTrue(np.isclose(np.median(output[0,:]/output[50,:]),output[0,0]/output[50,0]))

    def test_shape(self):
        [U,s,Vh] = svd_decompose(self.signal2D)
        s2 = np.zeros(s.shape)
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertTrue(self.signal2D.shape==output.shape)

        [U,s,Vh] = svd_decompose(self.signal3D)
        s2 = np.zeros(s.shape)
        output = np.dot(U,np.dot(np.diag(s2),Vh))
        self.assertTrue(output.ndim==2)
        self.assertFalse(self.signal3D.shape==output.shape)

    def test_err(self):
        signal1d = np.random.randn(100)
        signal1d_obj = Spectrum()
        self.assertRaises(TypeError, svd_decompose, signal1d)
        self.assertRaises(TypeError, svd_decompose, signal1d_obj)
        self.assertRaises(TypeError, svd_decompose, [])

class SVDRecomposeTest(unittest.TestCase):

    def setUp(self):
        self.signal2D = np.random.randn(100,1000)
        self.signal3D = np.random.randn(10,10,1000)
        self.signal2D_obj = Spectra(self.signal2D)
        self.signal3D_obj = Hsi(self.signal3D)
        [self.U2,self.s2,self.Vh2] = svd_decompose(self.signal2D)
        [self.U3,self.s3,self.Vh3] = svd_decompose(self.signal2D)

    def test_basic(self):
        output = svd_recompose(self.U2,self.s2,self.Vh2)
        output2 = np.dot(self.U2,np.dot(np.diag(self.s2),self.Vh2))
        self.assertTrue(np.allclose(output,output2))

        output = svd_recompose(self.U2,np.diag(self.s2),self.Vh2)
        output2 = np.dot(self.U2,np.dot(np.diag(self.s2),self.Vh2))
        self.assertTrue(np.allclose(output,output2))


        output = svd_recompose(self.U3,self.s3,self.Vh3)
        output2 = np.dot(self.U3,np.dot(np.diag(self.s3),self.Vh3))
        self.assertTrue(np.allclose(output,output2))
        self.assertFalse(output.shape == self.signal3D.shape)

        output = svd_recompose(self.U3,self.s3,self.Vh3, data_obj=self.signal3D)
        output2 = np.dot(self.U3,np.dot(np.diag(self.s3),self.Vh3))
        self.assertTrue(np.allclose(output.ravel(),output2.ravel()))
        self.assertTrue(output.shape == self.signal3D.shape)

    def test_svs(self):
        output = svd_recompose(self.U2,self.s2,self.Vh2,svs=[0])
        self.assertFalse(np.allclose(output,0))
        self.assertTrue(np.isclose(np.median(output[0,:]/output[50,:]),output[0,0]/output[50,0]))

    def test_overwrite(self):
        output = svd_recompose(self.U3,self.s3,self.Vh3,
                               data_obj=self.signal3D, svs=[], overwrite=True)
        self.assertIsNone(output)
        self.assertTrue(np.allclose(self.signal3D,0))
        output = svd_recompose(self.U3,self.s3,self.Vh3,
                               data_obj=self.signal3D_obj, svs=[], overwrite=True)

    def test_err(self):
        self.assertRaises(TypeError, svd_recompose, self.U2, np.random.randn(10,10,10), self.Vh2)
        self.assertRaises(TypeError, svd_recompose, [], self.s2, self.Vh2)
        self.assertRaises(TypeError, svd_recompose, self.U2, [], self.Vh2)
        self.assertRaises(TypeError, svd_recompose, self.U2, self.s2, [])
        self.assertRaises(TypeError, svd_recompose, self.U2, self.s2, self.Vh2,
                          overwrite=True, data_obj=[])

#    def test_no_svs(self):
#        # ndarray
#        [U,s,Vh] = svd_decompose(self.signal2D)
#        s2 = np.zeros(s.shape)
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertTrue(np.allclose(output,0))
#        self.assertTrue(self.signal2D.shape==output.shape)
#
#        # Spectra
#        [U,s,Vh] = svd_decompose(self.signal2D_obj)
#        s2 = np.zeros(s.shape)
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertTrue(np.allclose(output,0))
#        self.assertTrue(self.signal2D.shape==output.shape)
#
#        # Hsi
#        [U,s,Vh] = svd_decompose(self.signal3D_obj)
#        s2 = np.zeros(s.shape)
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertTrue(np.allclose(output,0))
#        self.assertFalse(self.signal3D.shape==output.shape)
#
#    def test_1_svs(self):
#        [U,s,Vh] = svd_decompose(self.signal2D)
#        s2 = np.zeros(s.shape)
#        s2[0] = s[0]
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertFalse(np.allclose(output,0))
#        self.assertTrue(np.isclose(np.median(output[0,:]/output[50,:]),output[0,0]/output[50,0]))
#
#    def test_shape(self):
#        [U,s,Vh] = svd_decompose(self.signal2D)
#        s2 = np.zeros(s.shape)
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertTrue(self.signal2D.shape==output.shape)
#
#        [U,s,Vh] = svd_decompose(self.signal3D)
#        s2 = np.zeros(s.shape)
#        output = np.dot(U,np.dot(np.diag(s2),Vh))
#        self.assertTrue(output.ndim==2)
#        self.assertFalse(self.signal3D.shape==output.shape)

#    def test_overwrite(self):
#        #ndarray
#        signal2D_copy = copy.deepcopy(self.signal2D)
#        signal3D_copy = copy.deepcopy(self.signal3D)
#        self.assertTrue(np.allclose(self.signal2D,signal2D_copy))
#        self.assertTrue(np.allclose(self.signal3D,signal3D_copy))
#        _ = svd_decompose(self.signal2D,svs=[],overwrite=True)
#        _ = svd_decompose(self.signal3D,svs=[],overwrite=True)
#        self.assertFalse(np.allclose(self.signal2D,signal2D_copy))
#        self.assertFalse(np.allclose(self.signal3D,signal3D_copy))
#        self.assertTrue(np.allclose(self.signal2D,0))
#        self.assertTrue(np.allclose(self.signal3D,0))
#
#        #Spectra
#        signal2D_obj_copy = copy.deepcopy(self.signal2D_obj)
#        signal3D_obj_copy = copy.deepcopy(self.signal3D_obj)
#
#        self.assertTrue(np.allclose(self.signal2D_obj.data,signal2D_obj_copy.data))
#        self.assertTrue(np.allclose(self.signal3D_obj.data,signal3D_obj_copy.data))
#
#        self.assertFalse(np.allclose(self.signal2D_obj.data,0))
#        self.assertFalse(np.allclose(self.signal3D_obj.data,0))
#
#        _ = svd_decompose(self.signal2D_obj,svs=[],overwrite=True)
#        _ = svd_decompose(self.signal3D_obj,svs=[],overwrite=True)
#
#        self.assertFalse(np.allclose(self.signal2D_obj.data,signal2D_obj_copy.data))
#        self.assertFalse(np.allclose(self.signal3D_obj.data,signal3D_obj_copy.data))
#        self.assertTrue(np.allclose(self.signal2D_obj.data,0))
#        self.assertTrue(np.allclose(self.signal3D_obj.data,0))


# _ = svd_decompose(self.signal2D,svs=[],overwrite=True)