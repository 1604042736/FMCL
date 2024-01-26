import os
from Core import Version
from Events import *
import qtawesome as qta
from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import (
    QWidget,
    qApp,
    QListWidgetItem,
)
from qfluentwidgets import TransparentToolButton, StateToolTip
from .ui_SaveManager import Ui_SaveManager
from .SaveItem import SaveItem


class SaveManager(QWidget, Ui_SaveManager):
    def __init__(self, name, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(qta.icon("fa.save"))

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

        self.name = name
        self.game = Version(name)

        # 交给GameManager刷新
        # self.refresh()

    def refresh(self):
        statetooltip = StateToolTip(self.tr("正在加载存档"), "", self)
        statetooltip.move(statetooltip.getSuitablePos())
        statetooltip.show()

        self.lw_saves.clear()
        save_path = self.game.get_save_path()

        n = len(os.listdir(save_path))
        for i, save in enumerate(os.listdir(save_path)):
            path = os.path.join(save_path, save)
            if not os.path.isdir(path):
                continue
            item = QListWidgetItem()
            widget = SaveItem(path)
            widget.saveDeleted.connect(self.refresh)
            item.setSizeHint(widget.size())
            self.lw_saves.addItem(item)
            self.lw_saves.setItemWidget(item, widget)

            statetooltip.setContent(f"{i+1}/{n}({round((i+1)/n*100,1)}%)")
            qApp.processEvents()

        statetooltip.setContent(self.tr("加载完成"))
        statetooltip.setState(True)

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)
