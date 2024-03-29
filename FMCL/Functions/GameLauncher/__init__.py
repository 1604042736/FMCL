import os

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .GameLauncher import GameLauncher

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
    return {}


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None,
            _translate("GameLauncher", "选择游戏"),
            _translate("GameLauncher", "游戏列表"),
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")),
            editable=False,
        )
        if not ok:
            return
    gamelauncher = GameLauncher(name)
    gamelauncher.show()
