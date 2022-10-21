import os

from Core import Game
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QWidget
import qtawesome as qta
from .ModItem import ModItem
from .ui_ModManager import Ui_ModManager


class ModManager(QWidget, Ui_ModManager):
    def __init__(self, name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))

        self.game = Game(name)
        self.game.generate_setting()

        self.refresh()

    def refresh(self):
        self.lw_mods.clear()
        mods = self.game.get_mods()
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
