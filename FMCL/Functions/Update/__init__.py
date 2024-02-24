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
        a = list(setting.defaultsetting.get("system.startup_functions"))
        action = {"commands": ["Update True"]}
        if action not in a:
            a.insert(1, action)
            setting.defaultsetting["system.startup_functions"] = tuple(a)
    return {}


def main(only_check=False):
    if only_check:
        update = Update()
    else:
        update = Update()
        update.show()
