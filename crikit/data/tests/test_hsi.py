# -*- coding: utf-8 -*-
"""
Test crikit.data.hsi.Hsi

Created on Tue Apr 12 14:17:37 2016

@author: chc
"""

import unittest
import crikit.data.frequency as freq
import crikit.data.hsi as hsi
import crikit.data.replicate as replicate

import numpy as np

class HsiTest(unittest.TestCase):
    def setUp(self):
        self.x = np.linspace(0,100,10)
        self.x_rep = replicate.Replicate(data=self.x)
        self.x_rep.update_calib_from_data()

        self.y = np.linspace(0,100,10)
        self.y_rep = replicate.Replicate(data=self.y)
        self.y_rep.update_calib_from_data()

        self.freq = np.arange(20)
        self.data = np.random.rand(10,10,20)

        self.units = 'Intensity (au)'
        self.label = 'Test label'


    def test_Hsi_no_inputs(self):
        hsi.Hsi()

    def test_Hsi_proper_inputs(self):
        hs = hsi.Hsi(data=self.data,freq=self.freq,x=self.x,y=self.y,
                     x_rep=self.x_rep, y_rep=self.y_rep, label=self.label,
                     units=self.units, meta={})
        hs = hsi.Hsi(data=self.data,freq=self.freq,x_rep=self.x_rep,y_rep=self.y_rep,
                     label=self.label,units=self.units)
        self.assertTrue(np.allclose(hs.x,self.x))
        hs = hsi.Hsi(data=self.data,freq=self.freq,x_rep=self.x,y_rep=self.y,
                     label=self.label,units=self.units)
        self.assertTrue(np.allclose(hs.data,self.data))
        self.assertEqual(hs.shape, self.data.shape)
    def test_Hsi_wrong_input(self):
        self.assertRaises(TypeError, hsi.Hsi, data = [])
        self.assertRaises(TypeError, hsi.Hsi, data = np.ones((10)))

    def test_Hsi_NotImplemented(self):
        pass