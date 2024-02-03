from PyQt5.QtWidgets import QWidget

from .ui_VersionItem import Ui_VersionItem


class VersionItem(QWidget, Ui_VersionItem):
    def __init__(self, version: dict):
        super().__init__()
        self.setupUi(self)
        self.version = version
