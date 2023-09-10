import qtawesome as qta

from .Update import Update

from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("Update", "更新"),
        "icon": qta.icon("mdi6.update")
    }


fisrt_run = True


def main():
    global fisrt_run
    if fisrt_run:
        update = Update()
        fisrt_run = False
    else:
        update = Update()
        update.show()
