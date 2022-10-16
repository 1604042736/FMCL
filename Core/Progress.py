import threading
from PyQt5.QtWidgets import QListWidget, QGridLayout, QWidget, QLabel, QProgressBar, QListWidgetItem
from PyQt5.QtCore import QSize, QThread, pyqtSignal, QTimer
import qtawesome as qta


class Progress(QListWidget):
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
        self.setWindowTitle("进度")
        self.setWindowIcon(qta.icon("mdi.progress-download"))

    def add(self, func):
        item = QListWidgetItem()
        item.setSizeHint(QSize(256, 64))
        self.addItem(item)
        callback = Callback(func)
        callback.Finished.connect(lambda: self.remove(item))
        self.setItemWidget(item, callback)
        self.show()
        callback.start()

    def remove(self, item):
        self.takeItem(self.row(item))


class Callback(QWidget):
    Finished = pyqtSignal()

    def __init__(self, func):
        super().__init__()
        self.gridlayout = QGridLayout(self)
        self.le_status = QLabel(self)
        self.pbr_progress = QProgressBar(self)

        self.gridlayout.addWidget(self.le_status)
        self.gridlayout.addWidget(self.pbr_progress)

        self.task = Task(func)
        self.task.statusChanged.connect(self.setStatus)
        self.task.progressChanged.connect(self.setProgress)
        self.task.maxChanged.connect(self.setMax)
        self.task.Finished.connect(self.Finished.emit)

    def start(self):
        self.task.start()

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
    Finished = pyqtSignal()

    def __init__(self, func) -> None:
        super().__init__()
        self.func = func

    def run(self):
        self.func({
            "setStatus": self.statusChanged.emit,
            "setProgress": self.progressChanged.emit,
            "setMax": self.maxChanged.emit
        })
        self.Finished.emit()
