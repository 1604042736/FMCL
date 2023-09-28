import qtawesome as qta
from Core.Task import Task
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget

from .TaskItem import TaskItem
from .ui_TaskManager import Ui_TaskManager


class TaskManager(QWidget, Ui_TaskManager):
    instance = None
    new_count = 0

    def __new__(cls):
        if TaskManager.instance == None:
            TaskManager.instance = super().__new__(cls)
        TaskManager.new_count += 1
        return TaskManager.instance

    def __init__(self):
        if TaskManager.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.tasks"))

        self.task_item: dict[Task, QTreeWidgetItem] = {}

    @staticmethod
    def taskStarted(task: Task):
        self = TaskManager()
        if task in self.task_item:
            return
        root = self.task_item.get(task.parent(), None)
        item = QTreeWidgetItem()
        self.task_item[task] = item
        widget = TaskItem(task)
        item.setSizeHint(0, widget.size())
        if root:
            root.addChild(item)
            item.setExpanded(True)
            root.setExpanded(True)
        else:
            self.tw_tasks.addTopLevelItem(item)
            self.show()
        self.tw_tasks.setItemWidget(item, 0, widget)

    @staticmethod
    def taskFinished(task: Task):
        self = TaskManager()
        item = self.task_item.pop(task)
        if item.parent() != None:
            item.parent().removeChild(item)
        else:
            self.tw_tasks.takeTopLevelItem(
                self.tw_tasks.indexOfTopLevelItem(item))

    @pyqtSlot(bool)
    def on_pb_stop_clicked(self, _):
        _item = self.tw_tasks.currentItem()
        if _item == None:
            return
        for task, item in self.task_item.items():
            if item == _item:
                task.terminate()
                break
