import os
import sys
from typing import Literal

import qtawesome as qta
from PyQt5.QtCore import QEvent, QObject, QPoint, QSize, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import (QAction, QFrame, QListView, QListWidget,
                             QListWidgetItem, QMenu, QPushButton, QSizePolicy,
                             QSpacerItem, QStackedWidget, QVBoxLayout, QWidget,
                             qApp)

from .Constants import *
from .Events import *
from .TaskManager import TaskManager


class StartUi(QStackedWidget):
    """开始界面显示其他界面的地方"""

    def addWidget(self, w: QWidget) -> int:
        self.removeWidget(self.currentWidget())
        return super().addWidget(w)


class Start(QWidget):
    """开始界面"""
    func_getters: list = [
        lambda:[("任务管理器", qta.icon("fa.tasks"), lambda: TaskManager().show())]
    ]  # 功能
    panel_getters: list = []  # 面板控件

    __instance = None
    __new_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        cls.__new_count += 1
        return cls.__instance

    def __init__(self):
        if self.__new_count > 1:
            return
        super().__init__()
        self.setWindowTitle("开始界面")
        # 面板
        self.f_panel = QFrame(self)
        self.f_panel.move(0, 0)
        self.f_panel.resize(W_PANEL, self.height())
        self.f_panel.setStyleSheet(S_D_PANEL)
        self.f_panel.installEventFilter(self)

        self.vbox_panel = QVBoxLayout(self.f_panel)
        self.vbox_panel.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vbox_panel.setSpacing(0)
        self.vbox_panel.setContentsMargins(0, 0, 0, 0)
        # 分离上下面板
        self.si_separate = QSpacerItem(40, 20,
                                       QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vbox_panel.addSpacerItem(self.si_separate)

        self.pb_software = QPushButton()
        self.pb_software.setText("软件")
        self.pb_software.resize(W_PANEL, H_PANELBUTTON)
        self.pb_software.setStyleSheet(S_D_PANELBUTTON)
        self.pb_software.setIcon(qta.icon("mdi.application"))
        self.pb_software.setIconSize(self.pb_software.size())
        self.pb_software.clicked.connect(self.showSoftwareMenu)
        self.addPanelWidget(self.pb_software)

        self.pb_expand = QPushButton()
        self.pb_expand.setText("展开")
        self.pb_expand.resize(W_PANEL, H_PANELBUTTON)
        self.pb_expand.setStyleSheet(S_D_PANELBUTTON)
        self.pb_expand.setIconSize(self.pb_expand.size())
        self.pb_expand.setIcon(qta.icon("msc.three-bars"))
        self.pb_expand.clicked.connect(self.expandPanel)
        self.addPanelWidget(self.pb_expand, "top")

        self.ui = StartUi(self)
        self.ui.move(W_PANEL, 0)

        self.pb_allfunc = QPushButton()
        self.pb_allfunc.setText("所有应用")
        self.pb_allfunc.resize(W_PANEL, H_PANELBUTTON)
        self.pb_allfunc.setStyleSheet(S_D_PANELBUTTON)
        self.pb_allfunc.setIconSize(self.pb_allfunc.size())
        self.pb_allfunc.setIcon(qta.icon("mdi.format-list-checkbox"))
        self.pb_allfunc.clicked.connect(
            lambda: self.changeUi(self.pb_allfunc, AllFunctions))
        self.pb_allfunc.setCheckable(True)
        self.pb_allfunc.setAutoExclusive(True)
        self.addPanelWidget(self.pb_allfunc, index=-1)
        self.changeUi(self.pb_allfunc, AllFunctions)

        self.refresh()

        self.f_panel.raise_()

    def changeUi(self, button: QPushButton, ui_type: type):
        button.setChecked(True)
        ui = ui_type()
        self.ui.addWidget(ui)

    def expandPanel(self):
        """展开面板"""
        if self.f_panel.width() == W_PANEL:
            self.f_panel.resize(W_PANEL_EXPAND, self.height())
        elif self.f_panel.width() == W_PANEL_EXPAND:
            self.f_panel.resize(W_PANEL, self.height())

    def addPanelWidget(self, widget: QWidget, place: Literal["bottom", "top"] = "bottom", index: int = 0):
        """添加面板控件"""
        widget.setFixedHeight(widget.height())
        if place == "bottom":
            index = self.vbox_panel.indexOf(self.si_separate)+index+1
        self.vbox_panel.insertWidget(index, widget)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.f_panel.resize(self.f_panel.width(), self.height())
        self.ui.resize(self.width()-W_PANEL, self.height())
        return super().resizeEvent(a0)

    def showSoftwareMenu(self):
        menu = QMenu(self)

        a_quit = QAction(self, text="退出")
        a_quit.triggered.connect(qApp.quit)
        a_quit.setIcon(qta.icon("mdi.power"))

        a_restart = QAction(self, text="重启")
        a_restart.triggered.connect(self.restart)
        a_restart.setIcon(qta.icon("msc.debug-restart"))

        menu.addAction(a_quit)
        menu.addAction(a_restart)

        menu.exec_(self.pb_software.mapToGlobal(
            QPoint(0, -menu.sizeHint().height())))

    def restart(self):
        os.popen(f'start {sys.argv[0]}')
        qApp.quit()

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if a0 == self.f_panel:
            if a1.type() == QEvent.Type.Enter:
                self.f_panel.resize(W_PANEL_EXPAND, self.height())
            elif a1.type() == QEvent.Type.Leave:
                self.f_panel.resize(W_PANEL, self.height())
        return super().eventFilter(a0, a1)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)

    def refresh(self):
        for child in self.f_panel.findChildren(QWidget):  # 清空panel
            if child not in (self.pb_allfunc, self.pb_expand, self.pb_software):
                self.vbox_panel.removeWidget(child)
                child.deleteLater()
        for getter in Start.panel_getters:
            for args in getter():
                self.addPanelWidget(*args)


class AllFunctions(QListWidget):
    """所有应用"""

    __instance = None
    __new_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        cls.__new_count += 1
        return cls.__instance

    def __init__(self):
        if self.__new_count > 1:
            return
        super().__init__()
        self.setMovement(QListView.Movement.Static)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWordWrap(True)
        self.setStyleSheet("QListWidget{border:none;}")
        self.setWindowTitle("所有应用")
        self.setWindowIcon(qta.icon("mdi.format-list-checkbox"))

        self.itemClicked.connect(self.launchFunc)
        self.item_action = []

        for getter in Start.func_getters:
            for text, icon, action in getter():
                item = QListWidgetItem()
                item.setSizeHint(QSize(80, 80))
                item.setText(text)
                item.setIcon(icon)
                self.addItem(item)
                self.item_action.append((item, action))

    def launchFunc(self):
        for item, action in self.item_action:
            if item == self.currentItem():
                action()
                break
