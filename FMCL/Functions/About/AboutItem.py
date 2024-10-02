from PyQt5.QtGui import QPixmap
from qfluentwidgets import PrimaryPushButton, CardWidget

from .ui_AboutItem import Ui_AboutItem


class AboutItem(CardWidget, Ui_AboutItem):
    def __init__(
        self,
        name: str,
        description: str = "",
        icon: QPixmap = None,
        operators: tuple[dict] = None,
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
                button.setText(operator["name"])
                button.clicked.connect(lambda _, op=operator: op["action"]())
                self.hl_operators.addWidget(button)
