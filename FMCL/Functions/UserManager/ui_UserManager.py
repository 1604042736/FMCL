# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UserManager(object):
    def setupUi(self, UserManager):
        UserManager.setObjectName("UserManager")
        UserManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(UserManager)
        self.gridLayout.setContentsMargins(4, 4, 4, 4)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_add = TransparentToolButton(UserManager)
        self.pb_add.setText("")
        self.pb_add.setObjectName("pb_add")
        self.gridLayout.addWidget(self.pb_add, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.scrollArea = ScrollArea(UserManager)
        self.scrollArea.setStyleSheet("QScrollArea{\n"
"    border:none;\n"
"}")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 992, 587))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridlayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridlayout.setContentsMargins(16, 16, 16, 16)
        self.gridlayout.setObjectName("gridlayout")
        self.gl_userinfo = QtWidgets.QGridLayout()
        self.gl_userinfo.setObjectName("gl_userinfo")
        self.gridlayout.addLayout(self.gl_userinfo, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridlayout.addItem(spacerItem1, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 2)

        self.retranslateUi(UserManager)
        QtCore.QMetaObject.connectSlotsByName(UserManager)

    def retranslateUi(self, UserManager):
        _translate = QtCore.QCoreApplication.translate
        UserManager.setWindowTitle(_translate("UserManager", "用户管理"))
from qfluentwidgets import ScrollArea, TransparentToolButton
