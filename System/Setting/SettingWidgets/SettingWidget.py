import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QEvent, pyqtSlot
from PyQt5.QtWidgets import QLabel, QTreeWidgetItem, QWidget
from System.Constants import *

from ..SettingItems import SettingItem
from .ui_SettingWidget import Ui_SettingWidget

_translate = QCoreApplication.translate


class SettingWidget(QWidget, Ui_SettingWidget):
    def __init__(self, id: str, value):
        super().__init__()
        self.setupUi(self)
        self.id = id  # 设置项的名称
        self.value = value

        self.resize(W_SETTING, H_SETTING)
        self.setWindowIcon(qta.icon("ri.settings-5-line"))
        self.setWindowTitle(_translate('Setting', '设置'))

        self.item_widget = []
        for key, val in self.value.items():
            self.addSettingItem(val, key)

    def refresh(self):
        for child in self.w_setting.findChildren(QWidget):
            if hasattr(child, "refresh"):
                child.refresh()
        self.sync()

    def addSettingItem(self, value: dict, key, root=None):
        item = QTreeWidgetItem()
        text = value["name"]
        item.setText(0, text)
        if root == None:
            self.tw_setting.addTopLevelItem(item)

            label = QLabel()
            label.setText(text)
            font = label.font()
            font.setBold(True)
            font.setPixelSize(16)
            label.setFont(font)
            self.gl_setting.addWidget(label)
            self.item_widget.append((item, label, key))
        else:
            root.addChild(item)
        id = f"{self.id}.{key}"
        if not isinstance(value["value"], dict):
            widget = SettingItem(f"{id}.{key}", value)
            self.gl_setting.addWidget(widget)
            return
        for key, val in value["value"].items():
            if isinstance(val["value"], dict):
                self.addSettingItem(val, key, item)
            widget = SettingItem(f"{id}.{key}", val)
            self.gl_setting.addWidget(widget)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_tw_setting_itemClicked(self, item, _):
        for item_, widget, _ in self.item_widget:
            if item_ == item:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break

    def show(self, id="") -> None:
        for _, widget, id_ in self.item_widget:
            if id_ == id:
                self.sa_setting.verticalScrollBar().setValue(widget.pos().y())
                break
        return super().show()

    def sync(self):
        from ..Setting import Setting
        Setting(self.id.split("#")[0]).sync()

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)
