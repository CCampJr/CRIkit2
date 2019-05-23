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

.. image:: ./docs/source/_static/CRIkit2_Logo.png
    :alt: CRIkit2 Logo

CRIKit2, formerly the Coherent Raman Imaging toolKit, is a hyperspectral
imaging (HSI) platform. It is composed of command line tools, interactive tools,
and a user interface.

HSI Processing:

-   Dark subtraction
-   Detrending
-   Denoising via SVD

Coherent Raman-Specific Processing:

-   Kramers-Kronig phase retrieval
-   Phase- and scale-error correction

Coming Soon:

-   SVD automated selection tools
-   Analysis toolkit (separate UI)
-   Interactive Raman database
-   Much more

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

It is advisable to clone CRIkit2 via git (https://git-scm.com/) and install
in a *developmental* mode via *pip* or *conda* as this will enable you to
easily (relatively) update your copy of CRIkit2 as new functionality
is *pushed*.

**Note** If you choose to clone an updatable copy of CRIkit2, do not
clone to a directory within your Python installation. Rather, create a new
directory elsewhere. That way if you update your Python distribution, you won't
lose your copy of CRIkit2.

Option 1: Dynamic, Updatable Clone of CRIkit2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code::

    # Note: in Windows, commands will be followed by .exe
    # Note: On multi-python systems, you should probably append a 3 to end
    # the end of commands, e.g., pip is pip3, python is python3

    # Assume the new directory will be CRIkit2 (it can be anything)
    # Clone from github
    git clone https://github.com/CCampJr/crikit2.git CRIkit2

    # Within install directory
    pip install -e .

    # To update installation, from within the CRIkit2 directory
    git pull


Option 2: Static Copy
~~~~~~~~~~~~~~~~~~~~~~

The static copy will copy the CRIkit2 install into your Python distribution
and will not be updatable without re-installing CRIkit2

.. code::

    # Note: in Windows, commands will be followed by .exe
    # Note: On multi-python systems, you should probably append a 3 to end
    # the end of commands, e.g., pip is pip3, python is python3

    # Assume the new directory will be CRIkit2 (it can be anything)
    # Clone from github
    git clone https://github.com/CCampJr/crikit2.git CRIkit2

    # Within install directory
    pip install .

    # You can now delete the source files you downloaded if so desired

    # To update installation, from within the CRIkit2 directory
    git pull
    pip install .


(Re-) Building Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A pre-built version of the documentation is included with the installation;
thus, this step should not be necessary unless you are making modifications
to the software.

The documentation is accessible from within CRIkit2 under the *Help* header.
It is displayed in a web browser.

.. code::

    # From within the CRIkit2 directory (not crikit)
    cd docs

    # Clean out old docs (optional)
    make clean  # On Windows make.bat clean

    # Build API w/o pyuic5-generated files
    # Windows add .exe
    sphinx-apidoc -f -o ./source/ ../ ../crikit/ui/qt_* ../crikit/ui/*_rc* ../crikit/ui/old/** ../setup.py

    make html  # On Windows make.bat html


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

NONLICENSE
-----------
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

CITATION
---------

`C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, comparable coherent
anti-Stokes Raman scattering (CARS) spectroscopy: correcting errors in phase
retrieval", Journal of Raman Spectroscopy 47, 408-416 (2016). <https://www.ncbi.nlm.nih.gov/pubmed/28819335>`_




Contact
--------

Charles H Camp Jr: `charles.camp@nist.gov <mailto:charles.camp@nist.gov>`_

