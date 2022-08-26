from Core.Game import Game
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Desktop.Desktop import Desktop
from Ui.Downloader.ui_Minecraft import Ui_Minecraft
import Globals as g
from PyQt5.QtWidgets import QComboBox
import qtawesome as qta
from Translate import tr
from ..Setting.BoolSetting import BoolSetting


class Minecraft(QFBNWidget, Ui_Minecraft):
    icon_exp = 'qta.icon("mdi.minecraft")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowIcon(eval(self.icon_exp))

        self.isolate = False
        self.isolate_setting = BoolSetting(
            "isolate", tr("版本隔离"), self.isolate, target=self)
        self.gridLayout_2.addWidget(self.isolate_setting, 1, 0, 1, 1)

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
        g.dmgr.add_task(tr("下载")+name, Game(
            name, version, forge_version, fabric_version, optifine_version, self.isolate), "download_version", tuple())


Desktop.blankrightmenu[tr("下载Minecraft")] = (
    Minecraft.icon_exp, lambda: Minecraft().show())
