from PyQt5.QtWidgets import QWidget
import Globals as g
from PyQt5.QtCore import pyqtSignal


class SettingItem(QWidget):
    """设置项"""
    Saved = pyqtSignal()

    def __init__(self, id, name, val, do_after_save=None, target=g, parent=None) -> None:
        super().__init__(parent)
        self.id = id  # 设置对应的变量
        self.name = name  # 设置的名称
        self.val = val  # 设置的值
        self.target = target  # 变量对应的地方
        self.do_after_save = do_after_save  # 在保存完后做的

    def save(self):
        if self.do_after_save:
            self.do_after_save()
