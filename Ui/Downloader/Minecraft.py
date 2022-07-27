from Core.Game import Game
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.ui_Minecraft import Ui_Minecraft
import Globals as g
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QIcon
import Resources


class Minecraft(QFBNWidget, Ui_Minecraft):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(QIcon(":/Image/craft_table.png"))

        self.set_version()

        self.cb_minecraft.currentTextChanged.connect(self.set_other)
        self.pb_install.clicked.connect(self.install)

    @g.run_as_thread
    def set_version(self):
        self.cb_minecraft.clear()
        QComboBox.addItems(self.cb_minecraft, Game().get_versions())

    @g.run_as_thread
    def set_other(self, *_):
        version = self.cb_minecraft.currentText()
        self.cb_forge.clear()
        self.cb_optifine.clear()
        self.cb_liteloader.clear()
        self.cb_fabric.clear()

        self.cb_forge.addItems([""]+Game().get_forge(version))
        self.cb_optifine.addItems([""]+Game().get_optifine(version))
        self.cb_liteloader.addItems([""]+Game().get_liteloader(version))
        self.cb_fabric.addItems([""]+Game().get_fabric(version))

    def install(self):
        name = self.le_name.text()
        version = self.cb_minecraft.currentText()
        forge_version = self.cb_forge.currentText()
        fabric_version = self.cb_fabric.currentText()
        optifine_version = self.cb_optifine.currentText()
        g.dmgr.add_task(f"下载{name}", Game(
            name, version, forge_version, fabric_version, optifine_version), "download_version", tuple())
