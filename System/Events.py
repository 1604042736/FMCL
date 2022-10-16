from typing import Literal

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget


class TitleWidgetEvent(QEvent):
    """对标题栏控件操作的事件"""
    Type = QEvent.registerEventType()

    def __init__(self, operation: Literal["add", "remove"],
                 widget: QWidget, place: Literal["left", "right"] = "left", index: int = 0):
        super().__init__(self.Type)
        self.__operation = operation
        self.__widget = widget
        self.__place = place
        self.__index = index

    def operation(self):
        return self.__operation

    def widget(self):
        return self.__widget

    def place(self):
        return self.__place

    def index(self):
        return self.__index


class RestoreWidgetEvent(QEvent):
    """恢复独立出来的控件的事件"""
    Type = QEvent.registerEventType()

    def __init__(self, widget: QWidget):
        super().__init__(self.Type)
        self.__widget = widget

    def widget(self):
        return self.__widget


class WidgetCaughtEvent(QEvent):
    """控件被捕获事件"""
    Type = QEvent.registerEventType()

    def __init__(self, widget: QWidget):
        super().__init__(self.Type)
        self.__widget = widget

    def widget(self):
        return self.__widget
