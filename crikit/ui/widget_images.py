# -*- coding: utf-8 -*-
"""
Visualization Widgets (crikit.ui.widget_images)
=======================================================

widgetColorMath : Mathematical operations on raw data leading to color \
    images

widgetBWImg : Grayscale imagery

widgetSglColor : Single-color imagery

widgetCompositeColor : Composite-color imagery

_mplWin : Matplotlib window container

Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("16.03.14")
"""

import sys as _sys
import numpy as _np

# Generic imports for QT-based programs
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QWidget as _QWidget,
                             QSizePolicy as _QSizePolicy,
                             QColorDialog as _QColorDialog)

import PyQt5.QtCore as _QtCore

# Import from Designer-based GUI
from crikit.ui.qt_SglColorImage import Ui_Form as Ui_SglColorImage_Form
from crikit.ui.qt_ColorMath import Ui_Form as Ui_ColorMath_Form
from crikit.ui.qt_BWImage import Ui_Form as Ui_BWImage_Form
from crikit.ui.qt_CompositeColor import Ui_Form as Ui_CompositeColor_Form
#from crikit.ui.widget_mpl import MplCanvas as _MplCanvas
from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

# Generic imports for MPL-incorporation
import matplotlib as _mpl
import sciplot as _sciplot
#import matplotlib.pyplot as _plt

_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 10
#import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as _NavigationToolbar)

from crikit.ui.classes_ui import BW, SingleColor, CompositeColor

class widgetColorMath(_QWidget):
    """
    Contains information about what mathematical operations are possible for \
    taking raw HSI data and converting it to grayscale/color.

    Software Info
    --------------

    Original Python branch: Feb 16 2015

    author: ("Charles H Camp Jr")

    email: ("charles.camp@nist.gov")

    version: ("16.03.14")
    """
    OPERATION_STRINGS = ['','+','-','*','/','Peak b/w troughs','SUM']
    OPERATION_FREQ_COUNT = [1, 2, 2, 2,2, 3, 2]
    COND_TYPE_STRINGS = ['>','<','=','<=','>=']

    def __init__(self, parent = None):
        super(widgetColorMath, self).__init__(parent) ### EDIT ###
        self.ui = Ui_ColorMath_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.comboBoxCondOps.addItem('OFF')

        for item in widgetColorMath.OPERATION_STRINGS:
            self.ui.comboBoxOperations.addItem(item)
            self.ui.comboBoxCondOps.addItem(item)

        for item in widgetColorMath.COND_TYPE_STRINGS:
            self.ui.comboBoxCondInEquality.addItem(item)

        self.ui.comboBoxOperations.currentIndexChanged.connect(self.operationchange)
        self.ui.comboBoxCondOps.currentIndexChanged.connect(self.condOpsChange)

    def condOpsChange(self):
        index = self.ui.comboBoxCondOps.currentIndex()

        if index == 0:
            num_freq = 0
        else:
            num_freq = widgetColorMath.OPERATION_FREQ_COUNT[index-1]

        self.ui.pushButtonCondFreq1.setEnabled(False)
        self.ui.pushButtonCondFreq2.setEnabled(False)
        self.ui.pushButtonCondFreq3.setEnabled(False)
        self.ui.comboBoxCondInEquality.setEnabled(False)
        self.ui.spinBoxInEquality.setEnabled(False)

        if num_freq >= 1:
            self.ui.pushButtonCondFreq1.setEnabled(True)
            self.ui.comboBoxCondInEquality.setEnabled(True)
            self.ui.spinBoxInEquality.setEnabled(True)
        if num_freq >= 2:
            self.ui.pushButtonCondFreq2.setEnabled(True)
        if num_freq >= 3:
            self.ui.pushButtonCondFreq3.setEnabled(True)

    def operationchange(self):
        index = self.ui.comboBoxOperations.currentIndex()

        num_freq = widgetColorMath.OPERATION_FREQ_COUNT[index]

        self.ui.pushButtonOpFreq1.setEnabled(False)
        self.ui.pushButtonOpFreq2.setEnabled(False)
        self.ui.pushButtonOpFreq3.setEnabled(False)

        if num_freq >= 1:
            self.ui.pushButtonOpFreq1.setEnabled(True)
        if num_freq >= 2:
            self.ui.pushButtonOpFreq2.setEnabled(True)
        if num_freq >= 3:
            self.ui.pushButtonOpFreq3.setEnabled(True)

