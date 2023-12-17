import os

import qtawesome as qta
from Core.Version import Version
from Kernel import Kernel
from PyQt5.QtCore import QEvent, QSize, Qt, QPoint
from PyQt5.QtGui import QCursor, QPainter, QPixmap
from PyQt5.QtWidgets import QAction, QListView, QListWidgetItem, qApp
from qfluentwidgets import (
    RoundMenu,
    ListWidget,
    CheckableMenu,
    TransparentToolButton,
    Action,
)
from Setting import Setting
from Events import *


class Desktop(ListWidget):
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
        self.setWindowTitle(self.tr("桌面"))

        self.setMovement(QListView.Movement.Static)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.TopToBottom)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWordWrap(True)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightMenu)

        self.pb_quickswitchgamedir = TransparentToolButton()
        self.pb_quickswitchgamedir.setIcon(qta.icon("msc.file-symlink-directory"))
        self.pb_quickswitchgamedir.resize(46, 32)
        self.pb_quickswitchgamedir.clicked.connect(self.showGameDirMenu)

        self.item_action = []
        self.refresh()

    def showRightMenu(self):
        """显示右键菜单"""
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        menu = RoundMenu(self)

        if item:
            action_functions = Setting()["explorer.desktop.item_rightclicked_actions"]
            for action_function in action_functions:
                function = Kernel.getFunction(action_function)
                info = Kernel.getFunctionInfo(function)
                action = QAction(self)
                action.setText(info["name"])
                action.setIcon(info["icon"])
                action.triggered.connect(
                    lambda _, f=action_function: Kernel.execFunction(f, item.text())
                )
                menu.addAction(action)
        else:
            a_refresh = QAction(self.tr("刷新"), self)
            a_refresh.setIcon(qta.icon("mdi.refresh"))
            a_refresh.triggered.connect(self.refresh)

            a_background_image = QAction(self.tr("设置背景图片"), self)
            a_background_image.setIcon(qta.icon("fa.image"))
            a_background_image.triggered.connect(
                lambda: Kernel.execFunction(
                    "SettingEditor", id="explorer.desktop.background_image"
                )
            )

            menu.addAction(a_refresh)
            menu.addAction(a_background_image)

        menu.exec(QCursor.pos())

    def refresh(self):
        self.background_image = (
            Setting().get("explorer.desktop.background_image").replace("\\", "/")
        )
        self.clear()
        path = Setting()["game.directories"][0]
        if not os.path.exists(os.path.join(path, "versions")):
            os.makedirs(os.path.join(path, "versions"))
        for game_name in os.listdir(os.path.join(path, "versions")):
            item = QListWidgetItem()
            item.setSizeHint(QSize(80, 80))
            item.setText(game_name)
            item.setIcon(Version(game_name).get_icon())
            self.addItem(item)
        self.repaint()

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Type.Show:
            if Setting()["explorer.desktop.quick_switch_gamedir"]:
                qApp.sendEvent(
                    self.window(),
                    AddToTitleEvent(self.pb_quickswitchgamedir, "right", 0),
                )
            self.refresh()
        elif e.type() == QEvent.Type.Hide:
            qApp.sendEvent(
                self.window(), RemoveFromTitleEvent(self.pb_quickswitchgamedir)
            )
            self.pb_quickswitchgamedir.setParent(self)
        elif e.type() == QEvent.Type.Paint:
            painter = QPainter(self)
            painter.drawPixmap(self.rect(), QPixmap(self.background_image))
        return super().event(e)

    def showGameDirMenu(self):
        def switchGameDir(name):
            gamedir = Setting()["game.directories"]
            gamedir.remove(name)
            gamedir.insert(0, name)
            self.refresh()

        menu = CheckableMenu(self)
        actions = []
        for _, name in enumerate(Setting()["game.directories"]):
            action = Action(checkable=True)
            action.triggered.connect(lambda _, n=name: switchGameDir(n))
            action.setText(name)
            actions.append(action)
        actions[0].setChecked(True)
        menu.addActions(actions)
        menu.exec(
            self.pb_quickswitchgamedir.mapToGlobal(
                QPoint(0, self.pb_quickswitchgamedir.height())
            )
        )
