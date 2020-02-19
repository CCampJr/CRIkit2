import numpy as np

from crikit.cri.merge_nrbs import MergeNRBs

def test_basic():
    x = np.arange(0,1000)

    nrb_left = np.exp(-(x-500)**2/(100**2))
    nrb_right = np.exp(-(x-700)**2/(120**2))

    pix = 625

    # Left scale
    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=True)
    out_scaled_left = merge.calculate()
    assert nrb_right[pix] == out_scaled_left[pix]

    # Right scale
    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=False)
    out_scaled_right = merge.calculate()
    assert nrb_left[pix] == out_scaled_right[pix]

    merge = MergeNRBs(nrb_left, nrb_right, pix, left_side_scale=None)
    out_scaled_none = merge.calculate()
    assert nrb_right[pix] == out_scaled_none[pix]
    assert nrb_left[pix-1] == out_scaled_none[pix-1]