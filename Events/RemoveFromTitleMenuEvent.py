from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QAction, QWidget


class RemoveFromTitleMenuEvent(QEvent):
    """从标题栏菜单移除事件"""
    EventType = QEvent.registerEventType()

    def __init__(self, action: QAction):
        super().__init__(self.EventType)
        self.action = action
