import webbrowser

import multitasking
from Core import Network
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QImage, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget

from .ui_NewsInfo import Ui_NewsInfo


class NewsInfo(QWidget, Ui_NewsInfo):
    __instances = {}
    __new_count = {}

    def __new__(cls, info):
        if info["article_url"] not in cls.__instances:
            cls.__instances[info["article_url"]] = super().__new__(cls)
            cls.__new_count[info["article_url"]] = 0
        cls.__new_count[info["article_url"]] += 1
        return cls.__instances[info["article_url"]]

    def __init__(self, info):
        if self.__new_count[info["article_url"]] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.info = info

        self.l_title = QLabel()
        self.l_title.setText(self.info["default_tile"]["title"])
        self.l_title.setStyleSheet(
            """
QLabel{
    color:rgb(255,255,255);
    background-color:rgba(0,0,0,128);
}
"""
        )
        font = QFont("微软雅黑", 10)
        font.setBold(True)
        self.l_title.setFont(font)
        self.l_title.setWordWrap(True)
        self.l_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.l_subheader = QLabel()
        self.l_subheader.setText(self.info["default_tile"]["sub_header"])
        font.setBold(False)
        self.l_subheader.setFont(font)
        self.l_subheader.setStyleSheet(self.l_title.styleSheet())
        self.l_subheader.setWordWrap(True)
        self.l_subheader.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.l_subheader.show()

        self.w_caption = QWidget(self)
        self.gl_caption = QGridLayout(self.w_caption)
        self.gl_caption.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.gl_caption.setContentsMargins(0, 0, 0, 0)
        self.gl_caption.setSpacing(0)
        self.gl_caption.addWidget(self.l_title)
        self.gl_caption.addWidget(self.l_subheader)

        self.getImage()

    @multitasking.task
    def getImage(self):
        url = (
            f'https://www.minecraft.net{self.info["default_tile"]["image"]["imageURL"]}'
        )
        r = Network().get(url)
        # TODO failed minimal tag size sanity
        pixmap = QPixmap.fromImage(QImage.fromData(r.content))
        self.l_image.setPixmap(
            pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
        )

    def resizeEvent(self, a0: QResizeEvent) -> None:
        w_caption_height = 0
        for i in (self.l_title, self.l_subheader):
            font = i.font()
            fontm = QFontMetrics(font)
            w_caption_height += (
                fontm.width(i.text()) // i.width() + 1
            ) * fontm.height()
        self.w_caption.resize(self.width(), w_caption_height)
        self.w_caption.move(self.l_image.x(), self.height() - self.w_caption.height())
        return super().resizeEvent(a0)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Enter:
            self.l_subheader.show()
            self.resizeEvent(None)
        elif a0.type() == QEvent.Type.Leave:
            self.l_subheader.hide()
            self.resizeEvent(None)
        elif a0.type() == QEvent.Type.MouseButtonRelease:
            webbrowser.open(f'https://www.minecraft.net{self.info["article_url"]}')
        return super().event(a0)
