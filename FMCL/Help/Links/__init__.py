import webbrowser
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_Links import Ui_Links

_translate = QCoreApplication.translate


class Links(QWidget, Ui_Links):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_pb_mcofficialweb_clicked(self, _):
        webbrowser.open("https://www.minecraft.net/")

    @pyqtSlot(bool)
    def on_pb_wiki_clicked(self, _):
        webbrowser.open("https://minecraft.wiki/")

    @pyqtSlot(bool)
    def on_pb_mcmod_clicked(self, _):
        webbrowser.open("https://www.mcmod.cn/")

    @pyqtSlot(bool)
    def on_pb_plugin_clicked(self, _):
        webbrowser.open("https://mineplugin.org/")

    @pyqtSlot(bool)
    def on_pb_javaofficialweb_clicked(self, _):
        webbrowser.open("https://www.java.com/")

    @pyqtSlot(bool)
    def on_pb_openjdk_clicked(self, _):
        webbrowser.open("https://openjdk.org/")

    @pyqtSlot(bool)
    def on_pb_azul_clicked(self, _):
        webbrowser.open("https://www.azul.com/")

    @pyqtSlot(bool)
    def on_pb_dragonwell_clicked(self, _):
        webbrowser.open("https://dragonwell-jdk.io/")

    @pyqtSlot(bool)
    def on_pb_graalvm_clicked(self, _):
        webbrowser.open("https://www.graalvm.org/")

    @pyqtSlot(bool)
    def on_pb_modrinth_clicked(self, _):
        webbrowser.open("https://modrinth.com/")

    @pyqtSlot(bool)
    def on_pb_curseforge_clicked(self, _):
        webbrowser.open("https://www.curseforge.com/minecraft/")


def helpIndex():
    return {
        "links": {
            "name": _translate("LinksHelp", "常用网站"),
            "page": Links,
        }
    }
