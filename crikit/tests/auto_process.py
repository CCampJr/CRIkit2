# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 22:38:32 2016

@author: chc
"""

import os
import sys
#import pickle
import datetime

sys.path.append(os.path.abspath('../../'))
sys.path.append(os.path.abspath('../../../crikit2_skunkworks/'))

import timeit

import numpy as np

from scipy.optimize import nnls

import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 16
plt.rcParams['figure.figsize']=(10,5)


from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

from crikit.data.spectrum import Spectrum
from crikit.data.spectra import Spectra
from crikit.data.hsi import Hsi

from crikit.io.macros import import_hdf_nist_special as io_nist
from crikit.io.hdf5 import hdf_export_data as io_export

from crikit.preprocess.subtract_dark import SubtractDark
from crikit.preprocess.subtract_mean import SubtractMeanOverRange
from crikit.preprocess.crop import ZeroColumn
from crikit.preprocess.standardize import Anscombe, AnscombeInverse
from crikit.preprocess.denoise import SVDDecompose, SVDRecompose

from crikit2_sw.preprocess.moran_feature import MoranFeatureSelection

from crikit.cri.kk import KramersKronig

from crikit.cri.error_correction import PhaserErrCorrectALS, ScaleErrCorrectSG

from crikit.utils.general import (arange_nonzero,
                                  row_col_from_lin,
                                  lin_from_row_col)
from crikit.utils.breadcrumb import BCPre

from crikit.measurement.moran import MoranI

pth = '../../../'
filename = 'mP2_w_small.h5'
dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0_small'
#dset = '/BCARSImage/mP2_3_5ms_Pos_2_0/mP2_3_5ms_Pos_2_0'

dset_dark = '/Spectra/Dark_3_5ms_2'
dset_nrb = '/Spectra/CoverslipNRB_Time0_3_5ms_2'

cars = Hsi()
nrb = Spectra()
dark = Spectra()

io_nist(pth, filename, dset, cars)
io_nist(pth, filename, dset_dark, dark)
io_nist(pth, filename, dset_nrb, nrb)

tmr0 = timeit.default_timer()
tmr = timeit.default_timer()

breadcrumb = BCPre()
breadcrumb.add_step(['Raw'])

# Dark subtract
sub_dark = SubtractDark(dark.data)

# CARS
sub_dark.transform(cars.data)

#NRB
sub_dark.transform(nrb.data)
tmr -= timeit.default_timer()
print('Dark subtraction: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['SubDark'])

# Subtract residual dark (sub dark over range)
tmr = timeit.default_timer()
rng = cars.freq.get_index_of_closest_freq([-1500, -400])
sub_residual = SubtractMeanOverRange(rng)

# CARS
sub_residual.transform(cars.data)

# NRB
sub_residual.transform(nrb.data)

tmr -= timeit.default_timer()
print('Residual subtraction: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['SubResidual','RangeStart',-1500,'RangeEnd',-400])

# Set operating range
print('Setting range...')
cars.freq.op_list_freq = [500, 4000]
rng = cars.freq.op_range_pix
print('Range set...')

# Zero first (or few) columns
# Small image
if np.prod(cars.shape[0:2]) <= 1000:
    zr = ZeroColumn(first_or_last=0)
    zr.transform(cars.data)
else:  # Big image
    zr = ZeroColumn(first_or_last=[0, 1, 2, 3, 4])
    zr.transform(cars.data)

# Anscombe
print('Starting Anscombe...')
tmr = timeit.default_timer()
anscombe = Anscombe(gauss_std=12.44, gauss_mean=0.0, poisson_multi=1.4, rng=rng)
anscombe.transform(cars.data)
tmr -= timeit.default_timer()
print('Anscombe: {:.3g} sec'.format(-tmr))

# SVD Decompose
print('Starting SVD Decompose...')
tmr = timeit.default_timer()
svd_decompose = SVDDecompose(rng=rng)
U, s, Vh = svd_decompose.calculate(cars.data)
tmr -= timeit.default_timer()
print('SVD Decompose: {:.3g} sec'.format(-tmr))

# Spatial Feature Selection
tmr = timeit.default_timer()
mfs = MoranFeatureSelection(data=U, img_shape=cars.shape[0:2])
tmr -= timeit.default_timer()
print('Feature selection from scratch: {:.3g} sec'.format(-tmr))
indices = mfs.idx[mfs.idx < 40]
print('Indices: {}'.format(indices))

# SVD Recompose
print('Starting SVD Recompose...')
tmr = timeit.default_timer()
svd_recompose = SVDRecompose(rng=rng)
svd_recompose.transform(cars.data, U, s, Vh, svs=indices)
tmr -= timeit.default_timer()
print('SVD Recompose: {:.3g} sec'.format(-tmr))

# Anscombe
print('Starting Inverse Anscombe...')
tmr = timeit.default_timer()
inverse_anscombe = AnscombeInverse(gauss_std=12.44,
                                   gauss_mean=0.0,
                                   poisson_multi=1.4,
                                   rng=rng)
inverse_anscombe.transform(cars.data)
tmr -= timeit.default_timer()
print('Inverse Anscombe: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['AnscSVD','SV_List',indices])


# KK
tmr = timeit.default_timer()
kk = KramersKronig(cars_amp_offset=0,
                   nrb_amp_offset=0,
                   norm_to_nrb=True,
                   rng=rng,
                   pad_factor=1)
kkd = kk.calculate(cars.data, nrb.data)
cars.data = kkd
tmr -= timeit.default_timer()
print('KK: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['KK', 'CARSAmp', 0, 'NRBAmp', 0, 'Phase', 0, 'Norm', True])


# Zero first (or few) columns
# Small image
if np.prod(cars.shape[0:2]) <= 1000:
    zr = ZeroColumn(first_or_last=0)
    zr.transform(cars.data)
else:  # Big image
    zr = ZeroColumn(first_or_last=[0, 1, 2, 3, 4])
    zr.transform(cars.data)



# Phase Error Correct
tmr = timeit.default_timer()
phase_err_correct_als = PhaserErrCorrectALS(smoothness_param=1,
                                            asym_param=.01,
                                            redux_factor=10,
                                            rng=rng,
                                            print_iteration=False)
phase_err_correct_als.transform(cars.data)
tmr -= timeit.default_timer()
print('Phase Error Correction: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['PhaseErrorCorrect','Type','ALS','lambda',1,'p',.01,'redux',10])

# Scale Error Correct
tmr = timeit.default_timer()
scale_err_correct_sg = ScaleErrCorrectSG(win_size=601, order=2, rng=rng)
scale_err_correct_sg.transform(cars.data)
tmr -= timeit.default_timer()
print('Scale Error Correction: {:.3g} sec'.format(-tmr))
breadcrumb.add_step(['Scaling','Type','SG','order', 2, 'win_size', 601])

plt.figure()
plt.imshow(cars.data.imag.sum(axis=-1))
plt.show()

plt.figure()
plt.plot(cars.data.imag.mean(axis=(0,1)))
plt.show()

cars.meta.update(breadcrumb.attr_dict)
suffix = breadcrumb.dset_name_suffix
dset_save = dset+suffix

curr_time = datetime.datetime.now()
rnd_fname = 'PROCESS_' + str(curr_time.year) + str(curr_time.month) + \
str(curr_time.day) + '_' + str(curr_time.hour) + '_' + \
str(curr_time.minute) + '_' + str(curr_time.second) + '_' + \
str(curr_time.microsecond) + '.h5'

filename_save = filename.split('.h5')[0] + '_' + rnd_fname

io_export(cars, pth, filename_save, dset_save)