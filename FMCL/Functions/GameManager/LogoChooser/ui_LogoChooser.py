# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\GameManager\LogoChooser.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LogoChooser(object):
    def setupUi(self, LogoChooser):
        LogoChooser.setObjectName("LogoChooser")
        LogoChooser.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(LogoChooser)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_add = PushButton(LogoChooser)
        self.pb_add.setObjectName("pb_add")
        self.gridLayout.addWidget(self.pb_add, 0, 1, 1, 1)
        self.cb_logo = QtWidgets.QComboBox(LogoChooser)
        self.cb_logo.setStyleSheet("")
        self.cb_logo.setIconSize(QtCore.QSize(64, 64))
        self.cb_logo.setObjectName("cb_logo")
        self.gridLayout.addWidget(self.cb_logo, 0, 0, 1, 1)

        self.retranslateUi(LogoChooser)
        QtCore.QMetaObject.connectSlotsByName(LogoChooser)

    def retranslateUi(self, LogoChooser):
        _translate = QtCore.QCoreApplication.translate
        LogoChooser.setWindowTitle(_translate("LogoChooser", "Logo选择"))
        self.pb_add.setText(_translate("LogoChooser", "添加"))
from qfluentwidgets import PushButton
