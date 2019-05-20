# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PlotEffect.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(650, 200)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonOk = QtWidgets.QPushButton(Dialog)
        self.pushButtonOk.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonOk.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/open-iconic-master/png/check-3x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonOk.setIcon(icon)
        self.pushButtonOk.setIconSize(QtCore.QSize(35, 35))
        self.pushButtonOk.setDefault(False)
        self.pushButtonOk.setFlat(False)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButtonCancel.setLayoutDirection(QtCore.Qt.LeftToRight)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/open-iconic-master/png/thumb-down-3x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonCancel.setIcon(icon1)
        self.pushButtonCancel.setIconSize(QtCore.QSize(35, 35))
        self.pushButtonCancel.setDefault(False)
        self.pushButtonCancel.setFlat(False)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "PlotEffect Dialog"))
        self.pushButtonOk.setText(_translate("Dialog", "Ok"))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel"))


from . import icons_all_rc
