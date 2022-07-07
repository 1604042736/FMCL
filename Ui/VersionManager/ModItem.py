from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal

from Core.Mod import Mod


class ModItem(QWidget):
    ModEnDisAble = pyqtSignal(str, str)
    ModDeleted = pyqtSignal(str)

    def __init__(self, name, path, parent=None) -> None:
        super().__init__(parent)
        self.name = name
        self.path = path

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(self.name)
        if "disabled" in self.name:
            self.l_name.setStyleSheet("color:rgb(100,100,100);")

        self.pb_edable = QPushButton(self)
        self.pb_edable.setText("禁用")
        self.pb_edable.clicked.connect(self.endisable_mod)
        if "disabled" in self.name:
            self.pb_edable.setText("启用")

        self.pb_del = QPushButton(self)
        self.pb_del.setText("删除")
        self.pb_del.clicked.connect(self.del_mod)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pb_edable)
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)

    def endisable_mod(self):
        result, new_name = Mod(name=self.name, path=self.path).endisable_mod()
        if result == "disabled":
            self.pb_edable.setText("启用")
        else:
            self.pb_edable.setText("禁用")
        self.ModEnDisAble.emit(self.name, new_name)
        self.name = new_name

    def del_mod(self):
        reply = QMessageBox.warning(
            self, "删除", "确定删除?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            Mod(name=self.name, path=self.path).del_mod()
            self.ModDeleted.emit(self.name)
