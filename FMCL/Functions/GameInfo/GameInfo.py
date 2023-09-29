import qtawesome as qta
from Core import Game
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QLabel, QWidget, qApp
from qfluentwidgets import MessageBox, TransparentToolButton

from .ui_GameInfo import Ui_GameInfo


class GameInfo(QWidget, Ui_GameInfo):
    gameNameChanged = pyqtSignal(str)
    gameDeleted = pyqtSignal()

    def __init__(self, name: str) -> None:
        super().__init__()
        self.setupUi(self)
        t = self.tr('游戏信息')
        self.setWindowTitle(f"{t}:{name}")
        self.setWindowIcon(qta.icon("mdi6.information-outline"))
        self. __info_translate = {
            "version": self.tr("版本"),
            "forge_version": self.tr("Forge版本"),
            "fabric_version": self.tr("Fabric版本")
        }
        self.game = Game(name)
        self.info = self.game.get_info()
        self.le_name.setText(name)

        for key, val in self.info.items():
            if val:
                label = QLabel()
                label.setText(f"{self.__info_translate[key]}: {val}")
                self.gl_versions.addWidget(label)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.refresh()

    def refresh(self):
        pixmap = self.game.get_pixmap()
        if not pixmap.isNull():
            self.l_logo.setPixmap(pixmap.scaled(64, 64))

    @pyqtSlot(bool)
    def on_pb_opendir_clicked(self, _):
        self.game.open_directory()

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        def confirmDelete():
            self.game.delete()
            self.gameDeleted.emit()
            self.close()
        box = MessageBox(self.tr("删除"),
                         self.tr("确定删除?"),
                         self.window())
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot()
    def on_le_name_editingFinished(self):
        new_name = self.le_name.text()
        if new_name == self.game.name:
            return
        self.game.rename(new_name)
        if hasattr(self.game, "setting"):
            self.game.setting = None
        self.game = Game(new_name)
        self.refresh()
        self.gameNameChanged.emit(new_name)

    def showEvent(self, a0: QShowEvent) -> None:
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_refresh, "right", sender=self))
        return super().showEvent(a0)
