from QtFBN.QFBNWindowBasic import QFBNWindowBasic
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import QMoveEvent
from win32con import *
from win32gui import *
from ctypes.wintypes import *
import qtawesome as qta


class QFBNWindowWindows(QFBNWindowBasic):
    """适用于Windows系统的QFBNWindow"""

    y_shift = 0  # 偏移,最大化后不能用原来的坐标

    def set_windowstyle(self) -> None:
        """设置窗口样式"""
        super().set_windowstyle()

        hwnd = self.winId()
        style = GetWindowLong(hwnd, GWL_STYLE)
        SetWindowLong(hwnd, GWL_STYLE, style | WS_MAXIMIZEBOX |
                      WS_THICKFRAME | WS_CAPTION)

    def moveEvent(self, event: QMoveEvent) -> None:
        pos = event.pos()
        try:
            if pos.x() < 0 and pos.y() < 0:  # 防止超出屏幕(一般发生在最大化的时侯)
                # 桌面的宽高,也就是窗口最大化时的宽高
                width = QDesktopWidget().availableGeometry().width()
                height = QDesktopWidget().availableGeometry().height()
                if self.width() >= width and self.height() >= height:
                    self.pb_maxnormal.setIcon(qta.icon('mdi6.window-restore'))
                    # 得到偏移的大小
                    x = 0-pos.x() if pos.x() < 0 else 0
                    y = 0-pos.y() if pos.y() < 0 else 0
                    self.y_shift = y
                    # moveEvent比resizeEvent晚发出,所以不会影响
                    self.target.move(x, y+self.title_height)
                    self.target.resize(width, height-self.title_height)
                    self.title.move(x, y)
                    self.title.resize(width, self.title_height)
                    self.resize_title_widgets()
            else:
                self.pb_maxnormal.setIcon(qta.icon('mdi.square-outline'))
                self.y_shift = 0
                self.title.move(0, 0)
                self.resizeEvent(None)
        except AttributeError:
            pass

    def GET_X_LPARAM(self, param: int) -> int:
        return param & 0xffff

    def GET_Y_LPARAM(self, param: int) -> int:
        return param >> 16

    def nativeEvent(self, eventType, message):
        if self.parent():  # 作为子窗口时不处理
            return False, 0
        msg = MSG.from_address(message.__int__())
        if msg.message == WM_NCCALCSIZE:
            return True, 0
        elif msg.message == WM_NCHITTEST:
            xPos = self.GET_X_LPARAM(msg.lParam) - self.frameGeometry().x()
            yPos = self.GET_Y_LPARAM(msg.lParam) - self.frameGeometry().y()
            right = self.width()-self.RIGHT_DISTANCE
            bottom = self.height()-self.BOTTOM_DISTANCE
            if (self.TOP_DISTANCE < yPos < self.title_height+self.y_shift
                    and self.LEFT_DISTANCE+self.left_width < xPos < right-self.right_width
                ):  # 使标题栏上的按钮可点击
                return True, HTCAPTION
            if xPos <= self.LEFT_DISTANCE and yPos <= self.TOP_DISTANCE:
                return True, HTTOPLEFT
            elif xPos >= right and yPos <= self.TOP_DISTANCE:
                return True, HTTOPRIGHT
            elif yPos >= bottom and xPos <= self.LEFT_DISTANCE:
                return True, HTBOTTOMLEFT
            elif yPos >= bottom and xPos >= right:
                return True, HTBOTTOMRIGHT
            elif yPos <= self.TOP_DISTANCE:
                return True, HTTOP
            elif xPos <= self.LEFT_DISTANCE:
                return True, HTLEFT
            elif xPos >= right:
                return True, HTRIGHT
            elif yPos >= bottom:
                return True, HTBOTTOM
        return super().nativeEvent(eventType, message)
