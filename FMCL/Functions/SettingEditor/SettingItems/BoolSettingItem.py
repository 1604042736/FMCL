from qfluentwidgets import CheckBox
from .SettingItem import SettingItem


class BoolSettingItem(SettingItem):
    def __init__(self, id, setting) -> None:
        super().__init__(id, setting)
        self.w_value = CheckBox(self)
        self.w_value.setCheckState((0, 2)[self.setting.get(id)])
        self.w_value.stateChanged.connect(self.sync)
        self._layout.addWidget(self.w_value)

    def sync(self):
        self.setting.set(self.id, (False, True, True)
                         [self.w_value.checkState()])
        return super().sync()

    def refresh(self):
        self.w_value.setCheckState((0, 2)[self.setting.get(self.id)])
        return super().refresh()
