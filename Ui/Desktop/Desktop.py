import os
from Core.Game import Game
from Core.Launch import Launch
from QtFBN.QFBNWidget import QFBNWidget
import Globals as g
from PyQt5.QtWidgets import QMenu, QAction, QListWidget, QListView, QListWidgetItem
from PyQt5.QtGui import QCursor, QIcon, QResizeEvent
from Ui.VersionManager.VersionManager import VersionManager
from PyQt5.QtCore import Qt
from Translate import tr
import qtawesome as qta


class Desktop(QFBNWidget):  # 直接继承QTableWidget会出现鼠标移动事件无法正常捕获的问题

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("桌面"))
        self.w_versions = QListWidget(self)

        self.w_versions.setMovement(QListView.Static)
        self.w_versions.setViewMode(QListView.IconMode)
        self.w_versions.setFlow(QListView.TopToBottom)
        self.w_versions.setWordWrap(True)

        self.setObjectName("Desktop")
        self.w_versions.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.w_versions.customContextMenuRequested.connect(self.show_menu)
        self.set_versions()

    def set_versions(self):
        self.w_versions.clear()
        self.version_path = g.cur_gamepath+"/versions"
        if not os.path.exists(self.version_path):
            os.makedirs(self.version_path)
        for i in os.listdir(self.version_path):
            item = QListWidgetItem()
            item.setText(i)
            item.setIcon(QIcon(Game(i).get_info()["icon"]))
            self.w_versions.addItem(item)

    def show_menu(self, text=""):
        item = self.w_versions.itemAt(
            self.w_versions.mapFromGlobal(QCursor.pos()))
        menu = QMenu(self)
        if item:
            text = item.text()
            a_launch = QAction(tr("启动")+f'"{text}"', self)
            a_launch.triggered.connect(lambda: self.launch_game(text))
            a_launch.setIcon(qta.icon("mdi6.rocket-launch-outline"))
            a_manage = QAction(tr("管理")+f'"{text}"', self)
            a_manage.triggered.connect(
                lambda: self.open_version_manager(text))
            a_manage.setIcon(qta.icon("msc.versions"))
            menu.addAction(a_launch)
            menu.addAction(a_manage)
        else:
            a_refresh = QAction(tr("刷新"), self)
            a_refresh.triggered.connect(self.set_versions)
            menu.addAction(a_refresh)
        menu.exec_(QCursor.pos())

    def launch_game(self, version):
        if g.cur_user != None:
            g.dmgr.add_task(tr("启动")+version, Launch(
                version), "launch", (g.java_path,
                                     g.cur_user["name"],
                                     g.gamewidth,
                                     g.gameheight,
                                     g.maxmem,
                                     g.minmem))
        else:
            self.notify(tr("错误"), tr("未选择用户"))

    def open_version_manager(self, name):
        if name:
            versionmanager = VersionManager(name)
            versionmanager.GameDeleted.connect(self.set_versions)
            versionmanager.IconChanged.connect(self.set_versions)
            versionmanager.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.w_versions.resize(self.width(), self.height())
        self.set_versions()
