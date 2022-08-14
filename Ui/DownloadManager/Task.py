import traceback
from PyQt5.QtCore import pyqtSignal, QThread
import sys
from Core import CoreBase


class Task(QThread):
    """任务"""
    Finished = pyqtSignal()
    Progress = pyqtSignal(int, int)
    Error = pyqtSignal(str)

    def __init__(self, ins: CoreBase, func, args) -> None:
        super().__init__()
        self.ins = ins
        self.func = func
        self.args = args
        self.running = True

        self.ins.Progress.connect(
            lambda cur, total: self.Progress.emit(cur, total))
        self.ins.Error.connect(lambda a: self.Error.emit(a))

    def run(self):
        try:
            sys.settrace(self.tracer)
            getattr(self.ins, self.func)(self.args)
            sys.settrace(None)
            self.Finished.emit()
        except BaseException as e:
            sys.settrace(None)
            self.Error.emit(str(e))

    def tracer(self, frame, event, arg=None):
        """跟踪目标函数执行,并随时结束"""
        if not self.running:
            raise SystemExit()
        return self.tracer
