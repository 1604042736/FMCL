from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QResizeEvent, QFontMetrics, QImage, QMovie, QPixmap, QMouseEvent
from PyQt5.QtCore import Qt, QByteArray, QBuffer, QIODevice
import requests
import Globals as g
from Ui.News.NewsDetail import NewsDetail


class NewsInfo(QWidget):
    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.info = info

        self.l_img = QLabel(self)

        self.l_title = QLabel(self, text=info["title"])
        font = self.l_title.font()
        font.setPixelSize(16)
        font.setBold(True)
        self.l_title.setFont(font)
        self.l_title.setWordWrap(True)

        self.l_description = QLabel(self, text=info["description"])
        font = self.l_description.font()
        font.setPixelSize(16)
        self.l_description.setFont(font)
        self.l_description.setWordWrap(True)
        self.l_description.setAlignment(Qt.AlignTop)

        self.load_img()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.l_img.move(0, 0)
        self.l_img.resize(self.info["img_width"], self.height())

        self.l_title.move(self.l_img.width(), 0)
        font = self.l_title.font()
        fontm = QFontMetrics(font)
        self.l_title.resize(self.width()-self.l_img.width(), fontm.height())

        self.l_description.move(self.l_img.width(), self.l_title.height())
        self.l_description.resize(
            self.width()-self.l_img.width(), self.height()-self.l_title.height())

    @g.run_as_thread
    def load_img(self):
        url = self.info["article_img_url"]
        g.logapi.info(f"{url=}")
        r = requests.get(url)
        if "error" in r.text:
            return
        if ".gif" in url and False:
            a = QByteArray(r.content)
            b = QBuffer(a)
            b.open(QIODevice.OpenModeFlag.ReadOnly)
            self.l_img.setMovie(QMovie(b))
        else:
            pixmap = QPixmap.fromImage(QImage.fromData(r.content))
            self.l_img.setPixmap(pixmap.scaled(
                self.l_img.width(), self.l_img.height()))

    def mouseDoubleClickEvent(self, a0: QMouseEvent) -> None:
        newsdetail = NewsDetail(self.info)
        newsdetail.show()
