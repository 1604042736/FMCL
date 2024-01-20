import inspect
import logging
import sys

import qtawesome as qta
from PyQt5.QtCore import QObject, QTimer, pyqtSlot
from PyQt5.QtGui import QCloseEvent, QShowEvent
from PyQt5.QtWidgets import QTreeWidgetItem, QWidget, qApp

from .ui_WidgetManager import Ui_WidgetManager


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
    if hasattr(obj, "__dict__"):
        for cls in obj.__class__.__mro__:
            if "__dict__" in cls.__dict__:
                d = cls.__dict__["__dict__"]
                if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                    size += get_size(obj.__dict__, seen)
                break
    if isinstance(obj, dict):
        size += sum((get_size(v, seen) for v in obj.values()))
        size += sum((get_size(k, seen) for k in obj.keys()))
    elif hasattr(obj, "__iter__") and not isinstance(obj, (str, bytes, bytearray)):
        try:
            size += sum((get_size(i, seen) for i in obj))
        except TypeError:
            logging.exception(
                "Unable to get size of %r. This may lead to incorrect sizes. Please report this error.",
                obj,
            )
    if hasattr(obj, "__slots__"):  # can have __slots__ with __dict__
        size += sum(
            get_size(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s)
        )

    return size


class WidgetManager(QWidget, Ui_WidgetManager):
    instance = None
    new_count = 0

    def __new__(cls):
        if WidgetManager.instance == None:
            WidgetManager.instance = super().__new__(cls)
        WidgetManager.new_count += 1
        return WidgetManager.instance

    def __init__(self):
        if WidgetManager.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.widgets"))
        self.widget_attr = {
            self.tr("对象名称"): lambda obj: obj.objectName(),
            self.tr("类"): lambda obj: obj.__class__.__name__,
            self.tr("标题"): lambda obj: obj.windowTitle(),
            self.tr("内存"): lambda obj: f"{get_size(obj)}B",
        }
        self.tw_widgets.setColumnCount(len(self.widget_attr))
        self.tw_widgets.setHeaderLabels(self.widget_attr.keys())

        self.widget_item: dict[QObject, QTreeWidgetItem] = {}
        self.refresh()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh)

    def setItemAttr(self, widget: QObject, item: QTreeWidgetItem):
        """设置item属性"""
        for i, key in enumerate(self.widget_attr.keys()):
            try:
                item.setText(i, str(self.widget_attr[key](widget)))
            except:
                item.setText(i, "")
        if hasattr(widget, "windowIcon"):
            item.setIcon(0, widget.windowIcon())

    def removeItem(self, item: QTreeWidgetItem):
        try:
            if item.parent() != None:
                item.parent().removeChild(item)
            else:
                self.tw_widgets.takeTopLevelItem(
                    self.tw_widgets.indexOfTopLevelItem(item)
                )
        except RuntimeError:
            pass

    def refresh(self):
        widgets = qApp.allWidgets()
        # 移除不存在的widget
        for widget in tuple(self.widget_item.keys()):
            if widget not in widgets:
                item = self.widget_item.pop(widget)
                self.removeItem(item)
        # 为新的widget创建item
        for widget in widgets:
            if widget not in self.widget_item:
                item = QTreeWidgetItem()
                self.widget_item[widget] = item
        for widget in widgets:
            try:
                # 更改QTreeWidgetItem, 而不是删除之后再创建
                # 这样可以防止界面频繁刷新
                root = None
                if widget.parent() in self.widget_item:
                    root = self.widget_item[widget.parent()]
                child = self.widget_item[widget]
                self.setItemAttr(widget, child)
                if root:
                    if root.indexOfChild(child) == -1:
                        root.addChild(child)
                else:
                    self.tw_widgets.addTopLevelItem(child)
            except RuntimeError:
                if widget in self.widget_item:
                    self.widget_item.pop(widget)

    @pyqtSlot(bool)
    def on_pb_delete_clicked(self, _):
        for widget, item in self.widget_item.items():
            if self.tw_widgets.currentItem() == item:
                widget.deleteLater()
                self.refresh()
                break

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.timer.stop()
        return super().closeEvent(a0)

    def showEvent(self, a0: QShowEvent) -> None:
        self.timer.start(1000)
        return super().showEvent(a0)
