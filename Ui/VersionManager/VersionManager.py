import os
import json
import shutil
from Core.Game import Game
from QtFBN.QFBNWidget import QFBNWidget
from Ui.VersionManager.ui_VersionManager import Ui_VersionManager
import Globals as g
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal


class VersionManager(QFBNWidget, Ui_VersionManager):
    GameDeleted = pyqtSignal()

    def __init__(self, name, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.version_path = os.path.join(g.cur_gamepath, "versions")
        self.game_path = os.path.join(self.version_path, name)

        config = json.load(open(self.game_path+"/FMCL/config.json"))

        self.name = config["name"]
        self.version = config["version"]
        self.forge_version = config["forge_version"]

        self.le_name.setText(self.name)
        self.l_version.setText(self.version)
        self.l_forgeversion.setText(self.forge_version)

        self.pb_del.clicked.connect(self.del_game)
        self.pb_reinstall.clicked.connect(self.reinstall_game)
        self.pb_openfoder.clicked.connect(lambda: os.startfile(self.game_path))
        self.le_name.textEdited.connect(self.rename_game)

    def close(self, called_del=False) -> bool:
        if not called_del:
            config = {
                "name": self.name,
                "version": self.version,
                "forge_version": self.forge_version
            }
            json.dump(config, open(self.game_path+"/FMCL/config.json"))
        return super().close()

    def del_game(self):
        reply = QMessageBox.warning(self, "删除", "确认删除?",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            shutil.rmtree(self.game_path)
            if self.name == g.cur_version:
                g.cur_version = ""
            self.GameDeleted.emit()
            self.close(True)

    def reinstall_game(self):
        g.dmgr.add_task(f"下载{self.name}", Game(
            self.name, self.version, self.forge_version), "download_version", tuple())

    def rename_game(self):
        new_name = self.le_name.text()
        os.rename(self.game_path, os.path.join(self.version_path, new_name))
        if self.name == g.cur_version:
            g.cur_version = new_name
        self.name = new_name
        self.game_path = os.path.join(self.version_path, self.name)
