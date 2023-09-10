import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .ModDownloader import ModDownloader

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("ModDownloader", "Mod下载器"),
        "icon": qta.icon("mdi.puzzle-outline")
    }


def main():
    moddownloader = ModDownloader()
    moddownloader.show()
