from PyQt5.QtWidgets import QWidget, QGridLayout
from qfluentwidgets import ComboBox

from Setting import Setting


class ThemeChooser(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QGridLayout())

        self.cb_theme = ComboBox()
        self.cb_theme.addItems([self.tr("跟随系统"), self.tr("浅色"), self.tr("深色")])
        self.theme_index = ["Auto", "Light", "Dark"]
        self.cb_theme.setCurrentIndex(
            self.theme_index.index(Setting().get("system.theme"))
        )
        self.cb_theme.currentIndexChanged.connect(self.changeTheme)
        self.layout().addWidget(self.cb_theme)

        self.refresh()

    def refresh(self):
        i = self.theme_index.index(Setting().get("system.theme"))
        if i != self.cb_theme.currentIndex():
            self.cb_theme.setCurrentIndex(i)

    def changeTheme(self):
        Setting().set("system.theme", self.theme_index[self.cb_theme.currentIndex()])
