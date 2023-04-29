import os

import qtawesome as qta
from Core.Game import Game
from Kernel import Kernel
from PyQt5.QtCore import QEvent, QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QAction, QListView, QListWidget, QListWidgetItem,
                             QMenu)
from Setting import Setting

_translate = Kernel.translate


class Desktop(QListWidget):
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
        self.setWindowTitle(_translate("桌面"))

        self.setMovement(QListView.Movement.Static)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.TopToBottom)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWordWrap(True)
        self.setStyleSheet("QListWidget{border:none;}")
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showRightMenu)

        self.item_action = []
        self.refresh()

    def showRightMenu(self):
        """显示右键菜单"""
        item = self.itemAt(self.mapFromGlobal(QCursor.pos()))
        menu = QMenu(self)

        if item:
            action = QAction(self)
            action.setText(_translate("启动"))
            action.setIcon(qta.icon("mdi.rocket-launch-outline"))
            action.triggered.connect(lambda: Game(item.text()).launch())
            menu.addAction(action)

            action_functions = Setting(
            )["explorer.desktop.item_clicked_actions"]
            for action_function in action_functions:
                function = Kernel.getFunction(action_function)
                info = Kernel.getFunctionInfo(function)
                action = QAction(self)
                action.setText(info["name"])
                action.setIcon(info["icon"])
                action.triggered.connect(
                    lambda f=action_function: Kernel.execFunction(action_function, item.text()))
                menu.addAction(action)
        else:
            a_refresh = QAction(_translate("刷新"), self)
            a_refresh.setIcon(qta.icon("mdi.refresh"))
            a_refresh.triggered.connect(self.refresh)

            a_background_image = QAction(_translate("设置背景图片"), self)
            a_background_image.setIcon(qta.icon("fa.image"))
            a_background_image.triggered.connect(lambda: Kernel.execFunction(
                "SettingVisual", id="explorer.desktop.background_image"))

            menu.addAction(a_refresh)
            menu.addAction(a_background_image)

        menu.exec(QCursor.pos())

    def refresh(self):
        background_image = Setting().get(
            "explorer.desktop.background_image").replace("\\", "/")
        self.setStyleSheet(f"""
QListWidget{{
    border:none;
    border-image:url("{background_image}")
}}""")

        self.clear()
        path = Setting()["game.directories"][0]
        if not os.path.exists(os.path.join(path, "versions")):
            os.makedirs(os.path.join(path, "versions"))
        for game_name in os.listdir(os.path.join(path, "versions")):
            item = QListWidgetItem()
            item.setSizeHint(QSize(80, 80))
            item.setText(game_name)
            item.setIcon(Game(game_name).get_icon())
            self.addItem(item)

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(e)
