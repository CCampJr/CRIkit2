# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PopSpectrumGS.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(400, 0))
        Form.setMaximumSize(QtCore.QSize(400, 56))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.framePop = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framePop.sizePolicy().hasHeightForWidth())
        self.framePop.setSizePolicy(sizePolicy)
        self.framePop.setMaximumSize(QtCore.QSize(500, 16777215))
        self.framePop.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.framePop.setFrameShadow(QtWidgets.QFrame.Plain)
        self.framePop.setObjectName("framePop")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.framePop)
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonPop = QtWidgets.QPushButton(self.framePop)
        self.pushButtonPop.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPop.sizePolicy().hasHeightForWidth())
        self.pushButtonPop.setSizePolicy(sizePolicy)
        self.pushButtonPop.setObjectName("pushButtonPop")
        self.horizontalLayout.addWidget(self.pushButtonPop)
        self.pushButtonSpectrum = QtWidgets.QPushButton(self.framePop)
        self.pushButtonSpectrum.setEnabled(True)
        self.pushButtonSpectrum.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButtonSpectrum.setObjectName("pushButtonSpectrum")
        self.horizontalLayout.addWidget(self.pushButtonSpectrum)
        self.pushButtonGSPop = QtWidgets.QPushButton(self.framePop)
        self.pushButtonGSPop.setEnabled(True)
        self.pushButtonGSPop.setObjectName("pushButtonGSPop")
        self.horizontalLayout.addWidget(self.pushButtonGSPop)
        self.horizontalLayout_2.addWidget(self.framePop)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButtonPop.setText(_translate("Form", "Pop"))
        self.pushButtonSpectrum.setText(_translate("Form", "<Spectrum>"))
        self.pushButtonGSPop.setText(_translate("Form", "Grayscale"))

