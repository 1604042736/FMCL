import qtawesome as qta
from Events import *

from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget, qApp
from qfluentwidgets import TransparentToolButton

from .ui_ResDetail import Ui_ResDetail


class ResDetail(QWidget, Ui_ResDetail):
    instances = {}
    new_count = {}

    def __new__(cls, res):
        _res = str(res)
        if _res not in ResDetail.instances:
            ResDetail.instances[_res] = super().__new__(cls)
            ResDetail.new_count[_res] = 0
        ResDetail.new_count[_res] += 1
        return ResDetail.instances[_res]

    def __init__(self, res) -> None:
        if ResDetail.new_count[str(res)] > 1:
            return
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(qta.icon("mdi.puzzle-outline"))
        self.res = res

        self.pb_refresh = TransparentToolButton()
        self.pb_refresh.resize(46, 32)
        self.pb_refresh.setIcon(qta.icon("mdi.refresh"))
        self.pb_refresh.clicked.connect(lambda: self.refresh())

    def refresh(self):
        pass

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            qApp.sendEvent(self.window(), AddToTitleEvent(self.pb_refresh, "right"))
        elif a0.type() == QEvent.Type.Hide:
            qApp.sendEvent(self.window(), RemoveFromTitleEvent(self.pb_refresh))
            self.pb_refresh.setParent(self)
        return super().event(a0)
