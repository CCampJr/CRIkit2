# -*- coding: utf-8 -*-
"""
Coherent Raman Imaging toolKit User Interface Loader (main)
=======================================================

Use of this loader makes all the directories in the path properly and prevents \
the need to use odd _init.py path appending

For more info, see the docstring for crikit.CRIkitUI

References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.


Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("16.04.01")
"""



if __name__ == '__main__':

    import sys as _sys
    import os as _os
    _sys.path.append(_os.path.abspath('../sciplot_pyqt5'))
    from PyQt5.QtWidgets import (QApplication as _QApplication)

    from crikit import CRIkitUI
    #sys.exit(CRIkitUI.run())

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    win = CRIkitUI.CRIkitUI_process() ### EDIT ###


    win.showMaximized()

    _sys.exit(app.exec_())
