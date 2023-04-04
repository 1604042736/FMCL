from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QAction, QWidget


class AddToTitleMenuEvent(QEvent):
    """添加到标题栏菜单事件"""
    EventType = QEvent.registerEventType()

    def __init__(self, action: QWidget):
        super().__init__(self.EventType)
        self.action = action
