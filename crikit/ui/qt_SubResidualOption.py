# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_SubResidualOptions.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(291, 261)
        Dialog.setStyleSheet("font: 10pt \"Arial\";")
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frameDark = QtWidgets.QFrame(self.groupBox)
        self.frameDark.setFrameShape(QtWidgets.QFrame.Box)
        self.frameDark.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameDark.setObjectName("frameDark")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frameDark)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBoxMain = QtWidgets.QCheckBox(self.frameDark)
        self.checkBoxMain.setChecked(True)
        self.checkBoxMain.setObjectName("checkBoxMain")
        self.verticalLayout_2.addWidget(self.checkBoxMain)
        self.checkBoxBG = QtWidgets.QCheckBox(self.frameDark)
        self.checkBoxBG.setChecked(True)
        self.checkBoxBG.setObjectName("checkBoxBG")
        self.verticalLayout_2.addWidget(self.checkBoxBG)
        self.verticalLayout_3.addWidget(self.frameDark)
        self.frameResidual = QtWidgets.QFrame(self.groupBox)
        self.frameResidual.setEnabled(True)
        self.frameResidual.setFrameShape(QtWidgets.QFrame.Box)
        self.frameResidual.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameResidual.setObjectName("frameResidual")
        self.gridLayout = QtWidgets.QGridLayout(self.frameResidual)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frameResidual)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spinBoxMin = QtWidgets.QDoubleSpinBox(self.frameResidual)
        self.spinBoxMin.setMinimum(-10000.0)
        self.spinBoxMin.setMaximum(10000.0)
        self.spinBoxMin.setProperty("value", -1500.0)
        self.spinBoxMin.setObjectName("spinBoxMin")
        self.horizontalLayout.addWidget(self.spinBoxMin)
        self.spinBoxMax = QtWidgets.QDoubleSpinBox(self.frameResidual)
        self.spinBoxMax.setMinimum(-10000.0)
        self.spinBoxMax.setMaximum(10000.0)
        self.spinBoxMax.setProperty("value", -500.0)
        self.spinBoxMax.setObjectName("spinBoxMax")
        self.horizontalLayout.addWidget(self.spinBoxMax)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frameResidual)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.checkBoxMain, self.checkBoxBG)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Residual Subtract Options"))
        self.groupBox.setTitle(_translate("Dialog", "Residual Subtraction"))
        self.checkBoxMain.setText(_translate("Dialog", "Main Image"))
        self.checkBoxBG.setText(_translate("Dialog", "NRB (Background)"))
        self.label.setText(_translate("Dialog", "Frequency Range (cm-1)"))

