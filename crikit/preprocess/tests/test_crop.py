import numpy as np

from crikit.preprocess.crop import CutEveryNSpectra, ZeroRow, ZeroColumn

def test_zero_col_first_col():
    temp = np.random.rand(3, 4, 5)
    z = ZeroColumn(first_or_last=0)
    z.transform(temp)
    assert temp.sum(axis=(0, -1))[0] == 0
    assert temp.sum(axis=(1, -1))[0] != 0

def test_zero_row_first_row():
    temp = np.random.rand(3, 4, 5)
    z = ZeroRow(first_or_last=0)
    z.transform(temp)
    assert temp.sum(axis=(0, -1))[0] != 0
    assert temp.sum(axis=(1, -1))[0] == 0

def test_zero_col_last_col():
    temp = np.random.rand(3, 4, 5)
    z = ZeroColumn(first_or_last=-1)
    z.transform(temp)
    assert temp.sum(axis=(0, -1))[-1] == 0
    assert temp.sum(axis=(1, -1))[-1] != 0

def test_zero_row_last_row():
    temp = np.random.rand(3, 4, 5)
    z = ZeroRow(first_or_last=-1)
    z.transform(temp)
    assert temp.sum(axis=(0, -1))[-1] != 0
    assert temp.sum(axis=(1, -1))[-1] == 0

def test_cut_every_n_spectra():
    temp = np.array([1, 1, 0, 0, 1, 1, 0, 0])
    temp =  np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=2, every_n=4, action='cut')
    assert c.calculate(temp).sum() == 0
    
    c = CutEveryNSpectra(offset=2, cut_m=2, every_n=4, action='cut')
    assert c.calculate(temp).mean() == 1

    temp = np.array([0, 1, 2, 0, 1, 2])
    temp =  np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=1, every_n=3, action='before')
    assert c.calculate(temp).mean() == 10/6

    temp = np.array([0, 1, 2, 0, 1, 2])
    temp =  np.repeat(temp[:,None], 110, axis=-1)
    c = CutEveryNSpectra(offset=0, cut_m=1, every_n=3, action='after')
    assert c.calculate(temp).mean() == 8/6