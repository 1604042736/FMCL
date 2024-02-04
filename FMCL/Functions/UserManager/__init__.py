import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from qfluentwidgets import PushButton
from Setting import Setting

from .UserManager import UserManager

_translate = QCoreApplication.translate


def functionInfo():
    return {"name": _translate("UserManager", "用户管理"), "icon": qta.icon("ph.users")}


def defaultSettingAttr() -> dict:
    button = PushButton()
    button.setText(_translate("UserManager", "前往用户管理设置"))
    button.clicked.connect(main)
    setting = Setting()
    setting.attrs["users"]["settingcard"] = lambda: button
    setting.attrs["users.selectindex"]["settingcard"] = lambda: button
    return {}


def main():
    usermanager = UserManager()
    usermanager.show()
