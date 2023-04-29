from .TaskManager import TaskManager
import qtawesome as qta


def functionInfo():
    return {
        "name": "任务管理器",
        "icon": qta.icon("fa.tasks")
    }


def main():
    taskmanager = TaskManager()
    taskmanager.show()
