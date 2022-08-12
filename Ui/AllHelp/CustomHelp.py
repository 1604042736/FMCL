from QtFBN.QFBNWidget import QFBNWidget
from Ui.AllHelp.JoinWriteHelp import JoinWriteHelp
from Ui.AllHelp.ui_CustomHelp import Ui_CustomHelp
from PyQt5.QtCore import pyqtSlot

config = {
    "type": "个性化",
    "title": "自定义帮助",
    "description": "创建属于你的帮助界面",
    "mainclass": "CustomHelp"
}


class CustomHelp(QFBNWidget, Ui_CustomHelp):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_pb_lookup_clicked(self, _):
        JoinWriteHelp().show()
