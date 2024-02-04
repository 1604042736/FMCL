from .SettingCard import SettingCard

from .ui_IntSettingCard import Ui_IntSettingCard


class IntSettingCard(SettingCard, Ui_IntSettingCard):
    def __init__(self, getter, attrgetter, setter,attrsetter) -> None:
        super().__init__(getter, attrgetter, setter,attrsetter)
        self.setupUi(self)
        self.sb_val.setMaximum(self.attrgetter("max_value", 2**31 - 1))
        self.sb_val.setMinimum(self.attrgetter("min_value", -(2**31)))
        self.sb_val.setValue(self.getter())
        self.sb_val.valueChanged.connect(self.on_valueChanged)

    def refresh(self):
        self.sb_val.valueChanged.disconnect(self.on_valueChanged)
        self.sb_val.setValue(self.getter())
        self.sb_val.valueChanged.connect(self.on_valueChanged)
        return super().refresh()

    def value(self):
        return self.sb_val.value()
