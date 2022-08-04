from QtFBN.QFBNWindowBasic import QFBNWindowBasic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QMouseEvent


class QFBNWindowDefault(QFBNWindowBasic):
    """
    适用所有系统的QFBNWindow
    不支持调整窗口大小
    """

    def __init__(self, target) -> None:
        super().__init__(target)
        self.mousepos = []
        self.flags = {
            "move": False,
            "right": False,
            "left": False,
            "top": False,
            "bottom": False,
            "top-left": False,
            "top-right": False,
            "bottom-left": False,
            "bottom-right": False
        }
        self.setMouseTracking(True)

    def show(self) -> None:
        # self.set_all_mousetrack(self.title)
        super().show()

    def set_all_mousetrack(self, w):
        '''将所有控件设置为鼠标跟踪'''
        children = w.findChildren(QWidget)
        for child in children:
            child.setMouseTracking(True)
            child.mouseMoveEvent = self.mouseMoveEvent
            # 直接赋值会导致子控件部分功能无法使用
            # 比如按钮无法点击
            child.mousePressEvent = lambda a, child=child.mousePressEvent: self.mousePressEvent(
                a, child)
            child.mouseReleaseEvent = lambda a, child=child.mouseReleaseEvent: self.mouseReleaseEvent(
                a, child)
            self.set_all_mousetrack(child)

    def mousePressEvent(self, a0: QMouseEvent, child_event=None) -> None:
        x = a0.globalX()-self.x()
        y = a0.globalY()-self.y()

        if x <= self.LEFT_DISTANCE and y <= self.TOP_DISTANCE:  # 左上角
            self.flags["top-left"] = True
        elif x >= self.width()-self.RIGHT_DISTANCE and y >= self.height()-self.BOTTOM_DISTANCE:  # 右下角
            self.flags["bottom-right"] = True
        elif x >= self.width()-self.RIGHT_DISTANCE and y <= self.TOP_DISTANCE:  # 右上角
            self.flags["top-right"] = True
        elif x <= self.LEFT_DISTANCE and y >= self.height()-self.BOTTOM_DISTANCE:  # 左下角
            self.flags["bottom-left"] = True
        elif y <= self.TOP_DISTANCE:  # 上
            self.flags["top"] = True
        elif y >= self.height()-self.BOTTOM_DISTANCE:  # 下
            self.flags["bottom"] = True
        elif x <= self.LEFT_DISTANCE:  # 左
            self.flags["left"] = True
        elif x >= self.width()-self.RIGHT_DISTANCE:  # 右
            self.flags["right"] = True
        elif self.left_width < x < self.width()-self.right_width and y <= self.title_height:
            self.flags["move"] = True
        elif child_event != None:
            child_event(a0)
        self.mousepos = [a0.globalX(), a0.globalY()]

    def mouseReleaseEvent(self, a0: QMouseEvent, child_event=None) -> None:
        if child_event != None:
            child_event(a0)
        for key in self.flags:
            self.flags[key] = False

    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        if self.isMaximized():
            return
        dx = dy = 0
        if self.mousepos:
            dx = a0.globalX()-self.mousepos[0]
            dy = a0.globalY()-self.mousepos[1]
            self.mousepos = [a0.globalX(), a0.globalY()]

        x = a0.globalX()-self.x()
        y = a0.globalY()-self.y()

        if x <= self.LEFT_DISTANCE and y <= self.TOP_DISTANCE or self.flags["top-left"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif x >= self.width()-self.RIGHT_DISTANCE and y >= self.height()-self.BOTTOM_DISTANCE or self.flags["bottom-right"]:
            self.setCursor(Qt.SizeFDiagCursor)
        elif x >= self.width()-self.RIGHT_DISTANCE and y <= self.TOP_DISTANCE or self.flags["top-right"]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif x <= self.LEFT_DISTANCE and y >= self.height()-self.BOTTOM_DISTANCE or self.flags["bottom-left"]:
            self.setCursor(Qt.SizeBDiagCursor)
        elif y <= self.TOP_DISTANCE or self.flags["top"]:
            self.setCursor(Qt.SizeVerCursor)
        elif y >= self.height()-self.BOTTOM_DISTANCE or self.flags["bottom"]:
            self.setCursor(Qt.SizeVerCursor)
        elif x <= self.LEFT_DISTANCE or self.flags["left"]:
            self.setCursor(Qt.SizeHorCursor)
        elif x >= self.width()-self.RIGHT_DISTANCE or self.flags["right"]:
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if self.flags["right"]:
            self.resize(self.width()+dx, self.height())
        elif self.flags["left"]:
            # 左上角位置固定
            x = self.x()+self.width()
            self.resize(self.width()-dx, self.height())
            self.move(x-self.width(), self.y())
        elif self.flags["bottom"]:
            self.resize(self.width(), self.height()+dy)
        elif self.flags["top"]:
            y = self.y()+self.height()
            self.resize(self.width(), self.height()-dy)
            self.move(self.x(), y-self.height())
        elif self.flags["top-left"]:
            x = self.x()+self.width()
            self.resize(self.width()-dx, self.height())
            self.move(x-self.width(), self.y())

            y = self.y()+self.height()
            self.resize(self.width(), self.height()-dy)
            self.move(self.x(), y-self.height())
        elif self.flags["top-right"]:
            y = self.y()+self.height()
            self.resize(self.width(), self.height()-dy)
            self.move(self.x(), y-self.height())

            self.resize(self.width()+dx, self.height())
        elif self.flags["bottom-right"]:
            self.resize(self.width(), self.height()+dy)

            self.resize(self.width()+dx, self.height())
        elif self.flags["bottom-left"]:
            self.resize(self.width(), self.height()+dy)

            x = self.x()+self.width()
            self.resize(self.width()-dx, self.height())
            self.move(x-self.width(), self.y())
        elif self.flags["move"]:
            self.move(self.x()+dx, self.y()+dy)