class widgetBWImg(_QWidget):
    """
    Grayscale image widget
    """
    def __init__(self, parent = None, **kwargs):
        super(widgetBWImg, self).__init__(parent)
        self.ui = Ui_BWImage_Form()
        self.ui.setupUi(self)

        # Initialize underlying data
        self.initData()

        # Stand-in image data
        self.data.grayscaleimage = _np.dot(_np.ones([100,1]),_np.linspace(1,100,100)[None,:])
        self.data.set_x(_np.linspace(1,400,self.data.xlen))
        self.data.set_y(_np.linspace(1,400,self.data.ylen))
        
        # Calculate extent of image
        winextent = (self.data.x.min(), self.data.x.max(), self.data.y.min(), self.data.y.max())

        # MPL canvas
        self.mpl = _MplCanvas(**kwargs)
        self.mpl.cbar = None  # Monkey patch on a cbar object
        
        # Create stand-image plot
        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = winextent, showcbar = True,
                              axison = True)
        self.mpl.fig.tight_layout()
        
        # Insert canvas widget into this widget
        self.ui.verticalLayout.insertWidget(0,self.mpl,_QtCore.Qt.AlignHCenter)
        self.ui.verticalLayout.insertWidget(0,self.mpl.toolbar, _QtCore.Qt.AlignHCenter)

        # SIGNAL & SLOTS
        self.ui.checkBoxFixed.stateChanged.connect(self.checkBoxFixed)
        self.ui.checkBoxCompress.stateChanged.connect(self.checkBoxCompress)
        self.ui.checkBoxRemOutliers.stateChanged.connect(self.checkBoxRemOutliers)
        self.ui.spinBoxStdDevs.valueChanged.connect(self.spinBoxOutliersChanged)
        self.ui.lineEditMin.editingFinished.connect(self.textEditMinMaxSet)
        self.ui.lineEditMax.editingFinished.connect(self.textEditMinMaxSet)

    def initData(self):
        """
        (Re)-initialize self.data
        """
        self.data = BW()

    def createImg(self, img, xunits = None, yunits = None,
                  extent = None, showcbar = True, axison = True,
                  cmap = _mpl.cm.gray):
        self.mpl.ax.clear()
        self.mpl.img = self.mpl.ax.imshow(img, interpolation = 'none',
                                      extent = extent, cmap = cmap, origin='lower')
        if xunits is not None:
            self.mpl.ax.xaxis.set_label_text(xunits)
        if yunits is not None:
            self.mpl.ax.yaxis.set_label_text(yunits)

        if axison == False:
            self.mpl.ax.set_axis_off()

        if showcbar == True:
            if self.mpl.cbar is not None:
                self.mpl.cbar.remove()

            self.mpl.cbar = self.mpl.fig.colorbar(self.mpl.img)

        if self.ui.checkBoxFixed.isChecked() == False:
            self.ui.lineEditMax.setText(str(round(self.data.maxer,4)))
            self.ui.lineEditMin.setText(str(round(self.data.minner,4)))


    def textEditMinMaxSet(self):

        #len_min = len(self.ui.lineEditMin.text())
        #len_max = len(self.ui.lineEditMax.text())

        try:
            self.data.setmin = float(self.ui.lineEditMin.text())
            self.data.setmax = float(self.ui.lineEditMax.text())
            self.ui.checkBoxFixed.setChecked(True)
            self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
            self.mpl.draw()

        except:
            pass

    def spinBoxOutliersChanged(self):
        self.checkBoxRemOutliers()

    def checkBoxRemOutliers(self):
        """
        """
        if self.ui.checkBoxRemOutliers.isChecked() == False:
            self.data.setoutlierstds = None
        else:
            self.data.setoutlierstds = float(self.ui.spinBoxStdDevs.value())
        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

    def checkBoxFixed(self):
        """
        See if the min and max are identified as being fixed by
        checkbox
        """

        # See if there is a min and max in the textBrowsers

        len_min = len(self.ui.lineEditMin.text())
        len_max = len(self.ui.lineEditMax.text())

        if self.ui.checkBoxFixed.isChecked() == True:  # Checked
            if len_min > 0 and len_max > 0:
                try:
                    self.data.setmin = float(self.ui.lineEditMin.text())
                    self.data.setmax = float(self.ui.lineEditMax.text())
                    if self.ui.checkBoxCompress.isChecked() == False:
                        self.data.compress = False
                    else:
                        self.data.compress = True
                except:
                    pass
            else:
                pass
        else:
            self.data.setmin = None
            self.data.setmax = None
            self.data.compress = None

        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

    def checkBoxCompress(self):
        """
        See if compression is activated via the checkbox_4
        """

        if self.ui.checkBoxCompress.isChecked() == False:
            self.data.compress = False
        else:
            self.data.compress = True

        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

