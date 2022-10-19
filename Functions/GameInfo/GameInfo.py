
import qtawesome as qta
from Core import Game
from PyQt5.QtCore import QCoreApplication, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QLabel, QMessageBox, QWidget

from .ui_GamInfo import Ui_GameInfo

_translate = QCoreApplication.translate


class GameInfo(QWidget, Ui_GameInfo):
    gameNameChanged = pyqtSignal(str)

    def __init__(self, name: str) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi6.information-outline"))
        self. __info_translate = {
            "version": _translate("GameInfo", "版本"),
            "forge_version": _translate("GameInfo", "Forge版本"),
            "fabric_version": _translate("GameInfo", "Fabric版本")
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
        reply = QMessageBox.warning(self,
                                    _translate("GameInfo", "删除"),
                                    _translate("GameInfo", "确定删除?"),
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.game.delete()
            self.close()

    @pyqtSlot()
    def on_le_name_editingFinished(self):
        new_name = self.le_name.text()
        self.game.rename(new_name)
        if hasattr(self.game, "setting"):
            self.game.setting.deleteLater()
        self.game = Game(new_name)
