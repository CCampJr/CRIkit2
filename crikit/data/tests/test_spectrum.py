# -*- coding: utf-8 -*-
"""
Test crikit.data.spectrum.Spectrum

Created on Mon Apr 11 12:50:44 2016

@author: chc
"""

import unittest
import crikit.data.frequency as freq
import crikit.data.spectrum as spectrum

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

        self.freq_vec = np.linspace(1,1000)

        self.fcn = freq.calib_pix_wl

        self.units = 'Intensity (au)'
        self.label = 'Test label'


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

    def test_Spectrum_proper_inputs(self):
        frq = freq.Frequency(freq_vec=self.freq_vec)

        # Using freq_vec as the data as well
        sp = spectrum.Spectrum(data = self.freq_vec, freq=frq,
                               units=self.units, label=self.label)
        self.assertTrue(np.allclose(self.freq_vec, sp.data))
        self.assertTrue(np.allclose(self.freq_vec, sp.freq.freq_vec))
        self.assertEqual(sp.f_pix, self.freq_vec.size)
        sp = spectrum.Spectrum(data = self.freq_vec, freq=self.freq_vec,
                               units=self.units, label=self.label)
        self.assertEqual(self.units, sp.units)
        self.assertEqual(self.label, sp.label)


    def test_Spectrum_input_types(self):
        self.assertRaises(TypeError, spectrum.Spectrum, data=[])
        self.assertRaises(TypeError, spectrum.Spectrum, data=np.random.rand(10,10))
        spectrum.Spectrum(data=np.random.rand(100))
        spectrum.Spectrum(data=None)
        self.assertRaises(TypeError, spectrum.Spectrum, freq=[])
        sp = spectrum.Spectrum()
        self.assertRaises(TypeError, spectrum.Spectrum, label=[])
        self.assertRaises(TypeError, spectrum.Spectrum, units=[])
        self.assertRaises(TypeError, spectrum.Spectrum, meta=[])
        spectrum.Spectrum(meta={})
        sp = spectrum.Spectrum(meta=self.calib_dict)
        sp.meta['test'] = 5
        self.assertEqual(sp.meta['test'],5)
        self.assertDictContainsSubset(self.calib_dict,sp.meta)
