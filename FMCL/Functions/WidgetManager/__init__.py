import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from Setting import Setting

from .WidgetManager import WidgetManager

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("WidgetManager", "控件管理器"),
        "icon": qta.icon("mdi.widgets")
    }


def defaultSetting() -> dict:
    setting = Setting()
    a = setting.get("explorer.title_rightclicked_actions", tuple())
    if "WidgetManager" not in a:
        a.insert(1, "WidgetManager")
    return {}


def main():
    widgetmanager = WidgetManager()
    widgetmanager.show()
