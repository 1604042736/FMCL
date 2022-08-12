from QtFBN.QFBNWidget import QFBNWidget
from Ui.AllHelp.ui_JoinWriteHelp import Ui_JoinWriteHelp

config = {
    "type": "启动器",
    "title": "参与完善帮助",
    "description": "帮忙完善帮助界面",
    "mainclass": "JoinWriteHelp"
}


class JoinWriteHelp(QFBNWidget, Ui_JoinWriteHelp):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
