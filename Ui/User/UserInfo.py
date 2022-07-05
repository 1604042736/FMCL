from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
import qtawesome as qta
from PyQt5.QtCore import pyqtSignal
import Globals as g


class UserInfo(QWidget):
    CurUserChanged = pyqtSignal(dict)
    UserDel = pyqtSignal(dict)

    def __init__(self, info: dict, parent=None) -> None:
        super().__init__(parent)
        self.info = info

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(info["name"])

        self.l_type = QLabel(self)
        self.l_type.setText(info["type"])

        self.pb_settocur = QPushButton(self)
        self.pb_settocur.setText("设置成当前用户")
        self.pb_settocur.clicked.connect(
            lambda: self.CurUserChanged.emit(self.info))
        self.pb_settocur.hide()

        self.pb_del = QPushButton(self)
        self.pb_del.setIcon(qta.icon("mdi.delete"))
        self.pb_del.clicked.connect(lambda: self.UserDel.emit(self.info))

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.l_type)
        if info != g.cur_user:
            self.hbox.addWidget(self.pb_settocur)
            self.pb_settocur.show()
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)
