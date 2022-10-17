from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QLabel

from ..SettingWidgets import SettingWidget
from .SettingItem import SettingItem


class DictSettingItem(SettingItem):
    def __init__(self, id: str, setting: dict) -> None:
        super().__init__(id, setting)

        font = self.l_name.font()
        font.setBold(True)
        font.setPixelSize(16)
        self.l_name.setFont(font)

        self.l_content = QLabel()
        contents = []
        for _, val in self.setting["value"].items():
            contents.append(val["name"])
        self.l_content.setText(",".join(contents)+"...")
        self.cur_layout.addWidget(self.l_content)

    def mousePressEvent(self, a0: QMouseEvent) -> None:
        SettingWidget(self.id, self.setting["value"]).show()
        return super().mousePressEvent(a0)
