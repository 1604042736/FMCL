# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\SettingEditor\SettingCards\FloatSettingCard.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FloatSettingCard(object):
    def setupUi(self, FloatSettingCard):
        FloatSettingCard.setObjectName("FloatSettingCard")
        FloatSettingCard.resize(400, 300)
        FloatSettingCard.setWindowTitle("")
        self.gridLayout = QtWidgets.QGridLayout(FloatSettingCard)
        self.gridLayout.setObjectName("gridLayout")
        self.dsb_val = DoubleSpinBox(FloatSettingCard)
        self.dsb_val.setObjectName("dsb_val")
        self.gridLayout.addWidget(self.dsb_val, 0, 0, 1, 1)

        self.retranslateUi(FloatSettingCard)
        QtCore.QMetaObject.connectSlotsByName(FloatSettingCard)

    def retranslateUi(self, FloatSettingCard):
        pass
from qfluentwidgets import DoubleSpinBox
