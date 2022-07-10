from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QColorDialog
import Globals as g


class ColorSetting(QWidget):
    def __init__(self, id, name, val, parent=None):
        super().__init__(parent)
        self.id = id
        self.name = name
        self.val = val

        self.hbox = QHBoxLayout()

        self.l_name = QLabel(self)
        self.l_name.setText(self.name)

        self.l_color = QLabel(self)
        self.l_color.setStyleSheet(f"background-color:{self.val}")

        self.pb_change = QPushButton(self)
        self.pb_change.setText("更改")
        self.pb_change.clicked.connect(self.save)

        self.hbox.addWidget(self.l_name)
        self.hbox.addWidget(self.l_color)
        self.hbox.addWidget(self.pb_change)

        self.setLayout(self.hbox)

    def save(self):
        color = QColorDialog.getColor().getRgb()
        self.val = f"rgba({','.join(map(str,color))})"
        self.l_color.setStyleSheet(f"background-color:{self.val}")
        setattr(g, self.id, self.val)
        g.set_theme()
