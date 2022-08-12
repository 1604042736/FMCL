from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QMouseEvent, QPixmap, QImage, QResizeEvent
from PyQt5.QtCore import Qt
import requests
from Core.Mod import Mod
from Ui.Downloader.ModDetail import ModDetail
import Globals as g


class ModInfo(QWidget):
    def __init__(self, info, is_dependent=False, parent=None):
        super().__init__(parent)
        if is_dependent:
            self.info = Mod(info=info).get_mod_info()
        else:
            self.info = info

        self.l_icon = QLabel(self)

        self.l_title = QLabel(self, text=self.info['title'])
        font = self.l_title.font()
        font.setBold(True)
        self.l_title.setFont(font)

        self.l_describe = QLabel(self, text=self.info['description'])
        self.l_describe.setWordWrap(True)
        self.l_describe.setAlignment(Qt.AlignTop)

        self.load_icon()

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        self.moddetail = ModDetail(self.info)
        self.moddetail.show()

    @g.run_as_thread
    def load_icon(self):
        url = self.info["icon_url"]
        r = requests.get(url)
        image = QImage.fromData(r.content).scaled(
            self.l_icon.width(), self.l_icon.height())
        self.l_icon.setPixmap(QPixmap.fromImage(image))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.l_icon.resize(self.height(), self.height())
        self.l_icon.move(0, 0)
        self.l_title.move(4+self.height(), 0)
        self.l_title.resize(self.width()-self.height(), int(self.height()/2))
        self.l_describe.move(4+self.height(), int(self.height()/2))
        self.l_describe.resize(
            self.width()-self.height(), int(self.height()/2))
