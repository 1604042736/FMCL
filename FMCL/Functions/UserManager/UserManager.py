import qtawesome as qta
from Kernel import Kernel
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget
from Setting import Setting

from .ui_UserManager import Ui_UserManager
from .UserInfo import UserInfo


class UserManager(QWidget, Ui_UserManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.users"))
        self.userinfo: list[UserInfo] = []
        self.pb_add.setIcon(qta.icon("ei.plus"))
        self.refresh()

    def refresh(self):
        for i in range(self.gl_userinfo.count()):
            item = self.gl_userinfo.itemAt(i)
            self.gl_userinfo.removeItem(item)
            if item and item.widget():
                item.widget().deleteLater()
        for i in self.userinfo:
            i.deleteLater()
        self.userinfo = []
        for user in Setting()["users"]:
            userinfo = UserInfo(user)
            userinfo.userSelectChanged.connect(self.changeUserSelect)
            userinfo.userDeleted.connect(self.deleteUser)
            self.gl_userinfo.addWidget(userinfo)
            self.userinfo.append(userinfo)

    def deleteUser(self, uinfo):
        self.refresh()

    def changeUserSelect(self, uinfo):
        for userinfo in self.userinfo:
            if userinfo.userinfo != uinfo:
                userinfo.rb_select.setChecked(False)
        setting = Setting()
        setting["users.selectindex"] = setting["users"].index(uinfo)
        setting.sync()

    def showEvent(self, a0: QShowEvent) -> None:
        self.refresh()
        return super().showEvent(a0)

    @pyqtSlot(bool)
    def on_pb_add_clicked(self, _):
        Kernel.execFunction("CreateUser")
