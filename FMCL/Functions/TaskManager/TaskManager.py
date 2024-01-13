import qtawesome as qta

from PyQt5.QtCore import pyqtSlot, pyqtSignal, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, qApp
from qfluentwidgets import InfoBar, InfoBarPosition

from Core.Task import Task

from .ui_TaskManager import Ui_TaskManager


class TaskManager(QWidget, Ui_TaskManager):
    taskStarted = pyqtSignal(Task)
    taskFinished = pyqtSignal(Task)

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
        self.task_timer: dict[Task, QTimer] = {}
        self.taskStarted.connect(self.on_taskStarted)
        self.taskFinished.connect(self.on_taskFinished)

    def on_taskStarted(self, task: Task):
        if task in self.task_item:
            return
        root = self.task_item.get(task.parent(), None)
        item = QTreeWidgetItem()
        self.task_item[task] = item
        if root:
            root.addChild(item)
            item.setExpanded(True)
            root.setExpanded(True)
        else:
            self.tw_tasks.addTopLevelItem(item)
            self.show()
        timer = QTimer(self)
        self.task_timer[task] = timer
        timer.timeout.connect(lambda: self.sync(item, task))
        timer.start(1)

    def on_taskFinished(self, task: Task):
        item = self.task_item.pop(task)
        if item.parent() != None:
            item.parent().removeChild(item)
        else:
            self.tw_tasks.takeTopLevelItem(self.tw_tasks.indexOfTopLevelItem(item))
            for i in qApp.topLevelWidgets():
                if i.isVisible():
                    InfoBar.info(
                        title=f'{self.tr("完成")} {task.name}',
                        content="",
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=i,  # 在任务完成的时侯TaskManager可能并没有显示
                    )
                    break

    def sync(self, item, task):
        if task.isFinished():
            timer = self.task_timer.pop(task)
            timer.stop()
            return
        item.setText(0, task.name)
        item.setText(1, task.status)
        item.setText(
            2,
            f"{task.progress}/{task.maxprogress}({round(task.progress/task.maxprogress if task.maxprogress!=0 else 0,3)*100}%)",
        )
        item.setText(3, str(task.isRunning()))
        for child in task.children():
            if not child.isFinished():
                self.on_taskStarted(child)

    @pyqtSlot(bool)
    def on_pb_stop_clicked(self, _):
        _item = self.tw_tasks.currentItem()
        if _item == None:
            return
        for task, item in self.task_item.items():
            if item == _item:
                task.terminate()
                break
