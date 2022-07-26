from QtFBN.QFBNWidget import QFBNWidget
from Ui.VersionManager.ui_IconSelector import Ui_IconSelector
from PyQt5.QtGui import QResizeEvent, QIcon
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog
from PyQt5.QtCore import pyqtSignal


class IconSelector(QFBNWidget, Ui_IconSelector):
    UNIT_WIDTH = 64
    Selected = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.row_count = 1
        self.col_count = 1
        self.max_col_count = 16

        self.pb_ok.clicked.connect(self.selected)
        self.pb_ok.clicked.connect(self.close)
        self.pb_cancel.clicked.connect(self.close)
        self.pb_custom.clicked.connect(self.set_custom)
        self.set_default()

    def set_default(self):
        default_icons = ["bookshelf.png", "chest.png", "command.png", "craft_table.png", "fabric.png",
                         "forge.png", "furnace.png", "grass.png"]
        self.tw_default.clear()
        self.row_count = 1
        self.col_count = 1
        j = 0
        for i in default_icons:
            if j == self.max_col_count:
                j = 0
                self.row_count += 1
            elif j == self.col_count:
                self.col_count += 1
            self.tw_default.setRowCount(self.row_count)
            self.tw_default.setColumnCount(self.col_count)
            item = QTableWidgetItem()
            item.setText(i)
            item.setIcon(QIcon(f":/Image/{i}"))
            self.tw_default.setItem(self.row_count-1, j, item)
            j += 1

    def set_custom(self):
        path = QFileDialog.getOpenFileName(self, '选择图标', ".")[0]
        if path:
            self.le_custom.setText(path)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_default()

    def selected(self):
        if self.tw_default.currentItem():
            default_icon = f":/Image/{self.tw_default.currentItem().text()}"
        else:
            default_icon = ""
        custom_icon = self.le_custom.text()
        if custom_icon:
            self.Selected.emit(custom_icon)
        elif default_icon:
            self.Selected.emit(default_icon)
