from typing import Literal

import qtawesome as qta
from PyQt5.QtCore import (QEvent, QMetaObject, QObject, QPoint, QSize, Qt,
                          pyqtSlot)
from PyQt5.QtGui import QCloseEvent, QFont, QPainter, QPaintEvent
from PyQt5.QtWidgets import (QAction, QDesktopWidget, QMenu, QPushButton,
                             QSizePolicy, QSpacerItem, QStackedWidget, QWidget,
                             qApp)
from qframelesswindow import FramelessWindow

from .Constants import *
from .Events import *


class Window(FramelessWindow):
    """用于替代系统窗口"""

    def __init__(self, client: QWidget):
        super().__init__()
        # 用来分离标题栏左右控件
        self.si_separate = QSpacerItem(40, 20,
                                       QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.titleBar.hBoxLayout.insertSpacerItem(0, self.si_separate)

        self.separable_widgets: list[QWidget] = []  # 可分离的控件

        self.pb_sep = QPushButton()
        self.pb_sep.resize(W_D_TITLEBUTTON, self.titleBar.height())
        self.pb_sep.setIcon(qta.icon("ph.arrow-square-out-light"))
        self.pb_sep.setStyleSheet(S_D_TITLEBUTTON)
        self.pb_sep.hide()
        self.pb_sep.clicked.connect(self.separateWidget)
        self.addTitleWidget(self.pb_sep, "right")

        self.client_parent = client.parent()
        if self.client_parent != None:
            self.pb_restore = QPushButton()
            self.pb_restore.setObjectName("pb_restore")
            self.pb_restore.resize(W_D_TITLEBUTTON, self.titleBar.height())
            self.pb_restore.setIcon(qta.icon("msc.reply"))
            self.pb_restore.setStyleSheet(S_D_TITLEBUTTON)
            self.addTitleWidget(self.pb_restore, "right")

            self.pb_parent = QPushButton()
            self.pb_parent.setObjectName("pb_parent")
            self.pb_parent.resize(W_D_TITLEBUTTON, self.titleBar.height())
            self.pb_parent.setIcon(qta.icon("msc.window"))
            self.pb_parent.setStyleSheet(S_D_TITLEBUTTON)
            self.addTitleWidget(self.pb_parent, "right")

        # 客户区
        self.client = client
        self.client.setParent(self)
        self.client.move(0, self.titleBar.height())
        self.client.installEventFilter(self)
        self.client.show()

        self.setWindowTitle(self.client.windowTitle())
        self.setWindowIcon(self.client.windowIcon())
        self.resize(self.client.width(),
                    self.client.height() + self.titleBar.height())
        self.move(int((QDesktopWidget().width()-self.width())/2),
                  int((QDesktopWidget().height()-self.height())/2))

        self.titleBar.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.titleBar.customContextMenuRequested.connect(self.showTitleMenu)

        QMetaObject.connectSlotsByName(self)

    def paintEvent(self, a0: QPaintEvent) -> None:
        painter = QPainter(self)

        # 绘制标题
        painter.setFont(QFont("Microsoft YaHei", 10))
        title = self.windowTitle()
        painter.drawText(self.si_separate.geometry(),
                         Qt.AlignmentFlag.AlignCenter, title)

        return super().paintEvent(a0)

    def resizeEvent(self, e):
        self.client.resize(self.width(), self.height()-self.titleBar.height())
        return super().resizeEvent(e)

    def addTitleWidget(self, widget: QWidget, place: Literal["right", "left"] = "left", index: int = 0):
        """往标题栏上添加控件"""
        self.removeTitleWidget(widget)  # 防止重复添加
        widget.setFixedSize(QSize(widget.width(), self.titleBar.height()))
        if place == "right":
            index = self.titleBar.hBoxLayout.indexOf(self.si_separate)+index+1
        self.titleBar.hBoxLayout.insertWidget(index, widget)

    def removeTitleWidget(self, widget: QWidget):
        """移除标题栏上的控件"""
        self.titleBar.hBoxLayout.removeWidget(widget)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == TitleWidgetEvent.Type:
            operation = a0.operation()
            widget = a0.widget()
            if operation == "add":
                place = a0.place()
                index = a0.index()
                self.addTitleWidget(widget, place, index)
            elif operation == "remove":
                self.removeTitleWidget(widget)
        return super().event(a0)

    @pyqtSlot(bool)
    def on_pb_restore_clicked(self, _):
        from .Application import Application
        # 先使用parent有的方法
        if qApp.sendEvent(self.client_parent, RestoreWidgetEvent(self.client)):
            if isinstance(self.client_parent, QStackedWidget):  # 特殊
                self.client_parent.addWidget(self.client)
        Application.activateWidget(self.client_parent)

    @pyqtSlot(bool)
    def on_pb_parent_clicked(self, _):
        from .Application import Application
        Application.activateWidget(self.client_parent)

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 == self.client:
            if a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
                self.close()
            elif a1.type() == QEvent.Type.ParentChange:
                if a0.parent() != self:
                    self.close()
            elif a1.type() not in (QEvent.Type.Paint,):
                self.separable_widgets = list(
                    self.findSeparableWidgets(self.client))
                if self.separable_widgets:
                    self.pb_sep.show()
                else:
                    self.pb_sep.hide()
            elif a1.type() == QEvent.Type.WindowTitleChange:
                self.setWindowTitle(a0.windowTitle())
                self.repaint()
            elif a1.type() == QEvent.Type.WindowIconChange:
                self.setWindowIcon(a0.windowIcon())
        return super().eventFilter(a0, a1)

    def findSeparableWidgets(self, widget: QWidget) -> set[QWidget]:
        """查找可以分离的控件"""
        result = set()
        if isinstance(widget, QStackedWidget):
            widget = widget.currentWidget()
            # QStackedWidget.currentWidget默认可以分离
            if widget != None and not (hasattr(widget, "separable") and not widget.separable):
                result.add(widget)
        if widget == None:
            return result
        children = widget.findChildren(QWidget)
        for child in children:
            # separable为True的QWidget可以分离
            if hasattr(child, "separable") and child.separable:
                result.add(child)
            result |= self.findSeparableWidgets(child)
        return result

    def separateWidget(self):
        """分离控件"""
        from .Application import Application
        if len(self.separable_widgets) == 1:
            Application.showWidget(self.separable_widgets[0])
        elif len(self.separable_widgets) > 1:
            menu = QMenu(self)
            for widget in self.separable_widgets:
                action = QAction(self)
                action.setText(widget.windowTitle())
                action.setIcon(widget.windowIcon())
                action.triggered.connect(
                    lambda _, w=widget: Application.showWidget(w))
                menu.addAction(action)
            menu.exec(self.pb_sep.mapToGlobal(QPoint(0, self.pb_sep.height())))

    def showTitleMenu(self):
        """显示标题栏的右键菜单"""
        if hasattr(self.client, "showTitleMenu"):
            self.client.showTitleMenu()

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.client.removeEventFilter(self)
        self.client.close()
        # self可以删除但self.client不可以
        if self.client.parent() == self:
            self.client.setParent(None)
        # 用户添加的按钮也不删除
        for child in self.titleBar.findChildren(QWidget):
            if child not in (self.pb_sep, self.titleBar.minBtn, self.titleBar.maxBtn, self.titleBar.closeBtn):
                if self.client_parent != None:
                    if child not in (self.pb_parent, self.pb_restore):
                        child.setParent(None)
                else:
                    child.setParent(None)
        self.deleteLater()
        return super().closeEvent(a0)
