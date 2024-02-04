from qfluentwidgets import ColorDialog

from .SettingCard import SettingCard

from .ui_ColorSettingCard import Ui_ColorSettingCard


class ColorSettingCard(SettingCard, Ui_ColorSettingCard):
    def __init__(self, getter, attrgetter, setter,attrsetter) -> None:
        super().__init__( getter, attrgetter, setter,attrsetter)
        self.setupUi(self)

        self.color = self.getter()
        self.l_color.setStyleSheet(f"QLabel{{background-color:{self.color};}}")

        self.pb_choosecolor.clicked.connect(self.chooseColor)

    def refresh(self):
        self.color = self.getter()
        self.l_color.setStyleSheet(f"QLabel{{background-color:{self.color};}}")
        return super().refresh()

    def chooseColor(self):
        def changeColor(color):
            self.color = color.name()
            self.l_color.setStyleSheet(f"QLabel{{background-color:{self.color};}}")
            self.sync()
            self.on_valueChanged()

        colordialog = ColorDialog(self.color, self.tr("选择颜色"), self.window())
        colordialog.colorChanged.connect(changeColor)
        colordialog.exec()

    def value(self):
        return self.color