import os

import qtawesome as qta
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .ModManager import ModManager


def functionInfo():
    return {
        "name": "Mod管理",
        "icon": qta.icon("mdi.puzzle-outline")
    }


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None, "选择游戏", "游戏列表",
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    modmanager = ModManager(name)
    modmanager.show()
