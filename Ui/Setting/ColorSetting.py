from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QColorDialog
import Globals as g
from Translate import tr
from .SettingItem import SettingItem


class ColorSetting(SettingItem):
    def __init__(self, id, name, val, do_after_save=None, target=g, parent=None) -> None:
        super().__init__(id, name, val, do_after_save, target, parent)

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(self.name)

        self.l_color = QLabel(self)
        self.l_color.setStyleSheet(f"background-color:{self.val}")

        self.pb_change = QPushButton(self)
        self.pb_change.setText(tr("更改"))
        self.pb_change.clicked.connect(self.save)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.l_color)
        self.hbox.addWidget(self.pb_change)

        self.setLayout(self.hbox)

    def save(self):
        color = QColorDialog.getColor().getRgb()
        if color != (0, 0, 0, 255):
            self.val = f"rgba({','.join(map(str,color))})"
            self.l_color.setStyleSheet(f"background-color:{self.val}")
            setattr(self.target, self.id, self.val)
        super().save()
