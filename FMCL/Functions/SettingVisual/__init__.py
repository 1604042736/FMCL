import qtawesome as qta
from Setting import DEFAULT_SETTING_PATH, Setting

from .SettingWidget import SettingWidget


def functionInfo():
    return {
        "name": "设置",
        "icon": qta.icon("ri.settings-5-line")
    }


def main(setting_path=DEFAULT_SETTING_PATH, id=""):
    setting = Setting(setting_path)
    settingw = SettingWidget(setting)
    settingw.show(id)
