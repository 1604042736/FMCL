from PyQt5.QtWidgets import QGridLayout, QWidget


class SettingItem(QWidget):
    def __new__(cls, id, setting):
        if cls == SettingItem:
            from .BoolSettingItem import BoolSettingItem
            from .ColorSettingItem import ColorSettingItem
            from .IntSettingItem import IntSettingItem
            from .ListSettingItem import ListSettingItem
            from .StrSettingItem import StrSettingItem
            value = setting.get(id)
            if isinstance(value, bool):
                return BoolSettingItem(id, setting)
            elif isinstance(value, int):
                return IntSettingItem(id, setting)
            elif isinstance(value, str):
                if len(value) == 7 and value[0] == "#":
                    return ColorSettingItem(id, setting)
                return StrSettingItem(id, setting)
            elif isinstance(value, list):
                return ListSettingItem(id, setting)

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
