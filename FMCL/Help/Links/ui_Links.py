# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Help\Links\Links.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Links(object):
    def setupUi(self, Links):
        Links.setObjectName("Links")
        Links.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Links)
        self.gridLayout.setObjectName("gridLayout")
        self.ScrollArea = ScrollArea(Links)
        self.ScrollArea.setStyleSheet("QScrollArea{\n"
"    border:none;\n"
"}")
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setObjectName("ScrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 982, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_wiki = PushButton(self.scrollAreaWidgetContents)
        self.pb_wiki.setObjectName("pb_wiki")
        self.gridLayout_2.addWidget(self.pb_wiki, 1, 0, 1, 1)
        self.pb_mcmod = PushButton(self.scrollAreaWidgetContents)
        self.pb_mcmod.setObjectName("pb_mcmod")
        self.gridLayout_2.addWidget(self.pb_mcmod, 2, 0, 1, 1)
        self.pb_plugin = PushButton(self.scrollAreaWidgetContents)
        self.pb_plugin.setObjectName("pb_plugin")
        self.gridLayout_2.addWidget(self.pb_plugin, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.pb_officialweb = PushButton(self.scrollAreaWidgetContents)
        self.pb_officialweb.setObjectName("pb_officialweb")
        self.gridLayout_2.addWidget(self.pb_officialweb, 0, 0, 1, 1)
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.ScrollArea, 0, 0, 1, 1)

        self.retranslateUi(Links)
        QtCore.QMetaObject.connectSlotsByName(Links)

    def retranslateUi(self, Links):
        _translate = QtCore.QCoreApplication.translate
        Links.setWindowTitle(_translate("Links", "常用网站"))
        self.pb_wiki.setText(_translate("Links", "Minecraft Wiki"))
        self.pb_mcmod.setText(_translate("Links", "MC 百科"))
        self.pb_plugin.setText(_translate("Links", "插件百科"))
        self.pb_officialweb.setText(_translate("Links", "官网"))
from qfluentwidgets import PushButton, ScrollArea
