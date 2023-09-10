import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from .StrongholdFinder import StrongholdFinder

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("StrongholdFinder", "要塞寻址"),
        "icon": QIcon(f"{os.path.dirname(__file__)}/ender_eye.png")
    }


def main():
    strongholdfinder = StrongholdFinder()
    strongholdfinder.show()
