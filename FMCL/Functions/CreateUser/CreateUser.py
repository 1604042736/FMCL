import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget, qApp
from qfluentwidgets import TransparentToolButton

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

        self.pb_usermanager = TransparentToolButton()
        functioninfo = Kernel.getFunctionInfo(
            Kernel.getFunction("UserManager"))
        self.pb_usermanager.setIcon(functioninfo["icon"])
        self.pb_usermanager.resize(46, 32)
        self.pb_usermanager.clicked.connect(
            lambda: Kernel.execFunction("UserManager"))

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

    def showEvent(self, a0: QShowEvent) -> None:
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_usermanager, "right", sender=self))
        super().showEvent(a0)

    def show(self, tab="offline") -> None:
        if tab == "offline":
            self.pb_offline.click()
        elif tab == "microsoft":
            self.pb_microsoft.click()
        elif tab == "littleskin":
            self.pb_littleskin.click()
        return super().show()
