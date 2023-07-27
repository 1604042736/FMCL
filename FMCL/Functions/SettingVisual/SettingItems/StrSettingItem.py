from Kernel import Kernel
from qfluentwidgets import LineEdit

from .SettingItem import SettingItem

_translate = Kernel.translate


class StrSettingItem(SettingItem):
    def __init__(self, id: str, setting) -> None:
        super().__init__(id, setting)
        self.w_value = LineEdit(self)
        self.w_value.setText(self.setting.get(id))
        self.w_value.editingFinished.connect(self.sync)
        self._layout.addWidget(self.w_value)

        self.setToolTip(_translate("输入完后按回车键以保存"))

    def sync(self):
        self.setting.set(self.id, self.w_value.text())
        return super().sync()

    def refresh(self):
        self.w_value.setText(self.setting.get(self.id))
        return super().refresh()
