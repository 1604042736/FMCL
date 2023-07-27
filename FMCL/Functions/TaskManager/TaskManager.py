import qtawesome as qta
from Kernel import Kernel
from PyQt5.QtCore import QObject, QTimer, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QShowEvent
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget

from .ui_TaskManger import Ui_TaskManager


class TaskManager(QWidget, Ui_TaskManager):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.tasks"))
        self.task_attr = {
            "objectName": lambda obj: obj.objectName(),
            "class": lambda obj: obj.__class__.__name__,
            "windowTitle": lambda obj: obj.windowTitle()
        }
        self.tw_tasks.setColumnCount(len(self.task_attr))
        self.tw_tasks.setHeaderLabels(self.task_attr.keys())

        self.task_item: dict[QObject, QTreeWidgetItem] = {}
        self.roots = {}
        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(1000)

    def setItemAttr(self, task: QObject, item: QTreeWidgetItem):
        """设置item属性"""
        for i, key in enumerate(self.task_attr.keys()):
            try:
                item.setText(i, str(self.task_attr[key](task)))
            except:
                item.setText(i, "NULL")
        if hasattr(task, "windowIcon"):
            item.setIcon(0, task.windowIcon())

    def removeItem(self, item: QTreeWidgetItem):
        try:
            if item.parent() != None:
                item.parent().removeChild(item)
            else:
                self.tw_tasks.takeTopLevelItem(
                    self.tw_tasks.indexOfTopLevelItem(item))
        except RuntimeError:
            pass

    def refresh(self):
        tasks = list(Kernel.tasks)
        # 移除不存在的task
        for task in tuple(self.task_item.keys()):
            if task not in tasks:
                item = self.task_item.pop(task)
                self.removeItem(item)
        for task in tasks:
            try:
                root = None
                if task.parent() in self.task_item:
                    root = self.task_item[task.parent()]
                if task in self.task_item:
                    child = self.task_item[task]
                else:
                    child = QTreeWidgetItem(self.tw_tasks)
                self.setItemAttr(task, child)
                if root:
                    if root.indexOfChild(child) == -1:
                        self.removeItem(child)
                        root.addChild(child)
                        child.setExpanded(True)
                        root.setExpanded(True)
                else:
                    self.tw_tasks.addTopLevelItem(child)
                self.task_item[task] = child
            except RuntimeError:
                if task in self.task_item:
                    self.task_item.pop(task)

    @pyqtSlot(bool)
    def on_pb_stop_clicked(self, _):
        for task, item in self.task_item.items():
            if self.tw_tasks.currentItem() == item:
                task.close()
                self.removeItem(self.task_item.pop(task))
                break

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.timer.stop()
        return super().closeEvent(a0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.timer.start(1000)
        return super().showEvent(a0)
