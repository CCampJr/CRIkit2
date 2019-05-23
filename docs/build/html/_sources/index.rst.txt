.. -*- mode: rst -*-

.. image:: https://travis-ci.com/CCampJr/CRIkit2.svg?branch=master
    :alt: Travis CI Status
    :target: https://travis-ci.com/CCampJr/CRIkit2

.. image:: https://ci.appveyor.com/api/projects/status/1yrsrk6wfhjsn7bq/branch/master?svg=true
    :alt: AppVeyor CI Status
    :target: https://ci.appveyor.com/project/CCampJr/crikit2

.. image:: https://codecov.io/gh/CCampJr/CRIkit2/branch/master/graph/badge.svg
    :alt: Codecov
    :target: https://codecov.io/gh/CCampJr/CRIkit2

.. image:: https://img.shields.io/pypi/pyversions/CRIkit2.svg
    :alt: PyPI - Python Version
    :target: https://pypi.org/project/CRIkit2/

.. image:: https://img.shields.io/pypi/v/CRIkit2.svg
    :alt: PyPI Project Page
    :target: https://pypi.org/project/CRIkit2/

.. image:: https://img.shields.io/badge/License-NIST%20Public%20Domain-green.svg
    :alt: NIST Public Domain
    :target: https://github.com/CCampJr/CRIkit2/blob/master/LICENSE.md


CRIKit2: Hyperspectral imaging toolkit
=======================================

.. image:: _static/CRIkit2_Logo.png
    :alt: CRIkit2 Logo

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform. It is composed of command line tools, interactive tools,
and a user interface.

Contents:

.. toctree::
  :maxdepth: 2
  :caption: User Documentation

  installing
  running
  cri_walkthru
  algorithms
  io
  license

.. toctree::
  :maxdepth: 2
  :caption: Developer Documentation

  api
   
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`


Dependencies
-------------

Note: These are the developmental system specs. Older versions of certain
packages may work.

-   python >= 3.4
    
    -   Tested with 3.4.4, 3.5.2, 3.6.1, 3.7.2

-   NumPy
-   PyQT5
-   CVXOPT
-   LazyHDF5 >= 0.2.2
    
    -   Requires H5Py (>= 2.6)

-   SciPlot-PyQt >= 0.2.2
    
    -   https://github.com/CCampJr/SciPlot-PyQt/releases
    -   Requires Matplotlib (v1.*, 2.*, or 3.*)

-   Sphinx (optional)

IMPORTANT: For Python 3.4
~~~~~~~~~~~~~~~~~~~~~~~~~~
You will need to manually install PyQt5 and Qt5 or get it through a distribution:

-   PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5
-   Qt: https://www.qt.io/

For Python 3.5, installation through pip available
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    pip3 install pyqt5

Known Issues
-------------

Windows 10 with High-Resolution Monitors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The GUI may appear squashed with small font. There is a work-around described at https://github.com/CCampJr/CRIkit2/issues/79

PyQt 5.7.*
~~~~~~~~~~~

There is a bug in PyQt 5.7.* that will prevent SciPlot's tables from showing the individual plot entries 
(see https://www.riverbankcomputing.com/pipermail/pyqt/2017-January/038483.html). Apparently, this will be fixed in 5.7.2.

-   As WinPython 3.5.2.3Qt5 and 3.5.2.2Qt5 use PyQt 5.7.*, it is advised to use WinPython 3.5.2.1Qt5 or 3.4.4.5Qt5 until the matter is sorted out.
-   Alternatively, one can uninstall pyqt5.7.* and force an install of <= 5.6.*.


Installation
-------------

Option 1: Easily updatable through git (dynamic copy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # Make new directory for crikit2 and enter it
    # Clone from github
    git clone https://github.com/CCampJr/crikit2.git

    # Within install directory
    pip3 install -e .

    # To update installation, from within crikit2 directory
    git pull


Option 2: Static Copy
~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # Make new directory for crikit2 and enter it
    # Clone from github
    git clone https://github.com/CCampJr/crikit2.git

    # or download a copy from https://github.com/CCampJr/crikit2

    # Within install directory
    pip3 install .

    # You can now delete the source files you downloaded


(Re-) Building Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The documentation was built using Sphinx. A pre-built version of the html
files is included with this module, but you may wish to rebuild on your own
system.

.. code::

    # Build all APIs
    # From within the docs/ directory
    sphinx-apidoc -o ./source/ ../crikit/

    # Build API w/o pyuic5-generated files
    sphinx-apidoc -f -o .\source\ ..\crikit\ ..\crikit\ui\qt_* ..\crikit\ui\*_rc* ..\crikit\ui\old\**

    make html  
    # On Windows
    make.bat html

Starting the CRIkit2 UI
------------------------

.. code::

    python3 -m crikit 

    # or

    python -m crikit

Known Operational Nuances
--------------------------

-   The SVD visualization tool uses a complex-valued SVD for complex values; thus, there are a few
    things to avoid
    
    -   If your spectra are PURELY IMAGINARY, convert them to PURELY REAL
    -   If your real and imaginary parts of your spectra are IDENTICAL, then
        consider using just the real or imaginary portion
    -   NOTE: this does not affect the accuracy or performance of SVD or the returned
        results, but you will see unexpected visualizations of the spatial and spectral
        components.

LICENSE
----------
This software was developed by employees of the National Institute of Standards 
and Technology (NIST), an agency of the Federal Government. Pursuant to 
`title 17 United States Code Section 105 <http://www.copyright.gov/title17/92chap1.html#105>`_, 
works of NIST employees are not subject to copyright protection in the United States and are 
considered to be in the public domain. Permission to freely use, copy, modify, 
and distribute this software and its documentation without fee is hereby granted, 
provided that this notice and disclaimer of warranty appears in all copies.

THE SOFTWARE IS PROVIDED 'AS IS' WITHOUT ANY WARRANTY OF ANY KIND, EITHER 
EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED TO, ANY WARRANTY 
THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY IMPLIED WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND FREEDOM FROM INFRINGEMENT, 
AND ANY WARRANTY THAT THE DOCUMENTATION WILL CONFORM TO THE SOFTWARE, OR ANY 
WARRANTY THAT THE SOFTWARE WILL BE ERROR FREE. IN NO EVENT SHALL NIST BE LIABLE 
FOR ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL OR 
CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY WAY CONNECTED 
WITH THIS SOFTWARE, WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR 
OTHERWISE, WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY OR 
OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT OF THE 
RESULTS OF, OR USE OF, THE SOFTWARE OR SERVICES PROVIDED HEREUNDER.

CITATION
---------

`C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, comparable coherent
anti-Stokes Raman scattering (CARS) spectroscopy: correcting errors in phase
retrieval", Journal of Raman Spectroscopy 47, 408-416 (2016). <https://www.ncbi.nlm.nih.gov/pubmed/28819335>`_


Contact
--------

Charles H Camp Jr: `charles.camp@nist.gov <mailto:charles.camp@nist.gov>`_
