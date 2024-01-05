import os

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon

from Kernel import Kernel

from .ui_HowToGetData import Ui_HowToGetData
from .StrongholdFinder import StrongholdFinder

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("StrongholdFinder", "要塞寻址"),
        "icon": QIcon(f"{os.path.dirname(__file__)}/ender_eye.png"),
    }


def helpIndex():
    return {
        "strongholdfinder": {
            "name": _translate("StrongholdFinder", "要塞寻址"),
            "howtogetdata": {
                "name": _translate("StrongholdFinder", "如何获取数据"),
                "page": lambda: Kernel.getWidgetFromUi(Ui_HowToGetData),
            },
        }
    }


def main():
    strongholdfinder = StrongholdFinder()
    strongholdfinder.show()
