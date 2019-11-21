# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PlotEffect_CutEveryNSpectra.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 219)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.spinBoxSpectraToCut = QtWidgets.QSpinBox(Form)
        self.spinBoxSpectraToCut.setMinimum(1)
        self.spinBoxSpectraToCut.setMaximum(100000000)
        self.spinBoxSpectraToCut.setObjectName("spinBoxSpectraToCut")
        self.verticalLayout.addWidget(self.spinBoxSpectraToCut)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.spinBoxEveryNSpectra = QtWidgets.QSpinBox(Form)
        self.spinBoxEveryNSpectra.setMaximum(10000000)
        self.spinBoxEveryNSpectra.setProperty("value", 100)
        self.spinBoxEveryNSpectra.setObjectName("spinBoxEveryNSpectra")
        self.verticalLayout.addWidget(self.spinBoxEveryNSpectra)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.spinBoxOffset = QtWidgets.QSpinBox(Form)
        self.spinBoxOffset.setMaximum(100000000)
        self.spinBoxOffset.setObjectName("spinBoxOffset")
        self.verticalLayout.addWidget(self.spinBoxOffset)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.comboBoxAction = QtWidgets.QComboBox(Form)
        self.comboBoxAction.setObjectName("comboBoxAction")
        self.comboBoxAction.addItem("")
        self.comboBoxAction.addItem("")
        self.comboBoxAction.addItem("")
        self.comboBoxAction.addItem("")
        self.verticalLayout.addWidget(self.comboBoxAction)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "M Spectra to Cut"))
        self.label_2.setText(_translate("Form", "Every N Spectra"))
        self.label_3.setText(_translate("Form", "Offset"))
        self.label_4.setText(_translate("Form", "Action"))
        self.comboBoxAction.setItemText(0, _translate("Form", "Cut"))
        self.comboBoxAction.setItemText(1, _translate("Form", "Mean"))
        self.comboBoxAction.setItemText(2, _translate("Form", "Before"))
        self.comboBoxAction.setItemText(3, _translate("Form", "After"))
