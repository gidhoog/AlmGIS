# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'core/scopes/akte/gst_zuordnung.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GstZuordnung(object):
    def setupUi(self, GstZuordnung):
        GstZuordnung.setObjectName("GstZuordnung")
        GstZuordnung.resize(639, 585)
        self.centralwidget = QtWidgets.QWidget(GstZuordnung)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiHeaderHlay = QtWidgets.QHBoxLayout()
        self.uiHeaderHlay.setObjectName("uiHeaderHlay")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.uiHeaderHlay.addWidget(self.label)
        self.uiGdbDataTimeLbl = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.uiGdbDataTimeLbl.setFont(font)
        self.uiGdbDataTimeLbl.setObjectName("uiGdbDataTimeLbl")
        self.uiHeaderHlay.addWidget(self.uiGdbDataTimeLbl)
        self.uiLoadGdbPbtn = QtWidgets.QPushButton(self.centralwidget)
        self.uiLoadGdbPbtn.setMaximumSize(QtCore.QSize(160, 16777215))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.uiLoadGdbPbtn.setFont(font)
        self.uiLoadGdbPbtn.setObjectName("uiLoadGdbPbtn")
        self.uiHeaderHlay.addWidget(self.uiLoadGdbPbtn)
        self.verticalLayout.addLayout(self.uiHeaderHlay)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.uiTableVlay = QtWidgets.QVBoxLayout()
        self.uiTableVlay.setContentsMargins(-1, -1, -1, 0)
        self.uiTableVlay.setObjectName("uiTableVlay")
        self.verticalLayout.addLayout(self.uiTableVlay)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.uiNumberGstLbl = QtWidgets.QLabel(self.centralwidget)
        self.uiNumberGstLbl.setMinimumSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.uiNumberGstLbl.setFont(font)
        self.uiNumberGstLbl.setText("")
        self.uiNumberGstLbl.setObjectName("uiNumberGstLbl")
        self.horizontalLayout_3.addWidget(self.uiNumberGstLbl)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.uiNumberSelectedGstLbl = QtWidgets.QLabel(self.centralwidget)
        self.uiNumberSelectedGstLbl.setMinimumSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        self.uiNumberSelectedGstLbl.setFont(font)
        self.uiNumberSelectedGstLbl.setText("")
        self.uiNumberSelectedGstLbl.setObjectName("uiNumberSelectedGstLbl")
        self.horizontalLayout_3.addWidget(self.uiNumberSelectedGstLbl)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.uiVorgemerkteGstVlay = QtWidgets.QVBoxLayout()
        self.uiVorgemerkteGstVlay.setObjectName("uiVorgemerkteGstVlay")
        self.verticalLayout.addLayout(self.uiVorgemerkteGstVlay)
        GstZuordnung.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(GstZuordnung)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 639, 21))
        self.menubar.setObjectName("menubar")
        GstZuordnung.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(GstZuordnung)
        self.statusbar.setObjectName("statusbar")
        GstZuordnung.setStatusBar(self.statusbar)

        self.retranslateUi(GstZuordnung)
        QtCore.QMetaObject.connectSlotsByName(GstZuordnung)

    def retranslateUi(self, GstZuordnung):
        _translate = QtCore.QCoreApplication.translate
        GstZuordnung.setWindowTitle(_translate("GstZuordnung", "MainWindow"))
        self.label.setText(_translate("GstZuordnung", "GDB-Daten zuletzt eingelesen:"))
        self.uiGdbDataTimeLbl.setText(_translate("GstZuordnung", "TextLabel"))
        self.uiLoadGdbPbtn.setText(_translate("GstZuordnung", "GDB-Daten einlesen"))