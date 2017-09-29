"""
SVD Dialog

Citation Reference
------------------
[1] C H Camp Jr, Y J Lee, and M T Cicerone, "Quantitative, Comparable Coherent \
Anti-Stokes Raman Scattering (CARS) Spectroscopy: Correcting Errors in Phase \
Retrieval," Journal of Raman Spectroscopy (2016). arXiv:1507.06543.

"""

import sys as _sys
import numpy as _np

from PyQt5 import QtWidgets as _QtWidgets
from PyQt5.QtWidgets import (QApplication as _QApplication,
                             QDialog as _QDialog)
import PyQt5.QtCore as _QtCore

from scipy.linalg import (svd as _svd, diagsvd as _diagsvd)

# Import from Designer-based GUI
from crikit.ui.qt_Factorization import Ui_Dialog ### EDIT ###

# Generic imports for MPL-incorporation
import matplotlib as _mpl

from sciplot.ui.widget_mpl import MplCanvas as _MplCanvas

_mpl.use('Qt5Agg')
_mpl.rcParams['font.family'] = 'sans-serif'
_mpl.rcParams['font.size'] = 12

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
        self.ui.lcdSelectedFactors.display(len(self.selected_svs))

        self.svWins = []
        self.svLabelCheckBoxes = [self.ui.checkBox,
                                  self.ui.checkBox_2,
                                  self.ui.checkBox_3,
                                  self.ui.checkBox_4,
                                  self.ui.checkBox_5,
                                  self.ui.checkBox_6]

        for count in range(self.spanSV):
            self.svWins.append(_MplCanvas(subplot=211))
            self.svWins[count].ax[0].axis('Off')
            self.svWins[count].ax[1].hold('Off')

        self.ui.gridLayout.addWidget(self.svWins[0],1,0)
        self.ui.gridLayout.addWidget(self.svWins[1],1,1)
        self.ui.gridLayout.addWidget(self.svWins[2],1,2)

        self.ui.gridLayout.addWidget(self.svWins[3],3,0)
        self.ui.gridLayout.addWidget(self.svWins[4],3,1)
        self.ui.gridLayout.addWidget(self.svWins[5],3,2)

        self.reconCurrent = _MplCanvas(subplot=211)
        self.reconCurrent.ax[0].axis('Off')
        self.reconCurrent.ax[1].hold('Off')

        self.reconRemainder = _MplCanvas(subplot=211)
        self.reconRemainder.ax[0].axis('Off')
        self.reconRemainder.ax[1].hold('Off')


        self.ui.verticalLayout_3.insertWidget(1,self.reconCurrent)
        self.ui.verticalLayout_3.insertWidget(4,self.reconRemainder)

        for count in range(self.spanSV):
            self.svLabelCheckBoxes[count].setText('Keep: ' + str(count))

        if data is not None:
            self.data = data
            if data.ndim == 3:
                self.Mlen, self.Nlen, self.Olen = data.shape
                self.reconCurrent.ax[0].imshow(_np.mean(data, axis=-1),interpolation='none', origin='lower')
                self.reconCurrent.draw()

                data = data.reshape([-1, self.Olen])

                self.svddata = self.SvdData()
                self.svddata.orig_shape = [self.Mlen, self.Nlen, self.Olen]
                self.svddata.U, self.svddata.S, self.svddata.Vh = _svd(data, full_matrices=False)

                self.maxsvs = self.svddata.S.size

                self.ui.lcdMaxFactors.display(self.maxsvs)
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
                return svs
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
        self.ui.lcdSelectedFactors.display(len(self.selected_svs))
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
            if ':' in count:
                temp = count.split(':')
                self.selected_svs.update(set(_np.arange(int(temp[0]),int(temp[1])+1)))
            elif count.strip() == '':
                pass
            else:
                self.selected_svs.add(int(count))
        self.updateSVPlots(startnum=self.firstSV)
        self.ui.lcdSelectedFactors.display(len(self.selected_svs))
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
                                 self.reconCurrent.ax[0],
                                 self.reconCurrent.ax[1],
                                 self.reconCurrent)

        self.showMeanImg(self.svddata.return_remainder(self.selected_svs),
                         self.reconRemainder.ax[0],
                         self.reconRemainder.ax[1],
                         self.reconRemainder)

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
            self.svWins[count].ax[0].clear()
            temp = self.svddata.U[:,count + self.firstSV].copy()
            temp = _np.reshape(temp,[self.Mlen, self.Nlen])

            self.svWins[count].ax[0].imshow(-temp*self.svddata.S[count + self.firstSV], interpolation='none', cmap = _mpl.cm.gray , origin='lower')

            self.svWins[count].ax[0].axis('Off')

            self.svWins[count].ax[1].clear()
            self.svWins[count].ax[1].plot(-self.svddata.Vh[count + self.firstSV,:]*self.svddata.S[count + self.firstSV])
            #if count == 0:
            #    print(_np.min(self.svddata.Vh[count + self.firstSV,:]))
            self.svLabelCheckBoxes[count].setText('Keep: ' + str(startnum + count))
            self.svWins[count].draw()
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
        self.ui.lcdSelectedFactors.display(len(self.selected_svs))
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

    for count in range(y.size):
        data[count,:,:] = y[count]*_np.random.poisson(_np.dot(x[:,None],Spectrum[None,:]))

    win = DialogSVD.dialogSVD(data) ### EDIT ###

    print(win)


    _sys.exit(app.exec_())
#    _sys.exit()