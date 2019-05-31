""" Tests for crikit.utils.general.pad_edge_mean """

import numpy as np

import pytest

from crikit.utils.general import pad_edge_mean


def test_pad_1d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad_edge, window_edge = pad_edge_mean(y, 10)
    assert np.allclose(y_pad_edge[10:-10], y)
    assert np.allclose(y_pad_edge[:10], y[0])
    assert np.allclose(y_pad_edge[-10:], y[-1])

    assert np.allclose(window_edge[10:-10], 1)
    assert np.allclose(window_edge[:10], 0)
    assert np.allclose(window_edge[-10:], 0)

    assert np.allclose(y_pad_edge[..., window_edge==1], y)

def test_pad_1d_0_width():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad_edge, window_edge = pad_edge_mean(y, 0)
    assert np.allclose(y_pad_edge, y)
    assert np.allclose(y_pad_edge[..., window_edge==1], y)
    assert np.allclose(window_edge, 1)

def test_pad_2d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))
    y = np.vstack((y, y))

    assert y.shape[0] == 2
    assert y.shape[-1] == x.size

    y_pad_edge, window_edge = pad_edge_mean(y, 10)
    assert np.allclose(y_pad_edge[..., 10:-10], y)

    assert np.allclose(y_pad_edge[..., :10], np.dot(y[..., 0:1], np.ones((1, 10))))
    assert np.allclose(y_pad_edge[..., -10:], np.dot(y[..., -1:-2:-1], np.ones((1, 10))))

    assert np.allclose(window_edge[10:-10], 1)
    assert np.allclose(window_edge[:10], 0)
    assert np.allclose(window_edge[-10:], 0)

    assert np.allclose(y_pad_edge[..., window_edge==1], y)


def test_pad_2d_0_width():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))
    y = np.vstack((y, y))

    assert y.shape[0] == 2
    assert y.shape[-1] == x.size

    y_pad_edge, window_edge = pad_edge_mean(y, 0)
    assert np.allclose(y_pad_edge, y)
    assert np.allclose(window_edge, 1)
    assert np.allclose(y_pad_edge[..., window_edge==1], y)
