from PyQt5.QtWidgets import QLineEdit

from .SettingItem import SettingItem


class StrSettingItem(SettingItem):
    def __init__(self, id: str, setting: dict) -> None:
        super().__init__(id, setting)
        self.w_value = QLineEdit(self)
        self.w_value.setText(self.setting["value"])
        self.w_value.textChanged.connect(self.sync)

        self.cur_layout.addWidget(self.w_value, 0, 1)

    def sync(self):
        self.setting["value"] = self.w_value.text()
        return super().sync()
