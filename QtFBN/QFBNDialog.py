from QtFBN.QFBNWidget import QFBNWidget
from PyQt5.QtWidgets import QWidget, QPushButton, QFrame, QLabel
from PyQt5.QtGui import QResizeEvent, QPaintEvent, QPainter, QColor, QPen
import qtawesome as qta
from PyQt5.QtCore import QSize, Qt

from QtFBN.QFBNWindow import QFBNWindow
from QtFBN.QFBNWindowManager import QFBNWindowManager


class QFBNDialog(QFBNWidget):
    BUTTON_WIDTH = 45
    BUTTON_HEIGHT = 30

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        while (parent.parentWidget() != None
               and not isinstance(parent.parentWidget(), QFBNWindowManager)
                and not isinstance(parent.parentWidget(), QFBNWindow)):
            parent = parent.parentWidget()
        self.setParent(parent)
        self._default_size = [0, 0]

        self._cover = QWidget(parent)  # 用一个QWidget将父窗口遮住,阻止用户交互
        self._cover.show()

        self._f_title = QFrame(parent)
        self._f_title.setObjectName("f_title")
        self._f_title.show()

        self._pb_close = QPushButton(self._f_title)
        self._pb_close.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self._pb_close.setIcon(qta.icon("mdi6.close"))
        self._pb_close.setObjectName("pb_close")
        self._pb_close.clicked.connect(self.close)
        self._pb_close.setIconSize(
            QSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        self._pb_close.show()

        self._pb_sepwin = QPushButton(self._f_title)
        self._pb_sepwin.resize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self._pb_sepwin.setObjectName('pb_sepwin')
        self._pb_sepwin.setIcon(qta.icon('ph.arrow-square-out-light'))
        self._pb_sepwin.setIconSize(
            QSize(self.BUTTON_WIDTH, self.BUTTON_HEIGHT))
        self._pb_sepwin.clicked.connect(lambda: self.show("separate"))
        self._pb_sepwin.show()

        self._l_title = QLabel(self._f_title)
        self._l_title.setText(self.windowTitle())
        self._l_title.move(0, 0)
        self._l_title.show()

        self.parent_resizeEvent = None
        self.parent_widget_to_self = None

        if not isinstance(parent, QFBNWindow):
            # 保存父窗口的方法,并设置成自己的方法
            self.parent_resizeEvent = parent.resizeEvent
            parent.resizeEvent = self.resizeEvent

            if hasattr(parent, "widget_to_self"):
                self.parent_widget_to_self = parent.widget_to_self
            parent.widget_to_self = self.widget_to_self

        self._f_title.raise_()
        self.raise_()

    def recovery(self):
        """恢复"""
        self._cover.hide()
        self._pb_close.hide()
        self._pb_sepwin.hide()
        self._l_title.hide()
        self._f_title.hide()
        self.parent().resizeEvent = self.parent_resizeEvent

    def close(self) -> bool:
        self.recovery()
        self.parent().widget_to_self = self.parent_widget_to_self
        return super().close()

    def show(self, mode="default") -> None:
        if mode != 'original':
            self.recovery()
        return super().show(mode)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        if self.parent_resizeEvent != None:
            self.parent_resizeEvent(a0)
        if isinstance(self.parentWidget(), QFBNWindow):
            return

        self.move(int((self.parentWidget().width()-self.width())/2),
                  int((self.parentWidget().height()-self.height())/2))
        self._cover.setGeometry(0, 0, self.parentWidget().width(),
                                self.parentWidget().height())

        self._f_title.resize(self.width(), self.BUTTON_HEIGHT)
        self._f_title.move(self.x(), self.y()-self._f_title.height())
        self._pb_close.move(self._f_title.width()-self.BUTTON_WIDTH, 0)
        self._pb_sepwin.move(self._f_title.width()-self.BUTTON_WIDTH*2, 0)
        self._l_title.resize(self._f_title.width() -
                             self.BUTTON_WIDTH*2, self._f_title.height())

        if not isinstance(self.parentWidget(), QFBNWindow):
            self._default_size = [self.width(), self.height()]

    def widget_to_self(self, w) -> None:
        if self.parent_widget_to_self != None:
            self.parent_widget_to_self(w)

        self._cover.show()
        self._pb_close.show()
        self._pb_sepwin.show()
        self._l_title.show()
        self._f_title.show()

        self.parent_resizeEvent = self.parent().resizeEvent
        self.parent().resizeEvent = self.resizeEvent

        self.resize(*self._default_size)

    def setWindowTitle(self, a0: str) -> None:
        self._l_title.setText(a0)
        return super().setWindowTitle(a0)

    def paintEvent(self, a0: QPaintEvent) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QPen(Qt.black, 2, Qt.NoPen))
        qp.setBrush(QColor(240, 240, 240))
        qp.drawRect(0, 0, self.width(), self.height())
        qp.end()
