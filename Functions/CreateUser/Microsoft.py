import qtawesome as qta
from PyQt5.QtWidgets import QWidget

from .ui_Microsoft import Ui_Microsoft


class Microsoft(QWidget, Ui_Microsoft):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.microsoft"))
    # FIXME
