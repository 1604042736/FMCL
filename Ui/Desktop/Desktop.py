import os
from Core.Launch import Launch
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Desktop.ui_Desktop import Ui_Desktop
import Globals as g
from PyQt5.QtWidgets import QTableWidgetItem, QMenu, QAction
from PyQt5.QtGui import QCursor

from Ui.VersionManager.VersionManager import VersionManager


class Desktop(QFBNWidget, Ui_Desktop):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.row_count = 1
        self.col_count = 1
        self.max_row_count = 8

        self.tableWidget.customContextMenuRequested.connect(self.show_menu)
        self.set_versions()

    def set_versions(self):
        self.tableWidget.clear()
        self.version_path = g.cur_gamepath+"/versions"
        if not os.path.exists(self.version_path):
            os.makedirs(self.version_path)

        j = 0
        for i in os.listdir(self.version_path):
            self.tableWidget.setRowCount(self.row_count)
            self.tableWidget.setColumnCount(self.col_count)

            item = QTableWidgetItem()
            item.setText(i)
            self.tableWidget.setItem(j, self.col_count-1, item)
            j += 1
            if j == self.max_row_count:
                j = 0
                self.col_count += 1
            elif j == self.row_count:
                self.row_count += 1

    def show_menu(self):
        item = self.tableWidget.currentItem()
        if item:
            text = item.text()
            menu = QMenu(self.tableWidget)
            a_launch = QAction(f'启动"{text}"', self)
            a_launch.triggered.connect(lambda: self.launch_game(text))
            a_manage = QAction(f'管理"{text}"', self)
            a_manage.triggered.connect(
                lambda: self.open_version_manager(text))
            menu.addAction(a_launch)
            menu.addAction(a_manage)
            menu.exec_(QCursor.pos())

    def launch_game(self, version):
        g.dmgr.add_task(f"启动{version}", Launch(
            version), "launch", (g.java_path,
                                 g.cur_user["name"],
                                 g.width,
                                 g.height,
                                 g.maxmem,
                                 g.minmem))

    def open_version_manager(self, name):
        if name:
            try:
                versionmanager = VersionManager(name)
                versionmanager.GameDeleted.connect(self.set_versions)
                versionmanager.show()
            except Exception as e:
                self.notify("错误", e)
