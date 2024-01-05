import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from Setting import Setting

from .GameDownloader import GameDownloader

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("GameDownloader", "游戏下载器"),
        "icon": qta.icon("ph.download-simple"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "explorer.desktop.rightclicked_actions" in setting.defaultsetting:
        a = setting.defaultsetting["explorer.desktop.rightclicked_actions"]
        if "GameDownloader" not in a:
            a.insert(0, "GameDownloader")
    return {}


def main():
    gamedownloader = GameDownloader()
    gamedownloader.show()
