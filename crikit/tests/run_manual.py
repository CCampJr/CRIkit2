# -*- coding: utf-8 -*-
"""

Full blown run-through with real data

Created on Mon Jun  6 23:56:10 2016

@author: chc
"""

import numpy as _np
import matplotlib.pyplot as plt
import os
import sys

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
dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small'

dset_dark = '/Spectra/Dark_3_5ms_2'
dset_nrb = '/Spectra/CoverslipNRB_Time0_3_5ms_2'

cars = Hsi()
nrb = Spectra()
dark = Spectra()

io_nist(filename, dset, cars)
io_nist(filename, dset_dark, dark)
io_nist(filename, dset_nrb, nrb)

# Dark subtract
plt.figure()
plt.plot(cars.freq.data, cars.data[25, 25, :], label='cars raw')
plt.plot(cars.freq.data, nrb.data[25, :], label='nrb raw')

sub_dark(cars.data, dark.data, overwrite=True)
sub_dark(nrb.data, dark.data, overwrite=True)

plt.plot(cars.freq.data, cars.data[25, 25, :], label='cars sub dark')
plt.plot(cars.freq.data, nrb.data[25, :], label='nrb sub dark')

plt.legend()
#plt.show()

# Subtract residual dark (sub dark over range)
plt.figure()
plt.plot(cars.freq.data, cars.data[25, 25, :], label='cars')
rng = cars.freq.get_index_of_closest_freq([-5000, -500])
sub_residual(cars.data, rng, overwrite=True)
sub_residual(nrb.data, rng, overwrite=True)
plt.plot(cars.freq.data, cars.data[25, 25, :], label='sub residual')
plt.legend()
plt.axis([-1200, -200, -50, 50])
#plt.show()

# Set operating range
cars.freq.op_list_freq = [500, 4000]
#cars.freq.update()

# Anscombe
plt.figure()
plt.plot(cars.freq.op_range_freq,
         cars.data[25, 25, cars.freq.op_range_pix], label='cars')
anscombe(cars.data, gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4,
         overwrite=True)
plt.plot(cars.freq.op_range_freq,
         cars.data[25, 25, cars.freq.op_range_pix], label='cars')
plt.legend()
#plt.show()

# SVD
plt.figure()
#U, s, Vh = svd_decompose(cars.data, rng_list=cars.freq.op_list_pix)
U, s, Vh = svd_decompose(cars.data, rng=cars.freq.op_range_pix)

plt.semilogy(s/s.sum())
plt.plot((40,40),(1e-4,1),'r--', label='Example cutoff')
plt.axis((0, 50, 1e-4, 1))
plt.xlabel('Singular Value')
plt.ylabel('SV Contribution Fraction')
plt.legend()

plt.figure()
for num in range(9):
    plt.subplot(3, 3, num+1)
    plt.imshow(U[:, num].reshape((cars.y_rep.size, cars.x_rep.size))[1:, 1:], interpolation='none')

plt.figure()
for num in range(9):
    plt.subplot(9, 1, num+1)
    plt.plot(cars.freq.op_range_freq, Vh[num,:])

plt.figure()
plt.plot(cars.freq.data, cars.data[25, 25, :], label='cars')
svd_recompose(U, s, Vh, svs=_np.arange(0, 41), data=cars.data,
              rng=cars.freq.op_range_pix, overwrite=True)
#svd_recompose(U, s, Vh, svs=_np.arange(0, 41), data=cars.data,
#              rng_list=cars.freq.op_list_pix, overwrite=True)
plt.plot(cars.freq.data, cars.data[25, 25, :], label='cars post SVD')


# Inverse Anscombe
plt.plot(cars.freq.data, cars.data[25, 25, :], label='Anscombe')
anscombe_inverse(cars.data, gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4,
         overwrite=True)
plt.plot(cars.freq.data, cars.data[25, 25, :], label='Inverse Anscombe')

# KK -- note: not an overwrite-able fcn
kkd = kk(cars.data, nrb.data, rng=cars.freq.op_range_pix)
cars.data = kkd

plt.figure()
plt.plot(cars.freq.data, cars.data[25,25,:].imag, label='KK')
plt.legend()

# phase error correction
plt.figure()
plt.plot(cars.freq.op_range_freq, cars.data[25,25,cars.freq.op_range_pix].imag,
         label='KK')
phase_err_correct_als(cars.data, redux_factor=10, overwrite=True)
plt.plot(cars.freq.op_range_freq, cars.data[25,25,cars.freq.op_range_pix].imag,
         label='Phase Corrected')
plt.legend()

# scale error correction
plt.figure()
plt.plot(cars.freq.op_range_freq, cars.data[25,25,cars.freq.op_range_pix].imag,
         label='Phase Corrected')
scale_err_correct_sg(cars.data, overwrite=True)
plt.plot(cars.freq.op_range_freq, cars.data[25,25,cars.freq.op_range_pix].imag,
         label='Corrected')
plt.legend()
plt.show()

#plt.subplot(211)
#anscombe_inverse(cars.data, gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4,
#         overwrite=True)
#plt.plot(cars.freq.data, cars.data[25, 25, :], label='inv anscombe')
#plt.legend()
#plt.show()
