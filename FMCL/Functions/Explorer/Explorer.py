import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import QEvent, QObject, QPoint, Qt
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QAction, QPushButton, QStackedWidget, QWidget, qApp
from qfluentwidgets import RoundMenu, TransparentTogglePushButton
from Setting import Setting

from .Desktop import Desktop
from .Start import Start


class Explorer(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.resize(1000, 618)
        self.setWindowTitle("Functional Minecraft Launcher")
        self.caught_widgets: dict[QWidget, QPushButton] = {}  # 被捕获的QWidget
        self.currentChanged.connect(self.__currentChanged)
        qApp.installEventFilter(self)

        self.pb_start = QPushButton()
        self.pb_start.resize(46, 32)
        self.pb_start.setIcon(qApp.windowIcon())
        self.pb_start.setCheckable(True)
        self.pb_start.clicked.connect(self.showStart)
        self.pb_start.setStyleSheet("""
QPushButton{
    border:none;
}
QPushButton:hover{
    background-color:rgb(232,232,232);
}
QPushButton:checked{
    background-color:rgb(232,232,232);
}
""")

        self.a_showdesktop = QAction(self)
        self.a_showdesktop.setText(self.tr("显示桌面"))
        self.a_showdesktop.setIcon(qta.icon("ph.desktop"))
        self.a_showdesktop.triggered.connect(self.showDesktop)

        self.title_rightclicked_actions = [self.a_showdesktop]

        for name in Setting().get("explorer.title_rightclicked_actions"):
            action = QAction(self)
            func = Kernel.getFunction(name)
            info = Kernel.getFunctionInfo(func)
            action.setText(info["name"])
            action.setIcon(info["icon"])
            action.triggered.connect(lambda _, n=name: Kernel.execFunction(n))
            self.title_rightclicked_actions.append(action)

        self.showDesktop()

    def showEvent(self, a0: QShowEvent) -> None:
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_start, index=0))
        for _, button in self.caught_widgets.items():  # 恢复
            qApp.sendEvent(self.window(),
                           AddToTitleEvent(button, "right", -1))

        for action in self.title_rightclicked_actions:
            qApp.sendEvent(self.window(), AddToTitleMenuEvent(action))
        return super().showEvent(a0)

    def addWidget(self, widget: QWidget):
        """添加控件"""
        if widget == self:
            return
        if not isinstance(widget, Desktop) and not isinstance(widget, Start):
            if widget not in self.caught_widgets:
                # 添加任务栏的按钮
                button = self.addTitleButton(widget)
                self.caught_widgets[widget] = button

        super().addWidget(widget)
        widget.installEventFilter(self)

        self.setCurrentWidget(widget)
        Kernel.activateWidget(self)

    def addTitleButton(self, widget: QWidget):
        """添加标题栏按钮"""
        button = TransparentTogglePushButton()
        button.resize(100, 32)
        button.setText(widget.windowTitle())
        button.setIcon(widget.windowIcon())

        button.setToolTip(widget.windowTitle())
        button.clicked.connect(self.taskButtonClicked)
        button.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        button.customContextMenuRequested.connect(
            self.showRightMenu)
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(button, "right", -1))  # 相当于添加到左边的最后面
        return button

    def addFixedButton(self, cls: type):
        """添加固定的按钮"""
        button = TransparentTogglePushButton()
        button.resize(46, 32)
        button.clicked.connect(self.fixedButtonClicked)

        self.fixed_widgets[button] = cls

    def __currentChanged(self):
        for widget, button in self.caught_widgets.items():
            if widget == self.currentWidget():
                button.setChecked(True)
            else:
                button.setChecked(False)

        if not isinstance(self.currentWidget(), Start):
            self.pb_start.setChecked(False)
            for i in range(self.count()):
                widget = self.widget(i)
                if isinstance(widget, Start):
                    widget.navigationInterface.panel.collapse()
                    self.removeWidget(widget)
                    break
        else:
            self.pb_start.setChecked(True)

    def setCurrentWidget(self, widget: QWidget) -> None:
        if self.indexOf(widget) == -1:
            self.addWidget(widget)
        elif self.indexOf(widget) != self.count()-1:  # 置于最上层
            # 单纯的进行，不需要其他操作，所以使用父类的方法
            QStackedWidget.removeWidget(self, widget)
            QStackedWidget.addWidget(self, widget)
        super().setCurrentWidget(widget)

    def taskButtonClicked(self):
        sender = self.sender()
        for widget, button in self.caught_widgets.items():
            if button == sender:
                if self.currentWidget() == widget:
                    self.removeWidget(widget)
                else:
                    self.setCurrentWidget(widget)
                break

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 in self.caught_widgets:
            if a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
                a0.setParent(None)
            elif a1.type() == QEvent.Type.ParentChange and a0.parent() != self:
                self.removeTask(a0)
            elif a1.type() == QEvent.Type.Show:
                self.setCurrentWidget(a0)
        elif a1.type() == WidgetCaughtEvent.EventType:
            self.addWidget(a1.widget)
        return super().eventFilter(a0, a1)

    def removeTask(self, widget: QWidget):
        """移除一个任务(QWidget)"""
        self.removeWidget(widget)
        widget.removeEventFilter(self)
        if widget in self.caught_widgets:
            button = self.caught_widgets.pop(widget)
            qApp.sendEvent(
                self.window(), RemoveFromTitleEvent(button))
            button.deleteLater()

    def showRightMenu(self):
        """显示任务栏按钮的右键菜单"""
        sender = self.sender()
        for widget, button in self.caught_widgets.items():
            if button == sender:
                menu = RoundMenu(self)
                a_separate = QAction(self)
                a_separate.setText(self.tr("分离"))
                a_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
                a_separate.triggered.connect(
                    lambda: self.separateCaughtWidget(widget))
                menu.addAction(a_separate)

                a_close = QAction(self)
                a_close.setText(self.tr("关闭"))
                a_close.setIcon(qta.icon("mdi6.close"))
                a_close.triggered.connect(widget.close)
                menu.addAction(a_close)
                menu.exec(button.mapToGlobal(QPoint(0, button.height())))
                break

    def separateCaughtWidget(self, widget: QWidget):
        qApp.sendEvent(self, SeparateWidgetEvent(widget))
        a_back = QAction(widget)
        a_back.setText(self.tr("合并"))
        a_back.setIcon(qta.icon("msc.reply"))
        a_back.triggered.connect(lambda: self.addWidget(widget))
        qApp.sendEvent(widget.window(), AddToTitleMenuEvent(a_back))

    def showDesktop(self):
        """显示桌面"""
        while self.count():
            self.removeWidget(self.widget(0))
        desktop = Desktop()
        self.addWidget(desktop)

    def showStart(self):
        """显示开始界面"""
        widget = self.currentWidget()
        if not isinstance(widget, Start):
            start = Start()
            self.addWidget(start)
        else:
            self.removeWidget(widget)
