import os

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QDialog
from Setting import Setting

from .GameLauncher import GameLauncher
from .ui_StartupDialog import Ui_StartupDialog

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("GameLauncher", "启动游戏"),
        "icon": qta.icon("mdi.rocket-launch-outline"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "explorer.desktop.item_rightclicked_actions" in setting.defaultsetting:
        a = list(setting.defaultsetting["explorer.desktop.item_rightclicked_actions"])
        action = {
            "name": _translate("GameLauncher", "启动游戏"),
            "icon": 'qta.icon("mdi.rocket-launch-outline")',
            "commands": ['GameLauncher "{name}"'],
        }
        if action not in a:
            a.insert(0, action)
            setting.defaultsetting["explorer.desktop.item_rightclicked_actions"] = (
                tuple(a)
            )
    return {"gamelauncher.never_use_javawrapper": False}


def defaultSettingAttr() -> dict:
    return {
        "gamelauncher": {
            "name": _translate("GameLauncher", "游戏启动器"),
        },
        "gamelauncher.never_use_javawrapper": {
            "name": _translate("GameLauncher", "永远不使用JavaWrapper")
        },
    }


class StartupDialog(QDialog, Ui_StartupDialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.rocket-launch-outline"))

        self.cb_toberun.addItems(
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions"))
        )
        if not GameLauncher.instances:
            self.cb_running.setEnabled(False)
        else:
            self.cb_running.addItems([i.windowTitle() for i in GameLauncher.instances])

    def exec(self):
        ret = super().exec()
        if self.ckb_toberun.isChecked():
            return self.cb_toberun.currentText(), ret == QDialog.DialogCode.Accepted
        else:
            return (
                GameLauncher.instances[self.cb_running.currentIndex()],
                ret == QDialog.DialogCode.Accepted,
            )

    @pyqtSlot(bool)
    def on_pb_ok_clicked(self, _):
        self.accept()

    @pyqtSlot(bool)
    def on_pb_cancel_clicked(self, _):
        self.reject()


def main(name=None):
    if not name:
        dialog = StartupDialog()
        name, ok = dialog.exec()
        if not ok:
            return
        if isinstance(name, GameLauncher):
            name.show()
            return
    gamelauncher = GameLauncher(name)
    gamelauncher.show()
