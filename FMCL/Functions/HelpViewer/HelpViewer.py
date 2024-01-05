import logging
import qtawesome as qta
from Events import *

from PyQt5.QtCore import QEvent, pyqtSlot
from PyQt5.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QHBoxLayout,
    QLabel,
    qApp,
    QAction,
    QHeaderView,
)
from qfluentwidgets import TransparentToolButton

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

        self.w_operate = QWidget()
        self.hboxlayout = QHBoxLayout(self.w_operate)
        self.hboxlayout.setSpacing(0)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)

        self.pb_pre = TransparentToolButton()
        self.pb_pre.resize(46, 32)
        self.pb_pre.setIcon(qta.icon("mdi6.arrow-left"))
        self.pb_pre.clicked.connect(
            lambda: self.sw_pages.setCurrentIndex(
                self.sw_pages.currentIndex() - 1
                if self.sw_pages.currentIndex() - 1 >= 0
                else 0
            )
        )

        self.l_index = QLabel()
        self.l_index.setText("0/0")

        self.pb_next = TransparentToolButton()
        self.pb_next.resize(46, 32)
        self.pb_next.setIcon(qta.icon("mdi6.arrow-right"))
        self.pb_next.clicked.connect(
            lambda: self.sw_pages.setCurrentIndex(
                self.sw_pages.currentIndex() + 1
                if self.sw_pages.currentIndex() + 1 < self.sw_pages.count()
                else self.sw_pages.count() - 1
            )
        )

        self.pb_separate = TransparentToolButton()
        self.pb_separate.resize(46, 32)
        self.pb_separate.setIcon(qta.icon("ph.arrow-square-out-light"))
        self.pb_separate.clicked.connect(self.separate)

        self.pb_del = TransparentToolButton()
        self.pb_del.resize(46, 32)
        self.pb_del.setIcon(qta.icon("mdi.delete"))
        self.pb_del.clicked.connect(self.delete)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.hboxlayout.addWidget(self.pb_pre)
        self.hboxlayout.addWidget(self.l_index)
        self.hboxlayout.addWidget(self.pb_next)
        self.hboxlayout.addWidget(self.pb_separate)
        self.hboxlayout.addWidget(self.pb_del)
        self.hboxlayout.addWidget(self.pb_refresh)

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
                    button = TransparentToolButton()
                    button.setFixedWidth(32)
                    button.setToolTip(self.tr("打开页面"))
                    button.setIcon(qta.icon("mdi6.page-next-outline"))
                    button.clicked.connect(lambda _, id=_id: self.openPage(id))
                    self.tw_helpindex.setItemWidget(item, 1, button)

                sethelpindex(item, val, _id)

        sethelpindex(None, helpindex, "")

    def addTreeItem(self, root: QTreeWidgetItem | None, item: QTreeWidgetItem):
        if root == None:
            self.tw_helpindex.addTopLevelItem(item)
        else:
            root.addChild(item)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.w_operate, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.w_operate))
            self.w_operate.setParent(self)
        return super().event(a0)

    def openPage(self, id: str):
        logging.info(f"打开帮助页面: {id}")
        attr = Kernel.getHelpIndexAttr(self.helpindex, id)
        if "page" not in attr:
            return

        if id in self.page_instance:
            page = self.page_instance[id]
        else:
            page = attr["page"]()
            self.page_instance[id] = page
        self.sw_pages.addWidget(page)
        self.sw_pages.setCurrentIndex(self.sw_pages.count() - 1)

        for item, id_ in self.item_id:
            if id!=id_ and id.find(id_) == 0:
                item.setExpanded(True)

    def separate(self):
        widget = self.sw_pages.currentWidget()
        if widget == None:
            return
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

    def delete(self):
        widget = self.sw_pages.currentWidget()
        if widget == None:
            return
        self.sw_pages.removeWidget(widget)
        for key, val in self.page_instance.items():
            if val == widget:
                break
        else:
            return
        self.page_instance.pop(key)

    @pyqtSlot(int)
    def on_sw_pages_currentChanged(self, _):
        self.l_index.setText(
            f"{self.sw_pages.currentIndex()+1}/{self.sw_pages.count()}"
        )

    def show(self, id=""):
        super().show()
        if id:
            self.openPage(id)
