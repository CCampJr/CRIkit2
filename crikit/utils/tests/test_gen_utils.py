# -*- coding: utf-8 -*-
"""
Test general utilities

Created on Tue Apr 12 23:47:08 2016

@author: chc
"""

import unittest
from crikit.utils.gen_utils import find_nearest

import copy
import numpy as np

class TestGenUtils(unittest.TestCase):
    def setUp(self):
        self.x = np.linspace(0,100,10)

    def test_find_nearest(self):
        val, ind = find_nearest(self.x, 0)
        self.assertEqual(val,0)
        self.assertEqual(ind,0)

        val, ind = find_nearest(self.x, 100)
        self.assertEqual(val,100)
        self.assertEqual(ind,9)

        val, ind = find_nearest(self.x, [0,2,3])
        val, ind = find_nearest(self.x, [])
        self.assertIsNone(val)
        self.assertIsNone(ind)
        val, ind = find_nearest(self.x, np.array([0,2,3]))