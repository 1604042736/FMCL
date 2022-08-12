from importlib import import_module
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Help.HelpInfo import HelpInfo
from Ui.Help.ui_Help import Ui_Help
from Translate import tr
import qtawesome as qta
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from Ui.AllHelp import allhelp
from PyQt5.QtCore import QSize


class Help(QFBNWidget, Ui_Help):
    icon_exp = 'qta.icon("mdi6.help-circle-outline")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("帮助"))
        self.setWindowIcon(eval(self.icon_exp))

        self.tb_allhelp.removeItem(0)

        self.set_help()

    def set_help(self):
        # 思路同ModDetail
        self.help_groups = {}
        for i in allhelp:
            if isinstance(i, str):
                module = import_module(i)
            else:
                module = i
            if not hasattr(module, "config"):
                continue

            config = module.config
            if config["type"] not in self.help_groups:
                lw = QListWidget()
                self.help_groups[config["type"]] = lw
            lw = self.help_groups[config["type"]]
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = HelpInfo(module)
            lw.addItem(item)
            lw.setItemWidget(item, widget)

        for key, val in self.help_groups.items():
            self.tb_allhelp.addItem(val, key)
