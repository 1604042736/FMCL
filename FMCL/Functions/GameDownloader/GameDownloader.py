import multitasking
import qtawesome as qta
from Core import Version
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QWidget

from .ui_GameDownloader import Ui_GameDownloader


class GameDownloader(QWidget, Ui_GameDownloader):
    __addItems = pyqtSignal(QListWidget, list)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.download-simple"))
        self.__addItems.connect(lambda a, b: a.addItems(b))
        self.setVersions()
        self.setFabric()

    @multitasking.task
    def setVersions(self):
        self.lw_minecraft.clear()
        self.__addItems.emit(self.lw_minecraft, Version.get_versions())

    @multitasking.task
    def setFabric(self):
        self.lw_fabric.clear()
        self.lw_fabric.addItems(Version.get_fabric())

    @multitasking.task
    def setForge(self, version):
        self.lw_forge.clear()
        self.lw_forge.addItems(Version.get_forge(version))

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_lw_minecraft_currentItemChanged(self, current, previous):
        version = current.text()
        self.setForge(version)

    @pyqtSlot(bool)
    def on_pb_install_clicked(self, _):
        name = self.le_name.text()
        if self.lw_minecraft.currentItem():
            version = self.lw_minecraft.currentItem().text()
            forge_version = fabric_version = ""
            if self.lw_forge.currentItem():
                forge_version = self.lw_forge.currentItem().text()
            if self.lw_fabric.currentItem():
                fabric_version = self.lw_fabric.currentItem().text()
            Version(name).install(version, forge_version, fabric_version)
