import qtawesome as qta
from PyQt5.QtCore import QSize, QThread, pyqtSignal
from PyQt5.QtWidgets import QGridLayout, QLabel, QListWidgetItem, QWidget
from qfluentwidgets import ListWidget, ProgressBar, PushButton


class Progress(ListWidget):
    __instance = None
    __new_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        cls.__new_count += 1
        return cls.__instance

    def __init__(self):
        if self.__new_count > 1:
            return
        super().__init__()
        self.setWindowTitle(self.tr("进度"))
        self.setWindowIcon(qta.icon("mdi.progress-download"))

    def add(self, name, func):
        item = QListWidgetItem()
        item.setSizeHint(QSize(256, 64))
        self.addItem(item)
        taskitem = TaskItem(name, func)
        taskitem.Finished.connect(lambda: self.remove(item))
        self.setItemWidget(item, taskitem)
        self.show()
        taskitem.start()

    def remove(self, item):
        self.takeItem(self.row(item))


class TaskItem(QWidget):
    Finished = pyqtSignal()

    def __init__(self, name, func):
        super().__init__()
        self.gridlayout = QGridLayout(self)
        self.le_name = QLabel(text=name)
        self.le_status = QLabel()
        self.pbr_progress = ProgressBar()
        self.pb_cancel = PushButton()
        self.pb_cancel.setText(self.tr("取消"))
        self.pb_cancel.clicked.connect(self.cancel)

        self.gridlayout.addWidget(self.le_name)
        self.gridlayout.addWidget(self.le_status)
        self.gridlayout.addWidget(self.pbr_progress)
        self.gridlayout.addWidget(self.pb_cancel, 0, 1, 3, 1)

        self.task = Task(func)
        self.task.statusChanged.connect(self.setStatus)
        self.task.progressChanged.connect(self.setProgress)
        self.task.maxChanged.connect(self.setMax)
        self.task.finished.connect(self.Finished.emit)

    def start(self):
        self.task.start()

    def cancel(self):
        self.task.terminate()

    def setStatus(self, status: str):
        self.le_status.setText(status)

    def setProgress(self, progress: int):
        self.pbr_progress.setValue(progress)

    def setMax(self, new_max: int):
        self.pbr_progress.setRange(0, new_max)


class Task(QThread):
    statusChanged = pyqtSignal(str)
    progressChanged = pyqtSignal(int)
    maxChanged = pyqtSignal(int)

    def __init__(self, func) -> None:
        super().__init__()
        self.func = func

    def run(self):
        self.func({
            "setStatus": self.statusChanged.emit,
            "setProgress": self.progressChanged.emit,
            "setMax": self.maxChanged.emit
        })
