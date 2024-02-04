from typing import Callable
from .SettingCard import SettingCard

from .ui_FloatSettingCard import Ui_FloatSettingCard


class FloatSettingCard(SettingCard, Ui_FloatSettingCard):
    def __init__(self, getter, attrgetter, setter,attrsetter) -> None:
        super().__init__(getter, attrgetter, setter,attrsetter)
        self.setupUi(self)

        self.dsb_val.setMaximum(self.attrgetter("max_value", 2**31 - 1))
        self.dsb_val.setMinimum(self.attrgetter("min_value", -(2**31)))
        self.dsb_val.setValue(self.getter())
        self.dsb_val.valueChanged.connect(self.on_valueChanged)

    def refresh(self):
        self.dsb_val.valueChanged.disconnect(self.on_valueChanged)
        self.dsb_val.setValue(self.getter())
        self.dsb_val.valueChanged.connect(self.on_valueChanged)
        return super().refresh()

    def value(self):
        return self.dsb_val.value()