import traceback
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QLabel
import qtawesome as qta
from PyQt5.QtCore import QSize, Qt
import QtFBN as g
from PyQt5.QtGui import QFontMetrics


class QFBNWindowBasic(QWidget):
    """
    承载QFBNWidget的窗口
    这是一个基类,
    只负责界面,其余如移动,调整大小等操作由子类完成
    """
    TOP_DISTANCE = 4  # 上边框距离
    BOTTOM_DISTANCE = 4  # 下边框距离
    LEFT_DISTANCE = 4  # 左边框距离
    RIGHT_DISTANCE = 4  # 右边框距离

    title_height = 30  # 标题栏高度
    left_width = 0  # 标题栏靠左控件的宽度
    right_width = 0  # 标题栏靠右控件的宽度
    title_button_width = 45  # 标题栏按钮宽度

    def __init__(self, target) -> None:
        super().__init__()
        self.title_button_icon_size = QSize(20, 20)

        self.target = target
        self.resize(1000, 618)

        self.right_widgets: list[QWidget] = []  # 标题栏靠右的控件
        self.left_widgets: list[QWidget] = []  # 标题栏靠左的控件
        self.title = QFrame(self)
        self.title.setObjectName("f_title")
        self.title.move(0, 0)

        self.set_title()
        self.set_connection()

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
        self.setWindowIcon(self.target.windowIcon())
        QWidget.show(self.target)

    def set_windowstyle(self) -> None:
        """设置窗口样式"""
        self.setWindowFlags(self.windowFlags() |
                            Qt.FramelessWindowHint)

    def resize_title_widgets(self) -> None:
        """设置标题栏控件的大小"""
        self.right_width = 0
        for widget in self.right_widgets:
            if widget.isHidden():
                continue
            self.right_width += widget.width()
            widget.move(self.title.width()-self.right_width, 0)

        self.left_width = 0
        for widget in self.left_widgets:
            if widget.isHidden():
                continue
            widget.move(self.left_width, 0)
            self.left_width += widget.width()

        self.l_title.move(int(
            (self.title.width()-self.left_width-self.right_width-self.l_title.width())/2+self.left_width), 0)

    def add_right_widget(self, widget: QWidget, index: int = -1, set_icon_size=True) -> None:
        """添加右边的控件"""
        if widget in self.left_widgets:  # 不添加相同的控件
            return
        if index < 0:
            index = len(self.right_widgets)+index+1
        self.right_widgets.insert(index, widget)
        widget.setParent(self.title)
        widget.resize(widget.width(), self.title_height)
        if isinstance(widget, QPushButton) and set_icon_size:
            widget.setIconSize(self.title_button_icon_size)
        self.resize_title_widgets()

    def remove_right_widget(self, widget: QWidget) -> None:
        """删除右边的控件"""
        try:
            self.right_widgets.remove(widget)
            widget.hide()
            self.resize_title_widgets()
        except:
            pass

    def add_left_widget(self, widget: QWidget, index: int = -1, set_icon_size=True) -> None:
        """添加左边的控件"""
        if widget in self.left_widgets:  # 不添加相同的控件
            return
        if index < 0:
            index = len(self.left_widgets)+index+1
        self.left_widgets.insert(index, widget)
        widget.setParent(self.title)
        widget.resize(widget.width(), self.title_height)
        if isinstance(widget, QPushButton) and set_icon_size:
            widget.setIconSize(self.title_button_icon_size)
        self.resize_title_widgets()

    def remove_left_widget(self, widget: QWidget) -> None:
        """删除左边的控件"""
        try:
            self.left_widgets.remove(widget)
            widget.hide()
            self.resize_title_widgets()
        except:
            pass

    def set_title(self) -> None:
        """设置标题栏"""
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

        self.pb_backtomanager = QPushButton(self.title)
        self.pb_backtomanager.resize(
            self.title_button_width, self.title_height)
        self.pb_backtomanager.setObjectName('pb_backtomanager')
        self.pb_backtomanager.setIcon(qta.icon('msc.reply'))
        self.pb_backtomanager.setToolTip("回到原位置")
        if g.manager != None or self.target.parent_ != None:
            self.add_right_widget(self.pb_backtomanager)
        else:
            self.pb_backtomanager.hide()

        self.pb_home = QPushButton(self.title)
        self.pb_home.resize(self.title_button_width,
                            self.title_height)
        self.pb_home.setObjectName('pb_home')
        self.pb_home.setIcon(qta.icon('msc.window'))
        self.pb_home.setToolTip("显示原位置")
        if (self.target is not g.manager and g.manager != None) or self.target.parent_ != None:
            self.add_right_widget(self.pb_home)
        else:
            self.pb_home.hide()

        self.title.raise_()

    def set_connection(self) -> None:
        """设置信号连接"""
        self.pb_close.clicked.connect(self.close)
        self.pb_maxnormal.clicked.connect(self.change_show_state)
        self.pb_min.clicked.connect(self.showMinimized)

        self.pb_backtomanager.clicked.connect(self.back_to_manager)
        self.pb_home.clicked.connect(self.show_home)

    def show_home(self):
        if self.target.parent_ != None:
            try:
                if not self.target.parent_.isVisible():
                    if self.target.parent_.win != None:
                        self.target.parent_.show()
                    else:
                        g.manager.reshow()
                self.target.parent_.activateWindow()
            except:
                print(traceback.format_exc())
        elif g.manager != None:
            g.manager.reshow()

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

    def back_to_manager(self) -> None:
        """重新回到manager"""
        self.show_home()
        if self.target.parent_ == None:  # 回到manager
            self.target.show()
        else:  # 回到原来的widget中去
            self.target.setParent(self.target.parent_)
            QWidget.show(self.target)
            self.target.parent_.widget_to_self(self.target)
            self.close()

    def resizeEvent(self, a0) -> None:
        self.target.resize(self.width(), self.height()-self.title_height)
        self.target.move(0, self.title_height)
        self.title.resize(self.width(), self.title_height)
        self.resize_title_widgets()
        self.target.notifymanager.update_geometry()
        super().resizeEvent(a0)
