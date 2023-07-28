import qtawesome as qta
from Setting import Setting

from .LanguageChooser import LanguageChooser


def functionInfo():
    return {
        "name": "语言选择",
        "icon": qta.icon("fa.language")
    }


def defaultSettingAttr() -> dict:
    Setting().attrs["language.type"]["setting_item"] = LanguageChooser
    return {}


def main():
    languagechooser = LanguageChooser()
    languagechooser.show()
