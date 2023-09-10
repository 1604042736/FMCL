import os

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .LogoChooser import LogoChooser

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("LogoChooser", "图标选择"),
        "icon": qta.icon("ph.image")
    }


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None,
            _translate("LogoChooser", "选择游戏"),
            _translate("LogoChooser", "游戏列表"),
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    logochooser = LogoChooser(name)
    logochooser.show()
