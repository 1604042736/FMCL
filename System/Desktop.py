from PyQt5.QtCore import QCoreApplication, QEvent, QSize, Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QAction, QListView, QListWidget, QListWidgetItem,
                             QMenu)

from .Constants import *

_translate = QCoreApplication.translate


class Desktop(QListWidget):
    item_getters: list = []

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
        self.setWindowTitle(_translate("Desktop", "桌面"))

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

        a_refresh = QAction(_translate("Desktop", "刷新"), self)
        a_refresh.triggered.connect(self.refresh)
        menu.addAction(a_refresh)

        if item:
            for _item, actions in self.item_action:
                if item == _item:
                    menu.addActions(actions)
                    break

        menu.exec(QCursor.pos())

    def refresh(self):
        self.clear()
        self.item_action = []
        for getter in Desktop.item_getters:
            for text, icon, actions in getter():
                item = QListWidgetItem()
                item.setSizeHint(QSize(80, 80))
                item.setText(text)
                item.setIcon(icon)
                self.addItem(item)
                self.item_action.append((item, actions))

    def event(self, e: QEvent) -> bool:
        if e.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(e)
