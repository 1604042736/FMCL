import qtawesome as qta
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget

from .Page import Page
from .Pages import *
from .ui_Help import Ui_Help


class Help(QWidget, Ui_Help):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.help"))
        self.indexes = getIndexes()
        self.indexes_attr = getIndexesAttr()
        self.item_page = []
        self.items = {}
        for key, page in self.indexes.items():
            children = key.split(".")
            for i, val in enumerate(children):
                child = ".".join(children[:i]) if i > 0 else val
                parent = ".".join(children[:i-1]) if i-1 > 0 else "???"

                if child in self.items:
                    continue

                root = self.items.get(parent, None)
                item = QTreeWidgetItem()
                item.setText(0, self.indexes_attr.get(child, child))
                self.addTreeItem(root, item)
                self.items[child] = item

            self.item_page.append((item, page))

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
