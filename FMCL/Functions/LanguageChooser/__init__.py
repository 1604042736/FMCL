import qtawesome as qta

from .LanguageChooser import LanguageChooser
from Setting import Setting


def functionInfo():
    return {
        "name": "语言选择",
        "icon": qta.icon("fa.language")
    }


def main():
    languagechooser = LanguageChooser()
    languagechooser.show()
