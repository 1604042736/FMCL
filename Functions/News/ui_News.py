# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\王永健\PCG\FMCL\Ui\News\News.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_News(object):
    def setupUi(self, News):
        News.setObjectName("News")
        News.resize(1000, 618)
        self.gridLayout = QtWidgets.QGridLayout(News)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(News)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 998, 616))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gl_news = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gl_news.setObjectName("gl_news")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(News)
        QtCore.QMetaObject.connectSlotsByName(News)

    def retranslateUi(self, News):
        _translate = QtCore.QCoreApplication.translate
        News.setWindowTitle(_translate("News", "新闻"))