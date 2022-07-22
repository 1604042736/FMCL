from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Downloader import Downloader
from Ui.Homepage.ui_AllFunctions import Ui_AllFunctions
from Ui.More.More import More
from PyQt5.QtWidgets import QTableWidgetItem
import qtawesome as qta


class AllFunctions(QFBNWidget, Ui_AllFunctions):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.functions = {
            "下载": Downloader,
            "更多": More
        }
        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16
        self.set_functions()
        self.tw_func.cellDoubleClicked.connect(self.launch_function)

    def set_functions(self):
        self.tw_func.clear()
        j = 0
        for key, val in self.functions.items():
            self.tw_func.setRowCount(self.row_count)
            self.tw_func.setColumnCount(self.col_count)
            item = QTableWidgetItem()
            item.setText(key)
            if "icon" in val.__dict__:
                item.setIcon(qta.icon(val.icon))  # TODO 不是所有的图标都来自qta
            self.tw_func.setItem(self.row_count-1, j, item)
            j += 1
            if j == self.max_col_count:
                j = 0
                self.row_count += 1
            elif j == self.col_count:
                self.col_count += 1

    def launch_function(self, row, col):
        self.functions[self.tw_func.item(row, col).text()]().show()
