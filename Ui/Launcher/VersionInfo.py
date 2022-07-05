from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSignal


class VersionInfo(QWidget):
    OpenVersionManager = pyqtSignal(str)
    DirectLaunch = pyqtSignal(str)

    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.name = name

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(self.name)

        self.pb_launch = QPushButton(self)
        self.pb_launch.setText("直接启动")
        self.pb_launch.clicked.connect(
            lambda: self.DirectLaunch.emit(self.name))

        self.pb_manage = QPushButton(self)
        self.pb_manage.setText("管理")
        self.pb_manage.clicked.connect(
            lambda: self.OpenVersionManager.emit(self.name))

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pb_launch)
        self.hbox.addWidget(self.pb_manage)

        self.setLayout(self.hbox)
