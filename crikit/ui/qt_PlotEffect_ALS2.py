# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PlotEffect_ALS2.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 304)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(16777215, 304))
        Form.setStyleSheet("font: 10pt \"Arial\";")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(-1, 0, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.spinBoxWSubSections = QtWidgets.QSpinBox(Form)
        self.spinBoxWSubSections.setMaximum(5)
        self.spinBoxWSubSections.setObjectName("spinBoxWSubSections")
        self.verticalLayout_6.addWidget(self.spinBoxWSubSections)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.tableWidgetWeights = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetWeights.sizePolicy().hasHeightForWidth())
        self.tableWidgetWeights.setSizePolicy(sizePolicy)
        self.tableWidgetWeights.setMinimumSize(QtCore.QSize(0, 12))
        self.tableWidgetWeights.setMaximumSize(QtCore.QSize(16777215, 200))
        self.tableWidgetWeights.setBaseSize(QtCore.QSize(0, 65))
        self.tableWidgetWeights.setObjectName("tableWidgetWeights")
        self.tableWidgetWeights.setColumnCount(2)
        self.tableWidgetWeights.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetWeights.setHorizontalHeaderItem(0, item)
        self.tableWidgetWeights.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidgetWeights.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.tableWidgetWeights)
        self.gridLayout.addLayout(self.verticalLayout_5, 3, 2, 1, 2)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_13 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setTextFormat(QtCore.Qt.RichText)
        self.label_13.setWordWrap(True)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_10.addWidget(self.label_13)
        self.checkBoxWNIncreasing = QtWidgets.QCheckBox(Form)
        self.checkBoxWNIncreasing.setText("")
        self.checkBoxWNIncreasing.setChecked(True)
        self.checkBoxWNIncreasing.setObjectName("checkBoxWNIncreasing")
        self.verticalLayout_10.addWidget(self.checkBoxWNIncreasing, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_10.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_10, 3, 4, 1, 1)
        self.frame_4 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_8.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.frame_4)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_9.addWidget(self.label_9)
        self.spinBoxMaxIter = QtWidgets.QSpinBox(self.frame_4)
        self.spinBoxMaxIter.setMinimum(1)
        self.spinBoxMaxIter.setMaximum(1000000)
        self.spinBoxMaxIter.setProperty("value", 100)
        self.spinBoxMaxIter.setObjectName("spinBoxMaxIter")
        self.verticalLayout_9.addWidget(self.spinBoxMaxIter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem1)
        self.label_10 = QtWidgets.QLabel(self.frame_4)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_9.addWidget(self.label_10)
        self.verticalLayout_8.addLayout(self.verticalLayout_9)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem2)
        self.gridLayout.addWidget(self.frame_4, 1, 4, 1, 1)
        self.frame_2 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 1, 0, 1, 1)
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6, 0, QtCore.Qt.AlignTop)
        self.spinBoxAsymSubSections = QtWidgets.QSpinBox(self.frame)
        self.spinBoxAsymSubSections.setMaximum(5)
        self.spinBoxAsymSubSections.setObjectName("spinBoxAsymSubSections")
        self.verticalLayout.addWidget(self.spinBoxAsymSubSections, 0, QtCore.Qt.AlignTop)
        self.tableWidgetAsym = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetAsym.sizePolicy().hasHeightForWidth())
        self.tableWidgetAsym.setSizePolicy(sizePolicy)
        self.tableWidgetAsym.setMinimumSize(QtCore.QSize(0, 4))
        self.tableWidgetAsym.setMaximumSize(QtCore.QSize(16777215, 200))
        self.tableWidgetAsym.setBaseSize(QtCore.QSize(0, 140))
        self.tableWidgetAsym.setFrameShadow(QtWidgets.QFrame.Plain)
        self.tableWidgetAsym.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidgetAsym.setRowCount(0)
        self.tableWidgetAsym.setObjectName("tableWidgetAsym")
        self.tableWidgetAsym.setColumnCount(3)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAsym.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAsym.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetAsym.setHorizontalHeaderItem(2, item)
        self.tableWidgetAsym.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidgetAsym.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidgetAsym.horizontalHeader().setHighlightSections(False)
        self.tableWidgetAsym.horizontalHeader().setMinimumSectionSize(20)
        self.tableWidgetAsym.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.tableWidgetAsym)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addWidget(self.frame, 1, 1, 3, 1)
        self.frame_3 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.spinBoxRedux = QtWidgets.QSpinBox(self.frame_3)
        self.spinBoxRedux.setMinimum(1)
        self.spinBoxRedux.setMaximum(10000)
        self.spinBoxRedux.setObjectName("spinBoxRedux")
        self.verticalLayout_3.addWidget(self.spinBoxRedux, 0, QtCore.Qt.AlignTop)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignLeft)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.checkBox = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.checkBox.setText("")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.frame_3, 1, 2, 2, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_7.setText(_translate("Form", "Weighted (Subsections)"))
        self.label_8.setText(_translate("Form", "Weight Value"))
        item = self.tableWidgetWeights.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Start X"))
        self.label_5.setText(_translate("Form", "Fixed=P"))
        self.label_13.setText(_translate("Form", "<html><head/><body><p>Wavenumber Increasing <span style=\" font-weight:700;\">Left-to-Right</span></p></body></html>"))
        self.checkBoxWNIncreasing.setToolTip(_translate("Form", "Conjugate if the frequency axis increases right-to-left."))
        self.label_9.setText(_translate("Form", "Max Iterations"))
        self.label_10.setText(_translate("Form", "Min Difference"))
        self.label.setText(_translate("Form", "Define P (Asymmetry)"))
        self.label_6.setText(_translate("Form", "P Subsections"))
        item = self.tableWidgetAsym.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Start X"))
        item = self.tableWidgetAsym.horizontalHeaderItem(1)
        item.setText(_translate("Form", "End X"))
        item = self.tableWidgetAsym.horizontalHeaderItem(2)
        item.setText(_translate("Form", "P (Asymmetry) Value"))
        self.label_3.setText(_translate("Form", "Sub-Sampling Factor"))
        self.label_2.setText(_translate("Form", "Lambda (smoothness)"))
        self.label_4.setText(_translate("Form", "Fix End-Points"))
