import qtawesome as qta
from PyQt5.QtCore import QCoreApplication

from .CreateUser import CreateUser

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("CreateUser", "创建用户"),
        "icon": qta.icon("ph.user-circle-plus")
    }


def main():
    createuser = CreateUser()
    createuser.show()
