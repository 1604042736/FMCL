# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\Ui\More\More.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_More(object):
    def setupUi(self, More):
        More.setObjectName("More")
        More.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(More)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(More)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.l_fmclversion = QtWidgets.QLabel(self.groupBox)
        self.l_fmclversion.setObjectName("l_fmclversion")
        self.gridLayout_2.addWidget(self.l_fmclversion, 0, 0, 1, 1)
        self.pb_opensourceurl = QtWidgets.QPushButton(self.groupBox)
        self.pb_opensourceurl.setObjectName("pb_opensourceurl")
        self.gridLayout_2.addWidget(self.pb_opensourceurl, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(More)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pb_openbangurl = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_openbangurl.setObjectName("pb_openbangurl")
        self.gridLayout_3.addWidget(self.pb_openbangurl, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 1)
        self.pb_openhmclurl = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_openhmclurl.setObjectName("pb_openhmclurl")
        self.gridLayout_3.addWidget(self.pb_openhmclurl, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.retranslateUi(More)
        QtCore.QMetaObject.connectSlotsByName(More)

    def retranslateUi(self, More):
        _translate = QtCore.QCoreApplication.translate
        More.setWindowTitle(_translate("More", "更多"))
        self.groupBox.setTitle(_translate("More", "关于"))
        self.l_fmclversion.setText(_translate("More", "Functional Minecraft Launcher"))
        self.pb_opensourceurl.setText(_translate("More", "打开开源网址"))
        self.groupBox_2.setTitle(_translate("More", "鸣谢"))
        self.pb_openbangurl.setText(_translate("More", "打开网址"))
        self.label.setText(_translate("More", "bangbang93: 提供镜像源"))
        self.pb_openhmclurl.setText(_translate("More", "打开网址"))
        self.label_2.setText(_translate("More", "huanghongxun: 提供技术帮助(HMCL)"))
