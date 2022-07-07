from Core.Mod import Mod
from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.ModInfo import ModInfo
from Ui.Downloader.ui_Mods import Ui_Mods
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import QSize,pyqtSignal
import Globals as g


class Mods(QFBNWidget, Ui_Mods):
    _ResultsOut=pyqtSignal(list)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.pb_search.clicked.connect(self.search_mod)

        self._ResultsOut.connect(self.set_results)

    @g.run_as_thread
    def search_mod(self, *_):
        key = self.le_search.text()
        result = Mod(name=key).search_mod()
        self._ResultsOut.emit(result)

    def set_results(self, result):
        self.lw_result.clear()
        for i in result:
            item = QListWidgetItem()
            item.setSizeHint(QSize(256, 100))
            widget = ModInfo(i)
            self.lw_result.addItem(item)
            self.lw_result.setItemWidget(item, widget)
