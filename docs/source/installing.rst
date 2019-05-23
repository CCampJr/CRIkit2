.. image:: _static/CRIkit2_Logo.png
    :align: left

|
|
|
|
|
|
|

Installation Information
=========================

Dependencies
-------------

Note: These are the developmental system specs. Older versions of certain
packages may work.

-   python >= 3.4

    -   Tested with 3.4.4, 3.5.2, 3.6.1, 3.7.2

-   NumPy
-   SciPy
-   matplotlib (1.*, 2.*, 3.*)
-   packaging
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

The GUI may appear squashed with small font. There is a work-around
 described at https://github.com/CCampJr/CRIkit2/issues/79

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

Option 3: Installation via pip
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: 

    pip install CRIkit2


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

