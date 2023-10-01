from Core.User import User
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition, MessageBox

from .ui_LittleSkin import Ui_LittleSkin


class LittleSkin(QWidget, Ui_LittleSkin):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot(bool)
    def on_pb_logon_clicked(self, _):
        self.pb_logon.setEnabled(False)
        username = self.le_username.text()
        password = self.le_password.text()
        ret = User.create_littleskin(username, password)
        if ret == None:
            InfoBar.success(
                title=self.tr("创建成功"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window()
            )
        else:
            MessageBox(self.tr("创建失败"), str(ret), self.window()).exec()
        self.pb_logon.setEnabled(True)
