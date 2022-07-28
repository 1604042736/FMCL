from PyQt5.QtWidgets import QWidget, QFrame, QPushButton
import qtawesome as qta
from PyQt5.QtCore import QSize
import QtFBN as g


class QFBNWindowBasic(QWidget):
    """
    承载QFBNWidget的窗口
    这是一个基类,因为不同的系统有不同的实现
    """
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

    def add_right_widget(self, widget: QWidget, index: int = -1, set_icon_size=True) -> None:
        """添加右边的控件"""
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
        self.right_widgets.remove(widget)
        widget.hide()
        self.resize_title_widgets()

    def add_left_widget(self, widget: QWidget, index: int = -1, set_icon_size=True) -> None:
        """添加左边的控件"""
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
        self.left_widgets.remove(widget)
        widget.hide()
        self.resize_title_widgets()

    def set_title(self) -> None:
        """设置标题栏"""
        if g.manager != None:
            self.pb_backtomanager = QPushButton(self.title)
            self.pb_backtomanager.resize(
                self.title_button_width, self.title_height)
            self.pb_backtomanager.setObjectName('pb_backtomanager')
            self.pb_backtomanager.setIcon(qta.icon('msc.reply'))
            self.pb_backtomanager.setToolTip("回到主窗口")
            self.add_right_widget(self.pb_backtomanager)

        if self.target is not g.manager and g.manager != None:
            self.pb_home = QPushButton(self.title)
            self.pb_home.resize(self.title_button_width,
                                self.title_height)
            self.pb_home.setObjectName('pb_home')
            self.pb_home.setIcon(qta.icon('msc.window'))
            self.pb_home.clicked.connect(lambda: g.manager.reshow())
            self.pb_home.setToolTip("显示主窗口")
            self.add_right_widget(self.pb_home)

        self.title.raise_()

    def set_connection(self) -> None:
        """设置信号连接"""
        self.pb_backtomanager.clicked.connect(self.back_to_manager)

    def back_to_manager(self) -> None:
        """重新回到manager"""
        if self.target.parent_ == None:  # 回到manager
            self.target.show()
        else:  # 回到原来的widget中去
            self.target.setParent(self.target.parent_)
            QWidget.show(self.target)
            self.target.parent_.widget_to_self(self.target)
            self.close()

    def notify(self, title, msg):
        self.target.notify(title, msg)
