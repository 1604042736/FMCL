import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget, qApp
from qfluentwidgets import TransparentToolButton
from Setting import Setting

from .ui_UserManager import Ui_UserManager
from .UserInfo import UserInfo


class UserManager(QWidget, Ui_UserManager):
    instance = None
    new_count = 0

    def __new__(cls):
        if UserManager.instance == None:
            UserManager.instance = super().__new__(cls)
        UserManager.new_count += 1
        return UserManager.instance

    def __init__(self) -> None:
        if UserManager.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ph.users"))

        self.pb_add = TransparentToolButton()
        self.pb_add.setIcon(qta.icon("msc.add"))
        self.pb_add.resize(46, 32)
        self.pb_add.clicked.connect(lambda: Kernel.execFunction("CreateUser"))

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.userinfo: list[UserInfo] = []
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
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_add, "right", sender=self))
        qApp.sendEvent(self.window(),
                       AddToTitleEvent(self.pb_refresh, "right", sender=self))
        super().showEvent(a0)
