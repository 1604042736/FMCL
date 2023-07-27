import qtawesome as qta
from Core import Game
from Kernel import Kernel
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QWidget
from qfluentwidgets import MessageBox

from .ui_GameInfo import Ui_GameInfo

_translate = Kernel.translate


class GameInfo(QWidget, Ui_GameInfo):
    gameNameChanged = pyqtSignal(str)

    def __init__(self, name: str) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"{_translate('游戏信息')}:{name}")
        self.setWindowIcon(qta.icon("mdi6.information-outline"))
        self. __info_translate = {
            "version": _translate("版本"),
            "forge_version": _translate("Forge版本"),
            "fabric_version": _translate("Fabric版本")
        }
        self.game = Game(name)
        self.info = self.game.get_info()
        self.le_name.setText(name)

        for key, val in self.info.items():
            if val:
                label = QLabel()
                label.setText(f"{self.__info_translate[key]}: {val}")
                self.gl_versions.addWidget(label)

        self.refresh()

    def refresh(self):
        pixmap = self.game.get_pixmap()
        if not pixmap.isNull():
            self.l_logo.setPixmap(pixmap.scaled(64, 64))

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self, _):
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_opendir_clicked(self, _):
        self.game.open_directory()

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        def confirmDelete():
            self.game.delete()
            self.close()
        box = MessageBox(_translate("删除"),
                         _translate("确定删除?"),
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
