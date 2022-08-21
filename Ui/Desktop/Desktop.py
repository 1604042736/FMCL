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


class Desktop(QFBNWidget):  # 直接继承QTableWidget会出现鼠标移动事件无法正常捕获的问题
    UNIT_HEIGHT = 64

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("桌面"))
        self.tablewidget = QTableWidget(self)
        self.row_count = 1
        self.col_count = 1
        self.max_row_count = 8

        self.tablewidget.horizontalHeader().setVisible(False)
        self.tablewidget.horizontalHeader().setDefaultSectionSize(self.UNIT_HEIGHT)
        self.tablewidget.horizontalHeader().setHighlightSections(False)
        self.tablewidget.horizontalHeader().setMinimumSectionSize(self.UNIT_HEIGHT)
        self.tablewidget.verticalHeader().setVisible(False)
        self.tablewidget.verticalHeader().setDefaultSectionSize(self.UNIT_HEIGHT)
        self.tablewidget.verticalHeader().setHighlightSections(False)
        self.tablewidget.verticalHeader().setMinimumSectionSize(self.UNIT_HEIGHT)

        self.tablewidget.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection)
        self.tablewidget.setDragDropMode(
            QAbstractItemView.DragDropMode.NoDragDrop)
        self.tablewidget.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu)
        self.tablewidget.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setObjectName("Desktop")
        self.tablewidget.mousePressEvent = self.mousePressEvent
        self.tablewidget.customContextMenuRequested.connect(self.show_menu)
        self.set_versions()

    def set_versions(self):
        self.tablewidget.clear()
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

            self.tablewidget.setRowCount(self.row_count)
            self.tablewidget.setColumnCount(self.col_count)

            item = QTableWidgetItem()
            item.setToolTip(i)
            item.setText(i)
            item.setIcon(QIcon(Game(i).get_info()["icon"]))
            self.tablewidget.setItem(j, self.col_count-1, item)
            j += 1

    def show_menu(self):
        item = self.tablewidget.currentItem()
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
        self.tablewidget.resize(self.width(), self.height())
        self.max_row_count = int(self.height()/self.UNIT_HEIGHT)
        self.set_versions()

    def deselect(self, e: QMouseEvent):
        """取消选中"""
        point = e.pos()
        index = self.tablewidget.indexAt(point)
        # 如果是空单元格就相当于self.tablewidget.setCurrentItem(None)
        self.tablewidget.setCurrentItem(
            self.tablewidget.item(index.row(), index.column()))

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.deselect(e)
        return super().mousePressEvent(e)
