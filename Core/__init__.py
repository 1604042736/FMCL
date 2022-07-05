from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject


class CoreBase(QObject):
    """所有核心代码的基类"""
    Finished = pyqtSignal()
    Progress = pyqtSignal(int, int)
    Error = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
