from .GameManager import GameManager

import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox

def functionInfo():
    return {
        "name": "游戏管理",
        "icon": qta.icon("mdi6.minecraft")
    }


def main(name=None):
    if not name:
        QMessageBox.critical(None, "参数错误", "应传入游戏名")
        return 1
    gamemanager = GameManager(name)
    gamemanager.show()
