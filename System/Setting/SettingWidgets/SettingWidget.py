import qtawesome as qta
from PyQt5.QtWidgets import QWidget
import qtawesome as qta
from PyQt5.QtCore import QEvent
from System.Constants import *


class SettingWidget(QWidget):
    __instances = {}
    new_count = {}

    def __new__(cls, id, value):
        if cls == SettingWidget:
            from .DictSettingWidget import DictSettingWidget
            from .ListSettingWidget import ListSettingWidget
            if isinstance(value, dict):
                return DictSettingWidget(id, value)
            elif isinstance(value, list):
                return ListSettingWidget(id, value)

        if id not in SettingWidget.__instances:
            SettingWidget.__instances[id] = super().__new__(cls)
            SettingWidget.new_count[id] = 0
        SettingWidget.new_count[id] += 1
        return SettingWidget.__instances[id]

    def __init__(self, id: str, value):
        if SettingWidget.new_count[id] > 1:
            return
        super().__init__()
        self.id = id  # 设置项的名称
        self.value = value

        self.resize(W_SETTING, H_SETTING)
        self.setWindowIcon(qta.icon("ri.settings-5-line"))
        name = id.split("#")[-1].split("/")[-1]
        if name:
            self.window_title = f"设置: {name}"
        else:
            self.window_title = f"设置"
        self.setWindowTitle(self.window_title)

    def refresh(self):
        pass

    def event(self, a0: QEvent) -> bool:
        if a0.type() == QEvent.Type.Show:
            self.refresh()
        return super().event(a0)
