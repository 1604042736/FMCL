from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox
import Globals as g
from .SettingItem import SettingItem


class IntSetting(SettingItem):
    """类型为int的设置"""

    def __init__(self, id, name, val, do_after_save=None, target=g, parent=None) -> None:
        super().__init__(id, name, val, do_after_save, target, parent)

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.sb_val = QSpinBox(self)
        self.sb_val.setMaximum(2**31-1)
        self.sb_val.setValue(val)
        self.sb_val.valueChanged.connect(self.save)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.sb_val)

        self.setLayout(self.hbox)

    def save(self):
        setattr(self.target, self.id, self.sb_val.value())
        super().save()
