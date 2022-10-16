from PyQt5.QtWidgets import QWidget

from Core.User import User
from .ui_Offline import Ui_Offline
import qtawesome as qta
from PyQt5.QtCore import pyqtSlot


class Offline(QWidget, Ui_Offline):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.wifi-slash-light"))

    @pyqtSlot(bool)
    def on_pb_create_clicked(self, _):
        User.create_offline(self.le_username.text())
