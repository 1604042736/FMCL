import qtawesome as qta
from Core.Task import Task
from PyQt5.QtCore import QCoreApplication
from Setting import Setting
from .TaskManager import TaskManager

_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("TaskManager", "任务管理器"),
        "icon": qta.icon("fa.tasks"),
    }


def defaultSetting() -> dict:
    setting = Setting()
    if "explorer.title_rightclicked_actions" in setting.defaultsetting:
        a = setting.defaultsetting["explorer.title_rightclicked_actions"]
        action = {
            "name": _translate("TaskManager", "任务管理器"),
            "icon": 'qta.icon("fa.tasks")',
            "commands": ["TaskManager"],
        }
        if action not in a:
            a.insert(1, action)
    return {}


# 通过信号和槽保证TaskManager在处理时位于主线程
Task.startedCallback.append(lambda task: TaskManager().on_taskStarted(task))
Task.finishedCallback.append(lambda task: TaskManager().on_taskFinished(task))


def main():
    taskmanager = TaskManager()
    taskmanager.show()
