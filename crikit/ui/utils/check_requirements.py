import sys as _sys
from packaging.version import parse

from PyQt5.QtWidgets import (QApplication as _QApplication)
from PyQt5.QtWidgets import QMessageBox as _QMsg


def check_requirements():
    """ Check that all necessary libraries are installed and to the correct version """
    
    output = []

    # ! Assumes version numbers are >=
    # Not the best way to do it, but fine for now
    requirement_dict = {'numpy':None,
                        'matplotlib':None, 
                        'scipy':None,
                        'sciplot': '0.2.2', 
                        'cvxopt':None,
                        'lazy5':'0.2.2'}

    output = []
    for r in requirement_dict:
        try:
            temp = __import__(r)
            if requirement_dict[r]:
                if not (parse(temp.__version__) >= parse(requirement_dict[r])):
                    output.append([r, requirement_dict[r]])
            else:
                pass
            del temp
        except Exception as e:
            print(e)
            output.append([r, requirement_dict[r]])
    
    if output:
        output_str = ''.join('\n{}>={}'.format(o[0],o[1]) if o[1] is not None else '\n{}'.format(o[0],o[1]) for o in output)
        msg = _QMsg(_QMsg.Critical, 'Please Upgrade Libraries', 
                    'Please upgrade the following libraries:')
        msg.setInformativeText(output_str)
        msg.exec()
        return False
    else:
        return True


if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setQuitOnLastWindowClosed(True)
    app.setStyle('Cleanlooks')
    check_requirements()
    app.quit()
    _sys.exit()