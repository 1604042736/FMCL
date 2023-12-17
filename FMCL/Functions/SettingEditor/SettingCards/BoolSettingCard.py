from qfluentwidgets import CheckBox
from .SettingCard import SettingCard


class BoolSettingCard(SettingCard):
    def __init__(self, id, setting) -> None:
        super().__init__(id, setting)
        self.w_value = CheckBox(self)
        self.w_value.setCheckState((0, 2)[self.setting.get(id)])
        self.w_value.stateChanged.connect(self.sync)
        self._layout.addWidget(self.w_value)

    def sync(self):
        self.setting.set(self.id, (False, True, True)[self.w_value.checkState()])
        return super().sync()

    def refresh(self):
        self.w_value.stateChanged.disconnect(self.sync)
        self.w_value.setCheckState((0, 2)[self.setting.get(self.id)])
        self.w_value.stateChanged.connect(self.sync)
        return super().refresh()
