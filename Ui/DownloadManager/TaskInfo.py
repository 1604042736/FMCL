from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QProgressBar, QPushButton
from PyQt5.QtCore import pyqtSignal, QTimer
from Core import CoreBase
from Translate import tr

from Ui.DownloadManager.Task import Task


class TaskInfo(QWidget):
    Finished = pyqtSignal(int)
    Error = pyqtSignal(str, int)

    def __init__(self, name, ins: CoreBase, func, args, id, parent=None):
        super().__init__(parent)
        self.name = name  # 任务名称
        self.ins = ins  # 类的实例
        self.func = func  # 函数
        self.args = args  # 参数
        self.id = id

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(self.name)

        self.pbr_progress = QProgressBar(self)
        self.pbr_progress.setRange(0, 100)
        self.pbr_progress.setValue(0)

        self.pb_cancel = QPushButton(self)
        self.pb_cancel.setText(tr("取消"))
        self.pb_cancel.clicked.connect(lambda: self.Finished.emit(self.id))

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pbr_progress)
        self.hbox.addWidget(self.pb_cancel)

        self.setLayout(self.hbox)

        self.task = Task(ins, func, args)
        self.task.Progress.connect(self.progress)
        self.task.Finished.connect(lambda: self.Finished.emit(self.id))
        self.task.Error.connect(lambda a: self.Error.emit(a, self.id))

        self.cur_progress = (0, 1)

        # 防止界面卡死
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(500)

    def start(self):
        self.task.start()

    def progress(self, cur, total):
        self.cur_progress = (cur, total)

    def update_progress(self):
        try:
            cur, total = self.cur_progress
            self.pbr_progress.setValue(int(cur/total*100))
        except ValueError as e:
            print(e)
