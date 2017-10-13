"""
Plot-Effect Interface (crikit.ui.subui_ploteffect)
=======================================================


TODO: Do some manual tight layout assessment to make sure labels and titles \
are fully visible

"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog,
                             QColorDialog as _QColorDialog,
                             QDoubleSpinBox as _QDoubleSpinBox,
                             QComboBox as _QComboBox,
                             QLineEdit as _QLineEdit,
                             QStyledItemDelegate as _QStyledItemDelegate,
                             QWidget as _QWidget)

from PyQt5.QtCore import (QAbstractTableModel as _QAbstractTableModel,
                          QModelIndex as _QModelIndex,
                          QVariant as _QVariant,
                          Qt as _Qt,
                          pyqtSignal as _pyqtSignal,
                          QObject as _QObject)

from PyQt5.QtGui import (QPixmap as _QPixmap,
                         QIcon as _QIcon,
                         QColor as _QColor)

# Other imports
import numpy as _np

# Import from Designer-based GUI
from crikit.ui.qt_PlotEffect import Ui_Dialog as Ui_DialogPlotEffect
from crikit.ui.helper_plotOptions import plotStyle

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10
_mpl.rcParams['savefig.dpi'] = 300
_mpl.rcParams['figure.figsize'] = (4, 4)
#_mpl.rcParams['figure.autolayout'] = True
_mpl.rcParams['legend.fontsize'] = 10

from matplotlib.backends.backend_qt5agg import \
    (FigureCanvasQTAgg as _FigureCanvas,
     NavigationToolbar2QT as _NavigationToolbar)

from matplotlib.figure import Figure as _Figure


class _winMpl:
        def __init__(self):
            self.fig = None
            self.ax = None
            self.img = None
            self.canvas = None
            self.toolbar = None

class DialogPlotEffect(_QDialog):
    """
    Plotter subUI class
    """
    XLABEL = 'X (au)'
    YLABEL = 'Y (au)'
    
    def __init__(self, data, x=None, plugin=None, xlabel=None, ylabel=None, show_difference=False, parent=None):
        super(DialogPlotEffect, self).__init__(parent)
        self.ui = Ui_DialogPlotEffect()
        self.ui.setupUi(self)

        self.data = data
        
        self.mpl_orig = _winMpl()
        self.mpl_orig.fig = _Figure(facecolor=[1, 1, 1])
        self.mpl_orig.ax = self.mpl_orig.fig.add_subplot(111)
        self.mpl_orig.canvas = _FigureCanvas(self.mpl_orig.fig)
        self.mpl_orig.toolbar = _NavigationToolbar(self.mpl_orig.canvas, None)
        
        self.mpl_affected = _winMpl()
        self.mpl_affected.fig = _Figure(facecolor=[1, 1, 1])
        self.mpl_affected.ax = self.mpl_affected.fig.add_subplot(111)
        self.mpl_affected.canvas = _FigureCanvas(self.mpl_affected.fig)
        self.mpl_affected.toolbar = _NavigationToolbar(self.mpl_affected.canvas, None)

        self.ui.verticalLayout.insertWidget(1, self.mpl_orig.canvas)
        self.ui.verticalLayout.insertWidget(1, self.mpl_orig.toolbar)
        
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected.canvas)
        self.ui.verticalLayout.insertWidget(3, self.mpl_affected.toolbar)
        
        # Plugin that brings functionality to PlotEffect
        self.plugin = plugin
        
        # Signal emited when something changes in the plugin widget
        self.plugin.changed.connect(self.widget_changed)
        
        if xlabel is None:
            self.ui.xlabel = self.XLABEL
        else:
            self.ui.xlabel = xlabel

        if ylabel is None:
            self.ui.ylabel = self.YLABEL
        else:
            self.ui.ylabel = ylabel
            
        if x is None:
            self.x = _np.linspace(0,data.shape[0],self.data.shape[0])
        else:
            self.x = x
        
        self.show_diff = show_difference

        
        if not isinstance(data, list):
            try:
                self.mpl_orig.ax.plot(self.x,data)
            except:
                self.mpl_orig.ax.plot(self.x,data.T)
            
            self.mpl_orig.ax.xaxis.set_label_text(self.ui.xlabel)
            self.mpl_orig.ax.yaxis.set_label_text(self.ui.ylabel)
#            self.mpl_orig.fig.tight_layout(rect=[-.05,0.05,1,.95])
            self.mpl_orig.ax.set_title('Original')
        else:
            if self.plugin is not None:
                
                try:
                    self.mpl_orig.ax.plot(self.x,self.plugin.fcn(self.data))
                except:
                    self.mpl_orig.ax.plot(self.x,self.plugin.fcn(self.data).T)
                    
                self.mpl_orig.ax.xaxis.set_label_text(self.ui.xlabel)
                self.mpl_orig.ax.yaxis.set_label_text(self.ui.ylabel)
#                self.mpl_orig.fig.tight_layout(rect=[0,0.05,1,.9])
                self.mpl_orig.ax.set_title('Original')
                
        if self.plugin is not None:
            self.ui.verticalLayout.insertWidget(8, plugin)
        
        self.widget_changed()
        self.mpl_orig.canvas.draw()
        self.mpl_affected.canvas.draw()

        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
    
    def widget_changed(self):
        """
        Plugin widget has changed. Re-submit data to plugin function.
        """
#        try:
#            print(self.data.shape)
#        except:
#            pass
        if self.plugin is not None:
            self.mpl_affected.ax.clear()
            try:
#                print('Here 1')
                affected_data = self.plugin.fcn(self.data).T
                self.mpl_affected.ax.plot(self.x,affected_data)
            except:
                try:
#                    print('Here 2')
                    affected_data = self.plugin.fcn(self.data)
                    self.mpl_affected.ax.plot(self.x,affected_data)
                except:
                    pass
            self.mpl_affected.ax.xaxis.set_label_text(self.ui.xlabel)
            self.mpl_affected.ax.yaxis.set_label_text(self.ui.ylabel)
            self.mpl_affected.ax.set_title('Processed')
#            self.mpl_affected.fig.tight_layout(rect=[0,0.05,1,.95])
            
            self.mpl_affected.canvas.draw()
            
            if self.show_diff:
                self.mpl_orig.ax.clear()
                if not isinstance(self.data, list):
                    try:
                        self.mpl_orig.ax.plot(self.x,self.data.T)
                    except:
                        try:
                            self.mpl_orig.ax.plot(self.x,self.data)
                        except:
                            pass
                    
                    try:
                        self.mpl_orig.ax.plot(self.x,self.data.T-affected_data, linestyle='dashed')
                    except:
                        try:
                            self.mpl_orig.ax.plot(self.x,self.data-affected_data, linestyle='dashed')
                        except:
                            pass
                    
                        
                    self.mpl_orig.ax.xaxis.set_label_text(self.ui.xlabel)
                    self.mpl_orig.ax.yaxis.set_label_text(self.ui.ylabel)
        #            self.mpl_orig.fig.tight_layout(rect=[-.05,0.05,1,.95])
                    self.mpl_orig.ax.set_title('Original')
            self.mpl_orig.canvas.draw()
        
    @staticmethod
    def dialogPlotEffect(data, x = None, plugin=None, xlabel=None, ylabel=None, 
                         show_difference=False, parent = None):
        """
        Executes DialogPlotEffect
        
        Parameters
        ----------
        data : (np.ndarray, list)
            Array for straightforward plotting, list if plugin.fcn requires \
            multiple inputs
        plugin : object
            Plugin container class
        xlabel : str
            String describing independent variable
        ylabel : str
            String describing dependent variable
        show_difference : bool
            Plot the difference between the original data and the affected \
            (perfomed-on) data overlaid with the original data. Note: \
            difference shown with dashed line
        parent : object
            Parent object
            
        Returns
        -------
        out : object
            Returns access to the plugin variables
                
        """        
        dialog = DialogPlotEffect(data, x=x, plugin=plugin, xlabel=xlabel, 
                                  ylabel=ylabel, show_difference=show_difference,
                                  parent=parent)
        
        result = dialog.exec_()  # 1 = Aceepted, 0 = Rejected/Canceled
        
        if result == 1:
            #print('----------------\nReturned: Ok!\n')
            #print(dialog.plugin.__dict__)
            
            return dialog.plugin
            
        else:
            #print('----------------\nReturned: Cancel!\n')
            return None
        
    
if __name__ == '__main__':

    from crikit.ui.widget_ploteffect import (widgetNothing, widgetKK,
                                             widgetALS, widgetSG, 
                                             widgetCalibrate)
    
    app = _QApplication(_sys.argv)
    
    
    #################
    # KK Demo
    plugin = widgetKK()
    
    WN = _np.linspace(500,4000,800)
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
    
    winPlotEffect = DialogPlotEffect.dialogPlotEffect([WN, NRB, CARS], x=WN, 
                                                      plugin=plugin, 
                                                      xlabel='Wavenumber (cm$^{-1}$)', 
                                                      ylabel='Imag. {$\chi_R$} (au)')
    
    if winPlotEffect is not None:
        print('CARS Bias: {}'.format(winPlotEffect.cars_bias))
        print('NRB Bias: {}'.format(winPlotEffect.nrb_bias))
        print('Norm by NRB: {}'.format(winPlotEffect.nrb_norm))
        print('Phase correction constant: {}'.format(winPlotEffect.phaselin))
        print('KK algorithm pad factor: {}'.format(winPlotEffect.pad_factor))
        print('Phase correction constant type: {}'.format(winPlotEffect.phase_type))
    ##################
    
    ################
    # ALS Demo
    plugin = widgetALS()
    
    WN = _np.linspace(500,4000,800)
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
    CARS = _np.dot(_np.ones((5,1)),CARS[None,:])
    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN, plugin=plugin,
                                                      xlabel='Wavenumber (cm$^{-1}$)',
                                                      ylabel='Imag. {$\chi_R$} (au)',
                                                      show_difference=True)
    
    if winPlotEffect is not None:
        print('P-Value: {}'.format(winPlotEffect.p))
        print('Lambda-Value: {}'.format(winPlotEffect.lam))
        print('Redux: {}'.format(winPlotEffect.redux))
        
    ################
    # SG Demo
    plugin = widgetSG(win_size=501, order=5)
    
    WN = _np.linspace(500,4000,800)
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
    CARS = _np.dot(_np.ones((5,1)),CARS[None,:])
    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN, plugin=plugin,
                                                      xlabel='Wavenumber (cm$^{-1}$)',
                                                      ylabel='Imag. {$\chi_R$} (au)',
                                                      show_difference=True)
    
    if winPlotEffect is not None:
        print('Window Size: {}'.format(winPlotEffect.win_size))
        print('Order: {}'.format(winPlotEffect.order))
        

    ################
    # Calibrate Demo
    plugin = widgetCalibrate()
    
    
    calib_dict = {}
    calib_dict['n_pix'] = 1600
    calib_dict['ctr_wl'] = 730.0
    calib_dict['ctr_wl0'] = 730.0
    calib_dict['probe'] = 771.461
    calib_dict['units'] = 'nm'
    calib_dict['a_vec'] = (-0.167740721307557, 863.8736708961577)  # slope, intercept

    from crikit.data.frequency import calib_pix_wl, calib_pix_wn
    wl_vec, units_wl = calib_pix_wl(calib_dict)
    WN, units_wn = calib_pix_wn(calib_dict)
    
    #WN = _np.linspace(500,4000,800)
    CARS = _np.abs(1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
    NRB = 0*WN + .055
#    CARS = _np.dot(_np.ones((5,1)),CARS[None,:])
    winPlotEffect = DialogPlotEffect.dialogPlotEffect(CARS, x=WN, plugin=plugin,
                                                      xlabel='Wavenumber (cm$^{-1}$)',
                                                      ylabel='Imag. {$\chi_R$} (au)',
                                                      show_difference=False)
    
    if winPlotEffect is not None:
        print('New Calibration Dictionary: {}'.format(winPlotEffect.new_calib_dict))
#        print('Order: {}'.format(winPlotEffect.order))

        
    #################
    # Nothing Demo
    plugin = widgetNothing()
    
    x = _np.linspace(1,100,100)
    data = _np.random.randn(100)
    
    winPlotEffect = DialogPlotEffect.dialogPlotEffect(data, x=x, plugin=plugin, xlabel='Wavenumber (cm$^{-1}$)', ylabel='Imag. {$\chi_R$} (au)')
    
    if winPlotEffect is not None:
        print('This plugin did nothing, as expected.')
    ##################
    
#    print(winPlotEffect.__dict__)

    _sys.exit()