# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 13:48:29 2016

@author: chc
"""

import unittest
import crikit.data.freq as freq
import copy
import numpy as np

class FreqTest(unittest.TestCase):
    def setUp(self):
        self.calib_dict = {}
        self.calib_dict['n_pix'] = 1600
        self.calib_dict['ctr_wl'] = 730.0
        self.calib_dict['ctr_wl0'] = 730.0
        self.calib_dict['probe'] = 771.461
        #self.calib_dict['units'] = 'nm'
        self.calib_dict['a_vec'] = (-0.167740721307557, 863.8736708961577)  # slope, intercept

    def test_Freq_no_inputs(self):
        self.assertRaises(TypeError, freq.Frequency)

    def test_Freq_calib_no_fcn(self):
        self.assertRaises(TypeError,freq.Frequency,calib=self.calib_dict)

    def test_Freq_calib_no_calib(self):
        self.assertRaises(TypeError,freq.Frequency,calib_fcn=freq.calib_pix_wl)

    def test_Freq_set_freq_vec(self):
        freq.Frequency(np.arange(100))
        freq.Frequency(np.arange(100), calib=self.calib_dict)
        freq.Frequency(np.arange(100), calib=self.calib_dict, calib_fcn=freq.calib_pix_wl)
        freq.Frequency(calib=self.calib_dict, calib_fcn=freq.calib_pix_wl)

    def test_Freq_update_err(self):
        self.assertRaises(TypeError, freq.Frequency(np.arange(100)).update)

    def test_Freq_update_err2(self):
        self.assertEqual(0,freq.Frequency(np.arange(100)).freq_vec[0])

    def test_Freq_change_dict(self):
        calib = copy.deepcopy(self.calib_dict)

        frq = freq.Frequency(calib=calib, calib_fcn=freq.calib_pix_wn)
        frq_1 = copy.deepcopy(frq)
        calib['n_pix'] = 4e3
        frq.calib = calib
        frq.update()
        self.assertNotEqual(frq_1.freq_vec[-1],frq.freq_vec[-1])
        self.assertEqual(frq_1.freq_vec[0],frq.freq_vec[0])
        self.assertNotEqual(frq_1.freq_vec.size,frq.freq_vec.size)
        self.assertNotEqual(frq_1.size,frq.size)
        del frq.calib_fcn
        self.assertRaises(TypeError, frq.update)
        frq.calib = freq.calib_pix_wn
        del frq.calib_orig
        del frq.calib
        frq.update()

    def test_calib_pix_wl_dict(self):
        wl_vec, units = freq.calib_pix_wl(self.calib_dict)
        self.assertEqual(wl_vec.size,1600)
        self.assertAlmostEqual(wl_vec.min(), 600, delta=100)
        self.assertAlmostEqual(wl_vec.max(), 860, delta=100)
        self.assertEqual(units,'nm')

    def test_calib_pix_wl_dict_err(self):
        calib = copy.deepcopy(self.calib_dict)
        calib['units'] = 'nm'
        wl_vec, units = freq.calib_pix_wl(calib)
        self.assertRaises(TypeError,freq.calib_pix_wl)
        calib.pop('n_pix')
        self.assertRaises(KeyError,freq.calib_pix_wl, calib)
        #calib.pop('ctr_wl')
        #self.assertRaises(TypeError,freq.calib_pix_wl, calib)

    def test_calib_pix_wn_dict(self):
        wn_vec, units = freq.calib_pix_wn(self.calib_dict)
        self.assertEqual(wn_vec.size,1600)
        self.assertAlmostEqual(wn_vec.min(), -1300, delta=100)
        self.assertAlmostEqual(wn_vec.max(), 3800, delta=100)
        self.assertEqual(units,'cm$^{-1}$')

    def test_calib_pix_wn_dict_err(self):
        calib = copy.deepcopy(self.calib_dict)
        calib['units'] = 'nm'

        wn_vec, units = freq.calib_pix_wn(calib)
        self.assertRaises(TypeError,calib)
        self.calib_dict.pop('n_pix')
        self.assertRaises(KeyError,freq.calib_pix_wn, self.calib_dict)

        calib['units'] = 'um'
        wn_vec, units = freq.calib_pix_wn(calib)

        calib['units'] = 'mm'
        self.assertRaises(ValueError, freq.calib_pix_wn, calib)

