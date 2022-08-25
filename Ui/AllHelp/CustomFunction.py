from QtFBN.QFBNWidget import QFBNWidget
from Ui.AllHelp.ui_CustomFunction import Ui_CustomFunction

config = {
    "type": "个性化",
    "title": "自定义功能",
    "description": "自定义启动器的功能",
    "mainclass": "CustomFunction"
}


class CustomFunction(QFBNWidget, Ui_CustomFunction):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
