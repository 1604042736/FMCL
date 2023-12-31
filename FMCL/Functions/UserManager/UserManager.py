import qtawesome as qta
from Events import *
from Kernel import Kernel
from PyQt5.QtCore import QEvent
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
        functioninfo = Kernel.getFunctionInfo(Kernel.getFunction("CreateUser"))
        self.pb_add.setIcon(functioninfo["icon"])
        self.pb_add.resize(46, 32)
        self.pb_add.clicked.connect(lambda: Kernel.execFunction("CreateUser"))

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

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_add, "right"))
            self.refresh()
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_add))
            self.pb_add.setParent(self)
        elif a0.type() == QEvent.Type.WindowActivate:
            self.refresh()
        return super().event(a0)
