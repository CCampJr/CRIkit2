"""
Coherent Raman Imaging toolKit 2:  User Interface Loader (main)
===============================================================

Use of this loader makes all the directories in the path properly and prevents \
the need to use odd _init.py path appending

For more info, see the docstring for crikit.CRIkitUI

References
----------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.


Authors
-------
Charles H. Camp Jr. <charles.camp@nist.gov>

"""

import sys as _sys
import os as _os
from PyQt5.QtWidgets import (QApplication as _QApplication)
from crikit import CRIkitUI
from crikit.ui.utils.check_requirements import check_requirements

def main(args=None):
    """
    The main routine.
    """

    if args is None:
        args = _sys.argv[1:]

    print('Starting up crikit2...')

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    has_requirements = check_requirements()
    if has_requirements:
        win = CRIkitUI.CRIkitUI_process() ### EDIT ###


        win.showMaximized()

        app.exec_()
    else:
        print('Closing... need to upgrade libraries')
        app.quit()
if __name__ == '__main__':
    _sys.exit(main())