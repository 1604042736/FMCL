from .TaskManager import TaskManager
import qtawesome as qta
from PyQt5.QtCore import QCoreApplication
_translate = QCoreApplication.translate


def functionInfo():
    return {
        "name": _translate("TaskManager", "任务管理器"),
        "icon": qta.icon("fa.tasks")
    }


def main():
    taskmanager = TaskManager()
    taskmanager.show()
