"""
From https://gist.github.com/jdreaver -- scientificspin.py

Created on Wed Dec  7 10:39:26 2016

@author: chc
"""

import re

from PyQt5 import QtWidgets, QtGui

# Regular expression to find floats. Match groups are the whole string, the
# whole coefficient, the decimal part of the coefficient, and the exponent
# part.
_float_re = re.compile(r'(([+-]?\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?)')

def valid_float_string(string):
    match = _float_re.search(string)
    return match.groups()[0] == string if match else False

class FloatValidator(QtGui.QValidator):

    def validate(self, string, position):
        if valid_float_string(string):
            state = QtGui.QValidator.Acceptable
        elif string == "" or string[position-1] in 'e.-+':
            state = QtGui.QValidator.Intermediate
        else:
            state = QtGui.QValidator.Invalid
        return (state, string, position)
    
    def fixup(self, text):
        match = _float_re.search(text)
        return match.groups()[0] if match else ""

class ScientificDoubleSpinBox(QtWidgets.QDoubleSpinBox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMinimum(-1e20)
        self.setMaximum(1e20)
        self.validator = FloatValidator()
        self.setDecimals(100)
        
    def validate(self, text, position):
        return self.validator.validate(text, position)
    
    def fixup(self, text):
        return self.validator.fixup(text)
    
    def valueFromText(self, text):
        return float(text)
    
    def textFromValue(self, value):
        return format_float(value)
    
    def stepBy(self, steps):
        text = self.cleanText()
        groups = _float_re.search(text).groups()
        decimal = float(groups[1])
        decimal += steps
        new_string = "{:g}".format(decimal) + (groups[3] if groups[3] else "")
        self.lineEdit().setText(new_string)
        
def format_float(value):
    """Modified form of the 'g' format specifier."""
    string = "{:g}".format(value).replace("e+", "e")
    string = re.sub("e(-?)0*(\d+)", r"e\1\2", string)
    return string