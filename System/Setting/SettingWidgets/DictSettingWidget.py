from .SettingWidget import SettingWidget
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QResizeEvent
from ..SettingItems import SettingItem


class DictSettingWidget(SettingWidget):
    def __init__(self, id, value):
        if SettingWidget.new_count[id] > 1:
            return
        super().__init__(id, value)

        self.lw_value = QListWidget(self)
        self.min_height = 0

        self.refresh()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.lw_value.resize(self.size())
        return super().resizeEvent(a0)

    def refresh(self):
        self.lw_value.clear()
        self.min_height = 0
        for key, val in self.value.items():
            item = QListWidgetItem()
            widget = SettingItem(self.id+"/"+key, val)
            item.setSizeHint(widget.size())
            self.min_height += widget.height()
            self.lw_value.addItem(item)
            self.lw_value.setItemWidget(item, widget)
        if self.parent():
            self.setMinimumHeight(self.min_height)
        else:
            self.setMinimumHeight(0)
