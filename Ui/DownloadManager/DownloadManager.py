from Core import CoreBase
from QtFBN.QFBNWidget import QFBNWidget
from Translate import tr
from Ui.DownloadManager.TaskInfo import TaskInfo
from Ui.DownloadManager.ui_DownloadManager import Ui_DownloadManager
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize, pyqtSignal
import Globals as g


class DownloadManager(QFBNWidget, Ui_DownloadManager):
    NoTask = pyqtSignal()
    HasTask = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.task_num = 0  # 任务数量
        self.setWindowTitle(tr("下载管理"))

    def add_task(self, name, ins: CoreBase, func, args):
        """添加一个任务"""
        item = QListWidgetItem()
        item.setSizeHint(QSize(256, 64))
        widget = TaskInfo(name, ins, func, args, item)
        widget.Finished.connect(self.task_finished)
        widget.Error.connect(self.task_error)
        self.lw_tasks.addItem(item)
        self.lw_tasks.setItemWidget(item, widget)
        widget.start()
        self.task_num += 1
        self.HasTask.emit()
        self.show()

    def task_finished(self, item):
        taskinfo = self.lw_tasks.itemWidget(item)
        # 如果发生错误发出Error信号就会导致taskinfo为None
        if taskinfo != None:
            name = taskinfo.name
            self.lw_tasks.takeItem(self.lw_tasks.row(item))
            self.task_num = self.lw_tasks.count()
            if self.task_num == 0:
                self.NoTask.emit()
                self.close()
            self.notify(tr("任务结束"), name)
            g.logapi.info(f"任务结束:{name}")

    def task_error(self, msg, item):
        self.lw_tasks.takeItem(self.lw_tasks.row(item))
        self.task_num = self.lw_tasks.count()
        if self.task_num == 0:
            self.NoTask.emit()
            self.close()
        self.notify(tr("错误"), msg)
        g.logapi.info(f"错误:{msg}")
