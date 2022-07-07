from typing import Literal
from PyQt5.QtWidgets import QApplication, QWidget
import QtFBN as g
from QtFBN.QFBNNotifyManager import QFBNNotifyManager
from QtFBN.QFBNWindow import QFBNWindow
from PyQt5.QtCore import QTimer


class QFBNWidget(QWidget):
    """扩展QWidget以达到目的"""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)
        self.resize(1000, 618)
        self.win: QFBNWindow = None
        self.parent_ = None  # 保存parent

        self.notifymanager = QFBNNotifyManager(self)
        self.notifymanager.hide()

    def notify(self, title, msg):
        widget = QApplication.activeWindow()
        if widget:
            widget.target.notifymanager.notify(title, msg)
            widget.target.notifymanager.show()
        else:
            # 等待一会儿再试试
            timer = QTimer()
            timer.timeout.connect(lambda: self.notify(title, msg))
            timer.start(500)

    def show(self, mode: Literal["default", "separate", "original"] = "default") -> None:
        if(mode == "default"
            and g.manager != None
            and self is not g.manager
            and g.manager.win.isVisible()
           ):  # 有符合条件的manager就让它捕获
            if self.win:
                self.win.close()
            try:
                if QApplication.activeWindow().target is not g.manager:
                    g.manager.reshow()
            except:
                pass
            g.manager.catch_widget(self)
            return

        if mode == "original":  # 原来的显示方法
            super().show()
            return

        if mode == "separate" or mode == "default":  # 独立显示
            self.win = QFBNWindow(self)
            self.on_win_ready()
            self.win.show()
            return

        raise Exception(f"未知的mode:{mode}")

    def close(self) -> bool:
        if g.manager != None and self is not g.manager:
            g.manager.release_widget(self)
        if self.win != None:
            self.win.close()
        return super().close()

    def on_win_ready(self) -> None:
        """QFBNWindow准备好了"""
        g.on_any_win_ready(self)

    def setParent(self, w) -> None:
        if w != None and not isinstance(w, QFBNWindow):
            self.parent_ = w
        super().setParent(w)

    def widget_to_self(self, w) -> None:
        """对回到自己的widget进行设置"""
