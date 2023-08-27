import os

import qtawesome as qta
from Core import Game
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QWidget
from qfluentwidgets import MessageBox

from .ModItem import ModItem
from .ui_ModManager import Ui_ModManager

_translate = Kernel.translate


class ModManager(QWidget, Ui_ModManager):
    def __init__(self, name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))

        self.game = Game(name)
        self.game.generate_setting()
        self.f_operate.setEnabled(False)

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
    def on_pb_refresh_clicked(self, _):
        self.refresh()

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
        box = MessageBox(_translate("删除"),
                         _translate("确认删除")+str(mods)+"?",
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
