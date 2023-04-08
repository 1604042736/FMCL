from .LogoChooser import LogoChooser

import qtawesome as qta
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting
import os


def functionInfo():
    return {
        "name": "图标选择",
        "icon": qta.icon("ph.image")
    }


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None, "选择游戏", "游戏列表",
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    logochooser = LogoChooser(name)
    logochooser.show()
