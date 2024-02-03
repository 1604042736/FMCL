import qtawesome as qta

from PyQt5.QtCore import QCoreApplication

from .ResourceDownloader import ResourceDownloader

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("ResourceDownloader", "资源下载器"),
        "icon": qta.icon("mdi.earth"),
    }


def main():
    resourcedownloader = ResourceDownloader()
    resourcedownloader.show()
