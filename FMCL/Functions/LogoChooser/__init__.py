from .LogoChooser import LogoChooser

import qtawesome as qta
from PyQt5.QtWidgets import QMessageBox


def functionInfo():
    return {
        "name": "图标选择",
        "icon": qta.icon("ph.image")
    }


def main(name=None):
    if not name:
        QMessageBox.critical(None, "参数错误", "应传入游戏名")
        return 1
    logochooser = LogoChooser(name)
    logochooser.show()
