from Kernel import Kernel
import os
import sys
from typing import *

import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QEvent, QObject, QPoint, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import (QAction, QFrame, QMenu, QPushButton, QSizePolicy,
                             QSpacerItem, QStackedWidget, QVBoxLayout, QWidget,
                             qApp)
from Setting import Setting

from .AllFunctions import AllFunctions

_translate = QCoreApplication.translate


class StartUi(QStackedWidget):
    """开始界面显示其他界面的地方"""

    def addWidget(self, w: QWidget) -> int:
        self.removeWidget(self.currentWidget())
        return super().addWidget(w)


class Start(QWidget):
    """开始界面"""

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
        self.setWindowTitle(_translate("Start", "开始界面"))
        # 面板
        self.f_panel = QFrame(self)
        self.f_panel.move(0, 0)
        self.f_panel.resize(46, self.height())
        self.f_panel.setStyleSheet("""
QFrame{
    background-color: rgb(255,255,255);
    border-right: 1px solid rgb(245, 245, 245);
}
""")
        self.f_panel.installEventFilter(self)

        self.vbox_panel = QVBoxLayout(self.f_panel)
        self.vbox_panel.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.vbox_panel.setSpacing(0)
        self.vbox_panel.setContentsMargins(0, 0, 0, 0)
        # 分离上下面板
        self.si_separate = QSpacerItem(0, 0,
                                       QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.vbox_panel.addSpacerItem(self.si_separate)

        self.pb_software = QPushButton()
        self.pb_software.setText(_translate("Start", "软件"))
        self.pb_software.resize(46, 46)
        self.pb_software.setStyleSheet("""
QPushButton{
    border: none;
    text-align: left;
}
QPushButton:hover{
    background-color: rgb(200,200,200);
}
QPushButton:checked{
    border-left: 2px solid black;
}
""")
        self.pb_software.setIcon(qta.icon("mdi.application"))
        self.pb_software.setIconSize(self.pb_software.size())
        self.pb_software.clicked.connect(self.showSoftwareMenu)
        self.addPanelWidget(self.pb_software)

        self.pb_expand = QPushButton()
        self.pb_expand.setText(_translate("Start", "展开"))
        self.pb_expand.resize(46, 46)
        self.pb_expand.setStyleSheet("""
QPushButton{
    border: none;
    text-align: left;
}
QPushButton:hover{
    background-color: rgb(200,200,200);
}
QPushButton:checked{
    border-left: 2px solid black;
}
""")
        self.pb_expand.setIconSize(self.pb_expand.size())
        self.pb_expand.setIcon(qta.icon("msc.three-bars"))
        self.pb_expand.clicked.connect(self.expandPanel)
        self.addPanelWidget(self.pb_expand, "top")

        self.ui = StartUi(self)
        self.ui.move(46, 0)

        self.pb_allfunc = QPushButton()
        self.pb_allfunc.setText(_translate("AllFunctions", "所有应用"))
        self.pb_allfunc.resize(46, 46)
        self.pb_allfunc.setStyleSheet("""
QPushButton{
    border: none;
    text-align: left;
}
QPushButton:hover{
    background-color: rgb(200,200,200);
}
QPushButton:checked{
    border-left: 2px solid black;
}
""")
        self.pb_allfunc.setIconSize(self.pb_allfunc.size())
        self.pb_allfunc.setIcon(qta.icon("mdi.format-list-checkbox"))
        self.pb_allfunc.clicked.connect(
            lambda: self.changeUi(self.pb_allfunc, AllFunctions))
        self.pb_allfunc.setCheckable(True)
        self.pb_allfunc.setAutoExclusive(True)
        self.addPanelWidget(self.pb_allfunc, index=-1)
        self.changeUi(self.pb_allfunc, AllFunctions)

        self.pb_user = QPushButton()
        self.pb_user.resize(46, 46)
        self.pb_user.setStyleSheet("""
QPushButton{
    border: none;
    text-align: left;
}
QPushButton:hover{
    background-color: rgb(200,200,200);
}
""")
        self.pb_user.setIconSize(self.pb_user.size())
        self.pb_user.setIcon(qta.icon("ph.user-circle"))
        self.pb_user.clicked.connect(
            lambda: Kernel.execFunction("SettingVisual", id="users"))
        self.addPanelWidget(self.pb_user)

        self.refresh()

        self.f_panel.raise_()

    def changeUi(self, button: QPushButton, ui_type: type):
        button.setChecked(True)
        ui = ui_type()
        self.ui.addWidget(ui)

    def expandPanel(self):
        """展开面板"""
        if self.f_panel.width() == 46:
            self.f_panel.resize(46*3, self.height())
        elif self.f_panel.width() == 46*3:
            self.f_panel.resize(46, self.height())

    def addPanelWidget(self, widget: QWidget, place: Literal["bottom", "top"] = "bottom", index: int = 0):
        """添加面板控件"""
        widget.setFixedHeight(widget.height())
        if place == "bottom":
            index = self.vbox_panel.indexOf(self.si_separate)+index+1
        self.vbox_panel.insertWidget(index, widget)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.f_panel.resize(self.f_panel.width(), self.height())
        self.ui.resize(self.width()-46, self.height())
        return super().resizeEvent(a0)

    def showSoftwareMenu(self):
        menu = QMenu(self)

        a_quit = QAction(self, text=_translate("Start", "退出"))
        a_quit.triggered.connect(qApp.quit)
        a_quit.setIcon(qta.icon("mdi.power"))

        a_restart = QAction(self, text=_translate("Start", "重启"))
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
                self.f_panel.resize(46*3, self.height())
            elif a1.type() == QEvent.Type.Leave:
                self.f_panel.resize(46, self.height())
        return super().eventFilter(a0, a1)

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
