import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .About import About

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("About", "关于"),
        "icon": qta.icon("mdi.information-outline"),
    }


def main():
    about = About()
    about.show()
