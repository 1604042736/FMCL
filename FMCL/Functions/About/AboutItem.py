from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame

from .ui_AboutItem import Ui_AboutItem


class AboutItem(QFrame, Ui_AboutItem):
    def __init__(self, name: str, description: str = "", icon: QPixmap = None, operator: tuple = None):
        super().__init__()
        self.setupUi(self)

        self.l_name.setText(name)
        self.l_desctiption.setText(description)

        if icon:
            self.l_icon.setPixmap(icon.scaled(self.l_icon.size()))
        else:
            self.l_icon.hide()
        if operator:
            self.pb_operator.clicked.connect(lambda: operator[0]())
            self.pb_operator.setText(operator[1])
        else:
            self.pb_operator.hide()
