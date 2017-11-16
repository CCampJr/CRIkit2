# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_AnscombeOptions.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(447, 108)
        Dialog.setStyleSheet("font: 10pt \"Arial\";")
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutGain = QtWidgets.QVBoxLayout()
        self.verticalLayoutGain.setContentsMargins(0, -1, -1, -1)
        self.verticalLayoutGain.setObjectName("verticalLayoutGain")
        self.labelGain = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.labelGain.setFont(font)
        self.labelGain.setObjectName("labelGain")
        self.verticalLayoutGain.addWidget(self.labelGain, 0, QtCore.Qt.AlignHCenter)
        self.spinBoxGain = QtWidgets.QDoubleSpinBox(Dialog)
        self.spinBoxGain.setDecimals(6)
        self.spinBoxGain.setProperty("value", 1.4)
        self.spinBoxGain.setObjectName("spinBoxGain")
        self.verticalLayoutGain.addWidget(self.spinBoxGain)
        self.gridLayout.addLayout(self.verticalLayoutGain, 0, 3, 1, 1)
        self.verticalLayoutStdDev = QtWidgets.QVBoxLayout()
        self.verticalLayoutStdDev.setObjectName("verticalLayoutStdDev")
        self.labelStdDev = QtWidgets.QLabel(Dialog)
        self.labelStdDev.setObjectName("labelStdDev")
        self.verticalLayoutStdDev.addWidget(self.labelStdDev, 0, QtCore.Qt.AlignHCenter)
        self.spinBoxStdDev = QtWidgets.QDoubleSpinBox(Dialog)
        self.spinBoxStdDev.setDecimals(6)
        self.spinBoxStdDev.setSingleStep(0.1)
        self.spinBoxStdDev.setProperty("value", 12.44)
        self.spinBoxStdDev.setObjectName("spinBoxStdDev")
        self.verticalLayoutStdDev.addWidget(self.spinBoxStdDev)
        self.gridLayout.addLayout(self.verticalLayoutStdDev, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 3, 1, 1, QtCore.Qt.AlignRight)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.spinBoxStdDev, self.spinBoxGain)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Anscombe Transform Parameters"))
        self.labelGain.setText(_translate("Dialog", "Poisson Noise Gain"))
        self.labelStdDev.setText(_translate("Dialog", "Gaussian Noise Std. Dev."))

