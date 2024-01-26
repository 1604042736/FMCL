import logging
import os
import traceback
import qtawesome as qta
from Events import *

from PyQt5.QtCore import QObject, QSize, QEvent, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QListWidgetItem, QInputDialog, qApp
from qfluentwidgets import MessageBox, TransparentToolButton, StateToolTip
from Core import Version

from .ui_ScreenshotManager import Ui_ScreenshotManager


class ScreenshotManager(QWidget, Ui_ScreenshotManager):
    def __init__(self, name):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("ei.picture"))
        self.icon_width = self.lw_overview.iconSize().width()
        self.lw_overview.installEventFilter(self)
        self.w_operate.setEnabled(False)
        self.game = Version(name)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        # 交给GameManager刷新
        # self.refresh()

    def refresh(self):
        statetooltip = StateToolTip(self.tr("正在加载截图"), "", self)
        statetooltip.move(statetooltip.getSuitablePos())
        statetooltip.show()

        self.lw_overview.clear()
        screenshot_path = self.game.get_screenshot_path()

        n = len(os.listdir(screenshot_path))
        for i, file in enumerate(os.listdir(screenshot_path)):
            path = os.path.join(screenshot_path, file)
            try:
                item = QListWidgetItem()
                item.setIcon(QIcon(path))
                item.setText(file)
                item.setToolTip(path)
                item.setSizeHint(QSize(256, 190))
                self.lw_overview.addItem(item)
            except:
                logging.error(f"无法加载截图{path}:\n{traceback.format_exc()}")

            statetooltip.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        statetooltip.setContent(self.tr("加载完成"))
        statetooltip.setState(True)

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a0 == self.lw_overview:
            if a1.type() == QEvent.Type.Resize:
                # 设置Spacing, 让所有Item尽量居中
                w = (
                    self.lw_overview.width()
                    - self.lw_overview.verticalScrollBar().sizeHint().width()
                )
                n = w // self.icon_width
                m = w - self.icon_width * n
                spacing = m // (n + 1)
                self.lw_overview.setSpacing(spacing)
        return super().eventFilter(a0, a1)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)

    @pyqtSlot(bool)
    def on_pb_openfolder_clicked(self, _):
        os.startfile(self.game.get_screenshot_path())

    @pyqtSlot()
    def on_lw_overview_itemSelectionChanged(self):
        self.w_operate.setEnabled(self.lw_overview.currentItem() != None)

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        item = self.lw_overview.currentItem()
        if item == None:
            return
        name = item.text()

        def confirmDelete():
            self.game.delete_screenshots(name)
            self.refresh()

        box = MessageBox(
            self.tr("删除"), self.tr("确认删除") + str(name) + "?", self.window()
        )
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_rename_clicked(self, _):
        item = self.lw_overview.currentItem()
        if item == None:
            return
        old_name = item.text()
        new_name, ok = QInputDialog.getText(
            None, self.tr("重命名"), self.tr("请输入新的名称"), text=old_name
        )
        if ok:
            self.game.rename_screenshot(old_name, new_name)
            self.refresh()

    @pyqtSlot(bool)
    def on_pb_open_clicked(self, _):
        item = self.lw_overview.currentItem()
        if item == None:
            return
        name = item.text()
        self.game.open_screenshot(name)
