# Major initiatives
* Selector option to use complex64 instead of 128
* Implement logging
* Continue development of out-of-core analysis package
* Carryover database package from SW into standalone and integrate

# Adjustment for External Package Updates
* Enhance ~~Implement~~ MPL2 testing and API (such as ax.hold deprecation)

# Enhancements
* Carryover SVD auto-selection tools from SW package
* Add rng functionality to all fcns
* Move from ALS-only to ALS/ArPLS detrending

# Minor updates
* Fix model to use way less memory (and test 64 vs 128-bit complex)
* Add label and units parameter to Frequency
* Use Frequency label and units in GUI
* Move noise and other settings from CRIkitUI to Model class
* Pop and Grayscale plots for single-color plots always in front (likely parentage issue)
    * Parentage is the main UI; thus, Qt makes it in front -- not ideal, but stuck with it
    for now
* ~~Minimum in qt_GrayScaleImgInfoBar is set to 0 -- needs to allow negative~~
* Undo also resets freq window (ie track frequency window settings)
* Re-evaluate how poisson noise is added to model inline. Very math-operation-order dependent.