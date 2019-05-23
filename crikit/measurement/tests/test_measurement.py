import numpy as np
import numpy.testing

import pytest

from crikit.data.hsi import Hsi
from crikit.measurement.peakamps import (MeasurePeak, MeasurePeakAdd, MeasurePeakMinus, 
                                         MeasurePeakMultiply, MeasurePeakDivide,
                                         MeasurePeakMax, MeasurePeakMin,
                                         MeasurePeakMaxAbs, MeasurePeakMinAbs,
                                         MeasurePeakSum, MeasurePeakBWTroughs, 
                                         MeasurePeakSumAbsReImag)

@pytest.fixture(scope="module")
def hsi_dataset():
    """ Setups and tears down a sample HSI Dataset """
    
    data_m, data_n, data_p = [2, 3, 5]
    spectrum = np.array([0,1,2,3,4])
    hsi = np.dot(np.ones((data_m*data_n, 1)), spectrum[None,:])
    hsi = hsi.reshape((data_m, data_n, data_p))
    
    yield hsi

    # Tear-down
    del hsi

def test_peak(hsi_dataset):
    """ Test peak amplitude """

    m_cls = MeasurePeak
    f1 = 2
    measurer = m_cls(f1)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_add(hsi_dataset):
    """ Test peak add """

    m_cls = MeasurePeakAdd
    f1 = 0
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_subtract(hsi_dataset):
    """ Test peak subtract """

    m_cls = MeasurePeakMinus
    f1 = 0
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, -2)
    assert np.allclose(out2, -2)

def test_multiply(hsi_dataset):
    """ Test peak multiplication """

    m_cls = MeasurePeakMultiply
    f1 = 0
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 0)
    assert np.allclose(out2, 0)

def test_divide(hsi_dataset):
    """ Test peak division """

    m_cls = MeasurePeakDivide
    f1 = 4
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_max_unordered(hsi_dataset):
    """ Test peak maximum with f1 > f2 (wrong) """

    m_cls = MeasurePeakMax

    f1 = 4
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 4)
    assert np.allclose(out2, 4)

def test_min_unordered(hsi_dataset):
    """ Test peak minimum  with f1 > f2 (wrong) """

    m_cls = MeasurePeakMin

    f1 = 4
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_max(hsi_dataset):
    """ Test peak maximum with f1 < f2 (right) """

    m_cls = MeasurePeakMax

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 4)
    assert np.allclose(out2, 4)

def test_min(hsi_dataset):
    """ Test peak minimum  with f1 < f2 (right) """

    m_cls = MeasurePeakMin

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_maxabs(hsi_dataset):
    """ Test peak maximum abs with f1 < f2 (right) """

    m_cls = MeasurePeakMaxAbs

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 4)
    assert np.allclose(out2, 4)

def test_minabs(hsi_dataset):
    """ Test peak minimum abs with f1 < f2 (right) """

    m_cls = MeasurePeakMinAbs

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 2)
    assert np.allclose(out2, 2)

def test_sum(hsi_dataset):
    """ Test peak summation f1 < f2 (right) """

    m_cls = MeasurePeakSum

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 9)
    assert np.allclose(out2, 9)

def test_sum_unordered(hsi_dataset):
    """ Test peak summation f1 > f2 (wrong) """

    m_cls = MeasurePeakSum

    f1 = 4
    f2 = 2
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 9)
    assert np.allclose(out2, 9)

def test_pbt(hsi_dataset):
    """ Test peak between trough f1 < f2 (right) """

    m_cls = MeasurePeakBWTroughs

    f1 = 2
    f2 = 0
    f3 = 4
    measurer = m_cls(f1, f2, f3)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2, f3)

    assert np.allclose(out1, 0)
    assert np.allclose(out2, 0)

def test_sum_re_im(hsi_dataset):
    """ Test peak summation f1 < f2 (right) """

    m_cls = MeasurePeakSumAbsReImag

    f1 = 2
    f2 = 4
    measurer = m_cls(f1, f2)

    measurer.calculate(hsi_dataset)
    out1 = measurer.output
    out2 = m_cls.measure(hsi_dataset, f1, f2)

    assert np.allclose(out1, 9)
    assert np.allclose(out2, 9)