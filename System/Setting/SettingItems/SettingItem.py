from PyQt5.QtWidgets import QGridLayout, QLabel, QWidget


class SettingItem(QWidget):
    def __new__(cls, id, setting):
        if cls == SettingItem:
            from .BoolSettingItem import BoolSettingItem
            from .DictSettingItem import DictSettingItem
            from .IntSettingItem import IntSettingItem
            from .ListSettingItem import ListSettingItem
            from .StrSettingItem import StrSettingItem
            value = setting["value"]
            if isinstance(value, dict):
                return DictSettingItem(id, setting)
            elif isinstance(value, bool):
                return BoolSettingItem(id, setting)
            elif isinstance(value, int):
                return IntSettingItem(id, setting)
            elif isinstance(value, list):
                return ListSettingItem(id, setting)
            elif isinstance(value, str):
                return StrSettingItem(id, setting)

        return super().__new__(cls)

    def __init__(self, id: str, setting: dict) -> None:
        super().__init__()
        self.resize(self.width(), 64)
        self.setting = setting
        self.id = id

        self.cur_layout = QGridLayout(self)

        self.l_name = QLabel(self)
        self.l_name.setText(self.setting["name"])

        self.cur_layout.addWidget(self.l_name)

    def sync(self):
        from ..Setting import Setting
        Setting().sync()
        if "callback" in self.setting:
            self.setting["callback"]()
