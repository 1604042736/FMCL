from PyQt5.QtCore import pyqtSignal, QThread

from Core import CoreBase


class Task(QThread):
    """任务"""
    Finished = pyqtSignal()
    Progress = pyqtSignal(int, int)
    Error=pyqtSignal(str)

    def __init__(self, ins:CoreBase, func, args) -> None:
        super().__init__()
        self.ins = ins
        self.func = func
        self.args = args

        self.ins.Finished.connect(lambda: self.Finished.emit())
        self.ins.Progress.connect(
            lambda cur, total: self.Progress.emit(cur, total))
        self.ins.Error.connect(lambda a:self.Error.emit(a))

    def run(self):
        getattr(self.ins, self.func)(*self.args)
