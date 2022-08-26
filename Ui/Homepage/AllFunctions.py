from importlib import import_module
import os
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.Mods import Mods
from Ui.About.About import About
from PyQt5.QtWidgets import QListWidgetItem, QListWidget, QListView
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent
from Ui.Help.Help import Help

from Ui.News.News import News


class AllFunctions(QListWidget, QFBNWidget):

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

        self.setMovement(QListView.Static)
        self.setViewMode(QListView.IconMode)

        self.set_functions()
        self.itemClicked.connect(self.launch_function)

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
        for key, val in self.functions.items():
            item = QListWidgetItem()
            item.setText(key)
            if "icon_exp" in val.__dict__:
                item.setIcon(eval(val.icon_exp))
            self.addItem(item)

    def launch_function(self, item):
        self.functions[item.text()]().show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.set_functions()
