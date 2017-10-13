"""
Created on Tue Feb 16 15:51:32 2016

@author: camp
"""

import sys as _sys
import os as _os

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget, QDialog as _QDialog,
                             QMainWindow as _QMainWindow,
                             QSizePolicy as _QSizePolicy)
import PyQt5.QtCore as _QtCore

# Other imports
import numpy as _np

from yapsy.PluginManager import (PluginManager as _PluginManager,
                                PluginInfo as _PluginInfo)

from crikit.ui.helper_plugin_categories import DeNoiser, ErrorCorrect
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Import from Designer-based GUI
from crikit.ui.qt_PluginSelector import Ui_Dialog


# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10
#import matplotlib.pyplot as plt

#from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as _FigureCanvas, \
#    NavigationToolbar2QT as _NavigationToolbar)

#from matplotlib.figure import Figure as _Figure

class DialogDenoisePlugins(_QDialog):
    """
    DialogDenoisePlugins : Denoise plugin selector
    
    Static Method
    -------------
    dialogDenoisePlugins : Used to call UI and retrieve results of dialog
    
    References
    ----------
    .. [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
    
    """

    def __init__(self, parent = None):
        super(DialogDenoisePlugins, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.temp = 0
        
        # Create plugin manager
        self.manager = _PluginManager()

        
        if _os.path.isdir(_os.path.abspath('./plugins')):
            plugins_loc = 'plugins'
        elif _os.path.isdir(_os.path.abspath('./crikit/ui/plugins')):
            plugins_loc = './crikit/ui/plugins'
        elif _os.path.isdir(_os.path.abspath('./ui/plugins')):
            plugins_loc = './ui/plugins'
        else:
            plugins_loc = None
            
        self.manager.setPluginPlaces([plugins_loc])
        self.manager.setCategoriesFilter({'DeNoiser' : DeNoiser})
        
        self.manager.collectPlugins()

        # Load plugins
        self.manager.locatePlugins()
        
        self.manager.loadPlugins()
        self.denoisers = {}
        self.denoiser_desc = {}
        
        for plugin in self.manager.getPluginsOfCategory('DeNoiser'):
            self.ui.comboBox.addItem(plugin.plugin_object.name)
            self.denoisers[plugin.plugin_object.name] = plugin.plugin_object
            self.denoiser_desc[plugin.plugin_object.name] = plugin._PluginInfo__details['Documentation']['description']
        
        #print(self.denoiser_desc[self.ui.comboBox.currentText])
        self.ui.plainTextEditDescription.setPlainText(self.denoiser_desc[self.ui.comboBox.currentText()])
        self.ui.comboBox.currentIndexChanged.connect(self.changeDesc)
    
    def changeDesc(self):
        self.ui.plainTextEditDescription.setPlainText(self.denoiser_desc[self.ui.comboBox.currentText()])
        
    @staticmethod
    def dialogDenoisePlugins(parent = None):
        """
        Static Method.
        
        XXX

        Inputs
        ----------
        None : None

        Returns
        ----------
        out : (tuple)
            XXX : (TYPE)

        """
        
        dialog = DialogDenoisePlugins(parent)

        result = dialog.exec_()
        
        
        if result == 1:  # Accepted
            return (dialog.denoisers[dialog.ui.comboBox.currentText()])
        else:  # Rejected/Cancel
            return None

class DialogErrCorrPlugins(_QDialog):
    """
    DialogErrCorrPlugins : Error correction plugin selector
    
    Static Method
    -------------
    dialogErrCorrPlugins : Used to call UI and retrieve results of dialog
    
    References
    ----------
    .. [1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
    Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
    Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.
    
    """
    
    def __init__(self, parent = None):
        super(DialogErrCorrPlugins, self).__init__(parent) ### EDIT ###
        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.temp = 0
        
        # Create plugin manager
        self.manager = _PluginManager()

        
        if _os.path.isdir(_os.path.abspath('./plugins')):
            plugins_loc = 'plugins'
        elif _os.path.isdir(_os.path.abspath('./crikit/ui/plugins')):
            plugins_loc = './crikit/ui/plugins'
        elif _os.path.isdir(_os.path.abspath('./ui/plugins')):
            plugins_loc = './ui/plugins'
        else:
            plugins_loc = None
            
        self.manager.setPluginPlaces([plugins_loc])
        self.manager.setCategoriesFilter({'ErrorCorrect' : ErrorCorrect})
        
        self.manager.collectPlugins()

        # Load plugins
        self.manager.locatePlugins()
        
        self.manager.loadPlugins()
        self.errcorrectors = {}
        self.errcorrectors_desc = {}
        
        for plugin in self.manager.getPluginsOfCategory('ErrorCorrect'):
            self.ui.comboBox.addItem(plugin.plugin_object.name)
            self.errcorrectors[plugin.plugin_object.name] = plugin.plugin_object
            self.errcorrectors_desc[plugin.plugin_object.name] = plugin._PluginInfo__details['Documentation']['description']
            
        self.ui.comboBox.currentIndexChanged.connect(self.changeDesc)

        try:
            self.ui.plainTextEditDescription.setPlainText(self.errcorrectors_desc[self.ui.comboBox.currentText()])
            
        except: # Fails if no plugins found
            pass
        
    def changeDesc(self):

        try:
            self.ui.plainTextEditDescription.setPlainText(self.errcorrectors_desc[self.ui.comboBox.currentText()])
        except: # Fails if no plugins found
            pass
        
    @staticmethod
    def dialogErrCorrPlugins(parent = None):
        """
        Static Method.
        
        XXX

        Inputs
        ----------
        None : None

        Returns
        ----------
        out : (tuple)
            XXX : (TYPE)

        """
        
        dialog = DialogErrCorrPlugins(parent)

        result = dialog.exec_()
        
        
        if result == 1:  # Accepted
            return (dialog.errcorrectors[dialog.ui.comboBox.currentText()])
        else:  # Rejected/Cancel
            return None
            
            
if __name__ == '__main__':

   
#    from crikit.data.classes import HSData
#    
    x = _np.linspace(100,200,50)
    y = _np.linspace(200,300,50)
    f = _np.linspace(500,3000,800)
    Ex = 30*_np.exp((-(f-1750)**2/(200**2)))
    Spectrum = _np.convolve(_np.flipud(Ex),Ex,mode='same')

    data = _np.zeros((y.size,x.size,f.size))
    for count in range(y.size):
        data[count,:,:] = y[count]*_np.random.poisson(_np.dot(x[:,None],Spectrum[None,:]))

    #temp = HSData()
    #temp.spectrafull = data
    
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    ### DeNoise Demo
    win = DialogDenoisePlugins.dialogDenoisePlugins()

    if win is not None:
        retwin = win.denoiseHSData(data)
        print('RetWin:{}'.format(retwin))
    
#    ### Error Correction Demo
#    win = DialogErrCorrPlugins.dialogErrCorrPlugins()
#    
##    temp = HSData()
#    
#    WN = _np.linspace(500,4000,1000)
#    
#    CARS = _np.zeros((20,20,WN.size), dtype=complex)
#    CARS[:,:,:] = (1/(1000-WN-1j*20) + 1/(3000-WN-1j*20) + .055)
#    temp.spectrafull = CARS
#    temp.freqvecfull = WN
#    
#    
#    NRB = 0*WN + .055
#    
#    if win is not None:
#        retwin = win.errorCorrectHSData(data)
#    #if win is not None:
#        #retwin = win.denoiseHSData(temp)
#        #print('RetWin:{}'.format(retwin))
#    
#    _sys.exit()
    app.exec_()