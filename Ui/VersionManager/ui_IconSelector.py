# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\Ui\VersionManager\IconSelector.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_IconSelector(object):
    def setupUi(self, IconSelector):
        IconSelector.setObjectName("IconSelector")
        IconSelector.resize(500, 309)
        self.gridLayout = QtWidgets.QGridLayout(IconSelector)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_ok = QtWidgets.QPushButton(IconSelector)
        self.pb_ok.setObjectName("pb_ok")
        self.gridLayout.addWidget(self.pb_ok, 2, 0, 1, 1)
        self.pb_custom = QtWidgets.QPushButton(IconSelector)
        self.pb_custom.setObjectName("pb_custom")
        self.gridLayout.addWidget(self.pb_custom, 1, 1, 1, 2)
        self.le_custom = QtWidgets.QLineEdit(IconSelector)
        self.le_custom.setObjectName("le_custom")
        self.gridLayout.addWidget(self.le_custom, 1, 0, 1, 1)
        self.pb_cancel = QtWidgets.QPushButton(IconSelector)
        self.pb_cancel.setObjectName("pb_cancel")
        self.gridLayout.addWidget(self.pb_cancel, 2, 1, 1, 2)
        self.lw_default = QtWidgets.QListWidget(IconSelector)
        self.lw_default.setMovement(QtWidgets.QListView.Static)
        self.lw_default.setViewMode(QtWidgets.QListView.IconMode)
        self.lw_default.setSelectionRectVisible(True)
        self.lw_default.setObjectName("lw_default")
        self.gridLayout.addWidget(self.lw_default, 0, 0, 1, 3)

        self.retranslateUi(IconSelector)
        QtCore.QMetaObject.connectSlotsByName(IconSelector)

    def retranslateUi(self, IconSelector):
        _translate = QtCore.QCoreApplication.translate
        IconSelector.setWindowTitle(_translate("IconSelector", "图标选择"))
        self.pb_ok.setText(_translate("IconSelector", "确定"))
        self.pb_custom.setText(_translate("IconSelector", "自定义图标"))
        self.le_custom.setPlaceholderText(_translate("IconSelector", "这是自定义图标的路径"))
        self.pb_cancel.setText(_translate("IconSelector", "取消"))
