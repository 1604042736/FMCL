import qtawesome as qta
from Core import Game
from FMCL.Functions.SettingEditor import SettingEditor
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from ..GameInfo import GameInfo
from ..LogoChooser import LogoChooser
from ..ModManager import ModManager
from .ui_GameManager import Ui_GameManager


class GameManager(QWidget, Ui_GameManager):

    __instances = {}
    __new_count = {}

    def __new__(cls, name: str):
        if name not in cls.__instances:
            cls.__instances[name] = super().__new__(cls)
            cls.__new_count[name] = 0
        cls.__new_count[name] += 1
        return cls.__instances[name]

    def __init__(self, name: str):
        if self.__new_count[name] > 1:
            return
        super().__init__()
        self.setupUi(self)
        t=self.tr('游戏管理')
        self.setWindowTitle(f"{t}:{name}")
        self.setWindowIcon(qta.icon("mdi6.minecraft"))
        self.pb_gameinfo.setIcon(qta.icon("mdi6.information-outline"))
        self.pb_gamesetting.setIcon(qta.icon("ri.settings-5-line"))
        self.pb_modmanager.setIcon(qta.icon("mdi.puzzle-outline"))
        self.name = name
        self.game = Game(name)
        self.refresh()

    def refresh(self):
        while self.sw_ui.count():
            self.sw_ui.removeWidget(self.sw_ui.widget(0))

        self.gameinfo = GameInfo(self.name)
        self.gameinfo.gameNameChanged.connect(self.renamed)
        self.gameinfo.gameDeleted.connect(self.close)

        self.game.DEFAULT_SETTING_ATTR["logo"]["settingcard"] = \
            lambda: LogoChooser(self.name)
        self.game.generate_setting()
        self.gamesetting = SettingEditor(self.game.setting)

        self.modmanager = ModManager(self.name)

        self.pb_gameinfo.setChecked(True)
        self.setUi(self.gameinfo)

    def renamed(self, name):
        Kernel.execFunction("GameManager", name=name)
        self.close()

    def setUi(self, widget: QWidget):
        while self.sw_ui.count():
            self.sw_ui.removeWidget(self.sw_ui.widget(0))
        self.sw_ui.addWidget(widget)

    @pyqtSlot(bool)
    def on_pb_gameinfo_clicked(self, _):
        self.pb_gameinfo.setChecked(True)
        self.setUi(self.gameinfo)

    @pyqtSlot(bool)
    def on_pb_gamesetting_clicked(self, _):
        self.pb_gamesetting.setChecked(True)
        self.setUi(self.gamesetting)

    @pyqtSlot(bool)
    def on_pb_modmanager_clicked(self, _):
        self.pb_modmanager.setChecked(True)
        self.setUi(self.modmanager)
