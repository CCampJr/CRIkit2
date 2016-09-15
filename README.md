# CRIKit2: Hyperspectral imaging toolkit #

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform (user interface, UI).

HSI Processing:
* Dark subtraction
* Detrending
* Denoising

Coherent Raman-Specific Processing:
* Kramers-Kronig phase retrieval
* Phase- and scale-error correction

Analysis:
* (Coming soon)

## Installation ##
```
# Make new directory for crikit2 and enter it
# Clone from github
git clone https://github.com/CCampJr/crikit2.git

# Install (mainly check installation)
pip install -e .

# IMPORTANT: You will need to manually install PyQt5 and Qt5
# These packages are not pip-installable at this time
```

## Starting CRIkit2 UI ##
```
python -m crikit
```

## Dependencies ##

Note: These are the developmental system specs. Older versions of certain
packages may work.

* Python >= 3.4
* Numpy (1.9.3)
* PyQT5 (5.5.1)
* Matplotlib (1.5.0rc3)
* Yapsy (1.11.223)
* H5Py (2.5)

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

