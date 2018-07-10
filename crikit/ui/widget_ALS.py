"""
Widget for PlotEffect that adjusts the parameters appropriate for
asymmetric least squares (ALS)

Created on Thu Dec 22 01:16:01 2016

@author: chc
"""
import numpy as _np

from PyQt5.QtWidgets import QTableWidgetItem as _QTableWidgetItem

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin
                                                 as _AbstractPlotEffectPlugin)

from crikit.ui.qt_PlotEffect_ALS2 import Ui_Form as _Ui_Form

from crikit.ui.widget_scientificspin import (ScientificDoubleSpinBox as
                                             _SciSpin)

from crikit.preprocess.algorithms.als import AlsCvxopt as _Als
from crikit.utils.general import find_nearest as _find_nearest

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

    def __init__(self, x=None, rng=None, smoothness_param=1, asym_param=1e-3, redux=10,
                 order=2, fix_end_points=True, fix_const=1, fix_rng=None,
                 max_iter=100, min_diff=1e-6, verbose=False, sub_asym_list=None,
                 sub_w_list=None, parent = None):

        super(widgetALS, self).__init__(parent) ### EDIT ###

        self._x = x
        self.rng = rng
        

        self.ui = _Ui_Form()
        self.ui.setupUi(self)


        self.sub_asym_list = sub_asym_list
        self.sub_w_list = sub_w_list

        # ! Change this into its own function after
        # ! the asym table widget is all setup
        if not self.sub_asym_list:
            self.parameters['asym_param'] = asym_param
        else:
            self.parameters['asym_param'] = 0*self.x + asym_param

        # Update parameter dict
        self.parameters['smoothness_param'] = smoothness_param
        self.parameters['rng'] = rng
        self.parameters['redux'] = redux
        self.parameters['order'] = order
        self.parameters['fix_end_points'] = fix_end_points
        self.parameters['fix_rng'] = fix_rng
        self.parameters['fix_const'] = fix_const
        self.parameters['max_iter'] = max_iter
        self.parameters['min_diff'] = min_diff
        self.parameters['verbose'] = verbose

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

        self.ui.spinBoxMaxIter.editingFinished.connect(self.spinBoxChanged)
        self.ui.spinBoxMinDiff.editingFinished.connect(self.spinBoxChanged)

        self.ui.checkBox.clicked.connect(self.selectFixedEnds)

        self.ui.spinBoxAsymSubSections.valueChanged.connect(self.asym_sub_val_change)
        self.ui.spinBoxWSubSections.valueChanged.connect(self.weight_sub_val_change)

        self.ui.spinBoxWeight = _SciSpin()
        self.ui.spinBoxWeight.setMinimum(0)
        self.ui.spinBoxWeight.setMaximum(1e10)
        self.ui.spinBoxWeight.setValue(1)
        self.ui.spinBoxWeight.editingFinished.connect(self.weightspinboxchanged)
        self.ui.verticalLayout_7.insertWidget(1, self.ui.spinBoxWeight)

    @property
    def x(self):
        if self.rng is None:
            return self._x
        else:
            return self._x[self.rng]

    def weight_sub_val_change(self):
        """ Weights Subsections spinbox has changed value """
        sbval = self.ui.spinBoxWSubSections.value()
        n_rows = self.ui.tableWidgetWeights.rowCount()
        n_cols = self.ui.tableWidgetWeights.columnCount()

        max_x = _np.max(self.x)
        min_x = _np.min(self.x)

        if sbval > n_rows:
            for nr in _np.arange(n_rows, sbval):
                self.ui.tableWidgetWeights.setRowCount(sbval)
                n_rows = self.ui.tableWidgetWeights.rowCount()

                # Start X
                scispin = _SciSpin()
                scispin.setMinimum(self._x.min())
                scispin.setMaximum(self._x.max())
                scispin.setValue(min_x)
                scispin.editingFinished.connect(self.weightspinboxchanged)
                self.ui.tableWidgetWeights.setCellWidget(nr, 0, scispin)

                # Stop X
                scispin = _SciSpin()
                scispin.setMinimum(self._x.min())
                scispin.setMaximum(self._x.max())
                scispin.setValue(max_x)
                scispin.editingFinished.connect(self.weightspinboxchanged)
                self.ui.tableWidgetWeights.setCellWidget(nr, 1, scispin)

                # Weight Parameter
                # scispin = _SciSpin()
                # scispin.setMinimum(0)
                # scispin.setMaximum(1e4)
                # scispin.setValue(1)
                # scispin.editingFinished.connect(self.weightspinboxchanged)
                # self.ui.tableWidgetWeights.setCellWidget(nr, 2, scispin)
        elif sbval < n_rows:
            for nr in _np.arange(sbval, n_rows):
                for nc in range(n_cols):
                    sw = self.ui.tableWidgetWeights.cellWidget(nr, nc)
                    sw.editingFinished.disconnect()

            self.ui.tableWidgetWeights.setRowCount(sbval)
            n_rows = self.ui.tableWidgetWeights.rowCount()

        self.weightspinboxchanged()

    def asym_sub_val_change(self):
        """ P Subsections spinbox has changed value """
        sbval = self.ui.spinBoxAsymSubSections.value()
        n_rows = self.ui.tableWidgetAsym.rowCount()
        n_cols = self.ui.tableWidgetAsym.columnCount()

        max_x = _np.max(self.x)
        min_x = _np.min(self.x)

        if sbval > n_rows:
            for nr in _np.arange(n_rows, sbval):
                self.ui.tableWidgetAsym.setRowCount(sbval)
                n_rows = self.ui.tableWidgetAsym.rowCount()

                # Start X
                scispin = _SciSpin()
                scispin.setMinimum(self._x.min())
                scispin.setMaximum(self._x.max())
                scispin.setValue(min_x)
                scispin.editingFinished.connect(self.asymspinboxchanged)
                self.ui.tableWidgetAsym.setCellWidget(nr, 0, scispin)

                # Stop X
                scispin = _SciSpin()
                scispin.setMinimum(self._x.min())
                scispin.setMaximum(self._x.max())
                scispin.setValue(max_x)
                scispin.editingFinished.connect(self.asymspinboxchanged)
                self.ui.tableWidgetAsym.setCellWidget(nr, 1, scispin)

                # Asym Parameter
                scispin = _SciSpin()
                scispin.setMinimum(0)
                scispin.setMaximum(1e20)
                scispin.setValue(self.ui.spinBoxP.value())
                scispin.editingFinished.connect(self.asymspinboxchanged)
                self.ui.tableWidgetAsym.setCellWidget(nr, 2, scispin)
        elif sbval < n_rows:
            for nr in _np.arange(sbval, n_rows):
                for nc in range(n_cols):
                    sw = self.ui.tableWidgetAsym.cellWidget(nr, nc)
                    sw.editingFinished.disconnect()

            self.ui.tableWidgetAsym.setRowCount(sbval)
            n_rows = self.ui.tableWidgetAsym.rowCount()

        self.asymspinboxchanged()

    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """

        data_out = _np.zeros(data_in.shape)
        baseline = _np.zeros(data_in.shape)

        # if callable(self.parameters['asym_param']):
        #     self.parameters['asym_param'] = \
        #         self.parameters['asym_param'](data_in.shape[-1])

        # smoothness_param = self.parameters['smoothness_param']
        # asym_param = self.parameters['asym_param']
        # redux = self.parameters['redux']
        # fep = self.parameters['fix_end_points']
        # max_iter = self.parameters['max_iter']
        # min_diff = self.parameters['min_diff']
        # order = self.parameters['order']
        # rng = self.parameters['rng']
        # fix_rng = self.parameters['fix_rng']
        # smoothness_param=1e3, asym_param=1e-4, redux=1,
        #          order=2, rng=None, fix_end_points=False, fix_rng=None, 
        #          fix_const=1, max_iter=100, min_diff=1e-5, verbose=False

        _als = _Als(**self.parameters)

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

    def asymspinboxchanged(self):
        """
        Asymetry parameter-related values have changed
        """
        n_rows = self.ui.tableWidgetAsym.rowCount()
        
        # * Currently, asym_param in ALS is in the full vector space
        x = self._x

        self.sub_asym_list = []

        if n_rows == 0:
            self.parameters['asym_param'] = self.ui.spinBoxP.value()
        else:
            self.parameters['asym_param'] = self.ui.spinBoxP.value() + 0*x
            for rc in range(n_rows):
                xstart_pix = _find_nearest(x,
                                           self.ui.tableWidgetAsym.cellWidget(rc, 0).value())[1]
                xstop_pix = _find_nearest(x,
                                          self.ui.tableWidgetAsym.cellWidget(rc, 1).value())[1]
                asym = self.ui.tableWidgetAsym.cellWidget(rc, 2).value()

                self.parameters['asym_param'][xstart_pix:xstop_pix+1] = 1*asym
                print('XStart: {}, XStop: {}, ASym: {}'.format(xstart_pix, xstop_pix, asym))
                self.sub_asym_list.append([xstart_pix, xstop_pix, asym])

            print('---------')
        self.changed.emit()
    
    def weightspinboxchanged(self):
        """
        Weight parameter-related values have changed
        """
        n_rows = self.ui.tableWidgetWeights.rowCount()
        
        # * Currently, fix_rng (weight parameters) in ALS is in the rng vector space
        x = self.x

        self.sub_w_list = []

        if n_rows == 0:
            self.parameters['fix_rng'] = None
        else:
            self.parameters['fix_rng'] = []
            for rc in range(n_rows):
                xstart_pix = _find_nearest(x,
                                           self.ui.tableWidgetWeights.cellWidget(rc, 0).value())[1]
                xstop_pix = _find_nearest(x,
                                          self.ui.tableWidgetWeights.cellWidget(rc, 1).value())[1]
                weight = self.ui.spinBoxWeight.value()

                # self.parameters['fix_rng'].extend(_np.arange(xstart_pix, xstop_pix+1).tolist())
                self.parameters['fix_rng'].extend(_np.arange(xstart_pix, xstop_pix).tolist())  # No +1

                # self.parameters['asym_param'][xstart_pix:xstop_pix+1] = 1*asym
                # print('XStart: {}, XStop: {}, ASym: {}'.format(xstart_pix, xstop_pix, asym))
                self.sub_w_list.append([xstart_pix, xstop_pix, weight])
            self.parameters['fix_rng'] = _np.array(self.parameters['fix_rng'])
            self.parameters['fix_const'] = self.ui.spinBoxWeight.value()
            print('---------')
        self.changed.emit()

    def spinBoxChanged(self):
        """
        Controller for all spinBoxes
        """
        sdr = self.sender()

        if sdr == self.ui.spinBoxLambda:
            self.parameters['smoothness_param'] = self.ui.spinBoxLambda.value()

        elif sdr == self.ui.spinBoxP:
            self.asymspinboxchanged()

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

    x = _np.linspace(500, 4000, 1001)
    winALS = widgetALS(x=x)

    winALS.show()

    app.exec_()
    print(winALS.parameters)
    _sys.exit()