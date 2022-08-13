from .SettingItem import SettingItem
from PyQt5.QtWidgets import QCheckBox, QVBoxLayout
from PyQt5.QtCore import Qt
import Globals as g


class BoolSetting(SettingItem):
    def __init__(self, id, name, val, do_after_save=None, target=g, parent=None) -> None:
        super().__init__(id, name, val, do_after_save, target, parent)

        self.vbox = QVBoxLayout(self)

        self.checkbox = QCheckBox(self)
        self.checkbox.setText(name)
        if val:
            self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.save)

        self.vbox.addWidget(self.checkbox)

    def save(self):
        self.val = self.checkbox.checkState()
        if self.val == Qt.Unchecked:
            self.val = False
        else:
            self.val = True
        setattr(self.target, self.id, self.val)
        return super().save()
