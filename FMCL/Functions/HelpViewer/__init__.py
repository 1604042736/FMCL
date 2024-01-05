import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .HelpViewer import HelpViewer

_translate = QCoreApplication.translate


def functionInfo():
    return {"name": _translate("HelpViewer", "帮助"), "icon": qta.icon("mdi.help")}


def main(id=""):
    helpviewer = HelpViewer()
    helpviewer.show(id)
