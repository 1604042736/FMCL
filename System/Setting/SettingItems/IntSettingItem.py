from PyQt5.QtWidgets import QSpinBox

from .SettingItem import SettingItem


class IntSettingItem(SettingItem):
    def __init__(self, id:str,setting: dict) -> None:
        super().__init__(id,setting)
        self.w_value = QSpinBox(self)
        self.w_value.setMaximum(2**31-1)
        self.w_value.setMinimum(-2**31)
        self.w_value.setValue(self.setting["value"])
        self.w_value.valueChanged.connect(self.sync)

        self.cur_layout.addWidget(self.w_value, 0, 1)

    def sync(self):
        self.setting["value"]=self.w_value.value()
        return super().sync()
