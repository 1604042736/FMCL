from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication
from PyQt5.QtCore import pyqtSignal
from QtFBN.QFBNMessageBox import QFBNMessageBox
from Core.Mod import Mod
from Translate import tr


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
            pass

        self.pb_edable = QPushButton(self)
        self.pb_edable.setText(tr("禁用"))
        self.pb_edable.clicked.connect(self.endisable_mod)
        if "disabled" in self.name:
            self.pb_edable.setText(tr("启用"))

        self.pb_del = QPushButton(self)
        self.pb_del.setText(tr("删除"))
        self.pb_del.clicked.connect(self.del_mod)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.pb_edable)
        self.hbox.addWidget(self.pb_del)

        self.setLayout(self.hbox)

    def endisable_mod(self):
        result, new_name = Mod(name=self.name, path=self.path).endisable_mod()
        if result == "disabled":
            self.pb_edable.setText(tr("启用"))
        else:
            self.pb_edable.setText(tr("禁用"))
        self.ModEnDisAble.emit(self.name, new_name)
        self.name = new_name

    def del_mod(self):
        def ok():
            Mod(name=self.name, path=self.path).del_mod()
            self.ModDeleted.emit(self.name)
        msgbox = QFBNMessageBox.info(self, tr("删除"), tr("确定删除")+"?", ok)
        msgbox.show("original")
