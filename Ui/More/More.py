import webbrowser
from QtFBN.QFBNWidget import QFBNWidget
from Ui.More.ui_More import Ui_More
from PyQt5.QtCore import pyqtSlot
import Globals as g
import qtawesome as qta


class More(QFBNWidget, Ui_More):
    icon_exp = 'qta.icon("ph.squares-four-fill")'

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(eval(self.icon_exp))

        self.l_fmclversion.setText(
            self.l_fmclversion.text()+f"[v{g.TAG_NAME}]")

    @pyqtSlot(bool)
    def on_pb_opensourceurl_clicked(self, _):
        webbrowser.open("https://github.com/1604042736/FMCL")

    @pyqtSlot(bool)
    def on_pb_openbangurl_clicked(self, _):
        webbrowser.open("https://bmclapidoc.bangbang93.com")

    @pyqtSlot(bool)
    def on_pb_openhmclurl_clicked(self, _):
        webbrowser.open("https://github.com/huanghongxun/HMCL")
