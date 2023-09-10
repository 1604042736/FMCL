from Kernel import Kernel
from qfluentwidgets import LineEdit

from .SettingCard import SettingCard


class StrSettingCard(SettingCard):
    def __init__(self, id: str, setting) -> None:
        super().__init__(id, setting)
        self.w_value = LineEdit(self)
        self.w_value.setText(self.setting.get(id))
        self.w_value.editingFinished.connect(self.sync)
        self._layout.addWidget(self.w_value)

        self.setToolTip(self.tr("输入完后按回车键以保存"))

    def sync(self):
        self.setting.set(self.id, self.w_value.text())
        return super().sync()

    def refresh(self):
        self.w_value.setText(self.setting.get(self.id))
        return super().refresh()
