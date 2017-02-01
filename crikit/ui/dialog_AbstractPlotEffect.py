"""
Created on Thu Dec 22 10:04:39 2016

@author: chc
"""

from PyQt5.QtWidgets import (QWidget as _QWidget)
from PyQt5.QtCore import (pyqtSignal as _pyqtSignal)

class AbstractPlotEffectPlugin(_QWidget):
    
    parameters = {
                  'name' : 'Name',
                  'long_name' : 'Longer Name'
                  }
    
    labels_orig = {
                   'x_label' : 'x',
                   'y_label' : 'y',
                   'title' : 'Original'
                   }
                   
    labels_affected = {
                       'x_label' : 'x',
                       'y_label' : 'y',
                       'title' : 'Affected'
                      }
                   
    changed = _pyqtSignal()
    
#    def __init__(self):
#        raise NotImplementedError
        
    def fcn(self, data_in):
        raise NotImplementedError