import logging
import os

import multitasking
from Core import Game
from Kernel import Kernel
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import MessageBox

from .ui_ModItem import Ui_ModItem

_translate = Kernel.translate


class ModItem(QWidget, Ui_ModItem):
    modDeleted = pyqtSignal()

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
            self.game.setModEnabled(self.modenabled, self.modname)

    @multitasking.task
    def setInfo(self):
        try:
            info = self.game.get_mod_info(self.modname, self.modenabled)
            info_list = []
            info_list.append(info["name"])
            info_list.append(info["description"].replace("\n", ""))
            info_list.append(_translate("版本")+": "+info["version"])
            info_list.append(_translate("作者")+": " +
                             ','.join(info["authors"]))

            text = ", ".join(info_list)
            self.l_info.setText(text)
            self.setToolTip(text)
        except Exception as e:
            logging.error(f'无法获取"{self.modname}"信息: {e}')

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        def confirmDelete():
            path = os.path.join(self.game.get_mod_path(),
                                self.modname+(".disabled" if not self.modenabled else ""))
            logging.info(f"删除{path}")
            os.remove(path)
            self.modDeleted.emit()
        box = MessageBox(_translate("删除"),
                         _translate("确认删除")+self.modname+"?",
                         self.window())
        box.yesSignal.connect(confirmDelete)
        box.exec()
