import os
import time
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from qfluentwidgets import MessageBox
from Core import Function, Save
from Kernel import Kernel

from .ui_SaveItem import Ui_SaveItem


class SaveItem(QWidget, Ui_SaveItem):
    saveDeleted = pyqtSignal()

    def __init__(self, path, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.path = path
        self.save = Save(path)
        self.l_icon.setPixmap(self.save.icon.scaled(self.l_icon.size()))
        self.l_levelname.setText(self.save.levelname)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_openfolder_clicked(self, _):
        os.startfile(self.path)

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        def confirmDelete():
            self.save.delete()
            self.saveDeleted.emit()

        box = MessageBox(
            self.tr("你确定要删除这个世界吗") + "?",
            self.tr('"{levelname}"将会失去很久! (真的很久!)').format(
                levelname=self.save.levelname
            ),
            self.window(),
        )
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_viewnbt_clicked(self, _):
        Function("NBTViewer").exec(self.save.path)

    def refresh(self):
        dir_name = self.path.replace("\\", "/").split("/")[-1]
        self.l_info1.setText(
            f"{dir_name} ({time.strftime('%Y-%m-%d %p %I-%M',time.localtime(self.save.lastplayed))})"
        )
        self.l_info2.setText(
            f"{self.save.gametype}{', '+self.tr('作弊') if self.save.allowcommands else ''}, {self.tr('版本')}: {self.save.version_name}"
        )
