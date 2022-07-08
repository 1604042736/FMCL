from Core import CoreBase
from QtFBN.QFBNWidget import QFBNWidget
from Ui.DownloadManager.TaskInfo import TaskInfo
from Ui.DownloadManager.ui_DownloadManager import Ui_DownloadManager
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize, pyqtSignal


class DownloadManager(QFBNWidget, Ui_DownloadManager):
    NoTask = pyqtSignal()
    HasTask = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.task_num = 0  # 任务数量

    def add_task(self, name, ins: CoreBase, func, args):
        """添加一个任务"""
        item = QListWidgetItem()
        item.setSizeHint(QSize(256, 64))
        widget = TaskInfo(name, ins, func, args, self.lw_tasks.count())
        widget.Finished.connect(self.task_finished)
        widget.Error.connect(self.task_error)
        self.lw_tasks.addItem(item)
        self.lw_tasks.setItemWidget(item, widget)
        self.task_num += 1
        self.HasTask.emit()
        self.show()
        widget.start()  # 防止任务执行太快

    def task_finished(self, task_id):
        self.notify("任务结束", self.lw_tasks.itemWidget(
            self.lw_tasks.item(task_id)).name)
        self.lw_tasks.takeItem(task_id)
        self.task_num = self.lw_tasks.count()
        if self.task_num == 0:
            self.NoTask.emit()
            self.close()

    def task_error(self, msg, task_id):
        self.notify("错误", msg)
        self.lw_tasks.takeItem(task_id)
        self.task_num = self.lw_tasks.count()
        if self.task_num == 0:
            self.NoTask.emit()
            self.close()
