from QtFBN.QFBNWidget import QFBNWidget
from Ui.Downloader.Minecraft import Minecraft
from Ui.Downloader.Mods import Mods
from Ui.More.More import More
from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QAbstractItemView
import qtawesome as qta
from PyQt5.QtGui import QResizeEvent


class AllFunctions(QTableWidget, QFBNWidget):
    UNIT_WIDTH = 64

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("所有应用")
        self.functions = {
            "下载Minecraft": Minecraft,
            "下载Mod": Mods,
            "更多": More
        }
        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16

        self.horizontalHeader().setVisible(False)
        self.horizontalHeader().setDefaultSectionSize(self.UNIT_WIDTH)
        self.horizontalHeader().setHighlightSections(False)
        self.horizontalHeader().setMinimumSectionSize(self.UNIT_WIDTH)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(self.UNIT_WIDTH)
        self.verticalHeader().setHighlightSections(False)
        self.verticalHeader().setMinimumSectionSize(self.UNIT_WIDTH)

        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.set_functions()
        self.cellClicked.connect(self.launch_function)

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
            if "icon_exp" in val.__dict__:
                item.setIcon(eval(val.icon_exp))
            self.setItem(self.row_count-1, j, item)
            j += 1

    def launch_function(self, row, col):
        self.functions[self.item(row, col).text()]().show()

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_functions()
