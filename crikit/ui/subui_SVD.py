# -*- coding: utf-8 -*-
"""
Singular Value Decomposition SubUI (crikit.ui.subui_SVD)
=======================================================

SubUiSVD : SVD SubUI

Citation Reference
------------------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

Software Info
--------------

Original Python branch: Feb 16 2015

author: ("Charles H Camp Jr")

email: ("charles.camp@nist.gov")

version: ("15.09.29")
"""

# Append sys path
import sys as _sys
import os as _os
if __name__ == '__main__':
    _sys.path.append(_os.path.abspath('../../'))

# Generic imports for QT-based programs
from PyQt5 import QtWidgets as _QtWidgets

from PyQt5.QtWidgets import (QApplication as _QApplication, \
QWidget as _QWidget, QMainWindow as _QMainWindow, QLayout as _QLayout,\
 QGridLayout as _QGridLayout, QInputDialog as _QInputDialog, QDialog as _QDialog)
import PyQt5.QtCore as _QtCore
from PyQt5.QtGui import (QCursor as _QCursor)

# Other imports
import numpy as _np
from scipy.linalg import (svd as _svd, diagsvd as _diagsvd)
import time as _time

from crikit.utils.general import find_nearest as _find_nearest

# Import from Designer-based GUI
from crikit.ui.qt_SVD import Ui_Dialog ### EDIT ###

# Generic imports for MPL-incorporation
import matplotlib as _mpl
_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 12

#import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as _FigureCanvas, \
    NavigationToolbar2QT as _NavigationToolbar)
from matplotlib.figure import Figure as _Figure


