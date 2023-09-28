import qtawesome as qta

from .Update import Update

from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate
from Setting import Setting

def functionInfo():
    return {
        "name": _translate("Update", "更新"),
        "icon": qta.icon("mdi6.update")
    }

def defaultSetting() -> dict:
    setting = Setting()
    a = setting.get("system.startup_functions", tuple())
    if "Update" not in a:
        a.insert(1, "Update")
    return {}


fisrt_run = True


def main():
    global fisrt_run
    if fisrt_run:
        update = Update()
        fisrt_run = False
    else:
        update = Update()
        update.show()
