from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSpinBox
import Globals as g


class IntSetting(QWidget):
    """类型为int的设置"""

    def __init__(self, id, name, val, parent=None) -> None:
        super().__init__(parent)
        self.id = id
        self.name = name
        self.val = val

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.sb_val = QSpinBox(self)
        self.sb_val.setMaximum(2**31-1)
        self.sb_val.setValue(val)
        self.sb_val.valueChanged.connect(self.save)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.sb_val)

        self.setLayout(self.hbox)

    def save(self) -> tuple:
        setattr(g, self.id, self.sb_val.value())
        g.save()