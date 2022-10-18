from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel

from ..SettingWidgets.ListSettingWidget import ListSettingWidget
from .SettingItem import SettingItem


class ListSettingItem(SettingItem):
    def __init__(self, id: str, setting: dict) -> None:
        super().__init__(id, setting)

        self.cur_layout.addWidget(ListSettingWidget(
            self.id, self.setting["value"]))