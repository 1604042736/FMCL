# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\HelpViewer\HelpViewer.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HelpViewer(object):
    def setupUi(self, HelpViewer):
        HelpViewer.setObjectName("HelpViewer")
        HelpViewer.resize(1000, 618)
        self.gridLayout_2 = QtWidgets.QGridLayout(HelpViewer)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter = QtWidgets.QSplitter(HelpViewer)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.tw_helpindex = TreeWidget(self.splitter)
        self.tw_helpindex.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tw_helpindex.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tw_helpindex.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tw_helpindex.setWordWrap(True)
        self.tw_helpindex.setExpandsOnDoubleClick(True)
        self.tw_helpindex.setColumnCount(2)
        self.tw_helpindex.setObjectName("tw_helpindex")
        self.tw_helpindex.headerItem().setText(0, "1")
        self.tw_helpindex.headerItem().setText(1, "2")
        self.tw_helpindex.header().setVisible(False)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tb_pages = TabBar(self.widget)
        self.tb_pages.setMovable(True)
        self.tb_pages.setScrollable(True)
        self.tb_pages.setProperty("tabMaxWidth", 200)
        self.tb_pages.setObjectName("tb_pages")
        self.gridLayout.addWidget(self.tb_pages, 0, 0, 1, 1)
        self.sw_pages = QtWidgets.QStackedWidget(self.widget)
        self.sw_pages.setObjectName("sw_pages")
        self.gridLayout.addWidget(self.sw_pages, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(HelpViewer)
        QtCore.QMetaObject.connectSlotsByName(HelpViewer)

    def retranslateUi(self, HelpViewer):
        _translate = QtCore.QCoreApplication.translate
        HelpViewer.setWindowTitle(_translate("HelpViewer", "帮助"))
from qfluentwidgets import TabBar, TreeWidget
