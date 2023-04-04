from PyQt5.QtCore import QEvent, QSize
from PyQt5.QtWidgets import QWidget


class SeparateWidgetEvent(QEvent):
    """控件分离事件"""
    EventType = QEvent.registerEventType()

    def __init__(self, widget: QWidget, size: QSize = None):
        super().__init__(self.EventType)
        self.widget = widget
        if size == None:
            size = widget.size()
        self.size = size
