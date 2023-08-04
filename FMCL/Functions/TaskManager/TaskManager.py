import inspect
import logging
import sys

import qtawesome as qta
from Kernel import Kernel
from PyQt5.QtCore import QObject, QTimer, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QShowEvent
from PyQt5.QtWidgets import QHeaderView, QTreeWidgetItem, QWidget

from .ui_TaskManger import Ui_TaskManager

_translate = Kernel.translate


def get_size(obj, seen=None):
    """Recursively finds size of objects in bytes"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if hasattr(obj, '__dict__'):
        for cls in obj.__class__.__mro__:
            if '__dict__' in cls.__dict__:
                d = cls.__dict__['__dict__']
                if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                    size += get_size(obj.__dict__, seen)
                break
    if isinstance(obj, dict):
        size += sum((get_size(v, seen) for v in obj.values()))
        size += sum((get_size(k, seen) for k in obj.keys()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        try:
            size += sum((get_size(i, seen) for i in obj))
        except TypeError:
            logging.exception(
                "Unable to get size of %r. This may lead to incorrect sizes. Please report this error.", obj)
    if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
        size += sum(get_size(getattr(obj, s), seen)
                    for s in obj.__slots__ if hasattr(obj, s))

    return size


class TaskManager(QWidget, Ui_TaskManager):
    instance = None
    new_count = 0

    def __new__(cls):
        if TaskManager.instance == None:
            TaskManager.instance = super().__new__(cls)
        TaskManager.new_count += 1
        return TaskManager.instance

    def __init__(self):
        if TaskManager.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.tasks"))
        self.task_attr = {
            _translate("对象"): lambda obj: obj.objectName(),
            _translate("类"): lambda obj: obj.__class__.__name__,
            _translate("标题"): lambda obj: obj.windowTitle(),
            _translate("内存"): lambda obj: f"{get_size(obj)}B"
        }
        self.tw_tasks.setColumnCount(len(self.task_attr))
        self.tw_tasks.setHeaderLabels(self.task_attr.keys())
        for i in range(len(self.task_attr.keys())):
            self.tw_tasks.header().setSectionResizeMode(i,
                                                        QHeaderView.ResizeMode.ResizeToContents)

        self.task_item: dict[QObject, QTreeWidgetItem] = {}
        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)

    def setItemAttr(self, task: QObject, item: QTreeWidgetItem):
        """设置item属性"""
        for i, key in enumerate(self.task_attr.keys()):
            try:
                item.setText(i, str(self.task_attr[key](task)))
            except:
                item.setText(i, "")
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
                self.refresh()
                break

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.timer.stop()
        return super().closeEvent(a0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.timer.start(1000)
        return super().showEvent(a0)
