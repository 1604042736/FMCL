import logging
import traceback
import webbrowser

import multitasking
import qtawesome as qta
from Core import Mod, Version
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_ModItem import Ui_ModItem


class ModItem(QWidget, Ui_ModItem):
    enabledChanged = pyqtSignal(bool)
    __infoSetFinished = pyqtSignal()

    def __init__(self, game: Version, mod: Mod):
        super().__init__()
        self.setupUi(self)
        self.pb_url.setIcon(qta.icon("mdi6.web"))

        self.game = game
        self.mod = mod
        self.url = ""

        self.cb_modenabled.setCheckState((0, 2)[self.mod.enabled])
        self.l_modname.setText(self.mod.name)
        self.pb_url.hide()
        self.__infoSetFinished.connect(lambda: self.pb_url.show() if self.url else None)
        self.setInfo()

    @pyqtSlot(int)
    def on_cb_modenabled_stateChanged(self, _):
        modenabled = (False, True, True)[self.cb_modenabled.checkState()]
        if modenabled != self.mod.enabled:
            self.mod.set_enabled(modenabled)
            self.enabledChanged.emit(modenabled)

    @multitasking.task
    def setInfo(self):
        try:
            info = self.mod.get_info()
            info_list = []
            if info["name"]:
                info_list.append(self.mod.name)
                self.l_modname.setText(info["name"])
            if info["description"]:
                info_list.append(info["description"].replace("\n", ""))
            if info["version"]:
                info_list.append(self.tr("版本") + ": " + info["version"])
            if info["authors"]:
                try:
                    while not isinstance(info["authors"][0], str):  # 可能是嵌套列表
                        info["authors"] = info["authors"][0]
                    info_list.append(self.tr("作者") + ": " + ",".join(info["authors"]))
                except:  # 防止一些奇奇怪怪的错误
                    logging.error(
                        f"{self.mod.name}: {info['authors']=} :\n{traceback.format_exc()}"
                    )
            if info["icon"] != None:
                self.l_icon.setPixmap(info["icon"].scaled(64, 64))
            self.url = info["url"]

            text = ", ".join(info_list)
            self.l_info.setText(text)
            self.setToolTip(text)
        except:
            logging.error(f'无法获取"{self.mod.name}"信息:\n{traceback.format_exc()}')
        self.__infoSetFinished.emit()

    @pyqtSlot(bool)
    def on_pb_url_clicked(self, _):
        if self.url:
            webbrowser.open(self.url)
