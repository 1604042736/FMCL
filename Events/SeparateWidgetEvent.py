from PyQt5.QtCore import QEvent, QSize
from PyQt5.QtWidgets import QWidget

from Window import Window


class SeparateWidgetEvent(QEvent):
    """控件分离事件"""

    EventType = QEvent.registerEventType()

    def __init__(self, widget: QWidget, size: QSize = None):
        """如果size为None, 那么widget分离后的大小将自动设置"""
        super().__init__(self.EventType)
        self.widget = widget
        if size == None:
            if isinstance(widget.window(), Window):
                window: Window = widget.window()
                size = QSize(
                    window.origin_size.width(),
                    window.origin_size.height() - window.titleBar.height(),
                )
            else:
                size = widget.size()
        self.size = size
