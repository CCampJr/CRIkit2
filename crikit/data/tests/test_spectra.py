# -*- coding: utf-8 -*-
"""
Test crikit.data.spectra.Spectra

Created on Mon Apr 11 12:50:44 2016

@author: chc
"""

import unittest
import crikit.data.frequency as freq
import crikit.data.spectra as spectra

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
        self.data1 = np.random.rand(self.freq_vec.size)
        self.data2 = np.random.rand(10,self.freq_vec.size)
        self.data3 = np.random.rand(10,10,self.freq_vec.size)

        self.fcn = freq.calib_pix_wl

        self.units = 'Intensity (au)'
        self.label = 'Test label'


    def test_Spectra_no_inputs(self):
        sp = spectra.Spectra()
        sp.freq.calib = self.calib_dict
        sp.freq.calib_fcn = freq.calib_pix_wn
        frq = freq.Frequency()
        frq.calib = self.calib_dict
        frq.calib_fcn = freq.calib_pix_wn
        frq.update()
        sp = spectra.Spectra(freq=frq)
        self.assertRaises(TypeError, spectra.Spectra, freq=[])

    def test_Spectra_proper_inputs(self):
        frq = freq.Frequency(freq_vec=self.freq_vec)

        sp = spectra.Spectra(data = self.data1, freq=frq,
                               units=self.units, label=self.label)
        self.assertTrue(np.allclose(self.data1, sp.data))
        self.assertTrue(np.allclose(self.freq_vec, sp.freq.freq_vec))
        self.assertEqual(sp.f_pix, self.freq_vec.size)
        self.assertEqual(sp.n_pix, 1)
        sp = spectra.Spectra(data = self.freq_vec, freq=self.freq_vec,
                               units=self.units, label=self.label)
        self.assertEqual(self.units, sp.units)
        self.assertEqual(self.label, sp.label)

    def test_Spectra_dimensionality(self):
        # Dimensionality tests
        sp = spectra.Spectra(data = self.data2, freq=self.freq_vec,
                             units=self.units, label=self.label)
        self.assertTrue(np.allclose(self.data2, sp.data))

        sp = spectra.Spectra(data = self.data3, freq=self.freq_vec,
                             units=self.units, label=self.label)
        self.assertTrue(np.allclose(self.data3.reshape((-1, self.freq_vec.size)), sp.data))


    def test_Spectra_input_types(self):
        self.assertRaises(TypeError, spectra.Spectra, data=[])
        spectra.Spectra(data=np.random.rand(100))
        spectra.Spectra(data=None)
        self.assertRaises(TypeError, spectra.Spectra, freq=[])
        sp = spectra.Spectra()
        self.assertRaises(TypeError, spectra.Spectra, label=[])
        self.assertRaises(TypeError, spectra.Spectra, units=[])
        self.assertRaises(TypeError, spectra.Spectra, meta=[])
        spectra.Spectra(meta={})
        sp = spectra.Spectra(meta=self.calib_dict)
        sp.meta['test'] = 5
        self.assertEqual(sp.meta['test'],5)
        self.assertDictContainsSubset(self.calib_dict,sp.meta)

    def test_Spectra_NotImplemented(self):
        sp = spectra.Spectra()
        self.assertIsNone(sp.reps)
