import os

from PyQt5.QtGui import QIcon

from .StrongholdFinder import StrongholdFinder


def functionInfo():
    return {
        "name": "要塞寻址",
        "icon": QIcon(f"{os.path.dirname(__file__)}/ender_eye.png")
    }


def main():
    strongholdfinder=StrongholdFinder()
    strongholdfinder.show()
