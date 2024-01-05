from Setting import Setting
import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .Update import Update

_translate = QCoreApplication.translate


def functionInfo():
    return {"name": _translate("Update", "更新"), "icon": qta.icon("mdi6.update")}


def defaultSetting() -> dict:
    setting = Setting()
    if "system.startup_functions" in setting.defaultsetting:
        a = setting.defaultsetting.get("system.startup_functions")
        if "Update" not in a:
            a.insert(1, "Update")
    return {}


fisrt_run = True


def main():
    global fisrt_run
    if "Update" not in Setting().get("system.startup_functions", tuple()):
        fisrt_run = False
    if fisrt_run:
        update = Update()
        fisrt_run = False
    else:
        update = Update()
        update.show()
