from PyQt5.QtWidgets import QWidget, QListWidgetItem
from .ui_Downloader import Ui_Downloader
import qtawesome as qta
from Core import Game
from PyQt5.QtCore import pyqtSlot


class Downloader(QWidget, Ui_Downloader):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.download-simple"))
        self.setVersions()
        self.setFabric()

    def setVersions(self):
        self.lw_minecraft.clear()
        self.lw_minecraft.addItems(Game.get_versions())
        self.lw_minecraft.setCurrentRow(0)

    def setFabric(self):
        self.lw_fabric.clear()
        self.lw_fabric.addItems(Game.get_fabric())

    @pyqtSlot(QListWidgetItem, QListWidgetItem)
    def on_lw_minecraft_currentItemChanged(self, current, previous):
        version = current.text()
        self.lw_forge.clear()
        self.lw_forge.addItems(Game.get_forge(version))

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
            Game(name).install(version, forge_version, fabric_version)
