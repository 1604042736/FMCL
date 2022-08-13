from PyQt5.QtCore import pyqtSignal, QThread

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

        self.ins.Progress.connect(
            lambda cur, total: self.Progress.emit(cur, total))
        self.ins.Error.connect(lambda a: self.Error.emit(a))

    def run(self):
        try:
            getattr(self.ins, self.func)(*self.args)
            # download不连接Finished信号会导致执行完后无法及时更新
            # 连接Finished信号会导致一个任务如果调用了多次download
            # 每次download结束都会发出Finished并传到Task.Finished
            # 造成DownloadManager错误的删除任务
            # 所以Task.Finished得在任务执行完后发出
            # 而不是与ins.Finished连接
            self.Finished.emit()
        except Exception as e:
            self.Error.emit(str(e))
