from QtFBN.QFBNWindowBasic import QFBNWindowBasic
from PyQt5.QtCore import Qt, QObject, QEvent
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
        self.installEventFilter(self)
        self.set_all_children(self)  # 针对已经添加进去的子控件

    def set_all_children(self, w):
        '''将所有子控件进行设置'''
        children = w.findChildren(QWidget)
        for child in children:
            child.setMouseTracking(True)
            child.installEventFilter(self)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        x = a0.globalX()-self.x()
        y = a0.globalY()-self.y()

        if a0.button() == Qt.LeftButton:
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
        self.mousepos = [a0.globalX(), a0.globalY()]

    def mouseReleaseEvent(self, a0: QMouseEvent) -> None:
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

        # 移动的时侯位置符合要求或鼠标已经按下就设置对应的光标
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

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.ChildAdded:
            a0.setMouseTracking(True)
            a0.installEventFilter(self)
            self.set_all_children(a0)
        elif a1.type() == QEvent.MouseMove:
            self.mouseMoveEvent(a1)
        elif a1.type() == QEvent.MouseButtonPress:
            self.mousePressEvent(a1)
            # 如果处于某种状态(比如开始朝某个方向拖动以改变窗口大小)就不让子控件处理点击事件
            if any([val for _, val in self.flags.items()]):
                return True
        elif a1.type() == QEvent.MouseButtonRelease:
            self.mouseReleaseEvent(a1)
        return super().eventFilter(a0, a1)
