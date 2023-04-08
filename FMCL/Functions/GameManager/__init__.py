import os

import qtawesome as qta
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .GameManager import GameManager


def functionInfo():
    return {
        "name": "游戏管理",
        "icon": qta.icon("mdi6.minecraft")
    }


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None, "选择游戏", "游戏列表",
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    gamemanager = GameManager(name)
    gamemanager.show()
