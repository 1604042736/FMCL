import qtawesome as qta
from Kernel import Kernel
from qfluentwidgets import PushButton
from Setting import Setting

from .UserManager import UserManager

_translate = Kernel.translate


def functionInfo():
    return {
        "name": "用户管理",
        "icon": qta.icon("ph.users")
    }


def defaultSettingAttr() -> dict:
    button = PushButton()
    button.setText(_translate("用户管理"))
    button.clicked.connect(main)
    setting = Setting()
    setting.attrs["users"]["settingcard"] = lambda: button
    setting.attrs["users.selectindex"]["settingcard"] = lambda: button
    return {}


def main():
    usermanager = UserManager()
    usermanager.show()
