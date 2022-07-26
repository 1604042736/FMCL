from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.Mods import Mods
from Ui.More.More import More
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent


class AllFunctions(QTableWidget, QFBNWidget):
    UNIT_WIDTH = 45

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.functions = {
            "下载Minecraft": Minecraft,
            "下载Mod": Mods,
            "更多": More
        }
        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(45)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(45)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(45)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setMinimumSectionSize(45)

        self.set_functions()
        self.cellDoubleClicked.connect(self.launch_function)

    def set_functions(self):
        self.clear()
        self.row_count = 1
        self.col_count = 1
        j = 0
        for key, val in self.functions.items():
            if j == self.max_col_count:
                j = 0
                self.row_count += 1
            elif j == self.col_count:
                self.col_count += 1
            self.setRowCount(self.row_count)
            self.setColumnCount(self.col_count)
            item = QTableWidgetItem()
            item.setText(key)
            if "icon" in val.__dict__:
                item.setIcon(qta.icon(val.icon))  # TODO 不是所有的图标都来自qta
            self.setItem(self.row_count-1, j, item)
            j += 1

    def launch_function(self, row, col):
        self.functions[self.item(row, col).text()]().show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_functions()
