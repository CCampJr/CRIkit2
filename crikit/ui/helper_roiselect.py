"""
"""

# Append sys path
import sys as _sys
import os as _os


# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget,
                             QDialog as _QDialog,
                             QMainWindow as _QMainWindow,
                             QSizePolicy as _QSizePolicy,
                             QTableWidgetItem as _QTableWidgetItem,
                             QTableView as _QTableView,
                             QColorDialog as _QColorDialog,
                             QDoubleSpinBox as _QDoubleSpinBox,
                             QComboBox as _QComboBox,
                             QPushButton as _QPushButton,
                             QLineEdit as _QLineEdit,
                             QStyle as _QStyle,
                             QStyledItemDelegate as _QStyledItemDelegate)

from PyQt5.QtCore import (QAbstractItemModel as _QAbstractItemModel,
                          QAbstractTableModel as _QAbstractTableModel,
                          QModelIndex as _QModelIndex,
                          QVariant as _QVariant,
                          Qt as _Qt)

from PyQt5.QtGui import (QPixmap as _QPixmap,
                         QIcon as _QIcon,
                         QColor as _QColor)

# Other imports
import numpy as _np

# Import from Designer-based GUI
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

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as _FigureCanvas, \
    NavigationToolbar2QT as _NavigationToolbar)

from matplotlib.figure import Figure as _Figure

class _PointsData:
    def __init__(self, num_current_plots=0):
        self.x = None
        self.y = None
        self.xpix = None
        self.ypix = None

        self.style = plotStyle(num_current_plots)


class ImageSelection:
    def __init__(self, parent=None):
        self.pointdata_list = []

    @property
    def num_selections(self):
        return len(self.pointdata_list)

    def clear_all(self):
        self.__init__()

    def append_selection(self, xpix, ypix, x=None, y=None):
        pt = _PointsData(self.num_selections)
        if xpix is not None:
            pt.xpix = xpix
            pt.ypix = ypix

            if (x is not None and y is not None):
                pt.x = x
                pt.y = y
            else:
                pt.x = xpix
                pt.y = ypix
        else:
            pass
        self.pointdata_list.append(pt)

if __name__ == '__main__':

    from PyQt5 import QtCore, QtGui, QtWidgets

    class Ui_MainWindow(object):

        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(984, 658)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout.setObjectName("gridLayout")
            self.verticalLayout = QtWidgets.QVBoxLayout()
            self.verticalLayout.setObjectName("verticalLayout")
            self.pushbutton = QtWidgets.QPushButton('Test')
            self.verticalLayout.addWidget(self.pushbutton)
            self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 984, 21))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    class testWindow(_QMainWindow):
        def __init__(self, parent=None):
            super(testWindow, self).__init__(parent) ### EDIT ###
            self.ui = Ui_MainWindow() ### EDIT ###
            self.ui.setupUi(self)     ### EDIT ###

    def buttonPress():
        winTest.cid = winTest.ui.mpl.canvas.mpl_connect('button_press_event', pointClick)

    def pointClick(event):
        if event.inaxes == winTest.ui.mpl.ax:
            x = int(_np.round(event.xdata))
            y = int(_np.round(event.ydata))


            selectiondata.append_selection(x,y)
            updatePlot()
            winTest.ui.mpl.canvas.mpl_disconnect(winTest.cid)

    def updatePlot():
        winTest.ui.mpl.ax.clear()
        winTest.ui.mpl.img = winTest.ui.mpl.ax.imshow(data_slice, interpolation='none', cmap = _mpl.cm.gray , origin='lower')
        getx = winTest.ui.mpl.ax.get_xlim()
        gety = winTest.ui.mpl.ax.get_ylim()

        winTest.ui.mpl.ax.hold(True)
        for pts in selectiondata.pointdata_list:
            winTest.ui.mpl.ax.plot(pts.x, pts.y,
                                   marker='+',
                                   markersize=pts.style.markersize,
                                   markerfacecolor=pts.style.color,
                                   markeredgecolor=pts.style.color,
                                   linestyle='None')

        winTest.ui.mpl.ax.set_xlim(getx)
        winTest.ui.mpl.ax.set_ylim(gety)

        winTest.ui.mpl.canvas.draw()

    class _winMpl:
        def __init__(self):
            self.fig = None
            self.ax = None
            self.img = None
            self.canvas = None
            self.toolbar = None

    app = _QApplication(_sys.argv)

    winTest = testWindow()
    winTest.ui.mpl = _winMpl()
    winTest.ui.mpl.fig = _Figure()
    winTest.ui.mpl.ax = winTest.ui.mpl.fig.add_subplot(111)

    data = _np.random.rand(20,20,50)
    data_slice = data[:,:,25]

    winTest.ui.mpl.img = winTest.ui.mpl.ax.imshow(data_slice, interpolation='none', cmap = _mpl.cm.gray , origin='lower')
    winTest.ui.mpl.canvas = _FigureCanvas(winTest.ui.mpl.fig)

    winTest.ui.verticalLayout.insertWidget(0,winTest.ui.mpl.canvas)

    winTest.ui.pushbutton.pressed.connect(buttonPress)

    winTest.show()

    selectiondata = ImageSelection()

    _sys.exit(app.exec_())