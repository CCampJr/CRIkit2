# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:50:44 2016

@author: chc
"""

import unittest
import crikit.data.freq as freq
import crikit.data.spectrum as spectrum

import copy
import numpy as np

class SpectrumTest(unittest.TestCase):
    def setUp(self):
        self.calib_dict = {}
        self.calib_dict['n_pix'] = 1600
        self.calib_dict['ctr_wl'] = 730.0
        self.calib_dict['ctr_wl0'] = 730.0
        self.calib_dict['probe'] = 771.461
        #self.calib_dict['units'] = 'nm'
        self.calib_dict['a_vec'] = (-0.167740721307557, 863.8736708961577)  # slope, intercept


    def test_Spectrum_no_inputs(self):
        sp = spectrum.Spectrum()
        sp.freq.calib = self.calib_dict
        sp.freq.calib_fcn = freq.calib_pix_wn
        frq = freq.Frequency()
        frq.calib = self.calib_dict
        frq.calib_fcn = freq.calib_pix_wn
        frq.update()
        sp = spectrum.Spectrum(freq=frq)
        self.assertRaises(TypeError, spectrum.Spectrum, freq=[])

    def test_Spectrum_input_types(self):
        self.assertRaises(TypeError, spectrum.Spectrum, data=[])
        self.assertRaises(TypeError, spectrum.Spectrum, data=np.random.rand(10,10))
        spectrum.Spectrum(data=np.random.rand(100))
        spectrum.Spectrum(data=None)
        self.assertRaises(TypeError, spectrum.Spectrum, freq=[])
        self.assertRaises(TypeError, spectrum.Spectrum, label=[])
        self.assertRaises(TypeError, spectrum.Spectrum, units=[])
        self.assertRaises(TypeError, spectrum.Spectrum, meta=[])
        spectrum.Spectrum(meta={})