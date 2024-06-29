import qtawesome as qta
from PyQt5.QtWidgets import QWidget
from .AboutItem import AboutItem
from .ui_About import Ui_About

from Kernel import Kernel


class About(QWidget, Ui_About):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.information-outline"))

        for key, val in Kernel.getAbout().items():
            gl = getattr(self, f"gl_{key}")
            for i in val:
                widget = AboutItem(*i)
                gl.addWidget(widget)
