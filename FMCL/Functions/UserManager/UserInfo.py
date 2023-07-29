from Core.User import User
from Kernel import Kernel
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QFrame
from qfluentwidgets import MessageBox

from .ui_UserInfo import Ui_UserInfo

_translate = Kernel.translate


class UserInfo(QFrame, Ui_UserInfo):
    userSelectChanged = pyqtSignal(dict)
    userDeleted = pyqtSignal(dict)

    def __init__(self, userinfo: dict) -> None:
        super().__init__()
        self.setupUi(self)
        self.userinfo = userinfo

        self.l_username.setText(userinfo["username"])
        _type = userinfo["type"]
        if _type == "offline":
            self.l_type.setText(_translate("离线登录"))
        elif _type == "authlibInjector":
            self.l_type.setText(_translate("外置登录"))
            self.l_mode.setText(userinfo["mode"])

        head = User.get_head(userinfo)
        head = QPixmap.fromImage(head)
        head = head.scaled(32, 32)
        self.l_head.setPixmap(head)

        if userinfo == User.get_cur_user():
            self.rb_select.setChecked(True)

    @pyqtSlot(bool)
    def on_rb_select_clicked(self, _):
        if self.rb_select.isChecked():
            self.userSelectChanged.emit(self.userinfo)
        self.rb_select.setChecked(True)

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        def confirmDeleted():
            User.delete(self.userinfo)
            self.userDeleted.emit(self.userinfo)
        box = MessageBox("",
                         _translate("确认删除")+"?",
                         self.window())
        box.yesSignal.connect(confirmDeleted)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_refresh_clicked(self, _):
        User.refresh(self.userinfo)
