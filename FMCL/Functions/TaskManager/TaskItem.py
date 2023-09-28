import time

import multitasking
from Core.Task import Task
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from .ui_TaskItem import Ui_TaskItem


class TaskItem(QWidget, Ui_TaskItem):

    __Refresh = pyqtSignal()

    def __init__(self, task: Task) -> None:
        super().__init__()
        self.setupUi(self)
        self.task = task
        self.name = task.name
        self.status = task.status
        self.progress = task.progress
        self.maxprogress = task.maxprogress
        self.__Refresh.connect(self.refresh)
        self.sync()

    @multitasking.task
    def sync(self):
        """同步"""
        while not self.task.isFinished():
            if (self.task.progress != self.progress
                or self.task.status != self.status
                    or self.task.maxprogress != self.maxprogress):
                # 防止频繁刷新
                self.__Refresh.emit()
            time.sleep(0.1)

    def refresh(self):
        self.name = self.task.name
        self.status = self.task.status
        self.progress = self.task.progress
        self.maxprogress = self.task.maxprogress
        self.l_name.setText(self.name)
        self.l_status.setText(self.status)
        self.pbr_progress.setValue(self.progress)
        self.pbr_progress.setMaximum(self.maxprogress)
