from importlib import import_module
import os
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.Mods import Mods
from Ui.About.About import About
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QAbstractItemView
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent
from Ui.Help.Help import Help

from Ui.News.News import News


class AllFunctions(QTableWidget, QFBNWidget):
    UNIT_WIDTH = 64

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("所有应用"))
        self.setWindowIcon(qta.icon("mdi.format-list-checkbox"))
        self.functions = {
            tr("下载Minecraft"): Minecraft,
            tr("下载Mod"): Mods,
            tr("关于"): About,
            tr("新闻"): News,
            tr("帮助"): Help
        }
        self.get_functions()

        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(self.UNIT_WIDTH)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(self.UNIT_WIDTH)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(self.UNIT_WIDTH)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setMinimumSectionSize(self.UNIT_WIDTH)

        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.set_functions()
        self.cellClicked.connect(self.launch_function)

    def get_functions(self):
        """从FMCL/Function中获取功能"""
        try:
            for i in os.listdir("FMCL/Function"):
                if i != "__init__.py" and i.endswith(".py"):
                    module = import_module(
                        f"FMCL.Function.{os.path.splitext(i)[0]}")
                    config = module.config
                    self.functions[config["name"]] = getattr(
                        module, config["mainclass"])
            if not os.path.exists("FMCL/__init__.py"):
                with open("FMCL/__init__.py", "w", encoding='utf-8'):
                    pass
            if not os.path.exists("FMCL/Function/__init__.py"):
                with open("FMCL/Function/__init__.py", "w", encoding='utf-8'):
                    pass
        except:
            pass

    def set_functions(self):
        self.clear()
        self.row_count = 1
        self.col_count = 1
        j = 0
        for key, val in self.functions.items():
            if j == self.max_col_count:
                j = 0
                self.row_count += 1
            elif j == self.col_count:
                self.col_count += 1
            self.setRowCount(self.row_count)
            self.setColumnCount(self.col_count)
            item = QTableWidgetItem()
            item.setText(key)
            if "icon_exp" in val.__dict__:
                item.setIcon(eval(val.icon_exp))
            self.setItem(self.row_count-1, j, item)
            j += 1

    def launch_function(self, row, col):
        self.functions[self.item(row, col).text()]().show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_functions()
