# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\GameLauncher\GameLauncher.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameLauncher(object):
    def setupUi(self, GameLauncher):
        GameLauncher.setObjectName("GameLauncher")
        GameLauncher.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(GameLauncher)
        self.gridLayout.setObjectName("gridLayout")
        self.l_info = QtWidgets.QLabel(GameLauncher)
        self.l_info.setText("")
        self.l_info.setObjectName("l_info")
        self.gridLayout.addWidget(self.l_info, 1, 0, 1, 1)
        self.pb_kill = PushButton(GameLauncher)
        self.pb_kill.setEnabled(False)
        self.pb_kill.setObjectName("pb_kill")
        self.gridLayout.addWidget(self.pb_kill, 1, 2, 1, 1)
        self.te_output = TextEdit(GameLauncher)
        self.te_output.setObjectName("te_output")
        self.gridLayout.addWidget(self.te_output, 0, 0, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)

        self.retranslateUi(GameLauncher)
        QtCore.QMetaObject.connectSlotsByName(GameLauncher)

    def retranslateUi(self, GameLauncher):
        _translate = QtCore.QCoreApplication.translate
        GameLauncher.setWindowTitle(_translate("GameLauncher", "启动游戏"))
        self.pb_kill.setText(_translate("GameLauncher", "结束游戏"))
from qfluentwidgets import PushButton, TextEdit