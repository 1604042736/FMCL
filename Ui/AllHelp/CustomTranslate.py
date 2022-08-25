from QtFBN.QFBNWidget import QFBNWidget
from Ui.AllHelp.ui_CustomTranslate import Ui_CustomTranslate

config = {
    "type": "个性化",
    "title": "自定义翻译",
    "description": "创建新的翻译或拓展原有翻译",
    "mainclass": "CustomTranslate"
}


class CustomTranslate(QFBNWidget, Ui_CustomTranslate):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
