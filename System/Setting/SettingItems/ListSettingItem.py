from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel

from ..SettingWidgets import SettingWidget
from .SettingItem import SettingItem


class ListSettingItem(SettingItem):
    def __init__(self, id: str, setting: dict) -> None:
        super().__init__(id, setting)

        font = self.l_name.font()
        font.setBold(True)
        font.setPixelSize(16)
        self.l_name.setFont(font)

        self.l_description = QLabel(self)
        self.l_description.setText(setting["description"])
        self.cur_layout.addWidget(self.l_description)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        SettingWidget(self.id, self.setting["value"]).show()
        return super().mousePressEvent(a0)
