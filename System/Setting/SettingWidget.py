import qtawesome as qta
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QLabel, QTreeWidgetItem, QWidget
from System.Constants import *

from .ui_SettingWidget import Ui_SettingWidget


class SettingWidget(QWidget, Ui_SettingWidget):
    def __init__(self, setting):
        super().__init__()
        self.setupUi(self)
        self.resize(W_SETTING, H_SETTING)
        self.setWindowIcon(qta.icon("ri.settings-5-line"))
        self.setting = setting
        self.items = {}
        self.item_widget_id = []
        self.setting_items = []

        for id, val in self.setting.setting.items():
            splitids = id.split(".")
            for i, splitid in enumerate(splitids):
                totalid = ".".join(splitids[:i+1])
                lastid = ".".join(splitids[:i])
                if totalid in self.items:
                    continue

                root = self.items.get(("???", lastid)[i-1 >= 0], None)
                item = QTreeWidgetItem()
                text = self.setting.getAttr(totalid, "name")
                item.setText(0, text)
                self.addTreeItem(root, item)
                self.items[totalid] = item

                widget = QLabel()
                widget.setText(text)
                self.gl_setting.addWidget(widget)
                self.item_widget_id.append((item, widget, totalid))

            setting_item = self.setting.getAttr(id, "setting_item")()
            self.gl_setting.addWidget(setting_item)
            self.setting_items.append(setting_item)

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_setting.addTopLevelItem(item)
        else:
            root.addChild(item)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_setting_itemClicked(self, item, _):
        for item_, widget, _ in self.item_widget_id:
            if item_ == item:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break

    def show(self, id="") -> None:
        for _, widget, id_ in self.item_widget_id:
            if id_ == id:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break
        return super().show()

    def refresh(self):
        for i in self.setting_items:
            if hasattr(i, "refresh"):
                i.refresh()

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self):
        self.refresh()
