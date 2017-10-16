# Major initiatives
* Selector option to use complex64 instead of 128
* Implement logging
* Continue development of out-of-core analysis package
* Carryover database package from SW into standalone and integrate

# Adjustment for External Package Updates
* Implement MPL2 testing and API (such as ax.hold deprecation)

# Enhancements
* Carryover SVD auto-selection tools from SW package
* Add rng functionality to all fcns
* Move from ALS-only to ALS/ArPLS detrending

# Issues for this branch (dev-NewImageWidgets)
* Pop and Grayscale plots for single-color plots always in front (likely parentage issue)
    * Parentage is the main UI; thus, Qt makes it in front -- not ideal, but stuck with it
    for now
* ~~Minimum in qt_GrayScaleImgInfoBar is set to 0 -- needs to allow negative~~