from Core import Function
from Kernel import Kernel
from PyQt5.QtCore import QEvent, QSize
from PyQt5.QtWidgets import QListView, QListWidgetItem
from qfluentwidgets import ListWidget


class AllFunctions(ListWidget):
    """所有功能"""

    __instance = None
    __new_count = 0

    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        cls.__new_count += 1
        return cls.__instance

    def __init__(self):
        if self.__new_count > 1:
            return
        super().__init__()
        self.setObjectName("AllFunctions")
        self.setMovement(QListView.Movement.Static)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setWordWrap(True)

        self.refresh()
        self.itemClicked.connect(self.launchFunc)

    def refresh(self):
        self.clear()
        self.item_id = []
        for function_info in Function.get_all_info():
            if "Explorer" in function_info["id"]:
                continue
            name = function_info["name"]
            icon = function_info["icon"]
            item = QListWidgetItem()
            item.setSizeHint(QSize(80, 80))
            item.setText(name)
            item.setIcon(icon)
            item.setToolTip(name)
            self.addItem(item)
            self.item_id.append((item, function_info["id"]))

    def launchFunc(self):
        for item, id in self.item_id:
            if item == self.currentItem():
                Function(id).exec()
                break

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)
