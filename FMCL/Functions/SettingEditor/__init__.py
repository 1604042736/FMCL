import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from Setting import DEFAULT_SETTING_PATH, Setting

from .SettingEditor import SettingEditor

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("SettingEditor", "设置"),
        "icon": qta.icon("ri.settings-5-line")
    }


def main(setting_path=DEFAULT_SETTING_PATH, id=""):
    setting = Setting(setting_path)
    settingeditor = SettingEditor(setting)
    settingeditor.show(id)