class _Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(200, 200)

        Form.setStyleSheet("font: 10pt \"Arial\";")
        self.verticalLayout = _QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        sizePolicy = _QtWidgets.QSizePolicy(_QtWidgets.QSizePolicy.Fixed, _QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy = _QtWidgets.QSizePolicy(_QtWidgets.QSizePolicy.Minimum, _QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.retranslateUi(Form)
        _QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = _QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


class _mplWinData:
    def __init__(self, parent=None):
        self.fig = _Figure()
        self.ax2 = self.fig.add_subplot(313)
        self.ax1 = self.fig.add_subplot(211)

        self.canvas = _FigureCanvas(self.fig)

class _mplWindow(_QWidget):
    def __init__(self, parent = None):

        # Generic load/init designer-based GUI
        super(_mplWindow, self).__init__(parent) ### EDIT ###

        self.ui = _Ui_Form() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###
        self.mpl = _mplWinData()
        self.ui.verticalLayout.addWidget(self.mpl.canvas)

class DialogSVD(_QDialog):
    """
    SubUiSVD : SVD SubUI
    """

    def __init__(self, data=None, parent = None):

        # Generic load/init designer-based GUI
        super(DialogSVD, self).__init__(parent) ### EDIT ###

        self.ui = Ui_Dialog() ### EDIT ###
        self.ui.setupUi(self)     ### EDIT ###

        self.ui.pushButtonNext.clicked.connect(self.advance)
        self.ui.pushButtonPrev.clicked.connect(self.advance)
        self.ui.pushButtonGoTo.clicked.connect(self.advance)
        self.ui.pushButtonCancel.clicked.connect(self.reject)
        self.ui.pushButtonOk.clicked.connect(self.accept)
        self.ui.pushButtonClear.clicked.connect(self.clear)
        self.ui.pushButtonApply.clicked.connect(self.applyCheckBoxes)
        self.ui.pushButtonScript.clicked.connect(self.runScript)

        self.firstSV = 0
        self.spanSV = 6

        self.Mlen = 0
        self.Nlen = 0
        self.Olen = 0

        self.data = _np.zeros([self.Mlen, self.Nlen, self.Olen])

        self.selected_svs = set()
        self.ui.lcdSelectedSVs.display(len(self.selected_svs))

        self.svWins = []
        self.svLabelCheckBoxes = [self.ui.checkBox,
                                  self.ui.checkBox_2,
                                  self.ui.checkBox_3,
                                  self.ui.checkBox_4,
                                  self.ui.checkBox_5,
                                  self.ui.checkBox_6]

        for count in range(self.spanSV):
            self.svWins.append(_mplWindow())
            self.svWins[count].mpl.ax1.axis('Off')
            self.svWins[count].mpl.ax2.hold('Off')

        self.ui.gridLayout.addWidget(self.svWins[0],1,0)
        self.ui.gridLayout.addWidget(self.svWins[1],1,1)
        self.ui.gridLayout.addWidget(self.svWins[2],1,2)

        self.ui.gridLayout.addWidget(self.svWins[3],3,0)
        self.ui.gridLayout.addWidget(self.svWins[4],3,1)
        self.ui.gridLayout.addWidget(self.svWins[5],3,2)

        self.reconCurrent = _mplWindow()
        self.reconCurrent.mpl.ax1.axis('Off')
        self.reconCurrent.mpl.ax2.hold('Off')

        self.reconRemainder = _mplWindow()
        self.reconRemainder.mpl.ax1.axis('Off')
        self.reconRemainder.mpl.ax2.hold('Off')


        self.ui.verticalLayout_3.insertWidget(1,self.reconCurrent)
        self.ui.verticalLayout_3.insertWidget(4,self.reconRemainder)

        for count in range(self.spanSV):
            self.svLabelCheckBoxes[count].setText('Keep: ' + str(count))

        if data is not None:
            self.data = data
            if data.ndim == 3:
                self.Mlen, self.Nlen, self.Olen = data.shape
                self.reconCurrent.mpl.ax1.imshow(_np.mean(data, axis=-1),interpolation='none', origin='lower')
                self.reconCurrent.mpl.canvas.draw()

                data = data.reshape([-1, self.Olen])

                self.svddata = self.SvdData()
                self.svddata.orig_shape = [self.Mlen, self.Nlen, self.Olen]
                self.svddata.U, self.svddata.S, self.svddata.Vh = _svd(data, full_matrices=False)

                self.maxsvs = self.svddata.S.size

                self.ui.lcdMaxSVs.display(self.maxsvs)
                self.ui.spinBoxGoTo.setMaximum(self.maxsvs)

                self.updateCurrentRemainder()

               #print('U: {}, S: {}, Vh: {}'.format(self.svddata.U.shape, self.svddata.S.shape, self.svddata.Vh.shape))

                self.updateSVPlots()

    @staticmethod
    def dialogSVD(data, parent = None):
        """
            Executes DialogSVD dialog and returns values
        """
        dialog = DialogSVD(data, parent)
        dialog.showMaximized()
        result = dialog.exec_()  # 1 = Aceepted, 0 = Rejected/Canceled

        if result == 1:
            svs = list(dialog.selected_svs)
            svs.sort()
            svs = _np.array(svs)

            if svs.size == 0:
                return None
            else:
                return [_np.reshape(dialog.svddata.return_svd(dialog.selected_svs),dialog.svddata.orig_shape),
                        ['SVD','SV_List', svs]]
        else:
            return None

    class SvdData:
        """
        Hold SVD factorized components of input data
        """
        def __init__(self):
            self.U = _np.zeros((0,0))
            self.S = _np.zeros((0))
            self.Vh = _np.zeros((0,0))
            self.orig_shape = [0,0,0]

        def return_svd(self, Select_list=None):
            #print('Select_list:{}'.format(Select_list))
            temp = self.s_from_selected(self.S, self.U.shape[-1], self.Vh.shape[0], Select_list)
            #print(temp[0:10,0])

            return _np.dot(self.U, _np.dot(temp, self.Vh))

        def return_remainder(self, Select_list=None):
            return _np.dot(self.U, _np.dot(self.s_from_unselected(self.S,
                                                            self.U.shape[-1],
                                                            self.Vh.shape[0],
                                                            Select_list),
                                       self.Vh))

        @staticmethod
        def s_from_selected(S, M, N, Select_list=None):
            """
            Return SVD S-matrix of SELECTED singular values
            """
            if Select_list is None:
                return _diagsvd(S, M, N)
            else:
                if type(Select_list) is set:
                    Select_list = list(Select_list)

                #print(Select_list)
                P = _np.zeros(S.size)
                #print('P-shape:{}'.format(P.shape))
                #print('Select List:{}'.format(Select_list))
                #print('S-of-select:{}'.format(S[Select_list]))
                P[Select_list] = S[Select_list]
                #print('P:{}'.format(P[0:10]))
                temp =  _diagsvd(P, M, N)
                return temp

        @staticmethod
        def s_from_unselected(S, M, N, Select_list=None):
            """
            Return SVD S-matrix of UNselected singular values
            """
            if Select_list is None:
                return _diagsvd(0*S, M, N)
            else:
                if type(Select_list) is set:
                    Select_list = list(Select_list)
                P = S.copy()
                P[Select_list] = 0
                return _diagsvd(P, M, N)

    def applyCheckBoxes(self):
        """
        Add checked singular values (and remove un-checked SVs)
        """
        for count, checkBox in enumerate(self.svLabelCheckBoxes):
            if checkBox.isChecked() == True:
                self.selected_svs.add(self.firstSV+count)
            else:
                try:
                    self.selected_svs.remove(self.firstSV+count)
                except:
                    pass

        #print('Self.S: {}'.format(self.svddata.S[0:3]))
        self.ui.lcdSelectedSVs.display(len(self.selected_svs))
        self.updateCurrentRemainder()

    def advance(self):
        """
        View next set of SVs
        """
        sender = self.sender().objectName()
        if sender == 'pushButtonPrev':
            self.updateSVPlots(startnum=self.firstSV-self.spanSV)
        elif sender == 'pushButtonNext':
            self.updateSVPlots(startnum=self.firstSV+self.spanSV)
        elif sender == 'pushButtonGoTo':
            self.updateSVPlots(startnum=self.ui.spinBoxGoTo.value())
        else:
            pass
    def runScript(self):
        """
        Run "script" of singular value selection

        Example:
            [1,2,3,5:7] = 1,2,3,5,6,7
        """
        script = self.ui.lineEditSelections.text()
        script = script.strip('[').strip(']')
        script = script.split(',')
        for count in script:
#            print(count)
            if ':' in count:
                temp = count.split(':')
                self.selected_svs.update(set(_np.arange(int(temp[0]),int(temp[1])+1)))
            else:
                self.selected_svs.add(int(count))
        self.updateSVPlots(startnum=self.firstSV)
        self.ui.lcdSelectedSVs.display(len(self.selected_svs))
        self.updateCurrentRemainder()

    def updateCurrentRemainder(self):
        """
        Update image reconstructed (mean over spectral vector) using remaining \
        (unselected) singular values
        """
        #print(self.selected_svs)
        temp = self.svddata.return_svd(self.selected_svs)
        #print(temp[0:10])
        self.showMeanImg(temp,
                                 self.reconCurrent.mpl.ax1,
                                 self.reconCurrent.mpl.ax2,
                                 self.reconCurrent.mpl.canvas)

        self.showMeanImg(self.svddata.return_remainder(self.selected_svs),
                         self.reconRemainder.mpl.ax1,
                         self.reconRemainder.mpl.ax2,
                         self.reconRemainder.mpl.canvas)

    def updateSVPlots(self, startnum=0):
        """
        Update images and spectra of set of singular values starting at SV \
        number startnum
        """
        if startnum <= 0:
            startnum = 0
            self.ui.pushButtonPrev.setEnabled(False)
            self.ui.pushButtonNext.setEnabled(True)
        elif startnum > self.Olen - self.spanSV:
            startnum = self.Olen - self.spanSV
            self.ui.pushButtonPrev.setEnabled(True)
            self.ui.pushButtonNext.setEnabled(False)
        else:
            self.ui.pushButtonPrev.setEnabled(True)
            self.ui.pushButtonNext.setEnabled(True)

        self.firstSV = startnum

        for count in range(self.spanSV):
            self.svWins[count].mpl.ax1.clear()
            temp = self.svddata.U[:,count + self.firstSV].copy()
            temp = _np.reshape(temp,[self.Mlen, self.Nlen])

            self.svWins[count].mpl.ax1.imshow(-temp*self.svddata.S[count + self.firstSV], interpolation='none', cmap = _mpl.cm.gray , origin='lower')

            self.svWins[count].mpl.ax1.axis('Off')

            self.svWins[count].mpl.ax2.clear()
            self.svWins[count].mpl.ax2.plot(-self.svddata.Vh[count + self.firstSV,:]*self.svddata.S[count + self.firstSV])
            #if count == 0:
            #    print(_np.min(self.svddata.Vh[count + self.firstSV,:]))
            self.svLabelCheckBoxes[count].setText('Keep: ' + str(startnum + count))
            self.svWins[count].mpl.canvas.draw()
            if self.firstSV + count in self.selected_svs:
                self.svLabelCheckBoxes[count].setChecked(True)
            else:
                self.svLabelCheckBoxes[count].setChecked(False)


    def showMeanImg(self, data, ax_img, ax_spectrum, canvas):
        """
        Update image reconstructed (mean over spectral vector) using selected \
        singular values
        """
        temp = _np.reshape(_np.sum(data,axis=-1),[self.Mlen, self.Nlen])
        #print(temp[0:10,0])
        ax_img.clear()
        ax_img.imshow(temp, interpolation='none', cmap = _mpl.cm.gray , origin='lower')
        #ax_img.figure.colorbar(img)
        #ax_img.imshow(_np.random.rand(100,100), interpolation='none', cmap = _mpl.cm.gray , origin='lower')
        ax_spectrum.clear()
        ax_spectrum.plot(_np.mean(data,axis=0))
        canvas.draw()

    def clear(self):
        """
        Clear selected singular values (i.e., none will be selected)
        """
        self.selected_svs = set()
        self.ui.lcdSelectedSVs.display(len(self.selected_svs))
        self.updateCurrentRemainder()
        self.updateSVPlots(startnum=self.firstSV)


if __name__ == '__main__':
    app = _QApplication(_sys.argv)
    app.setStyle('Cleanlooks')
    x = _np.linspace(100,200,50)
    y = _np.linspace(200,300,50)
    f = _np.linspace(500,3000,800)
    Ex = 30*_np.exp((-(f-1750)**2/(200**2)))
    Spectrum = _np.convolve(_np.flipud(Ex),Ex,mode='same')

    data = _np.zeros((y.size,x.size,f.size))
#    data[0:25,0:25,:] = 200
#    data[0:25,26::,:] = 2000
#    data[26::,0:25,:] = 100
#    data[26::,26::,:] = 3000
    for count in range(y.size):
        data[count,:,:] = y[count]*_np.random.poisson(_np.dot(x[:,None],Spectrum[None,:]))

    #data = _np.random.rand(50,50,800)

    win = DialogSVD.dialogSVD(data) ### EDIT ###

    print(win)


    #_sys.exit(app.exec_())
    _sys.exit()