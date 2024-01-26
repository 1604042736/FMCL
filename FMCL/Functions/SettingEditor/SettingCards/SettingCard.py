from PyQt5.QtWidgets import QGridLayout, QWidget
from PyQt5.QtCore import pyqtSignal


class SettingCard(QWidget):
    def __new__(cls, id, setting):
        if cls == SettingCard:
            from .BoolSettingCard import BoolSettingCard
            from .ColorSettingCard import ColorSettingCard
            from .IntSettingCard import IntSettingCard
            from .ListSettingCard import ListSettingCard
            from .StrSettingCard import StrSettingCard

            value = setting.get(id)
            if setting.getAttr(id, "type") == "color":
                return ColorSettingCard(id, setting)
            elif isinstance(value, bool):
                return BoolSettingCard(id, setting)
            elif isinstance(value, int):
                return IntSettingCard(id, setting)
            elif isinstance(value, str):
                return StrSettingCard(id, setting)
            elif isinstance(value, list):
                return ListSettingCard(id, setting)

        return super().__new__(cls)

    def __init__(self, id: str, setting) -> None:
        super().__init__()
        self.id = id
        self.setting = setting
        self._layout = QGridLayout(self)

    def sync(self):
        self.setting.sync()

    def refresh(self):
        pass
