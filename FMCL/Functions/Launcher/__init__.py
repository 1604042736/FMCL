import os

import qtawesome as qta
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .Launcher import Launcher


def functionInfo():
    return {
        "name": "启动游戏",
        "icon": qta.icon("mdi.rocket-launch-outline")
    }


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None, "选择游戏", "游戏列表",
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    launcher = Launcher(name)
    launcher.show()
    launcher.start()
