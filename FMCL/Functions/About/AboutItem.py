from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFrame
from qfluentwidgets import PrimaryPushButton

from .ui_AboutItem import Ui_AboutItem


class AboutItem(QFrame, Ui_AboutItem):
    def __init__(
        self,
        name: str,
        description: str = "",
        icon: QPixmap = None,
        operators: tuple[tuple] = None,
    ):
        super().__init__()
        self.setupUi(self)

        self.l_name.setText(name)
        self.l_desctiption.setText(description)

        if icon:
            self.l_icon.setPixmap(icon.scaled(self.l_icon.size()))
        else:
            self.l_icon.hide()
        if operators:
            for operator in operators:
                button = PrimaryPushButton()
                button.setText(operator[1])
                button.clicked.connect(lambda _, op=operator: op[0]())
                self.hl_operators.addWidget(button)
