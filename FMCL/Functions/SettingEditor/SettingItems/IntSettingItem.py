from qfluentwidgets import SpinBox

from .SettingItem import SettingItem


class IntSettingItem(SettingItem):
    def __init__(self, id: str, setting) -> None:
        super().__init__(id, setting)
        self.w_value = SpinBox(self)
        self.w_value.setMaximum(2**31-1)
        self.w_value.setMinimum(-2**31)
        self.w_value.setValue(self.setting.get(id))
        self.w_value.valueChanged.connect(self.sync)
        self._layout.addWidget(self.w_value)

    def sync(self):
        self.setting.set(self.id, self.w_value.value())
        return super().sync()

    def refresh(self):
        self.w_value.setValue(self.setting.get(self.id))
        return super().refresh()
