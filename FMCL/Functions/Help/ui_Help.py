# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\FMCL\Functions\Help\Help.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(Help)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(Help)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tw_indexes = TreeWidget(self.splitter)
        self.tw_indexes.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tw_indexes.setObjectName("tw_indexes")
        self.tw_indexes.headerItem().setText(0, "1")
        self.tw_indexes.header().setVisible(False)
        self.sw_pages = QtWidgets.QStackedWidget(self.splitter)
        self.sw_pages.setObjectName("sw_pages")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 4)
        self.pb_next = PushButton(Help)
        self.pb_next.setEnabled(False)
        self.pb_next.setMaximumSize(QtCore.QSize(128, 16777215))
        self.pb_next.setObjectName("pb_next")
        self.gridLayout.addWidget(self.pb_next, 0, 1, 1, 1)
        self.pb_pre = PushButton(Help)
        self.pb_pre.setEnabled(False)
        self.pb_pre.setMaximumSize(QtCore.QSize(128, 16777215))
        self.pb_pre.setObjectName("pb_pre")
        self.gridLayout.addWidget(self.pb_pre, 0, 0, 1, 1)
        self.l_index = QtWidgets.QLabel(Help)
        self.l_index.setText("")
        self.l_index.setAlignment(QtCore.Qt.AlignCenter)
        self.l_index.setObjectName("l_index")
        self.gridLayout.addWidget(self.l_index, 0, 2, 1, 1)
        self.pb_separate = PushButton(Help)
        self.pb_separate.setMaximumSize(QtCore.QSize(128, 16777215))
        self.pb_separate.setObjectName("pb_separate")
        self.gridLayout.addWidget(self.pb_separate, 0, 3, 1, 1)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "帮助"))
        self.pb_next.setText(_translate("Help", "下一页"))
        self.pb_pre.setText(_translate("Help", "上一页"))
        self.pb_separate.setText(_translate("Help", "分离"))
from qfluentwidgets import PushButton, TreeWidget
