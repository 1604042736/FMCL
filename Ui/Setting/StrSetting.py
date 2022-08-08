from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit
import Globals as g


class StrSetting(QWidget):
    """类型为字符串的设置"""

    def __init__(self, id, name, val, parent=None) -> None:
        super().__init__(parent)
        self.id = id
        self.name = name
        self.val = val

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.le_val = QLineEdit(self)
        self.le_val.textEdited.connect(self.save)
        self.le_val.setText(val)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.le_val)

        self.setLayout(self.hbox)

    def save(self) -> tuple:
        setattr(g, self.id, self.le_val.text())
        g.save()
