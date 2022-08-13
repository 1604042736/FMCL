from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
import Globals as g
from .SettingItem import SettingItem


class StrSetting(SettingItem):
    """类型为字符串的设置"""

    def __init__(self, id, name, val, do_after_save=None, target=g, parent=None) -> None:
        super().__init__(id, name, val, do_after_save, target, parent)

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.le_val = QLineEdit(self)
        self.le_val.textEdited.connect(self.save)
        self.le_val.setText(val)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.le_val)

        self.setLayout(self.hbox)

    def save(self) -> tuple:
        setattr(g, self.id, self.le_val.text())
        super().save()
