import qtawesome as qta

from .CreateUser import CreateUser


def functionInfo():
    return {
        "name": "创建用户",
        "icon": qta.icon("ph.user-circle-plus")
    }


def main():
    createuser = CreateUser()
    createuser.show()
