import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from qfluentwidgets import PushButton

from Setting import Setting

from .CreateUser import CreateUser

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("CreateUser", "创建用户"),
        "icon": qta.icon("ph.user-circle-plus"),
    }


def defaultSettingAttr() -> dict:
    button = PushButton()
    button.setText(_translate("CreateUser", "前往创建用户设置"))
    button.clicked.connect(main)
    setting = Setting()
    setting.attrs["users.authlibinjector_servers"]["settingcard"] = lambda: button
    return {}


def main(tab="offline"):
    createuser = CreateUser()
    createuser.show(tab)
