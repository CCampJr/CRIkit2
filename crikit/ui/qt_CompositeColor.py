# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_CompositeColor.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 100)
        Form.setStyleSheet("font: 10pt \"Arial\";")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayoutColorMode = QtWidgets.QVBoxLayout()
        self.verticalLayoutColorMode.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayoutColorMode.setContentsMargins(2, 2, 2, 2)
        self.verticalLayoutColorMode.setSpacing(2)
        self.verticalLayoutColorMode.setObjectName("verticalLayoutColorMode")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayoutColorMode.addWidget(self.label)
        self.comboBoxColorMode = QtWidgets.QComboBox(self.frame)
        self.comboBoxColorMode.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBoxColorMode.setObjectName("comboBoxColorMode")
        self.comboBoxColorMode.addItem("")
        self.comboBoxColorMode.addItem("")
        self.comboBoxColorMode.addItem("")
        self.verticalLayoutColorMode.addWidget(self.comboBoxColorMode)
        self.horizontalLayout.addLayout(self.verticalLayoutColorMode)
        self.verticalLayoutBGColor = QtWidgets.QVBoxLayout()
        self.verticalLayoutBGColor.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayoutBGColor.setContentsMargins(2, 2, 2, 2)
        self.verticalLayoutBGColor.setSpacing(2)
        self.verticalLayoutBGColor.setObjectName("verticalLayoutBGColor")
        self.labelBGColor = QtWidgets.QLabel(self.frame)
        self.labelBGColor.setObjectName("labelBGColor")
        self.verticalLayoutBGColor.addWidget(self.labelBGColor)
        self.comboBoxBGColor = QtWidgets.QComboBox(self.frame)
        self.comboBoxBGColor.setMinimumSize(QtCore.QSize(120, 30))
        self.comboBoxBGColor.setObjectName("comboBoxBGColor")
        self.verticalLayoutBGColor.addWidget(self.comboBoxBGColor)
        self.horizontalLayout.addLayout(self.verticalLayoutBGColor)
        self.verticalLayout.addWidget(self.frame)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Color Mode"))
        self.comboBoxColorMode.setItemText(0, _translate("Form", "Emission Mode"))
        self.comboBoxColorMode.setItemText(1, _translate("Form", "Absorption Mode"))
        self.comboBoxColorMode.setItemText(2, _translate("Form", "Absorption v2"))
        self.labelBGColor.setText(_translate("Form", "Background Color"))


