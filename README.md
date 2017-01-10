# CRIKit2: Hyperspectral imaging toolkit #

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform (user interface, UI).

HSI Processing:
* Dark subtraction
* Detrending
* Denoising via SVD

Coherent Raman-Specific Processing:
* Kramers-Kronig phase retrieval
* Phase- and scale-error correction

Coming Soon:
* SVD automated selection tools
* Analysis toolkit (separate UI)
* Interactive Raman database
* Much more

## Installation ##
```
# Make new directory for crikit2 and enter it
# Clone from github
git clone https://github.com/CCampJr/crikit2.git

# Install (mainly check installation)
pip3 install -e .

# IMPORTANT: for Python 3.4
# You will need to manually install PyQt5 and Qt5
# These packages are not pip-installable at this time

# For Python 3.5
pip3 install pyqt5 
```

## Starting CRIkit2 UI ##
```
python3 -m crikit 

# or

python -m crikit
```

## Dependencies ##

Note: These are the developmental system specs. Older versions of certain
packages may work.

* python >= 3.4 (Currently, transitioning to python 3.5)
* numpy (1.9.3)
* PyQT5 (5.5.1)
* matplotlib (1.5.0rc3)
* cvxopt (1.1.7)
* h5py (2.5)

## NONLICENSE ##
This software was developed at the National Institute of Standards and
Technology (NIST) by employees of the Federal Government in the course of
their official duties. Pursuant to [Title 17 Section 105 of the United States
Code](http://www.copyright.gov/title17/92chap1.html#105), this software is not
subject to copyright protection and is in the public domain. NIST assumes no
responsibility whatsoever for use by other parties of its source code, and
makes no guarantees, expressed or implied, about its quality, reliability, or
any other characteristic.

Specific software products identified in this open source project were used in
order to perform technology transfer and collaboration. In no case does such
identification imply recommendation or endorsement by the National Institute
of Standards and Technology, nor does it imply that the products identified
are necessarily the best available for the purpose.

## CITATION ##
C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, comparable coherent
anti-Stokes Raman scattering (CARS) spectroscopy: correcting errors in phase
retrieval", Journal of Raman Spectroscopy 47, 408-416 (2016).
DOI: 10.1002/jrs.4824

## Contact ##
Charles H Camp Jr: [charles.camp@nist.gov](mailto:charles.camp@nist.gov)

