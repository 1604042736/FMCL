import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from Setting import Setting

from .WidgetManager import WidgetManager

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("WidgetManager", "控件管理器"),
        "icon": qta.icon("mdi.widgets"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "explorer.title_rightclicked_actions" in setting.defaultsetting:
        a = list(setting.defaultsetting["explorer.title_rightclicked_actions"])
        action = {
            "name": _translate("WidgetManager", "控件管理器"),
            "icon": 'qta.icon("mdi.widgets")',
            "commands": ["WidgetManager"],
        }
        if action not in a:
            a.insert(0, action)
            setting.defaultsetting["explorer.title_rightclicked_actions"] = tuple(a)
    return {}


def main():
    widgetmanager = WidgetManager()
    widgetmanager.show()
