from Kernel import Kernel
from PyQt5.QtWidgets import QColorDialog, QLabel
from qfluentwidgets import ColorDialog, PushButton

from .SettingItem import SettingItem

_translate = Kernel.translate


class ColorSettingItem(SettingItem):
    def __init__(self, id, setting) -> None:
        super().__init__(id, setting)
        self.color = self.setting.get(id)
        self.l_color = QLabel()
        self.l_color.setStyleSheet(
            f"QLabel{{background-color:{self.color};}}")
        self._layout.addWidget(self.l_color, 0, 0)

        self.pb_choosecolor = PushButton()
        self.pb_choosecolor.setText(_translate("选择颜色"))
        self.pb_choosecolor.clicked.connect(self.chooseColor)
        self._layout.addWidget(self.pb_choosecolor, 0, 1)

    def sync(self):
        self.setting.set(self.id, self.color)
        return super().sync()

    def refresh(self):
        self.color = self.setting.get(self.id)
        self.l_color.setStyleSheet(
            f"QLabel{{background-color:{self.color};}}")
        return super().refresh()

    def chooseColor(self):
        def changeColor(color):
            self.color = color.name()
            self.l_color.setStyleSheet(
                f"QLabel{{background-color:{self.color};}}")
            self.sync()
        colordialog = ColorDialog(
            self.color, _translate("选择颜色"), self.window())
        colordialog.colorChanged.connect(changeColor)
        colordialog.exec()
