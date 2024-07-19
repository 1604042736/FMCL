import qtawesome as qta
from Core import Function, Version
from FMCL.Functions.SettingEditor import SettingEditor
from PyQt5.QtCore import QEvent, pyqtSlot, QObject
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import qconfig, isDarkTheme
from Setting import Setting

from .GameInfo import GameInfo
from .LogoChooser import LogoChooser
from .ModManager import ModManager
from .SaveManager import SaveManager
from .ScreenshotManager import ScreenshotManager
from .ui_GameManager import Ui_GameManager


class AutoSyncDefaultSettingFilter(QObject):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1.type() in (QEvent.Type.Show, QEvent.Type.WindowActivate):
            Version(self.name).generate_setting()
        return super().eventFilter(a0, a1)


class GameManager(QWidget, Ui_GameManager):
    __instances = {}
    __new_count = {}

    def __new__(cls, name: str):
        # 防止不同目录的同名版本
        dir = Setting()["game.directories"][0]
        key = f"{dir}/{name}"
        if key not in cls.__instances:
            cls.__instances[key] = super().__new__(cls)
            cls.__new_count[key] = 0
        cls.__new_count[key] += 1
        return cls.__instances[key]

    def __init__(self, name: str):
        dir = Setting()["game.directories"][0]
        key = f"{dir}/{name}"
        if self.__new_count[key] > 1:
            return
        super().__init__()
        self.setupUi(self)
        t = self.tr("游戏管理")
        self.setWindowTitle(f"{t}:{name}")
        self.setWindowIcon(qta.icon("mdi6.minecraft"))
        self.pb_gameinfo.setIcon(qta.icon("mdi6.information-outline"))
        self.pb_gamesetting.setIcon(qta.icon("ri.settings-5-line"))
        self.pb_modmanager.setIcon(qta.icon("mdi.puzzle-outline"))
        self.pb_savemanager.setIcon(qta.icon("fa.save"))
        self.pb_screenshotmanager.setIcon(qta.icon("ei.picture"))
        self.name = name
        self.game = Version(name)

        qconfig.themeChanged.connect(self.on_themeChanged)
        self.on_themeChanged()

        self.refresh()

    def on_themeChanged(self):
        self.f_panel.setStyleSheet(
            f"QFrame{{background-color:rgba(255,255,255,{13 if isDarkTheme() else 170})}}"
        )

    def refresh(self):
        while self.sw_ui.count():
            self.sw_ui.removeWidget(self.sw_ui.widget(0))

        self.gameinfo = GameInfo(self.name)
        self.gameinfo.gameNameChanged.connect(self.renamed)
        self.gameinfo.gameDeleted.connect(self.close)

        self.game.DEFAULT_SETTING_ATTR["logo"]["settingcard"] = lambda: LogoChooser(
            self.name
        )
        self.game.generate_setting()
        self.gamesetting = SettingEditor(self.game.setting)
        self.settingfilter = AutoSyncDefaultSettingFilter(self.name)
        self.gamesetting.installEventFilter(self.settingfilter)

        self.modmanager = None
        self.savemanager = None
        self.screenshotmanager = None

        self.pb_gameinfo.setChecked(True)
        self.setUi(self.gameinfo)

    def renamed(self, name):
        Function("GameManager").exec(name=name)
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
        self.gamesetting.show()

    @pyqtSlot(bool)
    def on_pb_modmanager_clicked(self, _):
        self.pb_modmanager.setChecked(True)
        if self.modmanager == None:
            self.modmanager = ModManager(self.name)
            self.setUi(self.modmanager)
            self.modmanager.refresh()
        else:
            self.setUi(self.modmanager)

    @pyqtSlot(bool)
    def on_pb_savemanager_clicked(self, _):
        self.pb_savemanager.setChecked(True)
        if self.savemanager == None:
            self.savemanager = SaveManager(self.name)
            self.setUi(self.savemanager)
            self.savemanager.refresh()
        else:
            self.setUi(self.savemanager)

    @pyqtSlot(bool)
    def on_pb_screenshotmanager_clicked(self, _):
        self.pb_screenshotmanager.setChecked(True)
        if self.screenshotmanager == None:
            self.screenshotmanager = ScreenshotManager(self.name)
            self.setUi(self.screenshotmanager)
            self.screenshotmanager.refresh()
        else:
            self.setUi(self.screenshotmanager)
