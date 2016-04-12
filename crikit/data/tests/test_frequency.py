# -*- coding: utf-8 -*-
"""
Test crikit.data.frequency.Frequency and associated function

Created on Sat Apr  9 13:48:29 2016

@author: chc
"""

import unittest
import crikit.data.frequency as freq
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

        self.freq_vec = np.linspace(1,1000)

        self.fcn = freq.calib_pix_wl

        self.units = 'nm'

    def test_Freq_no_inputs(self):
        freq.Frequency()

    def test_Freq_wrong_input_types(self):
        self.assertRaises(TypeError, freq.Frequency, freq_vec = [])
        self.assertRaises(TypeError, freq.Frequency, freq_vec = np.ones((10,10)))

        self.assertRaises(TypeError, freq.Frequency, calib = [])
        self.assertRaises(TypeError, freq.Frequency, calib_orig = [])
        self.assertRaises(TypeError, freq.Frequency, calib_fcn = [])
        self.assertRaises(TypeError, freq.Frequency, units = [])

    def test_Freq_proper_inputs(self):
        frq = freq.Frequency(freq_vec=self.freq_vec, calib=self.calib_dict,
                             calib_orig=self.calib_dict, calib_fcn=self.fcn,
                             units=self.units)
        self.assertTrue(np.allclose(self.freq_vec,frq.freq_vec))
        self.assertDictEqual(self.calib_dict,frq.calib)
        self.assertDictEqual(self.calib_dict,frq.calib_orig)
        self.assertEqual(self.units, frq.units)
        self.assertEqual(self.fcn, frq.calib_fcn)
        frq = freq.Frequency(calib=self.calib_dict,
                     calib_fcn=freq.calib_pix_wl, units=self.units)
        self.assertAlmostEqual(frq.freq_vec.min(), 600, delta=100)
        self.assertAlmostEqual(frq.freq_vec.max(), 860, delta=100)
        frq.update()

    def test_Freq_size(self):
        frq = freq.Frequency(calib=self.calib_dict,
             calib_fcn=freq.calib_pix_wl, units=self.units)
        self.assertEqual(frq.size,self.calib_dict['n_pix'])

    def test_Freq_pix_vec(self):
        frq = freq.Frequency(calib=self.calib_dict,
             calib_fcn=freq.calib_pix_wl, units=self.units)
        self.assertTrue(np.allclose(frq.pix_vec,np.arange(self.calib_dict['n_pix'])))

    def test_Freq_update(self):
        frq = freq.Frequency()
        self.assertRaises(TypeError, frq.update)
        frq = freq.Frequency(calib=self.calib_dict)
        self.assertRaises(TypeError, frq.update)
        frq = freq.Frequency(calib_fcn=self.fcn)
        self.assertRaises(TypeError, frq.update)
        frq = freq.Frequency(calib_orig=self.calib_dict, calib_fcn=self.fcn)
        frq.update()
        self.assertDictEqual(frq.calib, frq.calib_orig)

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
        self.assertRaises(TypeError,freq.calib_pix_wl, {})

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
        self.assertRaises(KeyError,freq.calib_pix_wn, {})

        calib['units'] = 'um'
        wn_vec, units = freq.calib_pix_wn(calib)

        calib['units'] = 'mm'
        self.assertRaises(ValueError, freq.calib_pix_wn, calib)

    def test_Freq_Not_Implemented(self):
        frq = freq.Frequency()
        self.assertRaises(NotImplementedError,lambda:frq.op_range_pix)
        self.assertRaises(NotImplementedError, lambda:frq.op_range_freq)
        self.assertRaises(NotImplementedError, lambda:frq.plot_range_pix)
        self.assertRaises(NotImplementedError, lambda:frq.plot_range_freq)
