"""
Widget for PlotEffect that adjusts the parameters appropriate for
Savitky-Golay filtering

Created on Thu Dec 22 11:18:36 2016

@author: chc
"""

from scipy.signal import savgol_filter as _sg

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_SG import Ui_Form as _Ui_Form

class widgetSG(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    Savitky-Golay filtering


    Parameters
    ----------
    window_length : int
        Window length

    polyorder : int
        Polynomial order
        
    parent : QObject
        Parent
        
    Methods
    ---------
    fcn : Performs the Savitky-Golay

    Signals:
        changed : a value in the UI has changed

    """

    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'SG', 
                  'long_name' : 'Savitky-Golay filtering'}
    
    # Labeling options for original data plot
    labels_orig = {
                   'x_label' : 'Wavenumber (cm$^{-1}$)',
                   'y_label' : 'Input Int (au)',
                   'title' : 'Original'
                   }
    
    # Labeling options for affected data plot              
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : 'Difference (au)',
                       'title' : 'Difference'
                      }
                      

    def __init__(self, window_length=601, polyorder=2, parent = None):
        super(widgetSG, self).__init__(parent)
        self.ui = _Ui_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        # Update parameter dict
        self.parameters['window_length'] = window_length
        self.parameters['polyorder'] = polyorder
                
        # Window size must be > polyorder
        if self.parameters['window_length'] <= self.parameters['polyorder']:
            self.parameters['window_length'] = self.parameters['polyorder'] + 1
            
        # Window size must be odd
        if self.parameters['window_length'] % 2 == 1:
            pass
        else:
            self.parameters['window_length'] += 1

        self.ui.spinBoxWinSize.setValue(self.parameters['window_length'])
        self.ui.spinBoxOrder.setValue(self.parameters['polyorder'])

        # SIGNALS & SLOTS
        self.ui.spinBoxWinSize.editingFinished.connect(self.changeWinSize)
        self.ui.spinBoxOrder.editingFinished.connect(self.changeOrder)

    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """

        baseline = _sg(data_in, window_length=self.parameters['window_length'],
                       polyorder=self.parameters['polyorder'], axis=-1)
        data_out = data_in - baseline

        return [baseline, data_out]

    def changeWinSize(self):
        temp_win_size = self.ui.spinBoxWinSize.value()
        if temp_win_size % 2 == 1:
            self.parameters['window_length'] = temp_win_size
        else:
            self.ui.spinBoxWinSize.setValue(temp_win_size + 1)
            self.parameters['window_length'] = temp_win_size + 1
        self.changed.emit()

    def changeOrder(self):
        self.parameters['polyorder'] = self.ui.spinBoxOrder.value()
        self.changed.emit()
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    win = widgetSG()
    
    win.show()
    
    app.exec_()
    print(win.parameters)
    _sys.exit()