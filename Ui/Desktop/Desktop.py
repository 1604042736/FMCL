import os
from Core.Game import Game
from Core.Launch import Launch
from QtFBN.QFBNWidget import QFBNWidget
import Globals as g
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction, QTableWidget, QAbstractItemView
from PyQt5.QtGui import QCursor, QIcon, QResizeEvent, QMouseEvent
from Ui.VersionManager.VersionManager import VersionManager
from PyQt5.QtCore import Qt
from Translate import tr
import qtawesome as qta


class Desktop(QTableWidget, QFBNWidget):
    UNIT_HEIGHT = 64

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("桌面"))
        self.row_count = 1
        self.col_count = 1
        self.max_row_count = 8

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(self.UNIT_HEIGHT)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(self.UNIT_HEIGHT)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(self.UNIT_HEIGHT)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setMinimumSectionSize(self.UNIT_HEIGHT)

        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setObjectName("Desktop")
        self.customContextMenuRequested.connect(self.show_menu)
        self.set_versions()

    def set_versions(self):
        self.clear()
        self.version_path = g.cur_gamepath+"/versions"
        if not os.path.exists(self.version_path):
            os.makedirs(self.version_path)
        self.row_count = 1
        self.col_count = 1
        j = 0
        for i in os.listdir(self.version_path):
            if j == self.max_row_count:
                j = 0
                self.col_count += 1
            elif j == self.row_count:
                self.row_count += 1

            self.setRowCount(self.row_count)
            self.setColumnCount(self.col_count)

            item = QTableWidgetItem()
            item.setToolTip(i)
            item.setText(i)
            item.setIcon(QIcon(Game(i).get_info()["icon"]))
            self.setItem(j, self.col_count-1, item)
            j += 1

    def show_menu(self):
        item = self.currentItem()
        menu = QMenu(self)
        if item:
            text = item.text()
            a_launch = QAction(tr("启动")+f'"{text}"', self)
            a_launch.triggered.connect(lambda: self.launch_game(text))
            a_launch.setIcon(qta.icon("fa.power-off"))
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
                                     g.width,
                                     g.height,
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
        self.max_row_count = int(self.height()/self.UNIT_HEIGHT)
        self.set_versions()

    def deselect(self, e: QMouseEvent):
        """取消选中"""
        point = e.pos()
        index = self.indexAt(point)
        # 判断该单元格是否是空单元格
        if (self.item(index.row(), index.column()) == None):
            # 取消选中
            self.setCurrentItem(None)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.deselect(e)
        return super().mousePressEvent(e)
