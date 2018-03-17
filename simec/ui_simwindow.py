# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SimWindow(object):
    def setupUi(self, SimWindow):
        SimWindow.setObjectName("SimWindow")
        SimWindow.resize(800, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimWindow.sizePolicy().hasHeightForWidth())
        SimWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(SimWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.centrallyout = QtWidgets.QGridLayout()
        self.centrallyout.setObjectName("centrallyout")
        self.gridLayout.addLayout(self.centrallyout, 0, 0, 1, 1)
        SimWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(SimWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        SimWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(SimWindow)
        self.statusbar.setObjectName("statusbar")
        SimWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SimWindow)
        QtCore.QMetaObject.connectSlotsByName(SimWindow)

    def retranslateUi(self, SimWindow):
        _translate = QtCore.QCoreApplication.translate
        SimWindow.setWindowTitle(_translate("SimWindow", "MainWindow"))

