"""
Extensible Dialog that shows the effect of a plugin on input data.

Created on Wed Dec 21 21:36:00 2016

@author: chc
"""
import numpy as _np

from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)
from PyQt5 import QtWidgets as _QtWidgets

from crikit.ui.qt_PlotEffect import Ui_Dialog as Ui_DialogPlotEffect

from crikit.ui.dialog_AbstractPlotEffect import (AbstractPlotEffectPlugin 
                                                     as
                                                     _AbstractPlotEffectPlugin)

from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

class DialogPlotEffect(_QDialog):
    """
    Extensible Dialog that shows the effect of a plugin on input data.
    
    Parameters
    ----------
    
    data : ndarray (ND)
        Input data
    
    x : ndarray (1D)
        Independent variable
        
    plugin : sub-class of AbstractPlotEffectPlugin
        Plugin class instance
        
    parent : QObject
        Parent
    """

    TRANSPOSE_ARR = True
    
    def __init__(self, data, x=None, plugin=None, mpl_kwargs={'width':8, 'height':2}, parent=None):
        super(DialogPlotEffect, self).__init__(parent)
        self.ui = Ui_DialogPlotEffect()
        self.ui.setupUi(self)

        self.data = data
        
        # Setup MPL containers
        self.mpl_orig = _MplCanvas(subplot=111, **mpl_kwargs)
        self.mpl_orig.fig.canvas.setMinimumSize(100,200)
        self.mpl_orig.fig.canvas.setSizePolicy(_QtWidgets.QSizePolicy.Expanding, _QtWidgets.QSizePolicy.Minimum)

        self.mpl_affected = _MplCanvas(subplot=111, **mpl_kwargs)
        self.mpl_affected.fig.canvas.setMinimumSize(100,200)
        self.mpl_affected.fig.canvas.setSizePolicy(_QtWidgets.QSizePolicy.Expanding, _QtWidgets.QSizePolicy.Minimum)

        # Show(), although not needed, enables mpl-tight_layout 
        # to work later on
        self.show()
        
        self.ui.verticalLayout.insertWidget(1, self.mpl_orig, stretch=1)
        self.ui.verticalLayout.insertWidget(1, self.mpl_orig.toolbar)
        
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected)
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected.toolbar)

        # Plugin that brings functionality to PlotEffect
        self.plugin = plugin
        
        
        # Signal emited when something changes in the plugin widget
        self.plugin.changed.connect(self.widget_changed)
            
        # Setup indep. variable
        if x is None:
            self.x = _np.linspace(0,data.shape[0],self.data.shape[0])
        else:
            self.x = x

        self.make_orig_plots(self.data)
                
        if self.plugin is not None:
            self.ui.verticalLayout.insertWidget(8, plugin)
        
        self.show()
        self.widget_changed()
        self.mpl_orig.draw()
        self.mpl_affected.draw()

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        
    def make_orig_plots(self, data, lw=1, ls='-'):
        """

        """
        self.make_plots(self.mpl_orig, data, lw=lw, ls=ls)

    def make_affected_plots(self, data, lw=1, ls='-'):
        """

        """
        self.make_plots(self.mpl_affected, data, lw=lw, ls=ls)
        
    def make_plots(self, canvas, data, lw=1, ls='-'):
        """

        """
        # If data is a list (assumed to be a list of ndarrays),
        # plot each item in list
        if isinstance(data, _np.ndarray):
            # TRANSPOSE ARRAY in case of plt.plot(data) -- in a for-loop, this is opposite
            if self.TRANSPOSE_ARR:
                if data.ndim > 1:
                    for num, d in enumerate(data):
                        canvas.ax.plot(self.x,d, lw=lw, ls=ls, color='C{}'.format(num % 10))
                else:
                    canvas.ax.plot(self.x,data, lw=lw, ls=ls, color='C0')
            else:
                if data.ndim > 1:
                    for num, d in enumerate(data.T):
                        canvas.ax.plot(self.x,d, lw=lw, color='C{}'.format(num % 10))
                else:
                    canvas.ax.plot(self.x,data, lw=lw, color='C0')

        elif isinstance(data, list):
            for d in data:
                if d.ndim > 1:
                    if self.TRANSPOSE_ARR:
                        for num, d2 in enumerate(d):
                            canvas.ax.plot(self.x, d2, lw=lw, ls=ls, color='C{}'.format(num % 10))
                    else:
                        for num, d2 in enumerate(d.T):
                            canvas.ax.plot(self.x, d2, lw=lw, ls=ls, color='C{}'.format(num % 10))
                else:
                    canvas.ax.plot(self.x, d, lw=lw, ls=ls, color='C0')                
            
        self.plot_labels()
        try:
            canvas.fig.tight_layout()
        except Exception:
            print('Tight layout failed (dialog_ploteffect')
        
        
    @staticmethod
    def dialogPlotEffect(data, x=None, plugin=None, parent=None):
        """
        Static method that is actually called
        """        
        dialog = DialogPlotEffect(data, x=x, plugin=plugin, 
                                  parent=parent)
        # Resize to fit plugin
        if dialog.width() < dialog.plugin.width():
            dialog.resize(int(dialog.plugin.width()*1.1), dialog.height())

        result = dialog.exec_()  # 1 = Accepted, 0 = Rejected/Canceled
        
        if result == 1:
            return dialog.plugin
        else:
            return None
            
    def widget_changed(self):
        """
        Plugin widget has changed. Re-submit data to plugin function.
        """
        try:
            affected_data = self.plugin.fcn(self.data)
        except Exception as e:
            print('Error in plugin.fcn: {}'.format(e))
        else:
            # If affected_data is a list, [0] is added to the original data
            # plots and is bolded
            if isinstance(affected_data, list):
                # Split affected data into the addon and te affected axis
                # data
                orig_data_addon = affected_data[0]
                affected_data = affected_data[1]
                
            else:
                orig_data_addon = None
            
            # If there already exists an original plot, keep those
            # axis limits upon re-plotting
            if len(self.mpl_orig.ax.lines) > 0:
                lim_orig = self.mpl_orig.ax.axis()
            else:
                lim_orig = None
                
            self.mpl_orig.ax.clear()
            
            self.make_orig_plots(self.data)
            
            if orig_data_addon is not None:
                self.make_orig_plots(orig_data_addon, lw=0.75, ls=':')

            # If there already exists an affected plot, keep those
            # axis limits upon re-plotting
            if len(self.mpl_affected.ax.lines) > 0:
                lim_affected = self.mpl_affected.ax.axis()
            else:
                lim_affected = None
                
            # If affected data return is None, hide the affected axis
            if affected_data is None:
                self.mpl_affected.setVisible(False)
                self.mpl_affected.toolbar.setVisible(False)
            else:
                self.mpl_affected.setVisible(True)
                self.mpl_affected.toolbar.setVisible(True)
                
                self.mpl_affected.ax.clear()
                self.make_affected_plots(affected_data)
            
            # Reset axis limits to previous setting before re-plotting
            if lim_orig is not None:
                self.mpl_orig.ax.axis(lim_orig)
                
            # Reset axis limits to previous setting before re-plotting
            if lim_affected is not None:
                self.mpl_affected.ax.axis(lim_affected)
                
            self.mpl_orig.draw()
            self.mpl_affected.draw()
            
    def plot_labels(self):
        """
        Add axis labels and titles
        """
        self._plot_labels_ax(self.mpl_orig.ax, self.plugin.labels_orig)
        self._plot_labels_ax(self.mpl_affected.ax, self.plugin.labels_affected)
    
    def _plot_labels_ax(self, ax, labels):
        for k in labels:
            val = labels[k]
            k_lower = k.lower()
            if k_lower == 'x_label':
                ax.set_xlabel(val)
            elif k_lower == 'y_label':
                ax.set_ylabel(val)
            elif k_lower == 'title':
                ax.set_title(val)
                
        
