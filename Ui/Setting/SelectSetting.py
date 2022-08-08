from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QHBoxLayout
import Globals as g


class SelectSetting(QWidget):
    """类型为tuple的设置"""

    def __init__(self, id, name, val, parent=None) -> None:
        super().__init__(parent)
        self.id = id
        self.name = name
        self.val = val

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(name)

        self.cb_val = QComboBox(self)
        self.cb_val.addItems(val)
        self.cb_val.setCurrentText(getattr(g, self.id))
        self.cb_val.currentIndexChanged.connect(self.save)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.cb_val)

        self.setLayout(self.hbox)

    def save(self):
        setattr(g, self.id, self.cb_val.currentText())
        g.save()