# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_PlotEffect_ALS.ui'
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
        self.spinBoxP = QtWidgets.QDoubleSpinBox(Form)
        self.spinBoxP.setKeyboardTracking(False)
        self.spinBoxP.setDecimals(5)
        self.spinBoxP.setMaximum(1000000.0)
        self.spinBoxP.setSingleStep(0.001)
        self.spinBoxP.setProperty("value", 0.001)
        self.spinBoxP.setObjectName("spinBoxP")
        self.verticalLayout.addWidget(self.spinBoxP)
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
        self.spinBoxLambda = QtWidgets.QDoubleSpinBox(Form)
        self.spinBoxLambda.setKeyboardTracking(False)
        self.spinBoxLambda.setDecimals(4)
        self.spinBoxLambda.setMaximum(1000000.0)
        self.spinBoxLambda.setSingleStep(100.0)
        self.spinBoxLambda.setProperty("value", 1000.0)
        self.spinBoxLambda.setObjectName("spinBoxLambda")
        self.verticalLayout_2.addWidget(self.spinBoxLambda)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.spinBoxRedux = QtWidgets.QSpinBox(Form)
        self.spinBoxRedux.setKeyboardTracking(False)
        self.spinBoxRedux.setMinimum(1)
        self.spinBoxRedux.setObjectName("spinBoxRedux")
        self.verticalLayout_3.addWidget(self.spinBoxRedux)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "p-value (asymmetry)"))
        self.label_2.setText(_translate("Form", "Lambda (smoothness)"))
        self.label_3.setText(_translate("Form", "Interpolation Step Size (Pixels)"))

