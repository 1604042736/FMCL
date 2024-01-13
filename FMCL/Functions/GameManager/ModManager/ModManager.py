import os

import qtawesome as qta
from Core import Mod, Version
from Events import *
from PyQt5.QtCore import pyqtSlot, QEvent, Qt
from PyQt5.QtWidgets import QListWidgetItem, QWidget, qApp
from qfluentwidgets import MessageBox, TransparentToolButton, InfoBar, InfoBarPosition

from .ModItem import ModItem
from .ui_ModManager import Ui_ModManager


class ModManager(QWidget, Ui_ModManager):
    def __init__(self, name: str):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))

        self.game = Version(name)
        self.game.generate_setting()
        self.f_operate.setEnabled(False)

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.total = 0
        self.enabled_num = 0

        self.refresh()

    def refresh(self):
        self.setEnabled(True)
        if not self.game.mod_avaiable():
            InfoBar.info(
                title=self.tr("该版本不支持模组"),
                content="",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self.window(),
            )
            self.setEnabled(False)
            return
        keyword = self.le_search.text()
        self.lw_mods.clear()
        mods = self.game.get_mods(keyword)
        self.total = len(mods)
        self.enabled_num = 0
        for mod in mods:
            if mod.enabled:
                self.enabled_num += 1
            item = QListWidgetItem()
            widget = ModItem(self.game, mod)
            widget.enabledChanged.connect(self.singlemodEnabledChanged)
            item.setSizeHint(widget.size())
            self.lw_mods.addItem(item)
            self.lw_mods.setItemWidget(item, widget)
        self.setStatistics()

    def singlemodEnabledChanged(self, enabled):
        if enabled:
            self.enabled_num += 1
        else:
            self.enabled_num -= 1
        self.setStatistics()

    def setStatistics(self):
        t1 = self.tr("总共")
        t2 = self.tr("启用")
        t3 = self.tr("禁用")
        t4 = self.tr("已选择")
        self.l_statistics.setText(
            f"{t1}: {self.total}, {t2}: {self.enabled_num}, {t3}: {self.total-self.enabled_num}, {t4}: {len(self.lw_mods.selectedItems())}"
        )

    @pyqtSlot(bool)
    def on_pb_openmodir_clicked(self, _):
        os.startfile(self.game.get_mod_path())

    @pyqtSlot()
    def on_le_search_editingFinished(self):
        self.refresh()

    @pyqtSlot()
    def on_lw_mods_itemSelectionChanged(self):
        if self.lw_mods.selectedItems():
            self.f_operate.setEnabled(True)
        else:
            self.f_operate.setEnabled(False)
        self.setStatistics()

    @pyqtSlot(bool)
    def on_pb_del_clicked(self, _):
        mods: list[Mod] = [
            self.lw_mods.itemWidget(item).mod for item in self.lw_mods.selectedItems()
        ]

        def confirmDelete():
            for mod in mods:
                mod.delete()
            self.refresh()

        box = MessageBox(
            self.tr("删除"), self.tr("确认删除") + str(mods) + "?", self.window()
        )
        box.yesSignal.connect(confirmDelete)
        box.exec()

    @pyqtSlot(bool)
    def on_pb_enabled_clicked(self, _):
        mods: list[Mod] = [
            self.lw_mods.itemWidget(item).mod for item in self.lw_mods.selectedItems()
        ]
        for mod in mods:
            mod.set_enabled(True)
        self.refresh()

    @pyqtSlot(bool)
    def on_pb_disabled_clicked(self, _):
        mods: list[Mod] = [
            self.lw_mods.itemWidget(item).mod for item in self.lw_mods.selectedItems()
        ]
        for mod in mods:
            mod.set_enabled(False)
        self.refresh()

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)
