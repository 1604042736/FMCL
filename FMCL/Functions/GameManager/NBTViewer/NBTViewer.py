import logging
import traceback
import qtawesome as qta
import os
from Events import *

from PyQt5.QtCore import pyqtSlot, QPoint, QEvent, QObject, Qt
from PyQt5.QtWidgets import (
    QWidget,
    QHeaderView,
    QTreeWidgetItem,
    QHBoxLayout,
    qApp,
    QAction,
)
from qfluentwidgets import TreeWidget, MessageBox, TransparentToolButton, RoundMenu

from Core import Save

from .ui_NBTViewer import Ui_NBTViewer


class NBTViewer(QWidget, Ui_NBTViewer):
    instances = {}
    new_count = {}

    def __new__(cls, path):
        if path not in NBTViewer.instances:
            NBTViewer.instances[path] = super().__new__(cls)
            NBTViewer.new_count[path] = 0
        NBTViewer.new_count[path] += 1
        return NBTViewer.instances[path]

    def __init__(self, path):
        if NBTViewer.new_count[path] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("msc.preview"))
        self.setWindowTitle(self.tr("NBT查看器") + f": {os.path.basename(path)}")
        self.tb_viewer.setAddButtonVisible(False)
        self.splitter.setSizes([200, 500])
        self.tw_directory.header().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.path = path
        # 打开方式
        self.open_way = {
            ".dat": DefaultViewer,
            ".dat_old": DefaultViewer,
        }
        self.item_file: list[tuple[QTreeWidgetItem, str]] = []
        self.viewer_instance = {}

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.refresh()

    def refresh(self):
        self.tw_directory.clear()
        while self.sw_viewer.count():
            self.deleteViewer(self.sw_viewer.currentWidget())

        def setdirectory(root: QTreeWidgetItem, path):
            for i in os.listdir(path):
                full_path = os.path.join(path, i)
                item = QTreeWidgetItem()
                item.setText(0, i)
                w_operate = None

                if os.path.isdir(full_path):
                    setdirectory(item, full_path)
                elif os.path.isfile(full_path):
                    name, ext = os.path.splitext(i)
                    if ext not in self.open_way:
                        continue
                    w_operate = QWidget()
                    hboxlayout = QHBoxLayout(w_operate)
                    hboxlayout.setSpacing(0)
                    hboxlayout.setContentsMargins(0, 0, 0, 0)

                    pb_open = TransparentToolButton()
                    pb_open.setFixedWidth(32)
                    pb_open.setToolTip(self.tr("打开"))
                    pb_open.setIcon(qta.icon("mdi6.page-next-outline"))
                    pb_open.clicked.connect(
                        lambda _, file=full_path: self.openFile(file)
                    )

                    pb_separate = TransparentToolButton()
                    pb_separate.setFixedWidth(32)
                    pb_separate.setToolTip(self.tr("打开并分离"))
                    pb_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
                    pb_separate.clicked.connect(
                        lambda _, file=full_path: self.openAndSeparateFile(file)
                    )

                    hboxlayout.addWidget(pb_open)
                    hboxlayout.addWidget(pb_separate)

                if not os.path.isdir(full_path) or item.childCount() > 0:
                    self.addTreeItem(root, item)
                    if w_operate != None:
                        self.tw_directory.setItemWidget(item, 1, w_operate)

        setdirectory(None, self.path)

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_directory.addTopLevelItem(item)
        else:
            root.addChild(item)

    def getViewer(self, file: str):
        if file in self.viewer_instance:
            return self.viewer_instance[file]
        _, ext = os.path.splitext(file)
        widget = self.open_way[ext](file)
        self.viewer_instance[file] = widget
        return widget

    def openFile(self, file: str):
        try:
            widget = self.getViewer(file)
            self.sw_viewer.addWidget(widget)
            self.sw_viewer.setCurrentIndex(self.sw_viewer.count() - 1)
        except:
            logging.error(traceback.format_exc())
            MessageBox("", self.tr("无法打开") + f"{file}", self).exec()

    def separateViewer(self, widget):
        qApp.sendEvent(self, SeparateWidgetEvent(widget, self.size()))
        a_back = QAction(widget)
        a_back.setText(self.tr("合并"))
        a_back.setIcon(qta.icon("msc.reply"))
        a_back.triggered.connect(
            lambda: (
                self.sw_viewer.addWidget(widget),
                self.sw_viewer.setCurrentIndex(self.sw_viewer.count() - 1),
            )
        )
        qApp.sendEvent(widget.window(), AddToTitleMenuEvent(a_back))

    def openAndSeparateFile(self, file: str):
        try:
            viewer = self.getViewer(file)
            if viewer == None:
                return
            self.separateViewer(viewer)
        except:
            logging.error(traceback.format_exc())
            MessageBox("", self.tr("无法打开") + f"{file}", self).exec()

    def deleteViewer(self, widget):
        self.removeViewer(widget)
        for key, val in self.viewer_instance.items():
            if val == widget:
                break
        else:
            return
        self.viewer_instance.pop(key)

    def removeViewer(self, widget):
        self.sw_viewer.removeWidget(widget)
        self.tb_viewer.removeTabByKey(widget.objectName())
        widget.removeEventFilter(self)

    @pyqtSlot(int)
    def on_sw_viewer_currentChanged(self, _):
        widget = self.sw_viewer.currentWidget()
        if widget == None:
            return
        if self.tb_viewer.tab(widget.objectName()) == None:
            tabitem = self.tb_viewer.addTab(
                widget.objectName(),
                text=widget.windowTitle(),
                icon=widget.windowIcon(),
                onClick=lambda: self.sw_viewer.setCurrentWidget(widget),
            )
            tabitem.closed.connect(lambda: self.deleteViewer(widget))
            tabitem.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            tabitem.customContextMenuRequested.connect(
                lambda: self.showRightMenu(widget, tabitem)
            )
            tabitem.setToolTip(widget.windowTitle())
            widget.installEventFilter(self)
        self.tb_viewer.setCurrentTab(widget.objectName())

    def showRightMenu(self, widget, button):
        menu = RoundMenu(self)
        a_separate = QAction(self)
        a_separate.setText(self.tr("分离"))
        a_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
        a_separate.triggered.connect(lambda: self.separateViewer(widget))
        menu.addAction(a_separate)

        menu.exec(
            button.mapToGlobal(
                QPoint((button.width() - menu.view.width()) // 2, button.height())
            )
        )

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if self.tb_viewer.tab(a0.objectName()) != None:
            if a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
                a0.setParent(None)
            elif a1.type() == QEvent.Type.ParentChange and a0.parent() != self:
                self.removeViewer(a0)
            elif a1.type() == QEvent.Type.Show:
                self.sw_viewer.setCurrentWidget(a0)
        return super().eventFilter(a0, a1)

    def event(self, a0: QEvent | None) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)


class DefaultViewer(TreeWidget):
    def __init__(self, file):
        super().__init__()
        self.setObjectName(file)
        self.setWindowTitle(os.path.basename(file))
        self.setColumnCount(2)
        self.headerItem().setText(0, self.tr("键(或者索引)"))
        self.headerItem().setText(1, self.tr("值"))
        self.file = file
        self.refresh()

    def refresh(self):
        self.clear()

        def setnbt(root: QTreeWidgetItem, nbt: dict | list):
            if isinstance(nbt, list):
                for i, val in enumerate(nbt):
                    item = QTreeWidgetItem()
                    item.setText(0, str(i))

                    if isinstance(val, (dict, list)):
                        setnbt(item, val)
                    else:
                        item.setText(1, str(val))

                    self.addTreeItem(root, item)
                return
            for key, val in nbt.items():
                item = QTreeWidgetItem()
                item.setText(0, key)

                if isinstance(val["value"], (dict, list)):
                    setnbt(item, val["value"])
                else:
                    item.setText(1, str(val["value"]))

                self.addTreeItem(root, item)

        setnbt(None, Save.get_nbt(self.file)["value"])

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.addTopLevelItem(item)
        else:
            root.addChild(item)