class widgetSglColor(_QWidget):
    """
    Single-color widget
    """

    COLORMAPS = {'Blue':[0, 0, 1], 'Red':[1, 0, 0], 'Green':[0, 1, 0],
                 'Cyan':[0, 1, 1], 'Magenta':[1, 0, 1], 'Yellow':[1, 1, 0],
                 'B&W':[1, 1, 1]}

    DEFAULT_COLORMAP_ORDER = ['Red', 'Green', 'Blue', 'B&W', 'Magenta', 'Yellow', 'Cyan', 'Other']

    def __init__(self, parent = None, **kwargs):
        super(widgetSglColor, self).__init__(parent)
        self.ui = Ui_SglColorImage_Form()
        self.math = widgetColorMath()
        self.ui.setupUi(self)
        for color in self.DEFAULT_COLORMAP_ORDER:
            self.ui.comboBox.addItem(color)

        # Initialize data
        self.initData()
        self.data.colormap = self.COLORMAPS[self.ui.comboBox.currentText()]
        self.external_plots = []
        
        # Create stand-in imahe                                    
        self.data.grayscaleimage = _np.dot(_np.ones([100,1]),_np.linspace(1,100,100)[None,:])
        self.data.set_x(_np.linspace(1,400,self.data.xlen))
        self.data.set_y(_np.linspace(1,400,self.data.ylen))

        # Instantiate MPL widget
        self.mpl = _MplCanvas(**kwargs)
        self.mpl.cbar = None  # Monkey patch on a cbar object

        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = False,
                              axison = False)

        self.mpl.fig.tight_layout()
        
       
        # Embed MPL widget into this widget
        self.ui.horizontalLayoutGainImg.addWidget(self.mpl)
        self.ui.verticalLayoutMain.insertWidget(1,self.mpl.toolbar, _QtCore.Qt.AlignVCenter)
        self.ui.verticalLayoutMain.addWidget(self.math)

        # SIGNALS & SLOTS
        self.ui.comboBox.currentIndexChanged.connect(self.changeColor)
        self.math.ui.lineEditMin.editingFinished.connect(self.textEditMinMaxSet)
        self.math.ui.lineEditMax.editingFinished.connect(self.textEditMinMaxSet)
        self.ui.gainSlider.valueChanged.connect(self.gainSliderChanged)
        self.ui.pushButtonGain1.pressed.connect(self.gain1)
        self.math.ui.checkBoxFixed.stateChanged.connect(self.checkBoxFixed)
        self.math.ui.checkBoxCompress.stateChanged.connect(self.checkBoxCompress)

        self.ui.pushButtonPop.pressed.connect(lambda: self.createImg_Ext(img = self.data.image,
                                                                         showcbar=False,
                                                                         extent=self.data.winextent,
                                                                         xunits=self.data.xunits,
                                                                         yunits=self.data.yunits))
        
        self.ui.pushButtonGSPop.pressed.connect(lambda: self.createImg_Ext(img = self.data.imageGS,
                                                                           showcbar=True,
                                                                           extent=self.data.winextent,
                                                                           xunits=self.data.xunits,
                                                                           yunits=self.data.yunits))

    def gain1(self):
        self.data.setgain = 1
        self.ui.gainSlider.setValue(10)
        self.ui.lineEditGainSlider.setText('1.0')

    def gainSliderChanged(self):
        sliderval = self.ui.gainSlider.value()/10

        self.data.setgain = sliderval

        self.ui.lineEditGainSlider.setText(str(sliderval))

        self.changeColor()

    def initData(self):
        """
        (Re)-initialize self.data
        """
        self.data = SingleColor()

    def textEditMinMaxSet(self):

        #len_min = len(self.ui.lineEditMin.text())
        #len_max = len(self.ui.lineEditMax.text())

        try:
            self.data.setmin = float(self.math.ui.lineEditMin.text())
            self.data.setmax = float(self.math.ui.lineEditMax.text())
