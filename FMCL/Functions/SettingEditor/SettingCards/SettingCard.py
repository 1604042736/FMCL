from typing import Callable

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget


class SettingCard(QWidget):
    TYPE_MAP = {
        "color": lambda: "#000000",
        "int": int,
        "float": float,
        "bool": bool,
        "str": str,
        "list": list,
        "dict": dict,
        "file": str,
        "directory": str,
    }
    valueChanged = pyqtSignal(QWidget)

    def __new__(
        cls,
        getter: Callable,
        attrgetter: Callable,
        setter: Callable,
        attrsetter: Callable,
    ):
        if cls == SettingCard:
            from .BoolSettingCard import BoolSettingCard
            from .ColorSettingCard import ColorSettingCard
            from .IntSettingCard import IntSettingCard
            from .ListSettingCard import ListSettingCard
            from .StrSettingCard import StrSettingCard
            from .DictSettingCard import DictSettingCard
            from .FloatSettingCard import FloatSettingCard

            value = getter()
            type = attrgetter("type")
            if type == "color":
                return ColorSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, bool):
                return BoolSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, int):
                return IntSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, float):
                return FloatSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, str):
                return StrSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, list):
                return ListSettingCard(getter, attrgetter, setter, attrsetter)
            elif isinstance(value, dict):
                return DictSettingCard(getter, attrgetter, setter, attrsetter)

        return super().__new__(cls)

    def __init__(
        self,
        getter: Callable,
        attrgetter: Callable,
        setter: Callable,
        attrsetter: Callable,
    ) -> None:
        super().__init__()
        self.getter = getter
        self.attrgetter = attrgetter
        self.setter = setter
        self.attrsetter = attrsetter
        if self.attrgetter("callback", None) == None:
            self.attrsetter("callback", [])
        # 单独设置变量是为了方便移除
        self.__callback = lambda *_: self.refresh()
        self.attrgetter("callback").append(self.__callback)

    def sync(self):
        """写入设置"""
        self.setter(self.value())

    def refresh(self):
        """读取设置"""

    def value(self):
        """获取值"""

    def on_valueChanged(self):
        self.valueChanged.emit(self)
        self.sync()

    def type(self):
        """类型"""
        value = self.getter()
        _type = self.attrgetter("type")
        if _type != None:
            return self.TYPE_MAP[_type]
        return self.TYPE_MAP[type(value).__name__]

    def deleteLater(self) -> None:
        self.attrgetter("callback").remove(self.__callback)
        return super().deleteLater()
