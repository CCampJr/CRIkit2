# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PlotEffect_DeTrending.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(867, 300)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frameOptions = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameOptions.sizePolicy().hasHeightForWidth())
        self.frameOptions.setSizePolicy(sizePolicy)
        self.frameOptions.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameOptions.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameOptions.setObjectName("frameOptions")
        self.gridLayout = QtWidgets.QGridLayout(self.frameOptions)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutButtons = QtWidgets.QVBoxLayout()
        self.verticalLayoutButtons.setObjectName("verticalLayoutButtons")
        self.gridLayout.addLayout(self.verticalLayoutButtons, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frameOptions)
        self.frameWidgets = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameWidgets.sizePolicy().hasHeightForWidth())
        self.frameWidgets.setSizePolicy(sizePolicy)
        self.frameWidgets.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameWidgets.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameWidgets.setObjectName("frameWidgets")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frameWidgets)
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayoutWidgets = QtWidgets.QVBoxLayout()
        self.verticalLayoutWidgets.setObjectName("verticalLayoutWidgets")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutWidgets.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.verticalLayoutWidgets)
        self.horizontalLayout.addWidget(self.frameWidgets)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

