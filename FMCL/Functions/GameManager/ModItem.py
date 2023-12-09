import logging
import traceback
import webbrowser

import multitasking
import qtawesome as qta
from Core import Game
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_ModItem import Ui_ModItem


class ModItem(QWidget, Ui_ModItem):
    enabledChanged = pyqtSignal(bool)
    __infoSetFinished = pyqtSignal()

    def __init__(self, game: Game, modenabled: bool, modname: str):
        super().__init__()
        self.setupUi(self)
        self.pb_url.setIcon(qta.icon("mdi6.web"))

        self.game = game
        self.modenabled = modenabled
        self.modname = modname
        self.url = ""

        self.cb_modenabled.setCheckState((0, 2)[modenabled])
        self.l_modname.setText(modname.replace('.jar', ""))
        self.pb_url.hide()
        self.__infoSetFinished.connect(
            lambda: self.pb_url.show() if self.url else None)
        self.setInfo()

    @pyqtSlot(int)
    def on_cb_modenabled_stateChanged(self, _):
        modenabled = (False, True, True)[self.cb_modenabled.checkState()]
        if modenabled != self.modenabled:
            self.modenabled = modenabled
            self.game.setModEnabled(self.modenabled, self.modname)
            self.enabledChanged.emit(self.modenabled)

    @multitasking.task
    def setInfo(self):
        try:
            info = self.game.get_mod_info(self.modname, self.modenabled)
            info_list = []
            if info["name"]:
                info_list.append(info["name"])
            if info["description"]:
                info_list.append(info["description"].replace("\n", ""))
            if info["version"]:
                info_list.append(self.tr("版本")+": "+info["version"])
            if info["authors"]:
                info_list.append(self.tr("作者")+": " +
                                 ','.join(info["authors"]))
            self.url = info["url"]

            text = ", ".join(info_list)
            self.l_info.setText(text)
            self.setToolTip(text)
        except:
            logging.error(
                f'无法获取"{self.modname}"信息: {traceback.format_exc()}')
        self.__infoSetFinished.emit()

    def getModFileName(self):
        """获取Mod文件名称"""
        return self.modname+(".disabled" if not self.modenabled else "")

    @pyqtSlot(bool)
    def on_pb_url_clicked(self, _):
        if self.url:
            webbrowser.open(self.url)