#            self.createImg(img = self.data.image, xunits = self.data.xunits,
#                              yunits = self.data.yunits,
#                              extent = self.data.winextent, showcbar = True,
#                              axison = True)
#            self.mpl.draw()
            self.math.ui.checkBoxFixed.setChecked(True)
            self.changeColor()
        except:
            pass
    def changeColor(self):

        try:
            color_str = self.ui.comboBox.currentText()
            if color_str == 'Other':
                color = _QColorDialog.getColor().getRgb()
                color = [round(color[0]/255,2), round(color[1]/255,2), round(color[2]/255,2)]

                self.data.colormap = color
                self.ui.comboBox.addItem(str(color))
                self.COLORMAPS[str(color)] = color
                pos = self.ui.comboBox.findText(str(color))
                self.ui.comboBox.setCurrentIndex(pos)

            else:
                self.data.colormap = self.COLORMAPS[color_str]
            self.createImg(img = self.data.image, xunits = self.data.xunits,
                                  yunits = self.data.yunits,
                                  extent = self.data.winextent, showcbar = False,
                                  axison = False)
            self.mpl.draw()
        except:
            print('Error')

    def createImg(self, img, xunits = None, yunits = None,
                  extent = None, showcbar = False, axison = False,
                  cmap = _mpl.cm.gray):
        self.mpl.ax.clear()
        self.mpl.img = self.mpl.ax.imshow(img, interpolation = 'none',
                                      extent = extent, cmap = cmap, origin='lower')
        if xunits is not None:
            self.mpl.ax.xaxis.set_label_text(xunits)
        if yunits is not None:
            self.mpl.ax.yaxis.set_label_text(yunits)

        if axison == False:
            self.mpl.ax.set_axis_off()

        if showcbar == True:
            if self.mpl.cbar is not None:
                self.mpl.cbar.remove()

            self.mpl.cbar = self.mpl.fig.colorbar(self.mpl.img)

        if self.math.ui.checkBoxFixed.isChecked() == False:
            self.math.ui.lineEditMax.setText(str(round(self.data.maxer,4)))
            self.math.ui.lineEditMin.setText(str(round(self.data.minner,4)))

    def createImg_Ext(self, img, xunits = None, yunits = None,
                  extent = None, showcbar = True, axison = True,
                  cmap = _mpl.cm.gray):
        """
        Create new figure window and show image of img
        """

        self.external_plots.append(_sciplot.main(parent=self))
        self.external_plots[-1].imshow(img, x_label=xunits, y_label=yunits, 
                      cmap=cmap, cbar=showcbar, extent=extent)
        
