import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox

from .GameInfo import GameInfo


def functionInfo():
    return {
        "name": "游戏信息",
        "icon": qta.icon("mdi6.information-outline")
    }


def main(name=None):
    if not name:
        QMessageBox.critical(None, "参数错误", "应传入游戏名")
        return 1
    gameinfo = GameInfo(name)
    gameinfo.show()
