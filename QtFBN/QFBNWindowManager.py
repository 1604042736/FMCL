import traceback
from QtFBN.QFBNWidget import QFBNWidget
from PyQt5.QtWidgets import QStackedWidget, QPushButton
import QtFBN as g
import qtawesome as qta


class QFBNWindowManager(QStackedWidget, QFBNWidget):
    """对软件中的窗口进行管理"""

    def __init__(self) -> None:
        super().__init__()

        self.caught_widgets: list[QFBNWidget] = []  # 被捕获的窗口
        g.manager = self
        self.currentChanged.connect(self.set_title_widget_state)

    def ready(self) -> None:
        """当一切准备好后"""

    def on_win_ready(self) -> None:
        self.pb_back = QPushButton(self.win.title)
        self.pb_back.resize(self.win.title_button_width, self.win.title_height)
        self.pb_back.setObjectName("pb_back")
        self.pb_back.setIcon(qta.icon("mdi.keyboard-backspace"))
        self.pb_back.hide()
        self.win.add_left_widget(self.pb_back, 0)

        self.win.remove_right_widget(self.win.pb_backtomanager)

        self.pb_sepwin = QPushButton(self.win.title)
        self.pb_sepwin.resize(self.win.title_button_width,
                              self.win.title_height)
        self.pb_sepwin.setObjectName('pb_sepwin')
        self.pb_sepwin.setIcon(qta.icon('ph.arrow-square-out-light'))
        self.pb_sepwin.hide()
        self.pb_sepwin.setToolTip("独立窗口")
        self.win.add_right_widget(self.pb_sepwin)

        self.pb_back.clicked.connect(self.go_back)
        self.pb_sepwin.clicked.connect(self.separate_window)

        return super().on_win_ready()

    def go_back(self) -> None:
        widget = self.currentWidget()
        self.release_widget(widget)

    def separate_window(self) -> None:
        try:
            widget = self.currentWidget()
            self.release_widget(widget)
            widget.show("separate")
        except:
            print(traceback.format_exc())

    def on_any_win_ready(self, win: QFBNWidget) -> None:
        """当任何一个窗口准备好后"""

    def set_title_widget_state(self) -> None:
        """设置控件的状态"""
        if self.count():
            self.pb_sepwin.show()
        else:
            self.pb_sepwin.hide()

        if self.count() > 1:
            self.pb_back.show()
        else:
            self.pb_back.hide()

        if self.win:
            self.win.resize_title_widgets()  # 防止按钮show或hide之后没有及时更新

        self.notifymanager.update_geometry()

    def catch_widget(self, widget: QFBNWidget) -> None:
        """捕获一个窗体"""
        self.caught_widgets.append(widget)
        self.addWidget(widget)
        self.setCurrentIndex(self.count()-1)

    def release_widget(self, widget: QFBNWidget) -> None:
        """释放一个窗体"""
        try:
            self.removeWidget(widget)
            self.caught_widgets.remove(widget)
        except ValueError:
            pass

    def show(self, call_ready=False) -> None:
        super().show()
        if call_ready:
            self.ready()

    def reshow(self):
        """重新显示"""
        if not self.isVisible():
            self.show()
        self.activateWindow()
