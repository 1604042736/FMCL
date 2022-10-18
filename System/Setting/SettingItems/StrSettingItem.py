from PyQt5.QtWidgets import QLineEdit

from .SettingItem import SettingItem


class StrSettingItem(SettingItem):
    def __init__(self, id: str, setting) -> None:
        super().__init__(id, setting)
        self.w_value = QLineEdit(self)
        self.w_value.setText(self.setting.get(id))
        self.w_value.editingFinished.connect(self.sync)
        self._layout.addWidget(self.w_value)

    def sync(self):
        self.setting.set(self.id, self.w_value.text())
        return super().sync()

    def refresh(self):
        self.w_value.setValue(self.setting.get(self.id))
        return super().refresh()
