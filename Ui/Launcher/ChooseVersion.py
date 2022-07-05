import os
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Launcher.VersionInfo import VersionInfo
from Ui.Launcher.ui_ChooseVersion import Ui_ChooseVersion
import Globals as g
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtWidgets import QListWidgetItem


class ChooseVersion(QFBNWidget, Ui_ChooseVersion):
    VersionChose = pyqtSignal(str)
    OpenVersionManager = pyqtSignal(str)
    DirectLaunch = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.lw_versions.itemDoubleClicked.connect(self.emit_chose_version)
        self.set_versions()

    def set_versions(self):
        self.lw_versions.clear()
        self.version_path = g.cur_gamepath+"/versions"
        if not os.path.exists(self.version_path):
            os.makedirs(self.version_path)
        for i in os.listdir(self.version_path):
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 64))
            widget = VersionInfo(i)
            widget.OpenVersionManager.connect(
                lambda a: self.OpenVersionManager.emit(a))
            widget.DirectLaunch.connect(lambda a: self.DirectLaunch.emit(a))
            self.lw_versions.addItem(item)
            self.lw_versions.setItemWidget(item, widget)

    def emit_chose_version(self, item):
        self.VersionChose.emit(self.lw_versions.itemWidget(item).name)
        self.close()
