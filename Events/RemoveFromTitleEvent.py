from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget


class RemoveFromTitleEvent(QEvent):
    """从标题栏移除事件"""
    EventType = QEvent.registerEventType()

    def __init__(self, widget: QWidget):
        super().__init__(self.EventType)
        self.widget = widget
