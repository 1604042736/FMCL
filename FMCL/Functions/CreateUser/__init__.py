from typing import Literal
import qtawesome as qta
from PyQt5.QtCore import QCoreApplication, QObject, QEvent
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


class __Monitor(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.instances: list[CreateUser] = []

    def eventFilter(self, a0: QObject, a1: QEvent):
        if isinstance(a0, CreateUser):
            if (
                a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete)
                and a0 in self.instances
            ):
                self.instances.remove(a0)
            elif a1.type() == QEvent.Type.Show and a0 not in self.instances:
                self.instances.append(a0)
        return super().eventFilter(a0, a1)


_monitor = None


def main(tab="offline", mode: Literal["new", "attach"] = "new"):
    """
    mode:
        new : 直接创建一个新的CreateUser并显示
        attach: 显示之前已经显示了的CreateUser, 如果没有就创建新的
    """
    global _monitor
    if _monitor == None:
        _monitor = __Monitor()

    if mode == "attach":
        for i in _monitor.instances:
            i.show(tab)
            return
    createuser = CreateUser()
    createuser.installEventFilter(_monitor)
    createuser.show(tab)
