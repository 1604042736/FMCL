import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .GameDownloader import GameDownloader

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("GameDownloader", "游戏下载器"),
        "icon": qta.icon("ph.download-simple")
    }


def main():
    gamedownloader = GameDownloader()
    gamedownloader.show()
