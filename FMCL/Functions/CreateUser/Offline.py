import qtawesome as qta
from Core.User import User
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition

from .ui_Offline import Ui_Offline


class Offline(QWidget, Ui_Offline):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.wifi-slash-light"))

    @pyqtSlot(bool)
    def on_pb_create_clicked(self, _):
        User.create_offline(self.le_username.text(), self.le_uuid.text())
        InfoBar.success(
            title=self.tr("创建成功"),
            content="",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self.window(),
        )
