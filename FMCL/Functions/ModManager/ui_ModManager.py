# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\ModManager\ModManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ModManager(object):
    def setupUi(self, ModManager):
        ModManager.setObjectName("ModManager")
        ModManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(ModManager)
        self.gridLayout.setObjectName("gridLayout")
        self.lw_mods = ListWidget(ModManager)
        self.lw_mods.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lw_mods.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.lw_mods.setResizeMode(QtWidgets.QListView.Adjust)
        self.lw_mods.setWordWrap(True)
        self.lw_mods.setObjectName("lw_mods")
        self.gridLayout.addWidget(self.lw_mods, 3, 0, 1, 5)
        self.f_operate = QtWidgets.QFrame(ModManager)
        self.f_operate.setEnabled(True)
        self.f_operate.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f_operate.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f_operate.setObjectName("f_operate")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.f_operate)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_enabled = PushButton(self.f_operate)
        self.pb_enabled.setEnabled(True)
        self.pb_enabled.setObjectName("pb_enabled")
        self.gridLayout_2.addWidget(self.pb_enabled, 0, 1, 1, 1)
        self.pb_del = PushButton(self.f_operate)
        self.pb_del.setEnabled(True)
        self.pb_del.setObjectName("pb_del")
        self.gridLayout_2.addWidget(self.pb_del, 0, 0, 1, 1)
        self.pb_disabled = PushButton(self.f_operate)
        self.pb_disabled.setEnabled(True)
        self.pb_disabled.setObjectName("pb_disabled")
        self.gridLayout_2.addWidget(self.pb_disabled, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.f_operate, 1, 0, 1, 2)
        self.pb_openmodir = PushButton(ModManager)
        self.pb_openmodir.setObjectName("pb_openmodir")
        self.gridLayout.addWidget(self.pb_openmodir, 0, 0, 1, 1)
        self.le_search = LineEdit(ModManager)
        self.le_search.setObjectName("le_search")
        self.gridLayout.addWidget(self.le_search, 0, 1, 1, 4)
        self.l_statistics = QtWidgets.QLabel(ModManager)
        self.l_statistics.setText("")
        self.l_statistics.setObjectName("l_statistics")
        self.gridLayout.addWidget(self.l_statistics, 1, 2, 1, 1)

        self.retranslateUi(ModManager)
        QtCore.QMetaObject.connectSlotsByName(ModManager)

    def retranslateUi(self, ModManager):
        _translate = QtCore.QCoreApplication.translate
        ModManager.setWindowTitle(_translate("ModManager", "Mod管理"))
        self.pb_enabled.setText(_translate("ModManager", "启动"))
        self.pb_del.setText(_translate("ModManager", "删除"))
        self.pb_disabled.setText(_translate("ModManager", "禁用"))
        self.pb_openmodir.setText(_translate("ModManager", "打开Mod文件夹"))
        self.le_search.setPlaceholderText(_translate("ModManager", "按回车以搜索"))
from qfluentwidgets import LineEdit, ListWidget, PushButton
