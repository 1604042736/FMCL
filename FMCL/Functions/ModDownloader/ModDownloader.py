import logging
import traceback

import multitasking
import qtawesome as qta
from Core import Mod, ApiModInfo
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QWidget

from .ApiModItem import ApiModItem
from .ui_ModDownloader import Ui_ModDownloader


class ModDownloader(QWidget, Ui_ModDownloader):
    __modGot = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))
        self.search_canceled = False

        self.mod = Mod()
        self.cb_downloadsource.addItems(self.mod.get_all_downloadsources())
        self.cb_downloadsource.setCurrentText(self.mod.get_all_downloadsources()[0])
        self.cb_sort.addItems(self.mod.get_all_sortmethod())
        self.cb_downloadsource.currentTextChanged.connect(self.mod.set_downloadsource)
        self.cb_downloadsource.currentTextChanged.connect(self.setSort)
        self.__modGot.connect(self.addMod)

    def setSort(self):
        self.cb_sort.clear()
        self.cb_sort.addItems(self.mod.get_all_sortmethod())

    @pyqtSlot(bool)
    def on_pb_search_clicked(self, _):
        self.search_canceled = False
        self.search()

    @pyqtSlot(bool)
    def on_pb_cancelsearch_clicked(self, _):
        self.search_canceled = True

    @multitasking.task
    def search(self):
        self.pb_search.setEnabled(False)
        self.lw_mods.clear()
        name = self.le_name.text()
        sort = self.cb_sort.currentText()
        try:
            for i in self.mod.search(name, sort, yield_=True):
                if self.search_canceled:
                    self.search_canceled = False
                    break
                self.__modGot.emit(i)
        except:
            logging.error(traceback.format_exc())
        self.pb_search.setEnabled(True)

    def setMods(self, mods: list):
        self.tw_mods.clear()
        for mod in mods:
            self.addMod(mod)

    def addMod(self, mod: ApiModInfo, root=None):
        item = QListWidgetItem()
        widget = ApiModItem(mod)
        item.setSizeHint(widget.size())
        self.lw_mods.addItem(item)
        self.lw_mods.setItemWidget(item, widget)
