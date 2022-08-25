from QtFBN.QFBNWidget import QFBNWidget
from Ui.AllHelp.JoinWriteHelp import JoinWriteHelp
from Ui.AllHelp.ui_JoinTranslate import Ui_JoinTranslate
from PyQt5.QtCore import pyqtSlot

config = {
    "type": "启动器",
    "title": "参与翻译",
    "description": "参与翻译启动器中的一些文字",
    "mainclass": "JoinTranslate"
}


class JoinTranslate(QFBNWidget, Ui_JoinTranslate):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_pb_lookup_clicked(self):
        JoinWriteHelp().show()
