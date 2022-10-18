from PyQt5.QtWidgets import QCheckBox

from .SettingItem import SettingItem


class BoolSettingItem(SettingItem):
    def __init__(self, id: str, setting: dict) -> None:
        super().__init__(id, setting)
        self.w_value = QCheckBox(self)
        self.w_value.setCheckState((0, 2)[self.setting["value"]])
        self.w_value.stateChanged.connect(self.sync)

        self.cur_layout.addWidget(self.w_value)

    def sync(self):
        self.setting["value"] = (False, True, True)[self.w_value.checkState()]
        return super().sync()

    def refresh(self):
        self.w_value.setCheckState((0, 2)[self.setting["value"]])
        return super().refresh()