# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 08:56:31 2016

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

from crikit.preprocess.standardize import anscombe, anscombe_inverse

class AnscTest(unittest.TestCase):

    def setUp(self):
        self.stddev = 20
        self.gain = 1

        self.f = np.linspace(500,4000,1000)
        self.sig = 10e4*np.exp(-(self.f-2000)**2/(500**2))

        self.gnoise = self.stddev*np.random.randn(self.f.size)

        self.sig_mix = np.random.poisson(self.sig) + self.gnoise
#        sig_mix_ansc = anscombe(sig_mix, gauss_std=stddev, poisson_multi=gain)
#        sig_ansc = anscombe(sig, gauss_std=stddev, poisson_multi=gain)

    def test_forward_np(self):
        # No overwrite
        sig_ansc = anscombe(self.sig, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        sig_mix_ansc = anscombe(self.sig_mix, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        self.assertAlmostEqual((sig_mix_ansc - sig_ansc).mean(),0,places=0)
        self.assertAlmostEqual((sig_mix_ansc - sig_ansc).std(),1,places=0)

        # overwrite
        out = anscombe(self.sig, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(self.sig,sig_ansc))

        out = anscombe(self.sig_mix, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(self.sig_mix,sig_mix_ansc))

    def test_inverse_np(self):
        # No overwrite
        sig_ansc = anscombe(self.sig, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        sig_ansc_inverted = anscombe_inverse(sig_ansc, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)

        self.assertTrue(np.allclose(self.sig,sig_ansc_inverted, rtol=1))

        # Overwrite
        out = anscombe_inverse(sig_ansc, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(self.sig,sig_ansc, rtol=1))

    def test_forward_Spectrum(self):
        # No overwrite
        sp = Spectrum(self.sig)
        sp_mix = Spectrum(self.sig_mix)
        sig_ansc = anscombe(sp.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        sig_mix_ansc = anscombe(sp_mix.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        self.assertAlmostEqual((sig_mix_ansc - sig_ansc).mean(),0,places=0)
        self.assertAlmostEqual((sig_mix_ansc - sig_ansc).std(),1,places=0)

        # overwrite
        out = anscombe(sp.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(sig_ansc,sp.data))

        out = anscombe(sp_mix.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(sig_mix_ansc,sp_mix.data))


    def test_inverse_Spectrum(self):
        sp = Spectrum(self.sig)

        sp_ansc = Spectrum()
        sp_ansc_inverted = Spectrum()

        # No overwrite
        sp_ansc.data = anscombe(sp.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)
        sp_ansc_inverted.data = anscombe_inverse(sp_ansc.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=False)

        self.assertTrue(np.allclose(self.sig,sp_ansc_inverted.data, rtol=1))

        # Overwrite
        out = anscombe_inverse(sp_ansc.data, gauss_std=self.stddev, poisson_multi=self.gain, overwrite=True)
        self.assertIsNone(out)
        self.assertTrue(np.allclose(self.sig,sp_ansc.data, rtol=1))

    def test_forward_wrong(self):
        self.assertRaises(TypeError, anscombe, data_obj={}, gauss_std=20)

    def test_inverse_wrong(self):
        self.assertRaises(TypeError, anscombe_inverse, data_obj={}, gauss_std=20)