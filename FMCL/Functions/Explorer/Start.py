import os
import sys
from typing import *

import qtawesome as qta
from Kernel import Kernel
from PyQt5.QtCore import QEvent, QPoint
from PyQt5.QtWidgets import QAction, QHBoxLayout, QStackedWidget, QWidget, qApp
from qfluentwidgets import (NavigationInterface, NavigationItemPosition,
                            NavigationPushButton, RoundMenu)
from Setting import Setting

from .AllFunctions import AllFunctions

_translate = Kernel.translate


class Navigation(NavigationInterface):
    def pos(self) -> QPoint:
        # 让NavigationPanel展开后处在正确位置上
        return QPoint(0, 32)


class Start(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.stackedWidget = QStackedWidget(self)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.navigationInterface = Navigation(self)
        self.widgetLayout = QHBoxLayout()

        # initialize layout
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addLayout(self.widgetLayout)

        self.widgetLayout.addWidget(self.stackedWidget)

        self.all_functions = AllFunctions()
        self.addSubInterface(self.all_functions,
                             qta.icon("mdi.format-list-checkbox"),
                             _translate("所有应用"))
        self.switchTo(self.all_functions)
        self.navigationInterface.setCurrentItem("AllFunctions")

        self.pb_user = NavigationPushButton(qta.icon("ph.user-circle"),
                                            _translate("未选择用户"),
                                            False)
        self.pb_user.clicked.connect(
            lambda: Kernel.execFunction("SettingVisual", id="users"))
        self.navigationInterface.addWidget(
            routeKey='user',
            widget=self.pb_user,
            position=NavigationItemPosition.BOTTOM
        )

        self.pb_software = NavigationPushButton(qta.icon("mdi.application"),
                                                _translate("软件"),
                                                False)
        self.pb_software.clicked.connect(self.showSoftwareMenu)
        self.navigationInterface.addWidget(
            routeKey='software',
            widget=self.pb_software,
            position=NavigationItemPosition.BOTTOM
        )

    def addSubInterface(self, interface: QWidget, icon, text: str,
                        position=NavigationItemPosition.TOP, parent=None):
        if not interface.objectName():
            raise ValueError(
                "The object name of `interface` can't be empty string.")
        if parent and not parent.objectName():
            raise ValueError(
                "The object name of `parent` can't be empty string.")

        self.stackedWidget.addWidget(interface)

        # add navigation item
        routeKey = interface.objectName()
        item = self.navigationInterface.addItem(
            routeKey=routeKey,
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text,
            parentRouteKey=parent.objectName() if parent else None
        )
        return item

    def switchTo(self, interface: QWidget):
        self.stackedWidget.setCurrentWidget(interface)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)

    def refresh(self):
        users = Setting()["users"]
        if users:
            self.pb_user.setText(users[0])
        else:
            self.pb_user.setText("未设置用户")

    def restart(self):
        os.popen(f'start {sys.argv[0]}')
        qApp.quit()

    def showSoftwareMenu(self):
        menu = RoundMenu(self)

        a_quit = QAction(self, text=_translate("退出"))
        a_quit.triggered.connect(qApp.quit)
        a_quit.setIcon(qta.icon("mdi.power"))

        a_restart = QAction(self, text=_translate("重启"))
        a_restart.triggered.connect(self.restart)
        a_restart.setIcon(qta.icon("msc.debug-restart"))

        menu.addAction(a_quit)
        menu.addAction(a_restart)

        menu.exec_(self.pb_software.mapToGlobal(
            QPoint(0, -menu.view.height())))
