from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtWidgets import QApplication, QDialog, QWidget

from .Events import *
from .Window import Window


class Application(QApplication):

    __windows: list = []  # 存储产生的Window
    tasks: set[QObject] = set()

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        if a1.type() == QEvent.Type.Show:
            Application.tasks.add(a0)
        elif a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
            if a0 in Application.tasks:
                Application.tasks.remove(a0)

        if (isinstance(a0, QWidget)
                and not isinstance(a0, Window)
                and not isinstance(a0, QDialog)
                and a0.windowType() != Qt.WindowType.ToolTip):
            if a1.type() == QEvent.Type.Show:
                if a0.parent() == None:
                    self.sendEvent(self, WidgetCaughtEvent(a0))
                    if a0.parent() == None:  # 使用默认方法
                        self.showWidget(a0)

        return super().notify(a0, a1)

    @staticmethod
    def showWidget(widget: QWidget):
        """使用Window来显示控件"""
        window = Window(widget)
        window.show()
        Application.__windows.append(window)

    @staticmethod
    def activateWidget(widget: QWidget):
        """激活一个控件"""
        if not widget.isVisible():
            widget.show()  # 自己要显示
            widget.window().show()  # 自己的窗口也得显示
        widget.activateWindow()
