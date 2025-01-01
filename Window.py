import typing

from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QCloseEvent, QCursor, QFont, QPainter, QPaintEvent, QColor
from PyQt5.QtWidgets import QAction, QDesktopWidget, QSizePolicy, QSpacerItem, QWidget
from qfluentwidgets import RoundMenu, qconfig, Theme
from qframelesswindow import FramelessWindow

from Events import *


class Window(FramelessWindow):
    """
    替换系统原生窗口
    保留原生窗口特性外还支持往标题栏上添加控件
    """

    def __init__(self, client: QWidget):
        super().__init__()
        self.titlemenu_actions: list[QAction] = []
        # 用来分离标题栏左右控件
        self.si_separate = QSpacerItem(
            0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.titleBar.hBoxLayout.insertSpacerItem(0, self.si_separate)
        self.titleBar.hBoxLayout.setStretch(1, 0)
        self.titleBar.hBoxLayout.setStretch(0, 1)

        # 客户区
        self.client = client
        self.client.setParent(self)
        self.client.move(0, self.titleBar.height())
        self.client.windowIconChanged.connect(self.setWindowIcon)
        self.client.windowTitleChanged.connect(self.setWindowTitle)
        self.client.installEventFilter(self)
        self.client.show()

        self.setWindowTitle(self.client.windowTitle())
        self.setWindowIcon(self.client.windowIcon())
        self.resize(self.client.width(), self.client.height() + self.titleBar.height())
        self.move(
            int((QDesktopWidget().width() - self.width()) / 2),
            int((QDesktopWidget().height() - self.height()) / 2),
        )

        self.titleBar.setObjectName("titleBar")
        self.titleBar.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.titleBar.customContextMenuRequested.connect(self.showTitleMenu)

        qconfig.themeChanged.connect(self.on_themeChanged)
        self.on_themeChanged()

        self.origin_size = self.size()

    def on_themeChanged(self):
        theme = qconfig.theme
        color = QColor(0, 0, 0) if theme == Theme.LIGHT else QColor(255, 255, 255)
        hoverbgcolor = (
            QColor(0, 0, 0, 26) if theme == Theme.LIGHT else QColor(255, 255, 255, 21)
        )
        pressedbgcolor = (
            QColor(0, 0, 0, 51) if theme == Theme.LIGHT else QColor(255, 255, 255, 51)
        )
        for button in (
            self.titleBar.minBtn,
            self.titleBar.maxBtn,
            self.titleBar.closeBtn,
        ):
            button.setNormalColor(color)
            button.setHoverColor(color)
            button.setPressedColor(color)
            if button != self.titleBar.closeBtn:
                button.setHoverBackgroundColor(hoverbgcolor)
                button.setPressedBackgroundColor(pressedbgcolor)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)
        # 绘制标题
        painter.setFont(QFont("Microsoft YaHei", 10))
        title = self.windowTitle()
        painter.drawText(
            self.si_separate.geometry(), Qt.AlignmentFlag.AlignCenter, title
        )
        return super().paintEvent(a0)

    def resizeEvent(self, e):
        self.client.resize(self.width(), self.height() - self.titleBar.height())
        return super().resizeEvent(e)

    def addTitleWidget(
        self,
        widget: QWidget,
        place: typing.Literal["right", "left"] = "left",
        index: int = 0,
    ):
        """往标题栏上添加控件"""
        self.removeTitleWidget(widget)  # 防止重复添加
        if place == "right":
            index = self.titleBar.hBoxLayout.indexOf(self.si_separate) + index + 1
        self.titleBar.hBoxLayout.insertWidget(index, widget, 0)

    def removeTitleWidget(self, widget: QWidget):
        """移除标题栏上的控件"""
        self.titleBar.hBoxLayout.removeWidget(widget)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 == self.client:
            if a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
                self.close()
            elif a1.type() == QEvent.Type.ParentChange:
                if a0.parent() != self:
                    self.close()
        return super().eventFilter(a0, a1)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.client.removeEventFilter(self)
        self.client.close()
        # 防止self.client被删除
        if self.client.parent() == self:
            self.client.setParent(None)
        # 用户添加的按钮也不删除
        for child in self.titleBar.findChildren(QWidget):
            if child not in (
                self.titleBar.minBtn,
                self.titleBar.maxBtn,
                self.titleBar.closeBtn,
            ):
                child.setParent(None)
        self.deleteLater()
        return super().closeEvent(a0)

    def showTitleMenu(self):
        """显示标题栏的右键菜单"""
        menu = RoundMenu(self)
        menu.addActions(self.titlemenu_actions)
        menu.exec(QCursor.pos())

    def event(self, a0: QEvent) -> bool:
        # 这些事件必须发送给顶层窗口
        if a0.type() == AddToTitleEvent.EventType:
            self.addTitleWidget(a0.widget, a0.place, a0.index)
        elif a0.type() == RemoveFromTitleEvent.EventType:
            self.removeTitleWidget(a0.widget)
        elif a0.type() == AddToTitleMenuEvent.EventType:
            if a0.action not in self.titlemenu_actions:
                self.titlemenu_actions.append(a0.action)
        elif a0.type() == RemoveFromTitleMenuEvent.EventType:
            if a0.action in self.titlemenu_actions:
                self.titlemenu_actions.remove(a0.action)
        elif a0.type() == QEvent.Type.Resize:
            if self.windowState() != Qt.WindowState.WindowMaximized:
                self.origin_size = self.size()
        return super().event(a0)
