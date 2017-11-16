.. _installing:

.. image:: _static/CRIkit2_Logo.png
    :align: left

|
|
|
|
|
|
|

Installation
============

Dependencies
---------------------
Note: the versions are those that have been tested, but older/newer
versions may also work.

- Python 3.4, 3.5, 3.6
- `SciPlot-PyQt <https://github.com/CCampJr/SciPlot-PyQt>`__ >= 0.1.3 (>=0.1.4 for MPL2)
- numpy (1.9.3)
- PyQt5 (5.5, 5.6)
- matplotlib (1.5, 2.0 -- see below for MPL2)
- cvxopt (1.1.7)
- h5py (2.5)
- Sphinx (1.5.2 -- only for documentation building)

Notes and Known Issues
----------------------

Matplotlib 2
~~~~~~~~~~~~
You will need to use SciPlot-PyQT v0.1.4 (or higher)
- Matplotlib 2 made numerous changes and deprecations that are being resolved
- See the installation instruction in the `SciPlot-pyQt README.md <https://github.com/CCampJr/SciPlot-PyQt>`__

Python 3.4
~~~~~~~~~~~
You will need to manually install PyQt5 and Qt5 or get it through a distribution
* PyQt5: https://www.riverbankcomputing.com/software/pyqt/download5
* Qt: https://www.qt.io/

PyQt 5.7 and WinPython 3.5
~~~~~~~~~~~~~~~~~~~~~~~~~~
There is a bug in PyQt 5.7.* that will prevent SciPlot's tables from showing the individual plot entries 
(see https://www.riverbankcomputing.com/pipermail/pyqt/2017-January/038483.html). Apparently, this will be fixed in 5.7.2.

- As WinPython 3.5.2.3Qt5 and 3.5.2.2Qt5 use PyQt 5.7.*, it is advised to use WinPython 3.5.2.1Qt5 or 3.4.4.5Qt5 until the matter is sorted out.
- Alternatively, one can uninstall pyqt5.7.* and force an install of <= 5.6.*.

SciPlot-PyQt
~~~~~~~~~~~~
Currently, SciPlot >= 0.1.3 is not available through pip. You can however clone the repository from github.
(see https://github.com/CCampJr/SciPlot-PyQt)

Instructions
------------

Git Dynamic copy
~~~~~~~~~~~~~~~~~~~
::

  # Make new directory for crikit2 (DIR)
  # Clone from github
  git clone https://github.com/CoherentRamanNIST/crikit2.git ./DIR

  # Within install directory (DIR)
  pip3 install -e .

  # To update installation, from within crikit2 directory
  git pull

Git Static copy
~~~~~~~~~~~~~~~~~~~
::

  # Make new directory for crikit2 (DIR)
  # Clone from github
  git clone https://github.com/CoherentRamanNIST/crikit2.git ./DIR

  # Within install directory (DIR)
  pip3 install .

  # You can now delete the source files you downloaded

(Re)-Building documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The documentation was built using Sphinx. A pre-built version of the html
files is included with this module, but you may wish to rebuild on your own
system.::

  # Build all APIs
  # From within the docs/ directory
  sphinx-apidoc -o ./source/ ../crikit/

  # Build API w/o pyuic5-generated files
  sphinx-apidoc -f -o .\source\ ..\crikit\ ..\crikit\ui\qt_* ..\crikit\ui\*_rc* ..\crikit\ui\old\**

  make html  
  # On Windows
  make.bat html
