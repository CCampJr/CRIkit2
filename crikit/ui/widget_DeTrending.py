"""
Widget for PlotEffect that contains and presents different detrending
algorithms. Whichever algorithm is plugged in effectively acts as the
widget as far as PlotEffect is concerned.

Created on Wed Dec  7 13:36:48 2016

@author: chc
"""

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QRadioButton as _QRadioButton,
                             QButtonGroup as _QButtonGroup)

from crikit.ui.qt_PlotEffect_DeTrending import Ui_Form as _Ui_Form

# At Minimum import ALS
from crikit.ui.widget_ALS import widgetALS
_widget_list_names = ['ALS']
_widget_list_classes = [widgetALS]

# Try to add arPLS to detrend options
try:
    from crikit.ui.widget_ArPLS import widgetArPLS
except Exception:
    pass
else:
    _widget_list_names.append('ArPLS')
    _widget_list_classes.append(widgetArPLS)
    
from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

class widgetDeTrending(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that contains and presents different detrending
    algorithms. Whichever algorithm is plugged in effectively acts as the
    widget as far as PlotEffect is concerned.
    
    """
        
    def __init__(self, parent = None):
        super(widgetDeTrending, self).__init__(parent) ### EDIT ###
        self.ui = _Ui_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.widget_list_names = _widget_list_names
        self.ui.widget_list = []
        for cl in _widget_list_classes:
            self.ui.widget_list.append(cl())
        
        self.ui.buttonGroup = _QButtonGroup()
        self.ui.radio_button_list = []
        
        for num, (wdgt, name) in enumerate(zip(self.ui.widget_list, 
                                               self.ui.widget_list_names)):

            self.ui.verticalLayoutWidgets.insertWidget(num, wdgt)
            self.ui.radio_button_list.append(_QRadioButton(name))
            self.ui.verticalLayoutButtons.insertWidget(num, self.ui.radio_button_list[num])
            self.ui.buttonGroup.addButton(self.ui.radio_button_list[num],0)
            if num == 0:
                wdgt.setVisible(True)
                self.ui.radio_button_list[0].setChecked(True)
                self.fcn = wdgt.fcn
                self.parameters = wdgt.parameters
                self.labels_orig = wdgt.labels_orig
                self.labels_affected = wdgt.labels_affected
                
                # Connect the changed-signal from the active widget
                # to this container's version of the change-signal
                try:
                    wdgt.changed.connect(self.widgetOptionsChanged)
                except Exception:
                    pass
            else:
                wdgt.setVisible(False)
                try:
                    wdgt.changed.disconnect(self.widgetOptionsChanged)
                except Exception:
                    pass
                
        # SIGNALS & SLOTS
        
        # Active widget changed
        self.ui.buttonGroup.buttonClicked.connect(self.changeWidget)
        
    def widgetOptionsChanged(self):
        """
        Options within the active widget were changed
        """
        self.changed.emit()
        
    def changeWidget(self, buttonId):
        """
        Change active widget
        """
        
        selection = self.ui.radio_button_list.index(buttonId)
        
        for num, (wdgt, name) in enumerate(zip(self.ui.widget_list, 
                                             self.ui.widget_list_names)):
            if num == selection:
                wdgt.setVisible(True)
                self.ui.radio_button_list[num].setChecked(True)
                self.fcn = wdgt.fcn
                self.parameters = wdgt.parameters
                self.labels_orig = wdgt.labels_orig
                self.labels_affected = wdgt.labels_affected
                
                # Connect the changed-signal from the active widget
                # to this container's version of the change-signal
                try:
                    wdgt.changed.connect(self.widgetOptionsChanged)
                except Exception:
                    pass
            else:
                wdgt.setVisible(False)
                
                # Disconnect non-active widget's changed-signal
                try:
                    wdgt.changed.disconnect(self.widgetOptionsChanged)
                except Exception:
                    pass
                
        self.changed.emit()
        

if __name__ == '__main__':
    
    import sys as _sys
    
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = widgetDeTrending()
    
    win.show()
    
    app.exec_()
    print(win.parameters)
    _sys.exit()
    