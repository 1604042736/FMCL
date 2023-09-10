import qtawesome as qta
from Setting import Setting

from .LanguageChooser import LanguageChooser

from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("LanguageChooser", "语言选择"),
        "icon": qta.icon("fa.language")
    }


def defaultSettingAttr() -> dict:
    Setting().attrs["language.type"]["settingcard"] = LanguageChooser
    return {}


def main():
    languagechooser = LanguageChooser()
    languagechooser.show()
