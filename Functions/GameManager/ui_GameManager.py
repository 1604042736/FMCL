# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\Functions\GameManager\GameManager.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GameManager(object):
    def setupUi(self, GameManager):
        GameManager.setObjectName("GameManager")
        GameManager.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(GameManager)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.f_panel = QtWidgets.QFrame(GameManager)
        self.f_panel.setMinimumSize(QtCore.QSize(0, 0))
        self.f_panel.setStyleSheet("QPushButton{\n"
"    border:none;\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:rgb(200,200,200);\n"
"}\n"
"QPushButton:checked{\n"
"    border-left:2px solid black;\n"
"}")
        self.f_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.f_panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.f_panel.setObjectName("f_panel")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.f_panel)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_gamesetting = QtWidgets.QPushButton(self.f_panel)
        self.pb_gamesetting.setMinimumSize(QtCore.QSize(0, 32))
        self.pb_gamesetting.setCheckable(True)
        self.pb_gamesetting.setAutoExclusive(True)
        self.pb_gamesetting.setObjectName("pb_gamesetting")
        self.gridLayout_2.addWidget(self.pb_gamesetting, 1, 0, 1, 1)
        self.pb_gameinfo = QtWidgets.QPushButton(self.f_panel)
        self.pb_gameinfo.setMinimumSize(QtCore.QSize(0, 32))
        self.pb_gameinfo.setCheckable(True)
        self.pb_gameinfo.setAutoExclusive(True)
        self.pb_gameinfo.setObjectName("pb_gameinfo")
        self.gridLayout_2.addWidget(self.pb_gameinfo, 0, 0, 1, 1)
        self.pb_modmanager = QtWidgets.QPushButton(self.f_panel)
        self.pb_modmanager.setMinimumSize(QtCore.QSize(0, 32))
        self.pb_modmanager.setCheckable(True)
        self.pb_modmanager.setAutoExclusive(True)
        self.pb_modmanager.setObjectName("pb_modmanager")
        self.gridLayout_2.addWidget(self.pb_modmanager, 2, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 3, 0, 1, 1)
        self.gridLayout.addWidget(self.f_panel, 0, 0, 1, 1)
        self.sw_ui = QtWidgets.QStackedWidget(GameManager)
        self.sw_ui.setObjectName("sw_ui")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.sw_ui.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.sw_ui.addWidget(self.page_2)
        self.gridLayout.addWidget(self.sw_ui, 0, 1, 1, 1)

        self.retranslateUi(GameManager)
        QtCore.QMetaObject.connectSlotsByName(GameManager)

    def retranslateUi(self, GameManager):
        _translate = QtCore.QCoreApplication.translate
        GameManager.setWindowTitle(_translate("GameManager", "游戏管理"))
        self.pb_gamesetting.setText(_translate("GameManager", "设置"))
        self.pb_gameinfo.setText(_translate("GameManager", "信息"))
        self.pb_modmanager.setText(_translate("GameManager", "Mod管理"))
