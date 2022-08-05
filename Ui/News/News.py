from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QAbstractItemView
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent
import Globals as g
from Core.News import News as News_
from PyQt5.QtCore import pyqtSignal, QSize
from Ui.News.NewsInfo import NewsInfo


class News(QFBNWidget):
    _NewsOut = pyqtSignal(list)
    icon_exp = 'qta.icon("fa.newspaper-o")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("新闻"))
        self.setWindowIcon(eval(self.icon_exp))
        self.page = 1

        self.lw_news = QListWidget(self)
        self.lw_news.verticalScrollBar().valueChanged.connect(self.get_more_news)

        self._NewsOut.connect(self.set_news)
        self.get_news(self.page)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.lw_news.setGeometry(0, 0, self.width(), self.height())

    @g.run_as_thread
    def get_news(self, page=1):
        news = News_().get_news(page)
        self._NewsOut.emit(news)

    def get_more_news(self, num):
        if self.lw_news.verticalScrollBar().maximum() == num:
            self.page += 1
            self.get_news(self.page)

    def set_news(self, news):
        for i in news:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, i["img_height"]))
            widget = NewsInfo(i)
            self.lw_news.addItem(item)
            self.lw_news.setItemWidget(item, widget)
