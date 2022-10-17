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
        self.lw_languages.clear()
        cur_lang = Setting().get("launcher/language")

        for key, val in self.languages.items():
            item = QListWidgetItem()
            item.setText(val)
            self.lw_languages.addItem(item)

            if key == cur_lang:
                self.lw_languages.setCurrentItem(item)

    @pyqtSlot(bool)
    def on_pb_ok_clicked(self, _):
        lang = self.lw_languages.currentItem().text()
        for key, val in self.languages.items():
            if val == lang:
                Setting().set_value("launcher/language", key)
                break
