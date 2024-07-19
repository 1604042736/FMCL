import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from Setting import DEFAULT_SETTING_PATH, Setting

from .SettingEditor import SettingEditor
from .LanguageChooser import LanguageChooser
from .ThemeChooser import ThemeChooser

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("SettingEditor", "设置"),
        "icon": qta.icon("ri.settings-5-line"),
    }


def defaultSetting() -> dict:
    return {}


def defaultSettingAttr() -> dict:
    Setting().attrs["language.type"]["settingcard"] = LanguageChooser
    Setting().attrs["system.theme"]["settingcard"] = ThemeChooser
    return {}


def main(setting_path=DEFAULT_SETTING_PATH, id=""):
    setting = Setting(setting_path)
    settingeditor = SettingEditor(setting)
    settingeditor.show(id)
