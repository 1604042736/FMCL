import qtawesome as qta
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QWidget
from Setting import Setting
from Kernel import Kernel
from .ui_LanguageChooser import Ui_LanguageChooser

_translate = Kernel.translate


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

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        filename = QFileDialog.getOpenFileName(self,
                                               _translate("选择翻译文件"),
                                               filter="Qt Translation Files (*.qm)")[0]
        if filename:
            self.languages[filename] = filename
            self.refresh()
