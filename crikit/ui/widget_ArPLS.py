"""
Widget for PlotEffect that adjusts the parameters appropriate for
asymmetrically reweights penalized least squares (arPLS)

Created on Thu Dec 22 01:16:01 2016

@author: chc
"""
import numpy as _np

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                     as
                                                     _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_ArPLS import Ui_Form as _Ui_Form

from crikit.ui.widget_scientificspin import (ScientificDoubleSpinBox as
                                             _SciSpin)

from crikit.preprocess.algorithms.arpls import ArPlsCvxopt as _Arpls

class widgetArPLS(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    asymmetrically reweights penalized least squares (arPLS)
    
    Parameters
    ----------
    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    redux : int, optional (default, 1)
        Reduction parameter to sub-sample input signal
        
    order : int, optional (default, 2)
        Derivative regularization term. Order=2 for Whittaker-smoother
    
    fix_end_points : bool, optional (default, False)
        Weight the baseline endpoints to approach equally the end-points
        of the data.
    
    max_iter : int, optional (default, 100)
        Maximum number of least-squares iterations to perform
        
    min_diff : float, optional (default, 1e-5)
        Break iterative calculations if difference is less than min_diff
        
    parent: QObject
        Parent
        
    Methods
    -------
    fcn : Perform arPLS detrending
    
    Signals:
        changed : a value in the UI has changed
    """
    
    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'arPLS', 
                  'long_name' : 'Asymmetrically reweighted penalized least \
                  squares'}
    
    # Labeling options for original data plot
    labels_orig = {
                   'x_label' : 'Wavenumber (cm$^{-1}$)',
                   'y_label' : 'Input Int (au)',
                   'title' : 'Original'
                   }
    
    # Labeling options for affected data plot                             
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : 'Output Int (au)',
                       'title' : 'Detrended'
                      }
                      
    def __init__(self, smoothness_param=1, redux=1, fix_end_points=True, 
                 max_iter=100, min_diff=1e-6, parent = None):
                      
        super(widgetArPLS, self).__init__(parent) ### EDIT ###
        
        self.ui = _Ui_Form()
        self.ui.setupUi(self)##
        
        # Update parameter dict
        self.parameters['smoothness_param'] = smoothness_param
        self.parameters['redux'] = redux
        self.parameters['fix_end_points'] = fix_end_points
        self.parameters['max_iter'] = max_iter
        self.parameters['min_diff'] = min_diff
        
        
        # Lambda/smoothness parameter rlated
        self.ui.label_2.setText('{} (Smoothness)'.format(u'\u03BB'))
        self.ui.spinBoxLambda = _SciSpin()
        self.ui.verticalLayout_2.insertWidget(1, self.ui.spinBoxLambda)
        self.ui.spinBoxLambda.setValue(self.parameters['smoothness_param'])
                
        # Redux factor
        self.ui.spinBoxRedux.setValue(self.parameters['redux'])

        # Fixed ends
        self.ui.checkBox.setChecked(self.parameters['fix_end_points'])
        
        # Max iterations
        self.ui.spinBoxMaxIter.setValue(self.parameters['max_iter'])
        
        # Min Difference
        self.ui.spinBoxMinDiff = _SciSpin()
        self.ui.verticalLayout_9.insertWidget(4, self.ui.spinBoxMinDiff)
        self.ui.spinBoxMinDiff.setValue(self.parameters['min_diff'])
        
        # SIGNALS & SLOTS
        self.ui.spinBoxLambda.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxRedux.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.spinBoxMaxIter.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxMinDiff.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.checkBox.clicked.connect(self.selectFixedEnds)
        
    
    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """
        
        data_out = _np.zeros(data_in.shape)
        baseline = _np.zeros(data_in.shape)
               
        smoothness_param = self.parameters['smoothness_param']
        redux = self.parameters['redux']
        fep = self.parameters['fix_end_points']
        max_iter = self.parameters['max_iter']
        min_diff = self.parameters['min_diff']
        
        _arpls = _Arpls(smoothness_param=smoothness_param, 
                        redux=redux, fix_end_points=fep, 
                        max_iter=max_iter, 
                        min_diff=min_diff, verbose=False)
        
        if data_in.ndim == 1:
            baseline = _arpls.calculate(data_in)
            data_out = data_in - baseline
        else:
            for num, spectrum in enumerate(data_in):
                baseline[num,:] = _arpls.calculate(spectrum)
                data_out[num,:] = spectrum - baseline[num,:]
        return [baseline, data_out]
        
    
    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """
        
        sdr = self.sender()
        
        if sdr == self.ui.spinBoxLambda:
            self.parameters['smoothness_param'] = self.ui.spinBoxLambda.value()
        
        elif sdr == self.ui.spinBoxRedux:
            self.parameters['redux'] = self.ui.spinBoxRedux.value()
            
        elif sdr == self.ui.spinBoxMaxIter:
            self.parameters['max_iter'] = self.ui.spinBoxMaxIter.value()
            
        elif sdr == self.ui.spinBoxMinDiff:
            self.parameters['min_diff'] = self.ui.spinBoxMinDiff.value()
            
        self.changed.emit()
        
    def selectFixedEnds(self):
        """
        Check selection of fixed end-points
        """
        
        self.parameters['fix_end_points'] =self.ui.checkBox.isChecked()
        self.changed.emit()
        
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    winArPLS = widgetArPLS()
    
    winArPLS.show()
    
    app.exec_()
    print(winArPLS.parameters)
    _sys.exit()