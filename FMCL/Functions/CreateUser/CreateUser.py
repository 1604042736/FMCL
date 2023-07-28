import qtawesome as qta
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from .LittleSkin import LittleSkin
from .Microsoft import Microsoft
from .Offline import Offline
from .ui_CreateUser import Ui_CreateUser


class CreateUser(QWidget, Ui_CreateUser):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.user-circle-plus"))
        self.offline = Offline()
        self.microsoft = Microsoft()
        self.littleskin = LittleSkin()

        self.pb_offline.setIcon(self.offline.windowIcon())
        self.pb_microsoft.setIcon(self.microsoft.windowIcon())

        self.pb_offline.setChecked(True)
        self.sw_way.addWidget(self.offline)

    @pyqtSlot(bool)
    def on_pb_offline_clicked(self, _):
        self.sw_way.removeWidget(self.sw_way.currentWidget())
        self.sw_way.addWidget(self.offline)

    @pyqtSlot(bool)
    def on_pb_microsoft_clicked(self, _):
        self.sw_way.removeWidget(self.sw_way.currentWidget())
        self.sw_way.addWidget(self.microsoft)

    @pyqtSlot(bool)
    def on_pb_littleskin_clicked(self, _):
        self.sw_way.removeWidget(self.sw_way.currentWidget())
        self.sw_way.addWidget(self.littleskin)
