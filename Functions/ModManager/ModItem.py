import logging

import multitasking
from Core import Game
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_ModItem import Ui_ModItem

_translate = QCoreApplication.translate


class ModItem(QWidget, Ui_ModItem):
    def __init__(self, game: Game, modenabled: bool, modname: str):
        super().__init__()
        self.setupUi(self)

        self.game = game
        self.modenabled = modenabled
        self.modname = modname

        self.cb_modenabled.setCheckState((0, 2)[modenabled])
        self.l_modname.setText(modname)
        self.setInfo()

    @pyqtSlot(int)
    def on_cb_modenabled_stateChanged(self, _):
        modenabled = (False, True, True)[self.cb_modenabled.checkState()]
        if modenabled != self.modenabled:
            self.modenabled = modenabled
            self.game.setModEnalbed(self.modenabled, self.modname)

    @multitasking.task
    def setInfo(self):
        try:
            info = self.game.get_mod_info(self.modname, self.modenabled)
            info_list = []
            info_list.append(info["name"])
            info_list.append(info["description"].replace("\n", ""))
            info_list.append(_translate("ModItem", "版本")+": "+info["version"])
            info_list.append(_translate("ModItem", "作者")+": " +
                             ','.join(info["authors"]))

            text = ", ".join(info_list)
            self.l_info.setText(text)
            self.setToolTip(text)
        except Exception as e:
            logging.error(f'无法获取"{self.modname}"信息: {e}')
