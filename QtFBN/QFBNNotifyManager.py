from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtCore import QTimer, QTimerEvent


class QFBNNotifyManager(QWidget):
    """显示通知的管理器"""
    RIGHT = 0  # 与右边的距离
    BOTTOM = 16  # 与底部的距离

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.wait_time = 5000  # 等待时间
        self.display_time = 100

        self.notices: list[QLabel] = []  # 所有的通知
        self.notice_timers: list[tuple[int, QLabel]] = []

        self.timer_update = self.startTimer(self.wait_time)

    def notify(self, title, msg):
        """新通知"""
        text = f"{title}:{msg}"
        label = QLabel(self)
        font = label.font()
        font.setPointSize(13)
        fontm = QFontMetrics(font)
        label.setFont(font)
        label.setObjectName("l_notice")
        label.setText(text)
        label.resize(fontm.width(text), fontm.height())

        timer = self.startTimer(self.wait_time)
        self.notice_timers.append((timer, label))

        self.notices.append(label)

        self.update_geometry()

    def update_geometry(self) -> None:
        """更新位置和大小"""
        if not self.notices:
            return
        width = max([i.width() for i in self.notices])  # 最大的宽度
        height = sum([i.height() for i in self.notices])  # 高度之和
        self.resize(width, height)

        widget = self.parentWidget()
        self.move(widget.width()-self.RIGHT-width,
                  widget.height()-height-self.BOTTOM)

        l = 0
        for i in self.notices:
            i.show()
            l += i.height()
            i.move(width-i.width(), height-l)

        self.raise_()

    def timerEvent(self, a0: QTimerEvent) -> None:
        if a0.timerId() == self.timer_update:
            self.update_geometry()
        else:
            for i in self.notice_timers:
                if i[0] == a0.timerId():  # 移除已过时的notice
                    self.notice_timers.remove(i)
                    i[1].hide()
                    i[1].deleteLater()
                    self.notices.remove(i[1])
                    self.killTimer(i[0])
                    self.update_geometry()
                    if not self.notices:
                        self.hide()
                    break
