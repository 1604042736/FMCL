from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtCore import Qt
from Ui.Downloader.ModDetail import ModDetail


class ModInfo(QWidget):
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.info = info

        self.vbox = QVBoxLayout()

        self.l_name = QLabel(self, text=info['name'])
        self.l_name.setStyleSheet('font-weight: bold;')
        self.l_describe = QLabel(self, text=info['describe'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

        self.vbox.addWidget(self.l_name)
        self.vbox.addWidget(self.l_describe)

        self.setLayout(self.vbox)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.moddetail = ModDetail(self.info)
        self.moddetail.show()
