"""
Visualization General Utilities (crikit.ui.visgentuils)
=======================================================

    roimask : Create a region-of-interest binary mask

"""

from matplotlib.path import Path as _Path
import numpy as _np


def roimask(imgx, imgy, xvec, yvec):
    """
    Create a region-of-interest binary mask from vertices.

    Parameters
    ----------
    imgx : ndarray
        X-axis vector in physical units

    imgy : ndarray
        Y-axis vector in physical units

    xvec : ndarray
        Vector of x-locations of selected points

    yvec : ndarray
        Vector of y-locations of selected points

    Returns
    -------
    mask : ndarray
        Binary mask

    path : MPL path object
        Matplotlib path object describing ROI
    """
    verts = _pts_to_verts(xvec, yvec)
    path = _verts_to_path(verts)
    mask = _mask_from_path(imgx, imgy, path)
    return (mask, path)


def _pts_to_verts(xvec, yvec):
    """
    Convert points to vertices, i.e., convert from 2 1D arrays (or list) of \
    x- and y-coordinates to a list-of-lists of [x,y] pairs
    """
    verts = []
    for count in range(len(xvec)):
        verts.append([xvec[count],yvec[count]])
    return verts


def _verts_to_path(verts, isclose = True):
    """
    Convert vertices to paths
    """
    if not isclose:
        verts += verts[0]
    else:
        pass
    codes = [_Path.MOVETO] + [_Path.LINETO]*(len(verts)-2) + [_Path.CLOSEPOLY]
    return _Path(verts, codes)


def _mask_from_path(x, y, path):
    """
    Create mask from path
    """
    X, Y = _np.meshgrid(x, y)
    allpts = _np.hstack((X.flatten()[:, None], Y.flatten()[:, None]))
    return _np.reshape(path.contains_points(allpts, radius=1e-12),[y.size, x.size])