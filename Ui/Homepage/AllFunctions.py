from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Downloader import Downloader
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.Mods import Mods
from Ui.Homepage.ui_AllFunctions import Ui_AllFunctions
from Ui.More.More import More
from PyQt5.QtWidgets import QTableWidgetItem
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent


class AllFunctions(QFBNWidget, Ui_AllFunctions):
    UNIT_WIDTH = 45

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.functions = {
            "下载Minecraft": Minecraft,
            "下载Mod": Mods,
            "更多": More
        }
        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16
        self.set_functions()
        self.tw_func.cellDoubleClicked.connect(self.launch_function)

    def set_functions(self):
        self.tw_func.clear()
        self.row_count = 1
        self.col_count = 1
        j = 0
        for key, val in self.functions.items():
            if j == self.max_col_count:
                j = 0
                self.row_count += 1
            elif j == self.col_count:
                self.col_count += 1
            self.tw_func.setRowCount(self.row_count)
            self.tw_func.setColumnCount(self.col_count)
            item = QTableWidgetItem()
            item.setText(key)
            if "icon" in val.__dict__:
                item.setIcon(qta.icon(val.icon))  # TODO 不是所有的图标都来自qta
            self.tw_func.setItem(self.row_count-1, j, item)
            j += 1

    def launch_function(self, row, col):
        self.functions[self.tw_func.item(row, col).text()]().show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_functions()
