import qtawesome as qta

import logging
import traceback
import webbrowser

from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt
from PyQt5.QtWidgets import QWidget

from qfluentwidgets import PrimaryPushButton, MessageBox, InfoBar, InfoBarPosition

from Core import User

from .ui_Yggdrasil import Ui_Yggdrasil


class Yggdrasil(QWidget, Ui_Yggdrasil):
    instances = {}
    new_count = {}

    deleteRequest = pyqtSignal(QWidget, dict)

    def __new__(cls, server):
        _hash = str(server)
        if _hash not in Yggdrasil.instances:
            Yggdrasil.instances[_hash] = super().__new__(cls)
            Yggdrasil.new_count[_hash] = 0
        Yggdrasil.new_count[_hash] += 1
        return Yggdrasil.instances[_hash]

    def __init__(self, server) -> None:
        if Yggdrasil.new_count[str(server)] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.pb_delete.setIcon(qta.icon("mdi.delete"))

        self.server = server

        self.link_translations = {
            "homepage": self.tr("主页"),
            "register": self.tr("注册"),
            "announcement": self.tr("公告"),
        }

        for i, (name, link) in enumerate(server["meta"]["links"].items()):
            button = PrimaryPushButton()
            button.setText(self.link_translations.get(name, name))
            button.clicked.connect(lambda _, link=link: webbrowser.open(link))
            self.hl_links.insertWidget(i, button)

    @pyqtSlot(bool)
    def on_pb_login_clicked(self, _):
        username = self.le_username.text()
        password = self.le_password.text()
        try:
            User.create_yggdrasil(self.server["url"], username, password)
            InfoBar.success(
                title=self.tr("创建成功"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window(),
            )
        except Exception as e:
            logging.error(traceback.format_exc())
            MessageBox(self.tr("无法登录"), str(e), self).exec()

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        self.deleteRequest.emit(self, self.server)
