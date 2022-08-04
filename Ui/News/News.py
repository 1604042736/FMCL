from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QAbstractItemView
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent
import Globals as g
from Core.News import News as News_
from PyQt5.QtCore import pyqtSignal, QSize
from Ui.News.NewsInfo import NewsInfo


class News(QListWidget, QFBNWidget):
    _NewsOut = pyqtSignal()
    icon_exp = 'qta.icon("fa.newspaper-o")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("新闻"))
        self.setWindowIcon(eval(self.icon_exp))

        self._NewsOut.connect(self.set_news)
        self.news = []
        self.get_news()

    @g.run_as_thread
    def get_news(self):
        self.news = News_().get_news()
        self._NewsOut.emit()

    def set_news(self):
        self.clear()

        for i in self.news:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 128))
            widget = NewsInfo(i)
            self.addItem(item)
            self.setItemWidget(item, widget)