#
        #new_win = _mplWin()
        #new_win.fig = _Figure(facecolor = [1,1,1])
        #new_win.fig = _plt.figure(figsize=(10,6))
        #plot_font = {'fontname':'Arial', 'size':'14'}
        #new_win.ax = new_win.fig.add_subplot(111)


        #new_win.img = new_win.ax.imshow(img, interpolation = 'none',
        #                              extent = extent, cmap = cmap, origin='lower')
#        if xunits is not None:
#            _plt.xlabel(xunits, **plot_font)
#        if yunits is not None:
#            _plt.ylabel(yunits, **plot_font)
#
#        if axison == False:
#            new_win.ax.set_axis_off()
#        else:
#            for label in (new_win.ax.get_xticklabels() + new_win.ax.get_yticklabels()):
#                label.set_fontname(plot_font['fontname'])
#                label.set_fontsize(plot_font['size'])
#        _plt.title("Color Image (Change Title)", **plot_font)
#        if showcbar == True:
#            if new_win.cbar is not None:
#                new_win.cbar.remove()
#
#            new_win.cbar = new_win.fig.colorbar(new_win.img)
#            new_win.cbar.ax.tick_params(labelsize=plot_font['size'])
#
#        if self.math.ui.checkBoxFixed.isChecked() == False:
#            self.math.ui.lineEditMax.setText(str(round(self.data.maxer,4)))
#            self.math.ui.lineEditMin.setText(str(round(self.data.minner,4)))
#
#        new_win.fig.show()

    def checkBoxFixed(self):
        """
        See if the min and max are identified as being fixed by
        checkbox
        """

        # See if there is a min and max in the textBrowsers

        len_min = len(self.math.ui.lineEditMin.text())
        len_max = len(self.math.ui.lineEditMax.text())

        if self.math.ui.checkBoxFixed.isChecked() == True:  # Checked
            if len_min > 0 and len_max > 0:
                try:
                    self.data.setmin = float(self.math.ui.lineEditMin.text())
                    self.data.setmax = float(self.math.ui.lineEditMax.text())
                    if self.math.ui.checkBoxCompress.isChecked() == False:
                        self.data.compress = False
                    else:
                        self.data.compress = True
                except:
                    pass
            else:
                pass
        else:
            self.data.setmin = None
            self.data.setmax = None
            self.data.compress = None
        self.changeColor()

    def checkBoxCompress(self):
        """
        See if compression is activated via the checkbox_4
        """

        if self.math.ui.checkBoxCompress.isChecked() == False:
            self.data.compress = False
        else:
            self.data.compress = True
        self.changeColor()

