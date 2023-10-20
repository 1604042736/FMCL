import qtawesome as qta
from Core.Task import Task
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
    if "explorer.title_rightclicked_actions" in setting.defaultsetting:
        a = setting.get("explorer.title_rightclicked_actions")
        if "TaskManager" not in a:
            a.insert(1, "TaskManager")
    return {}


Task.startedCallback.append(TaskManager.taskStarted)
Task.finishedCallback.append(TaskManager.taskFinished)


def main():
    taskmanager = TaskManager()
    taskmanager.show()
