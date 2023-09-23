import os

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QInputDialog
from Setting import Setting

from .Launcher import Launcher

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("Launcher", "启动游戏"),
        "icon": qta.icon("mdi.rocket-launch-outline")
    }


def defaultSetting() -> dict:
    setting = Setting()
    a = setting.get("explorer.desktop.item_rightclicked_actions", tuple())
    if "Launcher" not in a:
        a.insert(0, "Launcher")
    return {}


def main(name=None):
    if not name:
        name, ok = QInputDialog.getItem(
            None,
            _translate("Launcher", "选择游戏"),
            _translate("Launcher", "游戏列表"),
            os.listdir(os.path.join(Setting()["game.directories"][0], "versions")), editable=False)
        if not ok:
            return
    launcher = Launcher(name)
    launcher.show()
    launcher.start()