class widgetCompositeColor(_QWidget):
    def __init__(self, sgl_color_widget_list = None, parent = None, **kwargs):
        super(widgetCompositeColor, self).__init__(parent)
        self.ui = Ui_CompositeColor_Form()
        self.ui.setupUi(self)

        # Initialize underlying data
        self.initData(sgl_color_widget_list)

        # Create stand-in image data
        self.data.grayscaleimage = _np.dot(_np.ones([100,1]),_np.linspace(1,100,100)[None,:])
        self.data.set_x(_np.linspace(1,400,self.data.xlen))
        self.data.set_y(_np.linspace(1,400,self.data.ylen))
        winextent = (self.data.x.min(), self.data.x.max(), self.data.y.min(), self.data.y.max())

        # Instantiate mpl widget
        self.mpl = _MplCanvas(**kwargs)
        self.mpl.cbar = None  # Monkey patch on a cbar object

        # Create stand-in image data
        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = winextent, showcbar = False,
                              axison = True)
        self.mpl.fig.tight_layout()

        # Insert mpl widget into this widget
        self.ui.verticalLayout.insertWidget(0,self.mpl,_QtCore.Qt.AlignHCenter)
        self.ui.verticalLayout.insertWidget(0,self.mpl.toolbar, _QtCore.Qt.AlignHCenter)

        # SIGNALS & SLOTS
        self.ui.checkBoxFixed.stateChanged.connect(self.checkBoxFixed)
        self.ui.checkBoxCompress.stateChanged.connect(self.checkBoxCompress)
        self.ui.checkBoxRemOutliers.stateChanged.connect(self.checkBoxRemOutliers)
        self.ui.spinBoxStdDevs.valueChanged.connect(self.spinBoxOutliersChanged)

        #self.ui.lineEditMin.editingFinished.connect(self.textEditMinMaxSet)
        #self.ui.lineEditMax.editingFinished.connect(self.textEditMinMaxSet)

    def initData(self, sgl_color_widget_list):
        """
        (Re)-initialize self.data
        """

        if sgl_color_widget_list is None:
            self.data = CompositeColor()
        else:
            temp = []
            for count in sgl_color_widget_list:
                temp.append(count.data)

            self.data = CompositeColor(temp)

    def createImg(self, img, xunits = None, yunits = None,
                  extent = None, showcbar = True, axison = True,
                  cmap = _mpl.cm.gray):
        self.mpl.ax.clear()
        self.mpl.img = self.mpl.ax.imshow(img, interpolation = 'none',
                                      extent = extent, cmap = cmap, origin='lower')
        if xunits is not None:
            self.mpl.ax.xaxis.set_label_text(xunits)
        if yunits is not None:
            self.mpl.ax.yaxis.set_label_text(yunits)

        if axison == False:
            self.mpl.ax.set_axis_off()

        if showcbar == True:
            if self.mpl.cbar is not None:
                self.mpl.cbar.remove()

            self.mpl.cbar = self.mpl.fig.colorbar(self.mpl.img)


    def spinBoxOutliersChanged(self):
        self.checkBoxRemOutliers()

    def checkBoxRemOutliers(self):
        """
        """
        if self.ui.checkBoxRemOutliers.isChecked() == False:
            self.data.setoutlierstds = None
        else:
            self.data.setoutlierstds = float(self.ui.spinBoxStdDevs.value())
        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

    def checkBoxFixed(self):
        """
        See if the min and max are identified as being fixed by
        checkbox
        """

        # See if there is a min and max in the textBrowsers

        len_min = len(self.ui.lineEditMin.text())
        len_max = len(self.ui.lineEditMax.text())

        if self.ui.checkBoxFixed.isChecked() == True:  # Checked
            if len_min > 0 and len_max > 0:
                try:
                    self.data.setmin = float(self.ui.lineEditMin.text())
                    self.data.setmax = float(self.ui.lineEditMax.text())
                    if self.ui.checkBoxCompress.isChecked() == False:
                        self.data.compress = False
                    else:
                        self.data.compress = True
                except:
                    pass
            else:
                pass
        else:
            self.data.setmin = None
            self.data.setmax = None
            self.data.compress = None

        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

    def checkBoxCompress(self):
        """
        See if compression is activated via the checkbox_4
        """

        if self.ui.checkBoxCompress.isChecked() == False:
            self.data.compress = False
        else:
            self.data.compress = True

        self.createImg(img = self.data.image, xunits = self.data.xunits,
                              yunits = self.data.yunits,
                              extent = self.data.winextent, showcbar = True,
                              axison = True)
        self.mpl.draw()

class _mplWin:
    def __init__(self, parent = None):
        self.fig = None
        self.ax = None
        self.canvas = None
        self.img = None
        self.cbar = None
        self.toolbar = None

    def useToolBar(self, use=True):
        if use is True:
            self.toolbar = _NavigationToolbar(self.canvas, None,
                                                  coordinates = True)


if __name__ == '__main__':

    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')

    winSglColor = widgetSglColor()
    winSglColor.setWindowTitle('Single Color')
    winColorMath = widgetColorMath()
    winColorMath.setWindowTitle('Color Math')
    winBWImg = widgetBWImg()
    winBWImg.setWindowTitle('BW Image')
    winCompositeColor = widgetCompositeColor(sgl_color_widget_list=[winSglColor])

    winCompositeColor.setWindowTitle('Composite Color')
    # Final stuff
    winSglColor.show()
    winColorMath.show()
    winBWImg.show()
    winCompositeColor.show()

    _sys.exit(app.exec_())