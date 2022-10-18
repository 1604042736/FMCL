import qtawesome as qta
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QListWidgetItem, QWidget
from System import Setting

from .ui_LanguageChooser import Ui_LanguageChooser


class LanguageChooser(QWidget, Ui_LanguageChooser):
    languages = {
        ":/zh_CN.qm": '简体中文',
        ":/en.qm": "English"
    }

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.language"))
        self.refresh()

    def refresh(self):
        self.cb_lang.clear()
        cur_lang = Setting().get("launcher.language")
        self.cb_lang.addItem(self.languages[cur_lang])
        for key, val in self.languages.items():
            if key != cur_lang:
                self.cb_lang.addItem(val)

    @pyqtSlot(str)
    def on_cb_lang_currentTextChanged(self, lang):
        for key, val in self.languages.items():
            if val == lang:
                Setting().set("launcher.language", key)
                break