class widgetDemoPlotEffectPlugin(_AbstractPlotEffectPlugin):
    """
    Very simple demo of a plugin
    """
    
    parameters = {'name' : 'DEMO', 
                  'long_name' : 'Demo of PlotEffectPlugins'}
    
    labels_orig = {
                   'x_label' : 'Wavenumber (cm$^{-1}$)',
                   'y_label' : 'Input Int (au)',
                   'title' : 'Original'
                   }
                   
    labels_affected = {
                       'x_label' : labels_orig['x_label'],
                       'y_label' : 'Output Int (au)',
                       'title' : 'Affected'
                      }
                    
    def __init__(self, offset=0.1, parent=None):
        super(widgetDemoPlotEffectPlugin, self).__init__(parent) ### EDIT ###
        
        self.parameters['offset'] = offset 
    
    def fcn(self, data_in):
        """
        If return list, [0] goes to original, [1] goes to affected
        """
        return [0*data_in + .1, data_in + .1]
        
    
if __name__ == '__main__':
    
    import sys as _sys

    app = _QApplication(_sys.argv)
    
    # from crikit.ui.widget_Cut_every_n_spectra import widgetCutEveryNSpectra

    # x_reps = _np.arange(100)
    # dark = _np.random.rand(100,800)
    # dark[::10] *= 2

    # plugin = widgetCutEveryNSpectra()
    # winPlotEffect = DialogPlotEffect.dialogPlotEffect(dark.sum(axis=-1), x=x_reps, plugin=plugin)
    # if winPlotEffect is not None:
    #     print(winPlotEffect.parameters)
    # _sys.exit()

    WN = _np.linspace(500,4000,800)
    

    # calib_dict = {'n_pix' : 1600,
    #               'ctr_wl' : 730,
    #               'ctr_wl0' : 730,
    #               'a_vec' : [-0.167740721307557, 863.8736708961577],
    #               'probe': 771.461}
                  
    # pix = _np.arange(calib_dict['n_pix'])
    # wl = calib_dict['a_vec'][0]*pix + calib_dict['a_vec'][1]
    # WN = .01/(wl*1e-9) - .01/(calib_dict['probe']*1e-9)
    
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
    CARS = _np.dot(_np.arange(1,4)[:,None],CARS[None,:])
    
    
    
    # NRB_LEFT = 20e3*_np.exp(-(WN)**2/(1000**2)) + 500
    # NRB_RIGHT = 6e3*_np.exp(-(WN-2500)**2/(400**2)) + 500
    
    # NRB_LEFT[WN<500] *= 0
    # NRB_LEFT[WN<500] += 1e-6
    # NRB_RIGHT[WN<500] *= 0
    # NRB_RIGHT[WN<500] += 1e-6
    
    # from crikit.cri.merge_nrbs import MergeNRBs as _MergeNRBs
    # from crikit.utils.general import find_nearest as _find_nearest
    # NRB2 = _MergeNRBs(nrb_left=NRB_LEFT, nrb_right=NRB_RIGHT, 
    #                  pix=_find_nearest(WN, 1885.0)[1],
    #                  left_side_scale=False).calculate()
    
    # CARS2 = _np.abs(500*(1/(1000-WN-1j*20) + 1/(2700-WN-1j*20)) + NRB2**0.5)**2
    # CARS2 = _np.dot(_np.ones((3,1), dtype=_np.double),CARS2[None,:])
    
