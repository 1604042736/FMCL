import os

import qtawesome as qta
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from Setting import Setting

from .ui_LanguageChooser import Ui_LanguageChooser


class LanguageChooser(QWidget, Ui_LanguageChooser):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.language"))
        self.refresh()

    def refresh(self):
        self.cb_lang.clear()
        cur_lang = Setting().get("language.type")
        self.cb_lang.addItem(cur_lang)
        for name in os.listdir("FMCL/Translations"):
            lang, _ = os.path.splitext(name)
            if lang != cur_lang:
                self.cb_lang.addItem(lang)

    @pyqtSlot(str)
    def on_cb_lang_currentTextChanged(self, lang):
        Setting().set("language", lang)
