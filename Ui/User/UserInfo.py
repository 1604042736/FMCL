from PyQt5.QtWidgets import QWidget, QPushButton, QLabel
import qtawesome as qta
from PyQt5.QtCore import pyqtSignal, QSize
import Globals as g
from PyQt5.QtGui import QResizeEvent


class UserInfo(QWidget):
    CurUserChanged = pyqtSignal(dict)
    UserDel = pyqtSignal(dict)

    def __init__(self, info: dict, parent=None) -> None:
        super().__init__(parent)
        self.info = info

        self.l_name = QLabel(self)
        self.l_name.setText(info["name"])

        self.l_type = QLabel(self)
        self.l_type.setText(info["type"])

        self.pb_settocur = QPushButton(self)
        self.pb_settocur.clicked.connect(
            lambda: self.CurUserChanged.emit(self.info))
        self.pb_settocur.hide()
        self.pb_settocur.setIcon(qta.icon("fa5s.user-check"))

        self.pb_del = QPushButton(self)
        self.pb_del.setIcon(qta.icon("mdi.delete"))
        self.pb_del.clicked.connect(lambda: self.UserDel.emit(self.info))

        if info != g.cur_user:
            self.pb_settocur.show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        height = self.height()
        left_width = self.width()-int((self.height()-height)/2)
        self.pb_del.move(left_width-height, int((self.height()-height)/2))
        self.pb_del.resize(height, height)
        self.pb_del.setIconSize(
            QSize(self.pb_del.width(), self.pb_del.height()))

        self.pb_settocur.move(left_width-height*2,
                              int((self.height()-height)/2))
        self.pb_settocur.resize(height, height)
        self.pb_settocur.setIconSize(
            QSize(self.pb_settocur.width(), self.pb_settocur.height()))

        self.l_name.move(0, 0)
        self.l_name.resize(left_width-height, int(self.height()/2))

        self.l_type.move(0, int(self.height()/2))
        self.l_type.resize(left_width-height, int(self.height()/2))
