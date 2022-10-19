from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from .ui_ModItem import Ui_ModItem


class ModItem(QWidget, Ui_ModItem):
    modEnabledChanged = pyqtSignal(bool, str)

    def __init__(self, modenabled: bool, modname: str):
        super().__init__()
        self.setupUi(self)
        self.gl_main.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.modenabled = modenabled
        self.modname = modname

        self.cb_modenabled.setCheckState((0, 2)[modenabled])
        self.l_modname.setText(modname)

    @pyqtSlot(int)
    def on_cb_modenabled_stateChanged(self, _):
        modenabled = (False, True, True)[self.cb_modenabled.checkState()]
        if modenabled != self.modenabled:
            self.modenabled = modenabled
            self.modEnabledChanged.emit(self.modenabled, self.modname)
