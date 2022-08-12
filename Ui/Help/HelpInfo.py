from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QResizeEvent


class HelpInfo(QWidget):
    def __init__(self, module, parent=None) -> None:
        super().__init__(parent)
        self.module = module
        self.config = module.config

        self.vbox = QVBoxLayout(self)

        self.l_title = QLabel(self, text=self.config['title'])
        font = self.l_title.font()
        font.setBold(True)
        self.l_title.setFont(font)

        self.l_describe = QLabel(self, text=self.config['description'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

        self.vbox.addWidget(self.l_title)
        self.vbox.addWidget(self.l_describe)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        widget = getattr(self.module, self.config["mainclass"])()
        widget.show()
