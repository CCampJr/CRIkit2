# -*- coding: utf-8 -*-
"""
Test crikit.data.replicate.Replicate

Created on Tue Apr 12 12:32:26 2016

@author: chc
"""

import unittest
import crikit.data.replicate as rep
import copy
import numpy as np

class ReplicateTest(unittest.TestCase):
    def setUp(self):
        self.start = 0
        self.stop = 10
        self.step_size = .1

        self.x = np.arange(self.start, self.stop, self.step_size)
        self.calib = [self.start, self.stop, self.step_size]
        self.units = 'mm'

    def test_Replicate_no_inputs(self):
        rep.Replicate()

    def test_Replicate_wrong_input_types(self):
        self.assertRaises(TypeError, rep.Replicate, data = [])
        self.assertRaises(TypeError, rep.Replicate, data = np.ones((10,10)))
        self.assertRaises(TypeError, rep.Replicate, data = {})

        self.assertRaises(TypeError, rep.Replicate, calib = [])
        self.assertRaises(TypeError, rep.Replicate, calib = {})
        self.assertRaises(TypeError, rep.Replicate, units = [])


        rp = rep.Replicate(calib=self.calib)
        self.assertRaises(TypeError, rp.calib_data_agree)

        rp = rep.Replicate(data=self.x)
        self.assertRaises(TypeError, rp.calib_data_agree)


    def test_Replicate_proper_inputs(self):
        rp = rep.Replicate(data=self.x, calib=self.calib, units=self.units)
        self.assertTrue(rp.calib_data_agree())
        rp = rep.Replicate(calib=10, units=self.units)
        self.assertEqual(rp.calib,[0,10,1])
        rp = rep.Replicate(calib=[10], units=self.units)
        self.assertEqual(rp.calib,[0,10,1])
        rp = rep.Replicate(calib=[0, 10], units=self.units)
        self.assertEqual(rp.calib,[0,10,1])
        rp = rep.Replicate(data=self.x, calib=[0, 10], units=self.units)
        self.assertFalse(rp.calib_data_agree())
        self.assertEqual(self.units,rp.units)

    def test_Replicate_data_from_calib(self):
        rp = rep.Replicate(calib=self.calib, units=self.units)
        rp.update_data_from_calib()
        self.assertTrue(np.allclose(self.x,rp.data))

    def test_Replicate_calib_from_data(self):
        rp = rep.Replicate(data=self.x, units=self.units)
        rp.update_calib_from_data()
        self.assertEqual(self.calib,rp.calib)

    def test_Replicate_update_err(self):
        rp = rep.Replicate()
        self.assertRaises(TypeError, rp.update_calib_from_data)
        self.assertRaises(TypeError, rp.update_data_from_calib)


    def test_Replicate_size(self):
        rp = rep.Replicate(data=self.x, calib=self.calib, units=self.units)
        self.assertEqual(rp.size,self.x.size)
