import qtawesome as qta
from Core import Game
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem, QWidget

from .ui_LogoChooser import Ui_LogoChooser

_translate = QCoreApplication.translate


class LogoChooser(QWidget, Ui_LogoChooser):
    logos = [
        ":/Image/bookshelf.png",
        ":/Image/chest.png",
        ":/Image/command.png",
        ":/Image/craft_table.png",
        ":/Image/fabric.png",
        ":/Image/forge.png",
        ":/Image/furnace.png",
        ":/Image/grass.png"
    ]

    __instances = {}
    __new_count = {}

    def __new__(cls, game):
        if game not in cls.__instances:
            cls.__instances[game] = super().__new__(cls)
            cls.__new_count[game] = 0
        return cls.__instances[game]

    def __init__(self, game: Game):
        if self.__new_count[game] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.image"))

        self.game = game
        if self.game.setting.get("logo") not in self.logos:
            self.logos.append(self.game.setting.get("logo"))

        self.refresh()

    def refresh(self):
        self.lw_logos.clear()

        for i in self.logos:
            item = QListWidgetItem()
            item.setIcon(QIcon(i))
            item.setText(i)
            item.setToolTip(i)
            self.lw_logos.addItem(item)

            if i == self.game.setting.get("logo"):
                self.lw_logos.setCurrentItem(item)

    @pyqtSlot(bool)
    def on_pb_ok_clicked(self, _):
        self.game.setting.set_value("logo", self.lw_logos.currentItem().text())

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        filename, _ = QFileDialog.getOpenFileName(
            self, _translate("LogoChooser", "选择图标"), filter="Image Files(*.png *.jpg *.ico)")
        if filename:
            self.logos.append(filename)
            self.refresh()
