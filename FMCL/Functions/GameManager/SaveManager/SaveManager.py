import os
from Core import Version
from Setting import Setting
from Events import *
import qtawesome as qta
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, qApp, QLabel, QHBoxLayout
from qfluentwidgets import TransparentToolButton
from .ui_SaveManager import Ui_SaveManager
from .SaveItem import SaveItem


class NBTItem(QWidget):
    def __init__(self, key, val):
        super().__init__()
        self.hboxlayout = QHBoxLayout(self)
        self.l_key = QLabel(text=str(key))
        self.l_val = QLabel()
        self.hboxlayout.addWidget(self.l_key)
        if not isinstance(val, (dict, list)):
            self.l_val.setText(str(val))
            self.hboxlayout.addWidget(self.l_val)
        self.resize(0, 42)


class SaveManager(QWidget, Ui_SaveManager):
    def __init__(self, name, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.save"))

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.name = name
        self.game = Version(name)
        self.refresh()

    def refresh(self):
        def show_full_save_info(parent: QTreeWidgetItem, data: dict | list):
            if isinstance(data, dict):
                for key, val in data.items():
                    item = QTreeWidgetItem()
                    widget = NBTItem(key, val)
                    item.setSizeHint(0, widget.size())
                    parent.addChild(item)
                    self.tw_saves.setItemWidget(item, 0, widget)
                    if isinstance(val, (dict, list)):
                        show_full_save_info(item, val)
            elif isinstance(data, list):
                for i, val in enumerate(data):
                    item = QTreeWidgetItem()
                    widget = NBTItem(str(i), val)
                    item.setSizeHint(0, widget.size())
                    parent.addChild(item)
                    self.tw_saves.setItemWidget(item, 0, widget)
                    if isinstance(val, (dict, list)):
                        show_full_save_info(item, val)

        self.tw_saves.clear()
        save_path = self.game.get_save_path()
        for save in os.listdir(save_path):
            path = os.path.join(save_path, save)
            if not os.path.isdir(path):
                continue
            item = QTreeWidgetItem()
            widget = SaveItem(path)
            widget.saveDeleted.connect(self.refresh)
            item.setSizeHint(0, widget.size())
            self.tw_saves.addTopLevelItem(item)
            self.tw_saves.setItemWidget(item, 0, widget)
            if Setting()["gamemanager.savemanager.show_full_save_info"]:
                show_full_save_info(item, widget.save.level_json)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)