#    # Demo
#    plugin = widgetDemoPlotEffectPlugin()
#    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
#                                                            plugin=plugin)
#    if winPlotEffect is not None:
#        print(winPlotEffect.parameters)
#
#    # ALS
    from crikit.ui.widget_ALS import widgetALS as _widgetALS

    plugin = _widgetALS(x=WN)
    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
                                                            plugin=plugin)
    if winPlotEffect is not None:
        print(winPlotEffect.parameters)
#
#    # ArPLS
#    from crikit.ui.widget_ArPLS import widgetArPLS as _widgetArPLS
#    plugin = _widgetArPLS()
#    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
#                                                            plugin=plugin)
#    if winPlotEffect is not None:
#        print(winPlotEffect.parameters)
#    
#    # Detrending
#    from crikit.ui.widget_DeTrending import (widgetDeTrending as 
#                                                  _widgetDeTrending)
#    plugin = _widgetDeTrending()
#    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
#                                                            plugin=plugin)
#    if winPlotEffect is not None:
#        print(winPlotEffect.parameters)
#    
#    # SG
#    from crikit.ui.widget_SG import (widgetSG as _widgetSG)
#    plugin = _widgetSG()
#    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
#                                                            plugin=plugin)
#    if winPlotEffect is not None:
#        print(winPlotEffect.parameters)
#    
   # KK
    # from crikit.ui.widget_KK import (widgetKK as _widgetKK)
    # plugin = _widgetKK()
    # winPlotEffect = DialogPlotEffect.dialogPlotEffect([NRB,CARS], x=WN,
    #                                                        plugin=plugin)
    # if winPlotEffect is not None:
    #     print(winPlotEffect.parameters)
        
#    # Calibrate
#    from crikit.ui.widget_Calibrate import (widgetCalibrate as 
#                                                _widgetCalibrate)
#    plugin = _widgetCalibrate(calib_dict)
#    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN,
#                                                            plugin=plugin)
#    if winPlotEffect is not None:
#        print(winPlotEffect.parameters)
    
    # Merge NRBs
    # from crikit.ui.widget_mergeNRBs import (widgetMergeNRBs as 
    #                                         _widgetMergeNRBs)
    # plugin = _widgetMergeNRBs(WN, NRB_LEFT, NRB_RIGHT)
    # winPlotEffect = DialogPlotEffectFuture.dialogPlotEffect(CARS2, x=WN,
    #                                                         plugin=plugin)
    # if winPlotEffect is not None:
    #     print(winPlotEffect.parameters)
        
    
    
    
    
    
    
#        print('P-Value: {}'.format(winPlotEffect.p))
#        print('Lambda-Value: {}'.format(winPlotEffect.lam))
#        print('Redux: {}'.format(winPlotEffect.redux))
#        
    _sys.exit()
