# -*- coding: utf-8 -*-
"""

Full blown run-through with real data

Created on Mon Jun  6 23:56:10 2016

@author: chc
"""

import numpy as _np
#import matplotlib.pyplot as plt
import os
import sys
import timeit

sys.path.append(os.path.abspath('../../'))
#sys.path.append(os.path.abspath('../../..'))

from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

from crikit.io.macros import import_hdf_nist_special as io_nist
from crikit.preprocess.subtract_dark import sub_dark
from crikit.preprocess.subtract_mean import sub_mean_over_range as sub_residual

from crikit.preprocess.standardize import anscombe, anscombe_inverse
from crikit.preprocess.denoise import svd_decompose, svd_recompose

from crikit.cri.kk import kk

from crikit.cri.error_correction import phase_err_correct_als, scale_err_correct_sg

filename = '../../../mP2_w_small.h5'
#dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small'
dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0'

dset_dark = '/Spectra/Dark_3_5ms_2'
dset_nrb = '/Spectra/CoverslipNRB_Time0_3_5ms_2'

cars = Hsi()
nrb = Spectra()
dark = Spectra()


io_nist(filename, dset, cars)
io_nist(filename, dset_dark, dark)
io_nist(filename, dset_nrb, nrb)

tmr0 = timeit.default_timer()
tmr = timeit.default_timer()
# Dark subtract
sub_dark(cars.data, dark.data, overwrite=True)
sub_dark(nrb.data, dark.data, overwrite=True)
tmr -= timeit.default_timer()
print('Dark subtraction: {:.3g} sec'.format(-tmr))

# Subtract residual dark (sub dark over range)
tmr = timeit.default_timer()
rng = cars.freq.get_index_of_closest_freq([-5000, -500])
sub_residual(cars.data, rng, overwrite=True)
sub_residual(nrb.data, rng, overwrite=True)
tmr -= timeit.default_timer()
print('Residual subtraction: {:.3g} sec'.format(-tmr))

# Set operating range
print('Setting range...')
cars.freq.op_list_freq = [500, 4000]
rng = cars.freq.op_range_pix
print('Range set...')

# Anscombe
print('Starting Anscombe...')
tmr = timeit.default_timer()
anscombe(cars.data, gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4,
         rng=rng, overwrite=True)
tmr -= timeit.default_timer()
print('Anscombe: {:.3g} sec'.format(-tmr))

# SVD
print('Starting SVD Decompose...')
tmr = timeit.default_timer()
U, s, Vh = svd_decompose(cars.data, rng=rng)
tmr -= timeit.default_timer()
print('SVD Decompose: {:.3g} sec'.format(-tmr))

print('Starting SVD Recompose')
tmr = timeit.default_timer()
svd_recompose(U, s, Vh, svs=_np.arange(0, 41), data=cars.data,
              rng=rng, overwrite=True)
tmr -= timeit.default_timer()
print('SVD Recompose: {:.3g} sec'.format(-tmr))

# Inverse Anscombe
print('Starting Inverse Anscombe...')
tmr = timeit.default_timer()
anscombe_inverse(cars.data, gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4,
                 rng=rng, overwrite=True)
tmr -= timeit.default_timer()
print('Inverse Anscombe: {:.3g} sec'.format(-tmr))

# KK -- note: not an overwrite-able fcn
print('Starting KK...')
tmr = timeit.default_timer()
kkd = kk(cars.data, nrb.data, rng=rng)
print('Saving KK...')
cars.data = kkd
tmr -= timeit.default_timer()
print('KK: {:.3g} sec'.format(-tmr))

# phase error correction
print('Starting Phase Error Correction...')
tmr = timeit.default_timer()
phase_err_correct_als(cars.data, redux_factor=10, rng=rng, overwrite=True,
                      print_iteration=True)
tmr -= timeit.default_timer()
print('Phase Error Correction: {:.3g} sec'.format(-tmr))

# scale error correction
print('Starting Scale Error Correction...')
tmr = timeit.default_timer()
scale_err_correct_sg(cars.data, rng=rng, overwrite=True)
tmr -= timeit.default_timer()
print('Scale Error Correction: {:.3g} sec'.format(-tmr))

tmr0 -= timeit.default_timer()
print('Time: {:.3g} sec/spectrum'.format(-tmr0/(cars.size/cars.freq.size)))