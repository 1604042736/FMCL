# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\Ui\VersionManager\VersionManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VersionManager(object):
    def setupUi(self, VersionManager):
        VersionManager.setObjectName("VersionManager")
        VersionManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(VersionManager)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(VersionManager)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.l_forgeversion = QtWidgets.QLabel(self.groupBox)
        self.l_forgeversion.setText("")
        self.l_forgeversion.setObjectName("l_forgeversion")
        self.gridLayout_2.addWidget(self.l_forgeversion, 2, 1, 1, 2)
        self.pb_del = QtWidgets.QPushButton(self.groupBox)
        self.pb_del.setObjectName("pb_del")
        self.gridLayout_2.addWidget(self.pb_del, 4, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.l_version = QtWidgets.QLabel(self.groupBox)
        self.l_version.setText("")
        self.l_version.setObjectName("l_version")
        self.gridLayout_2.addWidget(self.l_version, 1, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.pb_reinstall = QtWidgets.QPushButton(self.groupBox)
        self.pb_reinstall.setObjectName("pb_reinstall")
        self.gridLayout_2.addWidget(self.pb_reinstall, 4, 0, 1, 1)
        self.le_name = QtWidgets.QLineEdit(self.groupBox)
        self.le_name.setObjectName("le_name")
        self.gridLayout_2.addWidget(self.le_name, 0, 1, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.pb_openfoder = QtWidgets.QPushButton(self.groupBox)
        self.pb_openfoder.setObjectName("pb_openfoder")
        self.gridLayout_2.addWidget(self.pb_openfoder, 4, 2, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(VersionManager)
        QtCore.QMetaObject.connectSlotsByName(VersionManager)

    def retranslateUi(self, VersionManager):
        _translate = QtCore.QCoreApplication.translate
        VersionManager.setWindowTitle(_translate("VersionManager", "版本管理"))
        self.groupBox.setTitle(_translate("VersionManager", "基础"))
        self.pb_del.setText(_translate("VersionManager", "删除"))
        self.label_3.setText(_translate("VersionManager", "Forge版本"))
        self.label.setText(_translate("VersionManager", "名称"))
        self.label_2.setText(_translate("VersionManager", "版本"))
        self.pb_reinstall.setText(_translate("VersionManager", "重新安装"))
        self.pb_openfoder.setText(_translate("VersionManager", "打开版本文件夹"))
