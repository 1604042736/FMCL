# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\Explorer\Help\Desktop.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Desktop(object):
    def setupUi(self, Desktop):
        Desktop.setObjectName("Desktop")
        Desktop.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Desktop)
        self.gridLayout.setObjectName("gridLayout")
        self.ScrollArea = ScrollArea(Desktop)
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
        spacerItem = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 9, 0, 1, 1)
        self.BodyLabel = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel.setWordWrap(True)
        self.BodyLabel.setObjectName("BodyLabel")
        self.gridLayout_2.addWidget(self.BodyLabel, 0, 0, 1, 1)
        self.BodyLabel_5 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_5.setWordWrap(True)
        self.BodyLabel_5.setObjectName("BodyLabel_5")
        self.gridLayout_2.addWidget(self.BodyLabel_5, 5, 0, 1, 1)
        self.BodyLabel_4 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_4.setWordWrap(True)
        self.BodyLabel_4.setObjectName("BodyLabel_4")
        self.gridLayout_2.addWidget(self.BodyLabel_4, 4, 0, 1, 1)
        self.BodyLabel_2 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_2.setWordWrap(True)
        self.BodyLabel_2.setObjectName("BodyLabel_2")
        self.gridLayout_2.addWidget(self.BodyLabel_2, 1, 0, 1, 1)
        self.BodyLabel_7 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_7.setWordWrap(True)
        self.BodyLabel_7.setObjectName("BodyLabel_7")
        self.gridLayout_2.addWidget(self.BodyLabel_7, 7, 0, 1, 1)
        self.BodyLabel_3 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_3.setWordWrap(True)
        self.BodyLabel_3.setObjectName("BodyLabel_3")
        self.gridLayout_2.addWidget(self.BodyLabel_3, 3, 0, 1, 1)
        self.BodyLabel_6 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_6.setWordWrap(True)
        self.BodyLabel_6.setObjectName("BodyLabel_6")
        self.gridLayout_2.addWidget(self.BodyLabel_6, 6, 0, 1, 1)
        self.BodyLabel_8 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_8.setWordWrap(True)
        self.BodyLabel_8.setObjectName("BodyLabel_8")
        self.gridLayout_2.addWidget(self.BodyLabel_8, 8, 0, 1, 1)
        self.BodyLabel_9 = BodyLabel(self.scrollAreaWidgetContents)
        self.BodyLabel_9.setWordWrap(True)
        self.BodyLabel_9.setObjectName("BodyLabel_9")
        self.gridLayout_2.addWidget(self.BodyLabel_9, 2, 0, 1, 1)
        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.ScrollArea, 0, 0, 1, 1)

        self.retranslateUi(Desktop)
        QtCore.QMetaObject.connectSlotsByName(Desktop)

    def retranslateUi(self, Desktop):
        _translate = QtCore.QCoreApplication.translate
        Desktop.setWindowTitle(_translate("Desktop", "桌面"))
        self.BodyLabel.setText(_translate("Desktop", "在你打开时见到的就是桌面"))
        self.BodyLabel_5.setText(_translate("Desktop", "”分离“可以让对应的界面以独立的窗口显示出来，右键这个独立出来的窗口的标题栏，同样会有菜单弹出，其中的“合并”项可以让这个窗口重新回到启动器中"))
        self.BodyLabel_4.setText(_translate("Desktop", "你可以右键这些按钮你会看到一个菜单，包括”分离“和”关闭“两个操作"))
        self.BodyLabel_2.setText(_translate("Desktop", "与Windows系统相同，它的最上面是任务栏，点击最左边的有着启动器图标的按钮可以进入开始界面"))
        self.BodyLabel_7.setText(_translate("Desktop", "右键桌面空白处同样会有菜单弹出，具体内容无须多言"))
        self.BodyLabel_3.setText(_translate("Desktop", "所有功能显示的窗口一般都会被捕获并显示在这一个窗口里，同时在任务栏显示一个有着相应图标和标题的按钮"))
        self.BodyLabel_6.setText(_translate("Desktop", "”关闭“顾名思义就是关闭对应的界面"))
        self.BodyLabel_8.setText(_translate("Desktop", "桌面会显示所有游戏版本，右键这些游戏版本同样会有菜单弹出"))
        self.BodyLabel_9.setText(_translate("Desktop", "右键标题栏会有菜单弹出"))
from qfluentwidgets import BodyLabel, ScrollArea
