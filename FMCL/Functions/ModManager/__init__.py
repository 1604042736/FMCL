import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox

from .ModManager import ModManager


def functionInfo():
    return {
        "name": "Mod管理",
        "icon": qta.icon("mdi.puzzle-outline")
    }


def main(name=None):
    if not name:
        QMessageBox.critical(None, "参数错误", "应传入游戏名")
        return 1
    modmanager = ModManager(name)
    modmanager.show()
