from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QMouseEvent, QPixmap, QImage
from PyQt5.QtCore import Qt
import requests
from Core.Mod import Mod
from Ui.Downloader.ModDetail import ModDetail


class ModInfo(QWidget):
    def __init__(self, info, is_dependent=False, parent=None):
        super().__init__(parent)
        if is_dependent:
            self.info = Mod(info=info).get_mod_info()
        else:
            self.info = info

        self.vbox = QVBoxLayout()

        self.l_title = QLabel(self, text=self.info['title'])
        self.l_title.setStyleSheet('font-weight: bold;')
        self.l_describe = QLabel(self, text=self.info['description'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

        self.vbox.addWidget(self.l_title)
        self.vbox.addWidget(self.l_describe)

        self.setLayout(self.vbox)

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.moddetail = ModDetail(self.info)
        self.moddetail.show()
