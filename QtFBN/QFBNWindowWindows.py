from QtFBN.QFBNWindowBasic import QFBNWindowBasic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QPushButton, QDesktopWidget, QWidget, QLabel
from PyQt5.QtGui import QMoveEvent, QFontMetrics
from win32con import *
from win32gui import *
from ctypes.wintypes import *
import qtawesome as qta


class QFBNWindowWindows(QFBNWindowBasic):
    """适用于Windows系统的QFBNWindow"""

    TOP_DISTANCE = 4  # 上边框距离
    BOTTOM_DISTANCE = 4  # 下边框距离
    LEFT_DISTANCE = 4  # 左边框距离
    RIGHT_DISTANCE = 4  # 右边框距离
    y_shift = 0  # 偏移,最大化后不能用原来的坐标

    def __init__(self, target) -> None:
        super().__init__(target)

        '''
        if self.target.parent() != None:
            self.resize(self.target.width(),
                        self.target.height()+self.title_height)
        else:
            self.resize(self.target.width(), self.target.height())
        '''
        self.target.setParent(self)

        self.set_windowstyle()

        self.setWindowTitle(self.target.windowTitle())
        QWidget.show(self.target)

    def set_windowstyle(self) -> None:
        """设置窗口样式"""
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint)  # 不设置会导致窗口大小不正确
        hwnd = self.winId()
        style = GetWindowLong(hwnd, GWL_STYLE)
        SetWindowLong(hwnd, GWL_STYLE, style | WS_MAXIMIZEBOX |
                      WS_THICKFRAME | WS_CAPTION)

    def set_title(self) -> None:
        self.pb_close = QPushButton(self.title)
        self.pb_close.resize(self.title_button_width, self.title_height)
        self.pb_close.setObjectName('pb_close')
        self.pb_close.setIcon(qta.icon('mdi6.close'))

        self.pb_maxnormal = QPushButton(self.title)
        self.pb_maxnormal.resize(self.title_button_width, self.title_height)
        self.pb_maxnormal.setObjectName('pb_maxnormal')
        self.pb_maxnormal.setIcon(qta.icon('mdi.square-outline'))
        self.pb_maxnormal.setIconSize(QSize(16, 16))

        self.pb_min = QPushButton(self.title)
        self.pb_min.resize(self.title_button_width, self.title_height)
        self.pb_min.setObjectName('pb_min')
        self.pb_min.setIcon(qta.icon('mdi.minus'))

        self.l_title = QLabel(self.title, text=self.target.windowTitle())
        self.l_title.resize(128, self.title_height)

        self.add_right_widget(self.pb_close)
        self.add_right_widget(self.pb_maxnormal, set_icon_size=False)
        self.add_right_widget(self.pb_min)

        return super().set_title()

    def set_connection(self) -> None:
        self.pb_close.clicked.connect(self.close)
        self.pb_maxnormal.clicked.connect(self.change_show_state)
        self.pb_min.clicked.connect(self.showMinimized)
        return super().set_connection()

    def change_show_state(self) -> None:
        """改变显示状态"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def setWindowTitle(self, a0: str) -> None:
        self.l_title.setText(a0)
        font = self.l_title.font()
        fontm = QFontMetrics(font)
        self.l_title.resize(fontm.width(a0), self.title_height)
        self.wintitle_width = fontm.width(a0)
        self.resize_title_widgets()
        return super().setWindowTitle(a0)

    def showMaximized(self) -> None:
        self.pb_maxnormal.setIcon(qta.icon('mdi6.window-restore'))
        return super().showMaximized()

    def showNormal(self) -> None:
        self.pb_maxnormal.setIcon(qta.icon('mdi.square-outline'))
        return super().showNormal()

    def resizeEvent(self, a0) -> None:
        self.target.resize(self.width(), self.height()-self.title_height)
        self.target.move(0, self.title_height)
        self.title.resize(self.width(), self.title_height)
        self.resize_title_widgets()
        super().resizeEvent(a0)

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

    def resize_title_widgets(self) -> None:
        super().resize_title_widgets()
        self.l_title.move(int(
            (self.title.width()-self.left_width-self.right_width-self.l_title.width())/2+self.left_width), 0)
