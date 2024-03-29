import minecraft_launcher_lib as mll
import multitasking
import qtawesome as qta

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QWidget, qApp
from qfluentwidgets import StateToolTip

from .NewsInfo import NewsInfo
from .ui_News import Ui_News


class News(QWidget, Ui_News):
    __NewsGot = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.newspaper-o"))
        self.__NewsGot.connect(self.setNewsInfo)

        self.max_col = 0
        self.cur_row = self.cur_col = 0
        self.newsinfo = []
        self.page_size = 20
        self.getNews()

    @multitasking.task
    def getNews(self):
        r = mll.utils.get_minecraft_news(self.page_size)
        self.__NewsGot.emit(r["article_grid"])

    def setNewsInfo(self, news):
        statetooltip = StateToolTip(self.tr("正在加载新闻"), "", self)
        statetooltip.move(statetooltip.getSuitablePos())
        statetooltip.show()

        n = len(news)
        for i, info in enumerate(news):
            widget = NewsInfo(info)
            widget.setFixedSize(widget.size())
            if widget not in self.newsinfo:
                self.newsinfo.append(widget)
                self.addWidget(widget)
            statetooltip.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        statetooltip.setContent(self.tr("加载完成"))
        statetooltip.setState(True)

    def addWidget(self, widget: QWidget):
        self.gl_news.addWidget(widget, self.cur_row, self.cur_col)
        self.cur_col += 1
        if self.cur_col == self.max_col:
            self.cur_row += 1
            self.cur_col = 0

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.cur_col = self.cur_row = 0
        self.max_col = self.width() // 256
        for newsinfo in self.newsinfo:
            self.addWidget(newsinfo)
        return super().resizeEvent(a0)

    @pyqtSlot(bool)
    def on_pb_loadmore_clicked(self, _):
        self.page_size *= 2
        self.getNews()
