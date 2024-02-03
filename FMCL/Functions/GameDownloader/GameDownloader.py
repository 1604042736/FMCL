import os
import multitasking
import qtawesome as qta

from Core import Version
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from Setting import Setting

from .ui_GameDownloader import Ui_GameDownloader


class GameDownloader(QWidget, Ui_GameDownloader):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.download-simple"))
        self.default_name = ""
        self.setVersions()
        self.setFabric()
        self.setQuilt()

    @multitasking.task
    def setVersions(self):
        items = Version.get_versions()
        self.cb_minecraft.clear()
        self.cb_minecraft.addItems(items)
        self.set_name()

    @multitasking.task
    def setFabric(self):
        items = [""] + Version.get_fabric()  # 防止用户在获取版本时点击cb_fabric导致多出一个空项
        self.cb_fabric.clear()
        self.cb_fabric.addItems(items)

    @multitasking.task
    def setForge(self, version):
        items = [""] + Version.get_forge(version)  # 同理
        self.cb_forge.clear()
        self.cb_forge.addItems(items)

    @multitasking.task
    def setQuilt(self):
        items = [""] + Version.get_quilt()
        self.cb_quilt.clear()
        self.cb_quilt.addItems(items)

    @pyqtSlot(str)
    def on_cb_minecraft_currentTextChanged(self, text):
        self.setForge(text)
        self.set_name()

    @pyqtSlot(str)
    def on_cb_fabric_currentTextChanged(self, text):
        if text:
            self.cb_forge.setEnabled(False)
        else:
            self.cb_forge.setEnabled(True)
        self.set_name()

    @pyqtSlot(str)
    def on_cb_forge_currentTextChanged(self, text):
        if text:
            self.cb_fabric.setEnabled(False)
        else:
            self.cb_fabric.setEnabled(True)
        self.set_name()

    @pyqtSlot(str)
    def on_cb_quilt_currentTextChanged(self, text):
        self.set_name()

    @pyqtSlot(bool)
    def on_pb_install_clicked(self, _):
        name = self.le_name.text()
        Version(name).install(*self.get_versions())

    @pyqtSlot(str)
    def on_le_name_textChanged(self, name):
        self.l_warning.setText("")
        if name == "":
            return
        if os.path.exists(
            os.path.join(Setting().get("game.directories")[0], "versions", name)
        ):
            self.l_warning.setText(self.tr("该版本已存在, 继续安装将会覆盖原来内容"))

    def get_versions(self):
        version = self.cb_minecraft.currentText()
        forge_version = fabric_version = quilt_version = ""
        if self.cb_forge.currentText():
            forge_version = self.cb_forge.currentText()
        if self.cb_fabric.currentText():
            fabric_version = self.cb_fabric.currentText()
        if self.cb_quilt.currentText():
            quilt_version = self.cb_quilt.currentText()
        return version, forge_version, fabric_version, quilt_version

    def set_name(self):
        versions = self.get_versions()
        if self.le_name.text() == self.default_name:
            self.default_name = versions[0]
            if versions[1]:
                self.default_name += f"-Forge{versions[1].split('-')[-1]}"
            if versions[2]:
                self.default_name += f"-Fabric{versions[2]}"
            if versions[3]:
                self.default_name += f"-Quilt{versions[3]}"
            self.le_name.setText(self.default_name)
