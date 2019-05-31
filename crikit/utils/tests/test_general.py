import numpy as np

import pytest

from crikit.utils.general import pad, pad_dual, pad_edge_mean

def test_pad_1d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad_edge, window_edge = pad(y, 10, 'edge')
    assert np.allclose(y_pad_edge[10:-10], y)
    assert np.allclose(y_pad_edge[:10], y[0])
    assert np.allclose(y_pad_edge[-10:], y[-1])

    assert np.allclose(window_edge[10:-10], 1)
    assert np.allclose(window_edge[:10], 0)
    assert np.allclose(window_edge[-10:], 0)

    assert np.allclose(y_pad_edge[..., window_edge==1], y)

    y_pad_constant, window_constant = pad(y, 10, 'constant')
    assert np.allclose(y_pad_constant[10:-10], y)
    assert np.allclose(y_pad_constant[:10], 0)
    assert np.allclose(y_pad_constant[-10:], 0)

    assert np.allclose(window_constant[10:-10], 1)
    assert np.allclose(window_constant[:10], 0)
    assert np.allclose(window_constant[-10:], 0)

    assert np.allclose(y_pad_constant[..., window_constant==1], y)

def test_pad_1d_0_width():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad_edge, window_edge = pad(y, 0, 'edge')
    assert np.allclose(y_pad_edge, y)
    assert np.allclose(y_pad_edge[..., window_edge==1], y)
    assert np.allclose(window_edge, 1)

    y_pad_constant, window_constant = pad(y, 0, 'constant')
    assert np.allclose(y_pad_constant, y)
    assert np.allclose(y_pad_constant[..., window_constant==1], y)
    assert np.allclose(window_constant, 1)

def test_pad_2d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))
    y = np.vstack((y, y))

    assert y.shape[0] == 2
    assert y.shape[-1] == x.size

    y_pad_edge, window_edge = pad(y, 10, 'edge')
    assert np.allclose(y_pad_edge[..., 10:-10], y)

    assert np.allclose(y_pad_edge[..., :10], np.dot(y[..., 0:1], np.ones((1, 10))))
    assert np.allclose(y_pad_edge[..., -10:], np.dot(y[..., -1:-2:-1], np.ones((1, 10))))

    assert np.allclose(window_edge[10:-10], 1)
    assert np.allclose(window_edge[:10], 0)
    assert np.allclose(window_edge[-10:], 0)

    assert np.allclose(y_pad_edge[..., window_edge==1], y)

    y_pad_constant, window_constant = pad(y, 10, 'constant')
    assert np.allclose(y_pad_constant[..., 10:-10], y)
    assert np.allclose(y_pad_constant[..., :10], 0)
    assert np.allclose(y_pad_constant[..., -10:], 0)

    assert np.allclose(window_constant[10:-10], 1)
    assert np.allclose(window_constant[:10], 0)
    assert np.allclose(window_constant[-10:], 0)

    assert np.allclose(y_pad_constant[..., window_constant==1], y)

def test_pad_2d_0_width():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))
    y = np.vstack((y, y))

    assert y.shape[0] == 2
    assert y.shape[-1] == x.size

    y_pad_edge, window_edge = pad(y, 0, 'edge')
    assert np.allclose(y_pad_edge, y)
    assert np.allclose(window_edge, 1)
    assert np.allclose(y_pad_edge[..., window_edge==1], y)

    y_pad_constant, window_constant = pad(y, 0, 'constant')
    assert np.allclose(y_pad_constant, y)
    assert np.allclose(window_constant, 1)
    assert np.allclose(y_pad_constant[..., window_constant==1], y)


def test_pad_dual_1d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad, window = pad_dual(y, 10, 20)

    assert np.allclose(y_pad[..., window==1], y)
    assert np.allclose(y_pad[..., :20], 0)
    assert np.allclose(y_pad[..., -20:], 0)
    assert np.allclose(y_pad[..., 20:30], y[0])
    assert np.allclose(y_pad[..., -30:-20], y[-1])

def test_pad_dual_1d_all_0s():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))

    y_pad, window = pad_dual(y, 0, 0)

    assert np.allclose(y_pad[..., window==1], y)
    assert np.allclose(window, 1)
    
def test_pad_dual_2d():
    x = np.arange(-1000,1001)
    y = np.real(1/(-500 - x - 1j*100))
    y = np.vstack((y,y))

    y_pad, window = pad_dual(y, 10, 20)

    assert np.allclose(y_pad[..., window==1], y)
    assert np.allclose(y_pad[..., :20], 0)
    assert np.allclose(y_pad[..., -20:], 0)
    assert np.allclose(y_pad[..., 20:30], np.dot(y[..., 0:1], np.ones((1, 10))))
    assert np.allclose(y_pad[..., -30:-20], np.dot(y[..., -1:-2:-1], np.ones((1, 10))))

