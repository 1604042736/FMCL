import os

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .GameManager import GameManager

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("GameManager", "游戏管理"),
        "icon": qta.icon("mdi6.minecraft"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "explorer.desktop.item_rightclicked_actions" in setting.defaultsetting:
        a = setting.defaultsetting["explorer.desktop.item_rightclicked_actions"]
        if "GameManager" not in a:
            a.insert(1, "GameManager")
    return {}


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None,
            _translate("GameManager", "选择游戏"),
            _translate("GameManager", "游戏列表"),
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")),
            editable=False,
        )
        if not ok:
            return
    gamemanager = GameManager(name)
    gamemanager.show()
