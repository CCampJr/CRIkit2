"""
Widget for PlotEffect that adjusts the parameters appropriate for
asymmetric least squares (ALS)

Created on Thu Dec 22 01:16:01 2016

@author: chc
"""
import numpy as _np

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_ALS2 import Ui_Form as _Ui_Form

from crikit.ui.widget_scientificspin import (ScientificDoubleSpinBox as
                                             _SciSpin)

from crikit.preprocess.algorithms.als import AlsCvxopt as _Als

class widgetALS(_AbstractPlotEffectPlugin):
    """
    Widget for PlotEffect that adjusts the parameters appropriate for
    asymmetric least squares (ALS)
    
    Parameters
    ----------
    smoothness_param : float, optional (default, 1e3)
        Smoothness parameter

    asym_param : float, optional (default, 1e-4)
        Assymetry parameter
        
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
    fcn : Perform ALS detrending
    
    Signals:
        changed : a value in the UI has changed
    """
    
    # Parameter dict that will be returned from PlotEffect
    # Will be updated later in program to contain all parameters
    # to pass to underlying algorithm
    parameters = {'name' : 'ALS', 
                  'long_name' : 'Asymmetric least squares'}
    
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
                      
    def __init__(self, asym_param=1e-3, smoothness_param=1, redux=10,
                 pstart=1e-2, pend=1e-3, fixed_p=True, fix_end_points=True, 
                 max_iter=100, min_diff=1e-6, parent = None):
                      
        super(widgetALS, self).__init__(parent) ### EDIT ###
        
        self.ui = _Ui_Form()
        self.ui.setupUi(self)
        
        # Update parameter dict
        self.parameters['smoothness_param'] = smoothness_param
        self.parameters['asym_param'] = asym_param
        self.parameters['fixed_p'] = fixed_p
        self.parameters['asym_param_start'] = pstart
        self.parameters['asym_param_end'] = pend
        self.parameters['redux'] = redux
        self.parameters['fix_end_points'] = fix_end_points
        self.parameters['max_iter'] = max_iter
        self.parameters['min_diff'] = min_diff
        
        self.setup_asym()  # Setup controls for asymmetry parameter
        self.setup_smoothness()  # Setup controls for smoothness parameter
        
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
        self.ui.spinBoxP.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxLambda.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxRedux.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.spinBoxPStart.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxPEnd.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxMaxIter.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxMinDiff.editingFinished.connect(self.spinBoxChanged)
        
        self.ui.radioButtonFixedP.clicked.connect(self.selectFixedOrLog)
        self.ui.radioButtonLogLinearP.clicked.connect(self.selectFixedOrLog)
        self.ui.checkBox.clicked.connect(self.selectFixedEnds)
        
    
    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """
        
        data_out = _np.zeros(data_in.shape)
        baseline = _np.zeros(data_in.shape)
        
        if callable(self.parameters['asym_param']):
            self.parameters['asym_param'] = \
                self.parameters['asym_param'](data_in.shape[-1])
        
        smoothness_param = self.parameters['smoothness_param']
        asym_param = self.parameters['asym_param']
        redux = self.parameters['redux']
        fep = self.parameters['fix_end_points']
        max_iter = self.parameters['max_iter']
        min_diff = self.parameters['min_diff']
        
        _als = _Als(smoothness_param=smoothness_param, 
                    asym_param=asym_param, 
                    redux=redux, fix_end_points=fep, 
                    max_iter=max_iter, 
                    min_diff=min_diff)
        
        if data_in.ndim == 1:
            baseline = _als.calculate(data_in)
            data_out = data_in - baseline
        else:
            for num, spectrum in enumerate(data_in):
                baseline[num,:] = _als.calculate(spectrum)
                data_out[num,:] = spectrum - baseline[num,:]
        return [baseline, data_out]
        
    
    def setup_smoothness(self):
        """ 
        Lambda/smoothness parameter rlated
        """
        
        self.ui.label_2.setText('{} (Smoothness)'.format(u'\u03BB'))
        self.ui.spinBoxLambda = _SciSpin()
        self.ui.verticalLayout_2.insertWidget(1, self.ui.spinBoxLambda)
        self.ui.spinBoxLambda.setValue(self.parameters['smoothness_param'])
        
    def setup_asym(self):
        """
        P/asymmetry parameter related
        """
        
        
        self.ui.spinBoxP = _SciSpin()
        self.ui.verticalLayout.insertWidget(1, self.ui.spinBoxP)
        self.ui.spinBoxP.setValue(self.parameters['asym_param'])
        if self.parameters['fixed_p']:
            self.ui.radioButtonFixedP.setChecked(True)
            self.ui.radioButtonLogLinearP.setChecked(False)
        else:
            self.ui.radioButtonFixedP.setChecked(False)
            self.ui.radioButtonLogLinearP.setChecked(True)
        self.selectFixedOrLog()
            
        self.ui.spinBoxPStart = _SciSpin()
        self.ui.verticalLayout_5.insertWidget(1, self.ui.spinBoxPStart)
        self.ui.spinBoxPStart.setValue(self.parameters['asym_param_start'])
        
        self.ui.spinBoxPEnd = _SciSpin()
        self.ui.verticalLayout_6.insertWidget(1, self.ui.spinBoxPEnd)
        self.ui.spinBoxPEnd.setValue(self.parameters['asym_param_end'])
        
    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """

        sdr = self.sender()
        
        if sdr == self.ui.spinBoxPStart:
            self.parameters['asym_param_start'] = self.ui.spinBoxPStart.value()
            self.selectFixedOrLog()
            
        elif sdr == self.ui.spinBoxPEnd:
            self.parameters['asym_param_end'] = self.ui.spinBoxPEnd.value()
            self.selectFixedOrLog()
            
        elif sdr == self.ui.spinBoxLambda:
            self.parameters['smoothness_param'] = self.ui.spinBoxLambda.value()
        
        elif sdr == self.ui.spinBoxP:
            self.parameters['asym_param'] = self.ui.spinBoxP.value()
    
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
        
    def selectFixedOrLog(self):
        """
        Check fixed or log-linear asymmetry parameter
        """
        
        self.parameters['fixed_p'] = self.ui.radioButtonFixedP.isChecked()
        if self.parameters['fixed_p']:
            self.ui.radioButtonFixedP.setChecked(True)
            self.ui.radioButtonLogLinearP.setChecked(False)
            self.ui.frame_2.setEnabled(False)
            self.ui.frame.setEnabled(True)
#            self.p = lambda x: self.ui.spinBoxP.value()
            self.parameters['asym_param'] = self.ui.spinBoxP.value()
            
        else:
            self.ui.radioButtonFixedP.setChecked(False)
            self.ui.radioButtonLogLinearP.setChecked(True)
            self.ui.frame_2.setEnabled(True)
            self.ui.frame.setEnabled(False)
            self.parameters['asym_param'] = \
                lambda x: _np.logspace(_np.log10(self.parameters['asym_param_start']),
                                       _np.log10(self.parameters['asym_param_end']),x) 

        self.changed.emit()
        
        
if __name__ == '__main__':
    import sys as _sys
    from PyQt5.QtWidgets import (QApplication as _QApplication)
    
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    winALS = widgetALS()
    
    winALS.show()
    
    app.exec_()
    print(winALS.parameters)
    _sys.exit()