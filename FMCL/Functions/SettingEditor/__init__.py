import qtawesome as qta
from Setting import DEFAULT_SETTING_PATH, Setting

from .SettingEditor import SettingEditor


def functionInfo():
    return {
        "name": "设置",
        "icon": qta.icon("ri.settings-5-line")
    }


def main(setting_path=DEFAULT_SETTING_PATH, id=""):
    setting = Setting(setting_path)
    settingeditor = SettingEditor(setting)
    settingeditor.show(id)
