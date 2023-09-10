import os

import qtawesome as qta
from Core import Game
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QListWidgetItem, QWidget, qApp
from qfluentwidgets import MessageBox, TransparentToolButton

from .ModItem import ModItem
from .ui_ModManager import Ui_ModManager


class ModManager(QWidget, Ui_ModManager):
    def __init__(self, name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))

        self.game = Game(name)
        self.game.generate_setting()
        self.f_operate.setEnabled(False)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.refresh()

    def refresh(self, keyword=""):
        if not self.game.mod_avaiable():
            self.setEnabled(False)
            return
        self.lw_mods.clear()
        mods = self.game.get_mods(keyword)
        for enabled, name in mods:
            item = QListWidgetItem()
            widget = ModItem(self.game, enabled, name)
            item.setSizeHint(widget.size())
            self.lw_mods.addItem(item)
            self.lw_mods.setItemWidget(item, widget)

    @pyqtSlot(bool)
    def on_pb_openmodir_clicked(self, _):
        os.startfile(self.game.get_mod_path())

    @pyqtSlot()
    def on_le_search_editingFinished(self):
        self.refresh(self.le_search.text())

    @pyqtSlot()
    def on_lw_mods_itemSelectionChanged(self):
        if self.lw_mods.selectedItems():
            self.f_operate.setEnabled(True)
        else:
            self.f_operate.setEnabled(False)

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        mods = [
            self.lw_mods.itemWidget(item).getModFileName() for item in self.lw_mods.selectedItems()
        ]

        def confirmDelete():
            self.game.deleteMods(mods)
            self.refresh()
        box = MessageBox(self.tr("删除"),
                         self.tr("确认删除")+str(mods)+"?",
                         self.window())
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_enabled_clicked(self, _):
        mods = [
            self.lw_mods.itemWidget(item).modname for item in self.lw_mods.selectedItems()
        ]
        self.game.setModEnabled(True, mods)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_disabled_clicked(self, _):
        mods = [
            self.lw_mods.itemWidget(item).modname for item in self.lw_mods.selectedItems()
        ]
        self.game.setModEnabled(False, mods)
        self.refresh()

    def showEvent(self, a0: QShowEvent) -> None:
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_refresh, "right", sender=self))
        return super().showEvent(a0)
