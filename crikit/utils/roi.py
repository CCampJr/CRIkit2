"""
Created on Wed Jun 15 23:33:41 2016

@author: chc
"""
import numpy as _np
from matplotlib.path import Path as _Path


def verts_to_path(verts, isclosed=True):
    """
    Convert vertices to paths
    """
    if not isclosed:
        verts += [verts[0]]
    else:
        pass
    codes = [_Path.MOVETO] + [_Path.LINETO] * (len(verts)-2) + \
            [_Path.CLOSEPOLY]

    return _Path(verts, codes)


def pts_in_path(path):
    """
    Return points (pixels) that fall within path (but not on boundary)
    """

    # Get bounding box of path (simplify geometry)
    exts = path.get_extents()

    # Bottom-left, top-right coordinates
    bl, tr = exts.get_points()

    # Temporary x- and y-vectors and meshgrids
    x = _np.arange(bl[0], tr[0])
    y = _np.arange(bl[1], tr[1])
    X, Y = _np.meshgrid(x, y)

    # Linearize meshgrid
    allpts = _np.hstack((X.flatten()[:, None], Y.flatten()[:, None]))

    # Mask of points within path (NOT including boundary)
    mask_allpts = path.contains_points(allpts)

    # Get and return x- and y-pixels
    x_pts, y_pts = _np.array([X.flatten()[mask_allpts],
                              Y.flatten()[mask_allpts]])
    return x_pts, y_pts


def pts_to_verts(xvec, yvec):
    """
    Convert points to vertices, i.e., convert from 2 1D arrays (or list) of \
    x- and y-coordinates to a list-of-lists of [x,y] pairs
    """
    verts = []
    for count in range(len(xvec)):
        verts.append([xvec[count], yvec[count]])
    return verts


def verts_to_points_in_roi(verts):
    """
    Vertice list defining ROI in, points within returned.
    """
    path = verts_to_path(verts, isclosed=False)
    x_pts, y_pts = pts_in_path(path)
    return x_pts, y_pts
