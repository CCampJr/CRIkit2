# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_PlotEffect_SG.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(643, 91)
        Form.setStyleSheet("font: 10pt \"Arial\";")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.spinBoxWinSize = QtWidgets.QSpinBox(Form)
        self.spinBoxWinSize.setKeyboardTracking(False)
        self.spinBoxWinSize.setMinimum(1)
        self.spinBoxWinSize.setMaximum(1000000)
        self.spinBoxWinSize.setObjectName("spinBoxWinSize")
        self.verticalLayout.addWidget(self.spinBoxWinSize)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.spinBoxOrder = QtWidgets.QSpinBox(Form)
        self.spinBoxOrder.setKeyboardTracking(False)
        self.spinBoxOrder.setMinimum(1)
        self.spinBoxOrder.setMaximum(101)
        self.spinBoxOrder.setObjectName("spinBoxOrder")
        self.verticalLayout_2.addWidget(self.spinBoxOrder)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Window Size"))
        self.label_2.setText(_translate("Form", "Order"))

