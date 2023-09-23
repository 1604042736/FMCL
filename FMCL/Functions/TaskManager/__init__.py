import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
from Setting import Setting

from .TaskManager import TaskManager

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("TaskManager", "任务管理器"),
        "icon": qta.icon("fa.tasks")
    }


def defaultSetting() -> dict:
    setting = Setting()
    a = setting.get("explorer.title_rightclicked_actions", tuple())
    if "TaskManager" not in a:
        a.insert(1, "TaskManager")
    return {}


def main():
    taskmanager = TaskManager()
    taskmanager.show()
