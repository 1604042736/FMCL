from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget


class WindowActivatedEvent(QEvent):
    """窗口被激活"""

    EventType = QEvent.registerEventType()

    def __init__(self, widget: QWidget):
        super().__init__(self.EventType)
        self.widget = widget
