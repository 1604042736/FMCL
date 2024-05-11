import qtawesome as qta
from PyQt5.QtWidgets import QWidget
from Setting import Setting
from Core import Translation

from .ui_LanguageChooser import Ui_LanguageChooser


class LanguageChooser(QWidget, Ui_LanguageChooser):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.language"))
        self.cb_lang.currentTextChanged.connect(self.changeLanguage)
        self.refresh()

    def refresh(self):
        self.cb_lang.currentTextChanged.disconnect(self.changeLanguage)
        self.cb_lang.clear()
        cur_lang = Setting().get("language.type")
        self.cb_lang.addItem(cur_lang)
        for lang in Translation.get_all_languages():
            if lang != cur_lang:
                self.cb_lang.addItem(lang)
        self.cb_lang.setCurrentText(cur_lang)
        self.cb_lang.currentTextChanged.connect(self.changeLanguage)

    def changeLanguage(self, lang):
        Setting().set("language.type", lang)
