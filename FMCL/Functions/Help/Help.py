import os

import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QAction, QTreeWidgetItem, QWidget, qApp

from .Page import Page
from .ui_Help import Ui_Help

_translate = Kernel.translate


class Help(QWidget, Ui_Help):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.help"))
        self.splitter.setSizes([100, 500])
        self.item_page = []
        self.items = {}
        for root, dirs, files in os.walk(os.path.dirname(__file__)+"/Pages"):
            for file in files:
                file_path = os.path.join(root, file)
                name, ext = os.path.splitext(file_path)
                if ext == ".md":
                    self.addHelp(file_path)

    def addHelp(self, file_path: str):
        full_path = file_path
        file_path = file_path.replace("/", "\\")
        file_path = file_path.replace(
            os.path.dirname(__file__)+"\\Pages\\", "")
        file_path = file_path.split("\\")
        for i in range(len(file_path)-1):
            root_name = '/'.join(file_path[:i])
            child_name = "/".join(file_path[:i+1])
            if child_name in self.items:
                continue
            root = self.items.get(root_name, None)
            item = QTreeWidgetItem()
            item.setText(0, file_path[i])
            self.addTreeItem(root, item)
            self.items[child_name] = item
        item = QTreeWidgetItem()
        item.setText(0, os.path.splitext(file_path[-1])[0])
        self.addTreeItem(self.items.get("/".join(file_path[:-1])), item)
        self.item_page.append((item, full_path))

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_indexes.addTopLevelItem(item)
        else:
            root.addChild(item)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_indexes_itemClicked(self, item, _):
        for item_, page in self.item_page:
            if item_ == item:
                self.sw_pages.addWidget(Page(page))
                self.sw_pages.setCurrentIndex(self.sw_pages.count()-1)
                break

    @pyqtSlot(int)
    def on_sw_pages_currentChanged(self, _):
        self.l_index.setText(
            f"{self.sw_pages.currentIndex()+1}/{self.sw_pages.count()}")
        if self.sw_pages.currentIndex() == self.sw_pages.count()-1:
            self.pb_next.setEnabled(False)
        else:
            self.pb_next.setEnabled(True)

        if self.sw_pages.currentIndex() == 0 or self.sw_pages.count() == 0:
            self.pb_pre.setEnabled(False)
        else:
            self.pb_pre.setEnabled(True)

    @pyqtSlot(bool)
    def on_pb_pre_clicked(self, _):
        self.sw_pages.setCurrentIndex(self.sw_pages.currentIndex()-1)

    @pyqtSlot(bool)
    def on_pb_next_clicked(self, _):
        self.sw_pages.setCurrentIndex(self.sw_pages.currentIndex()+1)

    @pyqtSlot(bool)
    def on_pb_separate_clicked(self, _):
        widget = self.sw_pages.currentWidget()
        if widget == None:
            return
        qApp.sendEvent(self, SeparateWidgetEvent(widget, self.size()))
        a_back = QAction(widget)
        a_back.setText(_translate("合并"))
        a_back.setIcon(qta.icon("msc.reply"))
        a_back.triggered.connect(lambda: (self.sw_pages.addWidget(
            widget), self.sw_pages.setCurrentIndex(self.sw_pages.count()-1)))
        qApp.sendEvent(widget, AddToTitleMenuEvent(a_back))
