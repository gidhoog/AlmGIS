# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app_core/scopes/gst/gst_version_banu.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GstVersionBanu(object):
    def setupUi(self, GstVersionBanu):
        GstVersionBanu.setObjectName("GstVersionBanu")
        GstVersionBanu.resize(400, 16)
        self.horizontalLayout = QtWidgets.QHBoxLayout(GstVersionBanu)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiNameLbl = QtWidgets.QLabel(GstVersionBanu)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.uiNameLbl.setFont(font)
        self.uiNameLbl.setObjectName("uiNameLbl")
        self.horizontalLayout.addWidget(self.uiNameLbl)
        self.uiAreaLbl = QtWidgets.QLabel(GstVersionBanu)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        self.uiAreaLbl.setFont(font)
        self.uiAreaLbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.uiAreaLbl.setObjectName("uiAreaLbl")
        self.horizontalLayout.addWidget(self.uiAreaLbl)

        self.retranslateUi(GstVersionBanu)
        QtCore.QMetaObject.connectSlotsByName(GstVersionBanu)

    def retranslateUi(self, GstVersionBanu):
        _translate = QtCore.QCoreApplication.translate
        GstVersionBanu.setWindowTitle(_translate("GstVersionBanu", "Form"))
        self.uiNameLbl.setText(_translate("GstVersionBanu", "TextLabel"))
        self.uiAreaLbl.setText(_translate("GstVersionBanu", "TextLabel"))