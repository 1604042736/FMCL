from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent


class QCustomButton(QPushButton):
    mouseDoubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        self.mouseDoubleClicked.emit()
