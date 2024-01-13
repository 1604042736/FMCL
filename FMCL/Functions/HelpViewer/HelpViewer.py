import logging
import qtawesome as qta
from Events import *

from PyQt5.QtCore import QEvent, pyqtSlot, Qt, QPoint, QObject
from PyQt5.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QLabel,
    qApp,
    QAction,
    QHeaderView,
)
from qfluentwidgets import TransparentToolButton, TabItem, RoundMenu

from Kernel import Kernel

from .ui_HelpViewer import Ui_HelpViewer


class HelpViewer(QWidget, Ui_HelpViewer):
    instance = None
    new_count = 0

    def __new__(cls):
        if HelpViewer.instance == None:
            HelpViewer.instance = super().__new__(cls)
        HelpViewer.new_count += 1
        return HelpViewer.instance

    def __init__(self) -> None:
        if HelpViewer.new_count > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.help"))
        self.splitter.setSizes([200, 500])
        self.tw_helpindex.header().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        self.item_id: list[tuple[QTreeWidgetItem, str]] = []
        self.page_instance = {}

        self.tb_pages.setAddButtonVisible(False)

        self.refresh()

    def refresh(self):
        self.item_id = []
        self.page_instance = {}

        self.tw_helpindex.clear()
        while self.sw_pages.count():
            self.sw_pages.removeWidget(self.sw_pages.currentWidget())
        helpindex = self.helpindex = Kernel.getHelpIndex()

        def sethelpindex(root: QTreeWidgetItem | None, data: dict, id: str):
            for key, val in data.items():
                if key in Kernel.HELPINDEX_KEYWORD:
                    continue
                item = QTreeWidgetItem()
                item.setText(0, val["name"])
                self.addTreeItem(root, item)

                _id = (id + f".{key}").strip(".")
                self.item_id.append((item, _id))

                if "page" in val:
                    w_operate = QWidget()
                    hboxlayout = QHBoxLayout(w_operate)
                    hboxlayout.setSpacing(0)
                    hboxlayout.setContentsMargins(0, 0, 0, 0)

                    pb_open = TransparentToolButton()
                    pb_open.setFixedWidth(32)
                    pb_open.setToolTip(self.tr("打开页面"))
                    pb_open.setIcon(qta.icon("mdi6.page-next-outline"))
                    pb_open.clicked.connect(lambda _, id=_id: self.openPage(id))

                    pb_separate = TransparentToolButton()
                    pb_separate.setFixedWidth(32)
                    pb_separate.setToolTip(self.tr("打开并分离页面"))
                    pb_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
                    pb_separate.clicked.connect(
                        lambda _, id=_id: self.openAndSeparatePage(id)
                    )

                    hboxlayout.addWidget(pb_open)
                    hboxlayout.addWidget(pb_separate)

                    self.tw_helpindex.setItemWidget(item, 1, w_operate)

                sethelpindex(item, val, _id)

        sethelpindex(None, helpindex, "")

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_helpindex.addTopLevelItem(item)
        else:
            root.addChild(item)

    def getPage(self, id: str) -> QWidget:
        """根据id获得对应的帮助界面"""
        attr = Kernel.getHelpIndexAttr(self.helpindex, id)
        if "page" not in attr:
            return
        if id in self.page_instance:
            page = self.page_instance[id]
        else:
            page = attr["page"]()
            self.page_instance[id] = page
        return page

    def openPage(self, id: str):
        logging.info(f"打开帮助页面: {id}")
        page = self.getPage(id)
        if page == None:
            return

        self.sw_pages.addWidget(page)
        self.sw_pages.setCurrentIndex(self.sw_pages.count() - 1)

        for item, id_ in self.item_id:
            if id != id_ and id.find(id_) == 0:
                item.setExpanded(True)

    def separatePage(self, widget):
        qApp.sendEvent(self, SeparateWidgetEvent(widget, self.size()))
        a_back = QAction(widget)
        a_back.setText(self.tr("合并"))
        a_back.setIcon(qta.icon("msc.reply"))
        a_back.triggered.connect(
            lambda: (
                self.sw_pages.addWidget(widget),
                self.sw_pages.setCurrentIndex(self.sw_pages.count() - 1),
            )
        )
        qApp.sendEvent(widget.window(), AddToTitleMenuEvent(a_back))

    def openAndSeparatePage(self, id: str):
        """打开并使帮助页面分离出去"""
        page = self.getPage(id)
        if page == None:
            return
        self.separatePage(page)

    def deletePage(self, widget):
        self.removePage(widget)
        for key, val in self.page_instance.items():
            if val == widget:
                break
        else:
            return
        self.page_instance.pop(key)

    def removePage(self, widget):
        self.sw_pages.removeWidget(widget)
        self.tb_pages.removeTabByKey(widget.objectName())
        widget.removeEventFilter(self)

    def show(self, id=""):
        super().show()
        if id:
            self.openPage(id)

    @pyqtSlot(int)
    def on_sw_pages_currentChanged(self, _):
        widget = self.sw_pages.currentWidget()
        if widget == None:
            return
        if self.tb_pages.tab(widget.objectName()) == None:
            tabitem = self.tb_pages.addTab(
                widget.objectName(),
                text=widget.windowTitle(),
                icon=widget.windowIcon(),
                onClick=lambda: self.sw_pages.setCurrentWidget(widget),
            )
            tabitem.closed.connect(lambda: self.deletePage(widget))
            tabitem.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            tabitem.customContextMenuRequested.connect(
                lambda: self.showRightMenu(widget, tabitem)
            )
            widget.installEventFilter(self)
        self.tb_pages.setCurrentTab(widget.objectName())

    def showRightMenu(self, widget, button):
        """显示任务栏按钮的右键菜单"""
        menu = RoundMenu(self)
        a_separate = QAction(self)
        a_separate.setText(self.tr("分离"))
        a_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
        a_separate.triggered.connect(lambda: self.separatePage(widget))
        menu.addAction(a_separate)

        menu.exec(
            button.mapToGlobal(
                QPoint((button.width() - menu.view.width()) // 2, button.height())
            )
        )

    def eventFilter(self, a0: QObject, a1: QEvent) -> bool:
        if self.tb_pages.tab(a0.objectName()) != None:
            if a1.type() in (QEvent.Type.Close, QEvent.Type.DeferredDelete):
                a0.setParent(None)
            elif a1.type() == QEvent.Type.ParentChange and a0.parent() != self:
                self.removePage(a0)
            elif a1.type() == QEvent.Type.Show:
                self.sw_pages.setCurrentWidget(a0)
        return super().eventFilter(a0, a1)
