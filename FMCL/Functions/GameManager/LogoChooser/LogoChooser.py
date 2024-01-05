import qtawesome as qta
from Core import Version
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog, QWidget

from .ui_LogoChooser import Ui_LogoChooser


class LogoChooser(QWidget, Ui_LogoChooser):
    logos = [
        ":/Image/bookshelf.png",
        ":/Image/chest.png",
        ":/Image/command.png",
        ":/Image/craft_table.png",
        ":/Image/fabric.png",
        ":/Image/forge.png",
        ":/Image/furnace.png",
        ":/Image/grass.png",
    ]

    __instances = {}
    __new_count = {}

    def __new__(cls, name):
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
            cls.__new_count[name] = 0
        return cls.__instances[name]

    def __init__(self, name: str):
        if self.__new_count[name] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.image"))

        self.game = Version(name)
        self.game.generate_setting()
        if self.game.setting.get("logo") not in self.logos:
            self.logos.append(self.game.setting.get("logo"))
        self.cb_logo.currentTextChanged.connect(self.changeLogo)
        self.refresh()

    def refresh(self):
        self.cb_logo.currentTextChanged.disconnect(self.changeLogo)
        self.cb_logo.clear()
        cur_logo = self.game.setting.get("logo")
        self.cb_logo.addItem(QIcon(cur_logo), cur_logo)

        for i in self.logos:
            if i != cur_logo:
                self.cb_logo.addItem(QIcon(i), i)
        self.cb_logo.setCurrentText(cur_logo)
        self.cb_logo.currentTextChanged.connect(self.changeLogo)

    def changeLogo(self, text):
        self.game.setting.set("logo", text)

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        filename, _ = QFileDialog.getOpenFileName(
            self, self.tr("选择图标"), filter="Image Files(*.png *.jpg *.ico)"
        )
        if filename:
            self.logos.append(filename)
            self.refresh()
