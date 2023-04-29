from PyQt5.QtWidgets import QColorDialog, QLabel, QPushButton
from .SettingItem import SettingItem
from Kernel import Kernel
_translate = Kernel.translate


class ColorSettingItem(SettingItem):
    def __init__(self, id, setting) -> None:
        super().__init__(id, setting)
        self.color = self.setting.get(id)
        self.l_color = QLabel()
        self.l_color.setStyleSheet(
            f"QLabel{{background-color:{self.color};}}")
        self._layout.addWidget(self.l_color, 0, 0)

        self.pb_choosecolor = QPushButton()
        self.pb_choosecolor.setText(_translate("选择颜色"))
        self.pb_choosecolor.clicked.connect(self.chooseColor)
        self._layout.addWidget(self.pb_choosecolor, 0, 1)

    def sync(self):
        self.setting.set(self.id, self.color)
        return super().sync()

    def refresh(self):
        self.color = self.setting.get(id)
        self.l_color.setStyleSheet(
            f"QLabel{{background-color:{self.color};}}")
        return super().refresh()

    def chooseColor(self):
        color = QColorDialog.getColor()
        if color.name() != "#000000":
            self.color = color.name()
            self.l_color.setStyleSheet(
                f"QLabel{{background-color:{self.color};}}")
            self.sync()
