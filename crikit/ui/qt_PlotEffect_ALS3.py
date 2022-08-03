# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui_PlotEffect_ALS3.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(911, 257)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2, 0, QtCore.Qt.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.spinBoxRedux = QtWidgets.QSpinBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxRedux.sizePolicy().hasHeightForWidth())
        self.spinBoxRedux.setSizePolicy(sizePolicy)
        self.spinBoxRedux.setMinimum(1)
        self.spinBoxRedux.setMaximum(10000)
        self.spinBoxRedux.setObjectName("spinBoxRedux")
        self.verticalLayout_3.addWidget(self.spinBoxRedux)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4, 0, QtCore.Qt.AlignTop)
        self.checkBox = QtWidgets.QCheckBox(self.frame)
        self.checkBox.setMinimumSize(QtCore.QSize(20, 20))
        self.checkBox.setText("")
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_4.addWidget(self.checkBox, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_13 = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(181, 0))
        self.label_13.setMaximumSize(QtCore.QSize(350, 20))
        self.label_13.setTextFormat(QtCore.Qt.RichText)
        self.label_13.setWordWrap(False)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_5.addWidget(self.label_13)
        self.checkBoxWNIncreasing = QtWidgets.QCheckBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxWNIncreasing.sizePolicy().hasHeightForWidth())
        self.checkBoxWNIncreasing.setSizePolicy(sizePolicy)
        self.checkBoxWNIncreasing.setText("")
        self.checkBoxWNIncreasing.setChecked(True)
        self.checkBoxWNIncreasing.setObjectName("checkBoxWNIncreasing")
        self.verticalLayout_5.addWidget(self.checkBoxWNIncreasing, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.verticalLayout_11.addWidget(self.frame)
        self.horizontalFrame_4 = QtWidgets.QFrame(Form)
        self.horizontalFrame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.horizontalFrame_4.setObjectName("horizontalFrame_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalFrame_4)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setContentsMargins(-1, 6, -1, -1)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QtWidgets.QLabel(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_2.addWidget(self.label_6)
        self.spinBoxAsymSubSections = QtWidgets.QSpinBox(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxAsymSubSections.sizePolicy().hasHeightForWidth())
        self.spinBoxAsymSubSections.setSizePolicy(sizePolicy)
        self.spinBoxAsymSubSections.setMaximum(5)
        self.spinBoxAsymSubSections.setObjectName("spinBoxAsymSubSections")
        self.horizontalLayout_2.addWidget(self.spinBoxAsymSubSections)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.verticalLayout_10.addLayout(self.horizontalLayout_2)
        self.tableWidgetAsym = QtWidgets.QTableWidget(self.horizontalFrame_4)
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
        self.verticalLayout_10.addWidget(self.tableWidgetAsym)
        self.horizontalLayout_5.addLayout(self.verticalLayout_10)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_3.addWidget(self.label_7)
        self.spinBoxWSubSections = QtWidgets.QSpinBox(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxWSubSections.sizePolicy().hasHeightForWidth())
        self.spinBoxWSubSections.setSizePolicy(sizePolicy)
        self.spinBoxWSubSections.setMaximum(5)
        self.spinBoxWSubSections.setObjectName("spinBoxWSubSections")
        self.horizontalLayout_3.addWidget(self.spinBoxWSubSections)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_8 = QtWidgets.QLabel(self.horizontalFrame_4)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_4.addWidget(self.label_8)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem8)
        self.verticalLayout_8.addLayout(self.horizontalLayout_4)
        self.tableWidgetWeights = QtWidgets.QTableWidget(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetWeights.sizePolicy().hasHeightForWidth())
        self.tableWidgetWeights.setSizePolicy(sizePolicy)
        self.tableWidgetWeights.setMinimumSize(QtCore.QSize(0, 12))
        self.tableWidgetWeights.setMaximumSize(QtCore.QSize(16777215, 300))
        self.tableWidgetWeights.setBaseSize(QtCore.QSize(0, 65))
        self.tableWidgetWeights.setColumnCount(2)
        self.tableWidgetWeights.setObjectName("tableWidgetWeights")
        self.tableWidgetWeights.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetWeights.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidgetWeights.setHorizontalHeaderItem(1, item)
        self.tableWidgetWeights.horizontalHeader().setDefaultSectionSize(80)
        self.tableWidgetWeights.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_8.addWidget(self.tableWidgetWeights)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)
        self.frameMinMaxIterDiff = QtWidgets.QFrame(self.horizontalFrame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameMinMaxIterDiff.sizePolicy().hasHeightForWidth())
        self.frameMinMaxIterDiff.setSizePolicy(sizePolicy)
        self.frameMinMaxIterDiff.setFrameShape(QtWidgets.QFrame.Box)
        self.frameMinMaxIterDiff.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frameMinMaxIterDiff.setObjectName("frameMinMaxIterDiff")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frameMinMaxIterDiff)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayoutMiNMaxIterDiff = QtWidgets.QVBoxLayout()
        self.verticalLayoutMiNMaxIterDiff.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayoutMiNMaxIterDiff.setObjectName("verticalLayoutMiNMaxIterDiff")
        self.label_9 = QtWidgets.QLabel(self.frameMinMaxIterDiff)
        self.label_9.setObjectName("label_9")
        self.verticalLayoutMiNMaxIterDiff.addWidget(self.label_9)
        self.spinBoxMaxIter = QtWidgets.QSpinBox(self.frameMinMaxIterDiff)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBoxMaxIter.sizePolicy().hasHeightForWidth())
        self.spinBoxMaxIter.setSizePolicy(sizePolicy)
        self.spinBoxMaxIter.setMinimum(1)
        self.spinBoxMaxIter.setMaximum(1000000)
        self.spinBoxMaxIter.setProperty("value", 100)
        self.spinBoxMaxIter.setObjectName("spinBoxMaxIter")
        self.verticalLayoutMiNMaxIterDiff.addWidget(self.spinBoxMaxIter)
        self.label_10 = QtWidgets.QLabel(self.frameMinMaxIterDiff)
        self.label_10.setObjectName("label_10")
        self.verticalLayoutMiNMaxIterDiff.addWidget(self.label_10)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutMiNMaxIterDiff.addItem(spacerItem9)
        self.verticalLayout_6.addLayout(self.verticalLayoutMiNMaxIterDiff)
        self.horizontalLayout_5.addWidget(self.frameMinMaxIterDiff)
        self.verticalLayout_11.addWidget(self.horizontalFrame_4)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_11.addItem(spacerItem10)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "P (Asymmetry)"))
        self.label_2.setText(_translate("Form", "Lambda (Smoothness)"))
        self.label_3.setText(_translate("Form", "Sub-Sampling Factor"))
        self.label_4.setText(_translate("Form", "Fix End-Points"))
        self.label_13.setText(_translate("Form", "<html><head/><body><p align=\"center\">Wavenumber Increasing <span style=\" font-weight:700;\">Left-to-Right</span></p></body></html>"))
        self.checkBoxWNIncreasing.setToolTip(_translate("Form", "Conjugate if the frequency axis increases right-to-left."))
        self.label_6.setText(_translate("Form", "P (Asymmetry) Subsections"))
        item = self.tableWidgetAsym.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Start X"))
        item = self.tableWidgetAsym.horizontalHeaderItem(1)
        item.setText(_translate("Form", "End X"))
        item = self.tableWidgetAsym.horizontalHeaderItem(2)
        item.setText(_translate("Form", "P (Asymmetry) Value"))
        self.label_7.setText(_translate("Form", "Weighted (Subsections)"))
        self.label_8.setText(_translate("Form", "Weight Value"))
        item = self.tableWidgetWeights.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Start X"))
        item = self.tableWidgetWeights.horizontalHeaderItem(1)
        item.setText(_translate("Form", "End X"))
        self.label_9.setText(_translate("Form", "Max Iterations"))
        self.label_10.setText(_translate("Form", "Min Difference"))