from PyQt5.QtWidgets import QWidget

from .ui_ResItem import Ui_ResItem


class ResItem(QWidget, Ui_ResItem):
    def __init__(self, res) -> None:
        super().__init__()
        self.setupUi(self)
        self.res = res
