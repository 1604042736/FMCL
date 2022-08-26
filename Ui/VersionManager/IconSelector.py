from QtFBN.QFBNDialog import QFBNDialog
from Translate import tr
from Ui.VersionManager.ui_IconSelector import Ui_IconSelector
from PyQt5.QtGui import QResizeEvent, QIcon
from PyQt5.QtWidgets import QFileDialog, QListWidgetItem
from PyQt5.QtCore import pyqtSignal


class IconSelector(QFBNDialog, Ui_IconSelector):
    UNIT_WIDTH = 80
    Selected = pyqtSignal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(tr("图标选择"))
        self.pb_custom.setText(tr("自定义图标"))
        self.le_custom.setPlaceholderText(tr("这是自定义图标的路径"))
        self.pb_ok.setText(tr("确定"))
        self.pb_cancel.setText(tr("取消"))

        self.pb_ok.clicked.connect(self.selected)
        self.pb_ok.clicked.connect(self.close)
        self.pb_cancel.clicked.connect(self.close)
        self.pb_custom.clicked.connect(self.set_custom)
        self.set_default()

    def set_default(self):
        default_icons = ["bookshelf.png", "chest.png", "command.png", "craft_table.png", "fabric.png",
                         "forge.png", "furnace.png", "grass.png"]
        self.lw_default.clear()
        for i in default_icons:
            item = QListWidgetItem()
            item.setText(i)
            item.setIcon(QIcon(f":/Image/{i}"))
            self.lw_default.addItem(item)

    def set_custom(self):
        path = QFileDialog.getOpenFileName(self, tr('选择图标'), ".")[0]
        if path:
            self.le_custom.setText(path)

    def resizeEvent(self, a0: QResizeEvent) -> None:
        self.max_col_count = int(self.width()/self.UNIT_WIDTH)
        self.set_default()
        super().resizeEvent(a0)

    def selected(self):
        if self.lw_default.currentItem():
            default_icon = f":/Image/{self.lw_default.currentItem().text()}"
        else:
            default_icon = ""
        custom_icon = self.le_custom.text()
        # 优先选择custom_icon
        if custom_icon:
            self.Selected.emit(custom_icon)
        elif default_icon:
            self.Selected.emit(default_icon)
